"""PreToolUse(Bash): блокирует включение autocrlf и запуск скриптов проекта без -X utf8."""
import json
import re
import sys

cmd = (json.load(sys.stdin).get("tool_input") or {}).get("command", "")

if re.search(r"git\s+config\b[^\n]*core\.autocrlf\s+(true|input)", cmd):
    sys.stderr.write("Заблокировано: core.autocrlf нельзя включать (SHA256 канона требует байтовой идентичности).\n")
    sys.exit(2)

if re.search(r"\b(?:python3?|py(?:\s+-3(?:\.\d+)?)?)\s+(?!-X\s+utf8|-I\b|-\s|-c\b|-m\b|--version|-V\b)\S*(?:tools|work)[/\\]\S+\.py", cmd):
    sys.stderr.write("Заблокировано: скрипты проекта запускать с `-X utf8` (иначе UnicodeEncodeError на кириллице).\n")
    sys.exit(2)
