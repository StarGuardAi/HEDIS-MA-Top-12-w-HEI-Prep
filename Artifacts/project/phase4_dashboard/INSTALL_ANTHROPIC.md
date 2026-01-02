# Quick Fix: Install Anthropic Package

## Problem
The AI Executive Insights page shows "AI API Not Configured" because the `anthropic` Python package is not installed.

## Solution

### Option 1: Install via Command Line (Recommended)
Open a terminal/PowerShell in the dashboard directory and run:

```bash
pip install anthropic
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

### Option 2: Run the Install Script
Double-click or run from command line:

```bash
INSTALL_DEPENDENCIES.bat
```

### Option 3: Install via Python
```bash
python -m pip install anthropic
```

## After Installing

1. **Restart Streamlit** - The app must be restarted to detect the new package
2. **Verify Installation** - The sidebar should now show "✅ Using ANTHROPIC API"

## Verify Your Setup

✅ API Key configured in `.streamlit/secrets.toml`  
✅ Anthropic package installed  
✅ Streamlit restarted  

If all three are done, the AI features should work!

## Troubleshooting

If you still see the error after installing:
1. Make sure you restarted Streamlit completely
2. Check that the package installed: `python -c "import anthropic; print('OK')"`
3. Verify secrets file exists at: `.streamlit/secrets.toml`









