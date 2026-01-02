"""
Auto-restart Streamlit on file changes
Watches for file changes and automatically restarts Streamlit server
"""

import os
import sys
import time
import subprocess
import signal
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
STREAMLIT_PORT = 8502
STREAMLIT_APP = "app.py"
WATCH_DIR = Path(__file__).parent
IGNORE_PATTERNS = [
    "__pycache__",
    ".pyc",
    ".pyo",
    ".pyd",
    ".git",
    "venv",
    ".venv",
    "node_modules",
    ".streamlit",
    "*.log",
    ".DS_Store",
    "*.swp",
    "*.tmp",
]

# Global process reference
streamlit_process = None


class StreamlitRestartHandler(FileSystemEventHandler):
    """Handle file system events and restart Streamlit"""
    
    def __init__(self):
        self.last_restart = 0
        self.debounce_seconds = 2  # Wait 2 seconds after last change before restarting
        
    def should_ignore(self, file_path):
        """Check if file should be ignored"""
        file_str = str(file_path).lower()
        return any(pattern.lower() in file_str for pattern in IGNORE_PATTERNS)
    
    def on_modified(self, event):
        """Called when a file is modified"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Ignore certain files/patterns
        if self.should_ignore(file_path):
            return
        
        # Only watch Python files and other relevant files
        if file_path.suffix not in ['.py', '.yaml', '.yml', '.json', '.txt', '.md', '.css', '.html', '.js']:
            return
        
        # Debounce: wait for a pause in file changes
        current_time = time.time()
        self.last_restart = current_time
        
        print(f"\n📝 File changed: {file_path.name}")
        print("⏳ Waiting for changes to settle...")
        
        # Wait for debounce period
        time.sleep(self.debounce_seconds)
        
        # Check if more changes happened during debounce
        if time.time() - self.last_restart >= self.debounce_seconds:
            print("🔄 Restarting Streamlit...")
            restart_streamlit()


def kill_streamlit_process():
    """Kill existing Streamlit process on port 8502"""
    try:
        # Windows: Find process using port 8502
        result = subprocess.run(
            ["netstat", "-ano"],
            capture_output=True,
            text=True,
            shell=True
        )
        
        for line in result.stdout.split('\n'):
            if f':{STREAMLIT_PORT}' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    try:
                        # Kill the process
                        subprocess.run(
                            ["taskkill", "/F", "/PID", pid],
                            capture_output=True,
                            shell=True
                        )
                        print(f"✅ Killed Streamlit process (PID: {pid})")
                        time.sleep(1)  # Give it time to fully stop
                        return
                    except Exception as e:
                        print(f"⚠️  Could not kill process {pid}: {e}")
        
        # Also try to kill any streamlit.exe processes
        subprocess.run(
            ["taskkill", "/F", "/IM", "streamlit.exe"],
            capture_output=True,
            shell=True
        )
        time.sleep(1)
        
    except Exception as e:
        print(f"⚠️  Error killing Streamlit: {e}")


def start_streamlit():
    """Start Streamlit server"""
    global streamlit_process
    
    try:
        os.chdir(WATCH_DIR)
        
        # Start Streamlit in background
        streamlit_process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", STREAMLIT_APP, "--server.port", str(STREAMLIT_PORT)],
            cwd=WATCH_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )
        
        print(f"✅ Streamlit started on port {STREAMLIT_PORT}")
        print(f"🌐 Open: http://localhost:{STREAMLIT_PORT}")
        return streamlit_process
        
    except Exception as e:
        print(f"❌ Error starting Streamlit: {e}")
        return None


def restart_streamlit():
    """Kill and restart Streamlit"""
    print("\n" + "="*60)
    print("🔄 RESTARTING STREAMLIT")
    print("="*60)
    
    kill_streamlit_process()
    time.sleep(2)  # Give it time to fully stop
    start_streamlit()
    
    print("="*60 + "\n")


def main():
    """Main function to start watcher and Streamlit"""
    print("="*60)
    print("🚀 STREAMLIT AUTO-RESTART WATCHER")
    print("="*60)
    print(f"📁 Watching: {WATCH_DIR}")
    print(f"📄 App: {STREAMLIT_APP}")
    print(f"🔌 Port: {STREAMLIT_PORT}")
    print(f"⏱️  Debounce: 2 seconds")
    print("="*60)
    print("\n💡 Tip: Save any file to trigger auto-restart")
    print("🛑 Press Ctrl+C to stop\n")
    
    # Start Streamlit initially
    start_streamlit()
    time.sleep(3)  # Give Streamlit time to start
    
    # Set up file watcher
    event_handler = StreamlitRestartHandler()
    observer = Observer()
    observer.schedule(event_handler, str(WATCH_DIR), recursive=True)
    observer.start()
    
    try:
        # Keep script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("🛑 STOPPING WATCHER")
        print("="*60)
        
        observer.stop()
        kill_streamlit_process()
        
        print("✅ Watcher stopped")
        print("✅ Streamlit stopped")
        print("="*60)
    
    observer.join()


if __name__ == "__main__":
    main()









