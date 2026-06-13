#!/usr/bin/env bash
set -euo pipefail

ROOT="$(pwd)"
PY="${ROOT}/.venv/bin/python"

run_uvicorn() {
  export PYTHONPATH="$1"
  UVICORN="${ROOT}/.venv/bin/uvicorn"
  if [ ! -x "${UVICORN}" ]; then
    UVICORN="uvicorn"
  fi
  echo "Starting ${UVICORN} PYTHONPATH=${PYTHONPATH} PORT=${PORT:-8000}"
  exec "${UVICORN}" app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
}

# Flat layout (app/ at repo root) — use after flatten-for-render-upload.ps1
if [ -f "${ROOT}/app/main.py" ]; then
  run_uvicorn "${ROOT}"
fi

# Standard layout (backend/app/)
if [ -f "${ROOT}/backend/app/main.py" ]; then
  run_uvicorn "${ROOT}/backend"
fi

if [ -f "${ROOT}/main.py" ] && [ -x "${PY}" ]; then
  echo "Fallback: .venv/bin/python main.py"
  exec "${PY}" "${ROOT}/main.py"
fi

echo "DEPLOY ERROR: no app/main.py on GitHub."
echo "Upload folder app/ from C:\\Users\\natur\\occult-forge-FLAT-UPLOAD"
echo "Run: .\\scripts\\flatten-for-render-upload.ps1"
echo ""
echo "Contents of ${ROOT}:"
ls -la "${ROOT}" || true
exit 1