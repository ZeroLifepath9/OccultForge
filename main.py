"""Render entrypoint — run from repo root: python main.py"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKEND = ROOT / "backend"

if (BACKEND / "app" / "main.py").is_file():
    sys.path.insert(0, str(BACKEND))
elif (ROOT / "app" / "main.py").is_file():
    pass
else:
    print("DEPLOY ERROR: no app/main.py under backend/ or repo root.", file=sys.stderr)
    print(f"Contents of {ROOT}:", file=sys.stderr)
    for p in sorted(ROOT.iterdir()):
        print(f"  {p.name}/" if p.is_dir() else f"  {p.name}", file=sys.stderr)
    raise SystemExit(1)

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)