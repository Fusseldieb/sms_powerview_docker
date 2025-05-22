#!/bin/bash
set -e

if [ ! -f /opt/powerview/banco/banco_de_dados.yap ]; then
    cp /opt/db/database.yap /opt/powerview/banco/banco_de_dados.yap
fi

source /opt/app/venv/bin/activate

LOG_FILE="/tmp/powerview.log"
PYTHON_PID=""
JAVA_PID=""
EXIT_CODE=0

cleanup() {
    echo "🔻 Cleaning up..."

    if [ -n "$PYTHON_PID" ] && kill -0 "$PYTHON_PID" 2>/dev/null; then
        echo "Stopping polling script (PID $PYTHON_PID)..."
        kill "$PYTHON_PID"
        wait "$PYTHON_PID" 2>/dev/null || true
    fi

    if [ -n "$JAVA_PID" ] && kill -0 "$JAVA_PID" 2>/dev/null; then
        echo "Stopping PowerView Java process (PID $JAVA_PID)..."
        kill "$JAVA_PID"
        wait "$JAVA_PID" 2>/dev/null || true
    fi

    echo "✅ Cleanup complete. Exiting with code $EXIT_CODE"
    exit $EXIT_CODE
}

# Trap SIGTERM and SIGINT for graceful exit
trap cleanup SIGTERM SIGINT

# Start polling script in background
python /opt/app/polling_endpoint.py &
PYTHON_PID=$!

echo "Starting PowerView..."

# Kill any leftover PowerView/Java processes
pkill -f "/opt/powerview/powerview" 2>/dev/null || true
pkill -f "java" 2>/dev/null || true
sleep 1

# 🔥 Clear the log file before starting
: > "$LOG_FILE"

# Start PowerView (it daemonizes)
 /opt/powerview/powerview start --no-gui >> "$LOG_FILE" 2>&1 &

# Wait a moment for java to spawn
sleep 5

# Get the actual Java process PID
JAVA_PID=$(pgrep -f "java" | head -n 1)

if [ -z "$JAVA_PID" ]; then
    echo "❌ Failed to start PowerView. No Java process found."
    EXIT_CODE=1
    cleanup
fi

echo "PowerView Java process running with PID $JAVA_PID"

# Monitor process and crash log
while kill -0 "$JAVA_PID" 2>/dev/null; do
    if grep -q "Embedded server stopped!!!" "$LOG_FILE"; then
        echo "🔥 Crash detected in log!"
        EXIT_CODE=1
        cleanup
    fi
    sleep 2
done

echo "❌ PowerView Java process exited unexpectedly."
EXIT_CODE=1
cleanup