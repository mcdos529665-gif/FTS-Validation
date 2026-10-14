"""Базовый узел дерева экспериментов: целостность канона на baseline.

Запускает tools/verify.py --strict; код возврата — код проверки.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
r = subprocess.run([sys.executable, "-X", "utf8", "tools/verify.py", "--strict"], cwd=ROOT)
sys.exit(r.returncode)
