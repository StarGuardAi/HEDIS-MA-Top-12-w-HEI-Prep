"""
Quick script to install the Anthropic package
Run this script to fix the "AI API Not Configured" error
"""
import subprocess
import sys

print("=" * 60)
print("Installing Anthropic Package for AI Insights")
print("=" * 60)
print()

try:
    print("Installing anthropic package...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "anthropic"],
        capture_output=True,
        text=True,
        check=True
    )
    print("✅ Successfully installed anthropic package!")
    print()
    
    # Verify installation
    print("Verifying installation...")
    import anthropic
    print(f"✅ Anthropic version {anthropic.__version__} is installed")
    print()
    print("=" * 60)
    print("Installation Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Restart your Streamlit app")
    print("2. Navigate to the AI Executive Insights page")
    print("3. You should now see '✅ Using ANTHROPIC API'")
    
except subprocess.CalledProcessError as e:
    print("❌ Error installing anthropic package:")
    print(e.stderr)
    print()
    print("Try running manually: pip install anthropic")
    sys.exit(1)
except ImportError as e:
    print("❌ Error importing anthropic after installation:")
    print(e)
    print()
    print("Try restarting your terminal and running again")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)









