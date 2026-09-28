#!/usr/bin/env bash
set -e

echo "==================================================="
echo "            VELYRA.AI — LOCAL LAUNCHER"
echo "             Speak English. Naturally."
echo "==================================================="
echo ""

# Check Python & Node
command -v python3 >/dev/null 2>&1 || { echo "[ERROR] Python 3 is required."; exit 1; }
command -v node >/dev/null 2>&1 || { echo "[ERROR] Node.js is required."; exit 1; }

echo "[1/4] Checking Python dependencies..."
pip install -r backend/requirements.txt -q

echo "[2/4] Initializing SQLite database and curriculum..."
python3 scripts/seed_database.py

echo "[3/4] Checking React frontend dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
fi
cd ..

echo "[4/4] Launching Velyra.ai..."
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:5173"

# Run servers in background
python3 -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!

cd frontend && npm run dev &
FRONTEND_PID=$!
cd ..

trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
