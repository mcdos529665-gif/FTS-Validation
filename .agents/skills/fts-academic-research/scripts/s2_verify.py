#!/usr/bin/env python3
"""Conservative Semantic Scholar lookup with DOI/title normalization and 429 backoff."""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable

BASE_URL = "https://api.semanticscholar.org/graph/v1"
FIELDS = "paperId,title,year,authors,externalIds,url,venue,publicationDate"


def normalize_doi(value: str | None) -> str:
    if not value:
        return ""
    text = value.strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "http://dx.doi.org/", "doi:"):
        if text.startswith(prefix):
            text = text[len(prefix) :]
            break
    return text.strip()


@dataclass
class SemanticScholarClient:
    opener: Callable[..., Any] = urllib.request.urlopen
    sleeper: Callable[[float], None] = time.sleep
    clock: Callable[[], float] = time.monotonic
    min_interval: float = 1.0
    max_retries: int = 3
    _last_request: float | None = None

    def _request(self, path: str, params: dict[str, str]) -> dict[str, Any]:
        url = f"{BASE_URL}{path}?{urllib.parse.urlencode(params)}"
        headers = {"User-Agent": "fts-academic-research/1.0"}
        api_key = os.environ.get("S2_API_KEY", "").strip()
        if api_key:
            headers["x-api-key"] = api_key

        for attempt in range(self.max_retries + 1):
            now = self.clock()
            if self._last_request is not None:
                wait = self.min_interval - (now - self._last_request)
                if wait > 0:
                    self.sleeper(wait)
            self._last_request = self.clock()
            request = urllib.request.Request(url, headers=headers)
            try:
                with self.opener(request, timeout=30) as response:
                    return json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                if exc.code != 429 or attempt >= self.max_retries:
                    raise
                retry_after = exc.headers.get("Retry-After", "1") if exc.headers else "1"
                try:
                    delay = max(1.0, min(float(retry_after), 60.0))
                except ValueError:
                    delay = 1.0
                self.sleeper(delay)
        raise RuntimeError("unreachable")

    def by_doi(self, doi: str) -> dict[str, Any]:
        normalized = normalize_doi(doi)
        if not normalized:
            raise ValueError("DOI is empty")
        paper = urllib.parse.quote(f"DOI:{normalized}", safe=":")
        return self._request(f"/paper/{paper}", {"fields": FIELDS})

    def by_title(self, title: str) -> dict[str, Any]:
        title = " ".join(title.split())
        if not title:
            raise ValueError("title is empty")
        result = self._request("/paper/search", {"query": title, "limit": "10", "fields": FIELDS})
        candidates = result.get("data", [])
        exact = [p for p in candidates if " ".join(p.get("title", "").split()).casefold() == title.casefold()]
        return {"query_title": title, "exact_matches": exact, "candidates": candidates}


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--doi")
    group.add_argument("--title")
    args = parser.parse_args()
    client = SemanticScholarClient()
    try:
        result = client.by_doi(args.doi) if args.doi else client.by_title(args.title)
    except urllib.error.HTTPError as exc:
        print(json.dumps({"ok": False, "provider": "semantic-scholar", "status": exc.code, "error": "http_error"}))
        return 2
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "provider": "semantic-scholar", "error": type(exc).__name__}))
        return 2
    print(json.dumps({"ok": True, "provider": "semantic-scholar", "result": result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
