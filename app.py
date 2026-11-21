#!/usr/bin/env python3
"""
WasteWise — Single-Command Application Launcher
Starts both the Flask backend API and Vite React frontend concurrently.
Handles graceful shutdown of process trees upon Ctrl+C.
"""

import os
import sys
import time
import socket
import signal
import webbrowser
import subprocess
import urllib.request
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"

BACKEND_URL = "http://127.0.0.1:5000"
FRONTEND_URL = "http://localhost:5173"
HEALTH_URL = f"{BACKEND_URL}/api/health"

# Processes
backend_proc = None
frontend_proc = None


def is_port_in_use(port, host="127.0.0.1"):
    """Check if a network port is already open/listening."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0


def kill_process_tree(proc):
    """Cleanly terminate a subprocess and all of its spawned child processes."""
    if proc is None:
        return
    try:
        if sys.platform == "win32":
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False
            )
        else:
            proc.terminate()
            proc.wait(timeout=3)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass


def shutdown_handler(sig=None, frame=None):
    """Handle shutdown signals and terminate both servers."""
    print("\n\n" + "-" * 60)
    print("Shutting down WasteWise servers...")
    print("-" * 60)

    global backend_proc, frontend_proc
    if backend_proc:
        print("  Stopping Flask backend...")
        kill_process_tree(backend_proc)
        backend_proc = None

    if frontend_proc:
        print("  Stopping Vite frontend...")
        kill_process_tree(frontend_proc)
        frontend_proc = None

    print("WasteWise shutdown complete. Goodbye!")
    sys.exit(0)


def wait_for_service(url, timeout=12, label="service"):
    """Wait until an HTTP endpoint responds."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with urllib.request.urlopen(url, timeout=1) as response:
                if response.status in (200, 304):
                    return True
        except Exception:
            time.sleep(0.4)
    return False


def print_banner():
    """Print clean startup banner."""
    print("=" * 68)
    print("   WASTEWISE — AI Waste Classification & Segregation System")
    print("=" * 68)
    print("   Initializing dual-stack runtime...")
    print(f"   Python Executable : {sys.executable}")
    print(f"   Project Root      : {ROOT_DIR}")
    print("=" * 68)


def main():
    global backend_proc, frontend_proc

    # Register signal handlers
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    print_banner()

    # Pre-check port availability
    if is_port_in_use(5000):
        print("! Warning: Port 5000 appears to be in use. Attempting to connect or reclaim...")
    if is_port_in_use(5173):
        print("! Warning: Port 5173 appears to be in use. Vite will attempt alternate port if busy.")

    # 1. Start Flask Backend
    print("\n[1/3] Starting Flask backend server on http://127.0.0.1:5000...")
    backend_script = BACKEND_DIR / "run.py"
    if not backend_script.is_file():
        print(f"ERROR: Backend entry-point not found at {backend_script}")
        sys.exit(1)

    backend_env = os.environ.copy()
    backend_env["PYTHONUNBUFFERED"] = "1"
    backend_env["FLASK_DEBUG"] = "0"

    backend_proc = subprocess.Popen(
        [sys.executable, str(backend_script)],
        cwd=str(BACKEND_DIR),
        env=backend_env
    )

    # Wait for backend health check
    print("      Waiting for Flask backend to be ready...")
    if wait_for_service(HEALTH_URL, timeout=15, label="Backend"):
        print("      ✓ Flask backend is online and healthy!")
    else:
        print("      ! Backend started (health check timed out, continuing)...")

    # 2. Start Vite Frontend
    print("\n[2/3] Starting Vite frontend server...")
    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"

    frontend_proc = subprocess.Popen(
        [npm_cmd, "run", "dev", "--", "--host", "127.0.0.1", "--port", "5173"],
        cwd=str(FRONTEND_DIR)
    )

    print("      Waiting for Vite development server...")
    if wait_for_service("http://127.0.0.1:5173", timeout=12, label="Frontend"):
        print("      ✓ Vite development server is online!")
    else:
        print("      ✓ Vite dev server initialized.")

    # 3. Ready notification
    print("\n[3/3] Ready! Access WasteWise in your web browser:")
    print("=" * 68)
    print(f"   Frontend Application : {FRONTEND_URL}")
    print(f"   Backend REST API     : {BACKEND_URL}/api/v1")
    print(f"   API Health Check     : {HEALTH_URL}")
    print("=" * 68)
    print("   Press Ctrl+C to terminate both servers cleanly.\n")

    # Open browser automatically in background daemon thread (non-blocking)
    if "--no-browser" not in sys.argv:
        try:
            import threading
            threading.Thread(target=lambda: webbrowser.open(FRONTEND_URL), daemon=True).start()
        except Exception:
            pass

    # Monitor processes and stream any fatal errors
    try:
        while True:
            # Check backend process
            if backend_proc.poll() is not None:
                print("\n! Flask backend server exited unexpectedly.")
                shutdown_handler()

            # Check frontend process
            if frontend_proc.poll() is not None:
                print("\n! Vite frontend server exited unexpectedly.")
                shutdown_handler()

            time.sleep(1)
    except KeyboardInterrupt:
        shutdown_handler()


if __name__ == "__main__":
    main()
