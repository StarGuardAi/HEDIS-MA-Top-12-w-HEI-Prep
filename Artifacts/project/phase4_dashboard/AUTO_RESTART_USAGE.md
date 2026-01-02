# 🔄 Streamlit Auto-Restart Watcher

**Start once, forget about it!** Automatically restarts Streamlit whenever you save any file.

## 🚀 Quick Start

### **Option 1: Double-click batch file (Easiest)**
```
start_auto_restart.bat
```

### **Option 2: Run Python directly**
```bash
python auto_restart.py
```

## ✨ How It Works

1. **Start the watcher** at the beginning of your coding session
2. **Code normally** in Cursor - just save files as usual (Ctrl+S)
3. **Auto-restarts** Streamlit within 2 seconds of any file change
4. **Never manually restart again!**

## 📁 What It Watches

The watcher monitors these directories:
- `.` (current directory - all Python files)
- `pages/` (all page files)
- `src/` (source code)
- `.streamlit/` (config files)

**File types watched:**
- `.py` - Python files
- `.md` - Markdown files
- `.toml` - Config files (like `.streamlit/config.toml`)
- `.css` - Stylesheets
- `.js` - JavaScript files
- `.json` - JSON config files

**Automatically ignored:**
- `__pycache__/`
- `.git/`
- `venv/` or `.venv/`
- `auto_restart.py` (the watcher itself)
- `.pytest_cache/`

## 🎯 Usage Workflow

### **Start of Day:**
1. Double-click `start_auto_restart.bat`
2. Leave the terminal window open (minimize it)
3. Start coding!

### **During Development:**
1. Edit files in Cursor
2. Save (Ctrl+S)
3. Wait 2 seconds
4. Streamlit automatically restarts
5. Refresh browser to see changes

### **End of Day:**
1. Press `Ctrl+C` in the watcher terminal
2. Streamlit stops
3. Close terminal

## 📊 Features

- ✅ **Zero configuration** - Works out of the box
- ✅ **Smart debouncing** - Waits 2 seconds after last change (prevents multiple restarts)
- ✅ **Automatic cleanup** - Kills old processes before starting new one
- ✅ **Port management** - Handles port 8502 automatically
- ✅ **File change detection** - Detects new, modified, and deleted files
- ✅ **Recursive watching** - Monitors subdirectories automatically

## 🔧 Configuration

Edit `auto_restart.py` to customize:

**Change port:**
```python
self.port = 8502  # Change to your port
```

**Add watch directories:**
```python
self.watch_dirs = ['.', 'pages', 'src', '.streamlit', 'utils']  # Add more
```

**Add file extensions:**
```python
self.watch_extensions = {'.py', '.md', '.toml', '.css', '.js', '.json', '.yaml'}  # Add more
```

**Change debounce time:**
```python
time.sleep(2)  # Change 2 to your preferred seconds
```

## 🛑 Stopping

Press `Ctrl+C` in the terminal where the watcher is running.

This will:
- Stop the file watcher
- Kill the Streamlit process
- Clean up all resources

## 💡 Tips

- **Leave it running** - Don't close the terminal window
- **Minimize it** - Keep it running in background
- **Check console** - See which files triggered restarts
- **One watcher only** - Don't run multiple instances

## 🐛 Troubleshooting

**Port already in use?**
- The watcher should automatically kill existing processes
- If not, manually kill: `taskkill /F /IM streamlit.exe`

**Not detecting changes?**
- Check that you're saving files in watched directories
- Verify file extension is in `watch_extensions`
- Check console output for detection messages

**Multiple restarts?**
- This is normal if you save multiple files quickly
- Debounce prevents excessive restarts
- Wait 2 seconds between saves if needed

**Streamlit not starting?**
- Check Python and Streamlit are installed
- Verify `app.py` exists in the directory
- Check console for error messages

## 📝 Example Output

```
============================================================
🔄 STREAMLIT AUTO-RESTART WATCHER
============================================================
📁 Watching: ., pages, src, .streamlit
📝 Extensions: .py, .md, .toml, .css, .js, .json
🚪 Port: 8502
============================================================

💡 This will auto-restart Streamlit when you save files
💡 Press Ctrl+C to stop

============================================================
🚀 Starting Streamlit on port 8502...
============================================================

✅ Streamlit running at http://localhost:8502
👀 Watching for file changes...

📝 File changed: app.py
⏳ Restarting in 2 seconds...
```

## 🎉 Benefits

- **No manual restarts** - Save and go!
- **Faster development** - See changes immediately
- **Less context switching** - Stay in your editor
- **Consistent workflow** - Same process every time

---

**Happy coding! 🚀**









