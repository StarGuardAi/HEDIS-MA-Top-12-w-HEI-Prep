# 🔄 Streamlit Auto-Restart Watcher

Automatically restarts Streamlit whenever you save a file.

## 🚀 Quick Start

### Option 1: Run the batch file
```bash
start_watcher.bat
```

### Option 2: Run directly
```bash
python watch_and_restart.py
```

## ✨ Features

- **Auto-restart on save**: Any `.py`, `.yaml`, `.json`, `.txt`, `.md`, `.css`, `.html`, or `.js` file change triggers a restart
- **Debounced**: Waits 2 seconds after the last change before restarting (prevents multiple restarts)
- **Smart filtering**: Ignores `__pycache__`, `.git`, `venv`, logs, and other non-essential files
- **Port management**: Automatically kills existing Streamlit processes on port 8502 before restarting

## 📋 How It Works

1. **Starts Streamlit** on port 8502
2. **Watches** the entire dashboard directory (recursive)
3. **Detects** file changes
4. **Debounces** for 2 seconds (waits for changes to settle)
5. **Kills** existing Streamlit process
6. **Restarts** Streamlit automatically

## 🎯 Usage

1. **Start the watcher** at the beginning of your session:
   ```bash
   python watch_and_restart.py
   ```

2. **Code normally** in Cursor - just save files as usual

3. **Every save** automatically restarts Streamlit

4. **Stop the watcher** with `Ctrl+C`

## ⚙️ Configuration

Edit `watch_and_restart.py` to customize:

- **Port**: Change `STREAMLIT_PORT = 8502`
- **App file**: Change `STREAMLIT_APP = "app.py"`
- **Debounce time**: Change `self.debounce_seconds = 2`
- **Ignored patterns**: Modify `IGNORE_PATTERNS` list

## 📝 Notes

- The watcher runs in the foreground (you'll see output)
- Streamlit will be available at `http://localhost:8502`
- File changes are logged to console
- Multiple rapid saves will be batched (debounced)

## 🛑 Stopping

Press `Ctrl+C` in the terminal where the watcher is running. This will:
- Stop the file watcher
- Kill the Streamlit process
- Clean up resources

## 🔧 Troubleshooting

**Port already in use?**
- The watcher should automatically kill existing processes
- If not, manually kill: `taskkill /F /IM streamlit.exe`

**Not restarting?**
- Check that `watchdog` is installed: `pip install watchdog`
- Verify file changes are being detected (check console output)
- Ensure you're saving files in the watched directory

**Multiple restarts?**
- Increase `debounce_seconds` in the script
- Check for multiple watchers running (kill extra processes)









