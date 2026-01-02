import os
import sys
import time
import subprocess
import signal
from pathlib import Path


class StreamlitAutoRestart:
    def __init__(self):
        self.process = None
        self.last_modified = {}
        self.port = 8502
        
        # Files/folders to watch
        self.watch_dirs = ['.', 'pages', 'src', '.streamlit']
        self.watch_extensions = {'.py', '.md', '.toml', '.css', '.js', '.json'}
        
        # Files/folders to ignore
        self.ignore_patterns = {'__pycache__', '.git', 'venv', '.venv', 
                               'auto_restart.py', '.pytest_cache'}
    
    def kill_streamlit(self):
        """Kill existing Streamlit processes"""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.process = None
        
        # Also kill by port (Windows)
        try:
            subprocess.run(
                f'for /f "tokens=5" %a in (\'netstat -aon ^| find ":{self.port}"\') do taskkill /F /PID %a',
                shell=True, capture_output=True
            )
        except:
            pass
        
        time.sleep(1)
    
    def start_streamlit(self):
        """Start Streamlit process"""
        print(f"\n{'='*60}")
        print(f"🚀 Starting Streamlit on port {self.port}...")
        print(f"{'='*60}\n")
        
        self.process = subprocess.Popen(
            [sys.executable, '-m', 'streamlit', 'run', 'app.py',
             '--server.port', str(self.port),
             '--server.headless', 'true',
             '--browser.gatherUsageStats', 'false'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Show startup messages
        for _ in range(15):
            if self.process.poll() is not None:
                break
            line = self.process.stdout.readline()
            if line:
                print(line.strip())
                if 'Local URL' in line or 'Network URL' in line:
                    break
        
        print(f"\n✅ Streamlit running at http://localhost:{self.port}")
        print(f"👀 Watching for file changes...\n")
    
    def get_file_mtime(self, filepath):
        """Get file modification time"""
        try:
            return os.path.getmtime(filepath)
        except:
            return 0
    
    def should_ignore(self, filepath):
        """Check if file should be ignored"""
        path_str = str(filepath)
        
        # Check ignore patterns
        for pattern in self.ignore_patterns:
            if pattern in path_str:
                return True
        
        # Check extension
        if filepath.suffix not in self.watch_extensions:
            return True
        
        return False
    
    def scan_files(self):
        """Scan all files for changes"""
        current_files = {}
        
        for watch_dir in self.watch_dirs:
            if not os.path.exists(watch_dir):
                continue
            
            path = Path(watch_dir)
            for file in path.rglob('*'):
                if file.is_file() and not self.should_ignore(file):
                    current_files[str(file)] = self.get_file_mtime(file)
        
        return current_files
    
    def check_for_changes(self):
        """Check if any files have changed"""
        current_files = self.scan_files()
        
        # First run - initialize
        if not self.last_modified:
            self.last_modified = current_files
            return False
        
        # Check for changes
        for filepath, mtime in current_files.items():
            if filepath not in self.last_modified:
                print(f"\n📄 New file detected: {filepath}")
                self.last_modified = current_files
                return True
            
            if mtime > self.last_modified[filepath]:
                print(f"\n📝 File changed: {filepath}")
                self.last_modified = current_files
                return True
        
        # Check for deleted files
        for filepath in self.last_modified:
            if filepath not in current_files:
                print(f"\n🗑️  File deleted: {filepath}")
                self.last_modified = current_files
                return True
        
        return False
    
    def run(self):
        """Main loop"""
        print("\n" + "="*60)
        print("🔄 STREAMLIT AUTO-RESTART WATCHER")
        print("="*60)
        print(f"📁 Watching: {', '.join(self.watch_dirs)}")
        print(f"📝 Extensions: {', '.join(self.watch_extensions)}")
        print(f"🚪 Port: {self.port}")
        print("="*60)
        print("\n💡 This will auto-restart Streamlit when you save files")
        print("💡 Press Ctrl+C to stop\n")
        
        # Initial scan
        self.last_modified = self.scan_files()
        
        # Start Streamlit
        self.start_streamlit()
        
        try:
            while True:
                time.sleep(1)  # Check every second
                
                if self.check_for_changes():
                    print("⏳ Restarting in 2 seconds...")
                    time.sleep(2)  # Debounce multiple rapid saves
                    
                    self.kill_streamlit()
                    self.start_streamlit()
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Shutting down...")
            self.kill_streamlit()
            print("👋 Goodbye!\n")


if __name__ == '__main__':
    watcher = StreamlitAutoRestart()
    watcher.run()









