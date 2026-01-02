"""
Test script for Anthropic API setup
Run this to verify your API key is working correctly
"""
from dotenv import load_dotenv
import os
import anthropic
import sys

# Force output flushing
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

# Load environment variables from .env file
load_dotenv()

# Check if API key is set
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key or api_key == "sk-ant-your-actual-key-here":
    print("❌ ERROR: API key not set or still using placeholder!")
    print("📝 Please update your .env file with your actual Anthropic API key")
    print("   Get your key from: https://console.anthropic.com/")
    sys.exit(1)

print("🔑 API key found in .env file")
print("🔌 Testing Anthropic API connection...")

# Initialize the Anthropic client
try:
    client = anthropic.Anthropic(api_key=api_key)
    
    # Test it works
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=50,
        messages=[{"role": "user", "content": "Say 'Setup successful!'"}]
    )
    print(f"✅ SUCCESS! API connection working!")
    print(f"📨 Response: {response.content[0].text}")
    print("\n🎉 Your Anthropic API setup is complete and working!")
    
except anthropic.AuthenticationError as e:
    print(f"❌ Authentication Error: Invalid API key")
    print(f"   Details: {e}")
    print("\n💡 Make sure you:")
    print("   1. Have a valid API key from https://console.anthropic.com/")
    print("   2. Have credits/billing set up in your Anthropic account")
    print("   3. Updated the .env file with your actual key (not the placeholder)")
    
except anthropic.APIError as e:
    print(f"❌ API Error: {e}")
    print(f"   Status: {e.status_code}")
    print(f"   Message: {e.message}")
    
except Exception as e:
    print(f"❌ Unexpected Error: {type(e).__name__}")
    print(f"   Details: {e}")

