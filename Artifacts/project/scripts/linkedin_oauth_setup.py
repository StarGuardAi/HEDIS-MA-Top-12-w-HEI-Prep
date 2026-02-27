#!/usr/bin/env python3
"""
LinkedIn OAuth 2.0 Setup Helper

This script helps you get a LinkedIn access token for automatic posting.

LinkedIn OAuth 2.0 Flow:
1. Register app at https://www.linkedin.com/developers/apps
2. Get Client ID and Client Secret
3. Run this script to get authorization URL
4. Authorize the app in your browser
5. Get the authorization code from redirect URL
6. Exchange code for access token
7. Save token to environment or config file

Required LinkedIn App Permissions:
- w_member_social (Post, comment and react on LinkedIn as you)
- r_liteprofile (Read your profile)

Access Token Validity:
- LinkedIn access tokens expire after 60 days
- You'll need to re-authenticate when it expires
"""

import os
import sys
import json
import webbrowser
from pathlib import Path
from urllib.parse import urlencode, parse_qs, urlparse
import logging

try:
    import requests
except ImportError:
    print("ERROR: requests library not installed")
    print("Run: pip install requests")
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LinkedInOAuth:
    """Handles LinkedIn OAuth 2.0 authentication"""
    
    # OAuth endpoints
    AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
    TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
    
    # Redirect URI (must match what's configured in LinkedIn app)
    # For local testing, use http://localhost:8888/callback
    REDIRECT_URI = "http://localhost:8888/callback"
    
    # Required scopes for posting
    SCOPES = ["w_member_social", "r_liteprofile"]
    
    def __init__(self, client_id: str = None, client_secret: str = None):
        self.client_id = client_id or os.getenv('LINKEDIN_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('LINKEDIN_CLIENT_SECRET')
        self.project_root = Path(__file__).parent.parent
        
    def get_authorization_url(self) -> str:
        """
        Generate LinkedIn authorization URL
        
        User needs to visit this URL to authorize the app
        """
        if not self.client_id:
            raise ValueError("LinkedIn Client ID not found. Set LINKEDIN_CLIENT_ID environment variable.")
        
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.REDIRECT_URI,
            'scope': ' '.join(self.SCOPES),
            'state': 'hedis_gsd_publisher'  # CSRF protection
        }
        
        auth_url = f"{self.AUTH_URL}?{urlencode(params)}"
        return auth_url
    
    def exchange_code_for_token(self, authorization_code: str) -> dict:
        """
        Exchange authorization code for access token
        
        Args:
            authorization_code: Code received from LinkedIn after authorization
        
        Returns:
            Dictionary with access_token and expires_in
        """
        if not self.client_id or not self.client_secret:
            raise ValueError("LinkedIn credentials not found. Set LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET.")
        
        data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': self.REDIRECT_URI,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        response = requests.post(self.TOKEN_URL, data=data, headers=headers)
        
        if response.status_code == 200:
            token_data = response.json()
            logger.info("✅ Successfully obtained access token")
            return token_data
        else:
            logger.error(f"❌ Failed to get access token: {response.status_code}")
            logger.error(response.text)
            raise Exception(f"Token exchange failed: {response.text}")
    
    def save_token_to_file(self, token_data: dict, filename: str = '.linkedin_token.json'):
        """Save token data to file"""
        token_file = self.project_root / filename
        
        with open(token_file, 'w', encoding='utf-8') as f:
            json.dump(token_data, f, indent=2)
        
        logger.info(f"Token saved to: {token_file}")
        logger.warning("⚠️ Keep this file secure! Add to .gitignore to prevent committing.")
        
        return token_file
    
    def load_token_from_file(self, filename: str = '.linkedin_token.json') -> dict:
        """Load token data from file"""
        token_file = self.project_root / filename
        
        if not token_file.exists():
            raise FileNotFoundError(f"Token file not found: {token_file}")
        
        with open(token_file, 'r', encoding='utf-8') as f:
            token_data = json.load(f)
        
        return token_data
    
    def test_token(self, access_token: str) -> bool:
        """Test if access token is valid by fetching user profile"""
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        profile_url = "https://api.linkedin.com/v2/me"
        response = requests.get(profile_url, headers=headers)
        
        if response.status_code == 200:
            profile = response.json()
            logger.info(f"✅ Token valid! Authenticated as: {profile.get('localizedFirstName')} {profile.get('localizedLastName')}")
            return True
        else:
            logger.error(f"❌ Token invalid or expired: {response.status_code}")
            logger.error(response.text)
            return False


def interactive_setup():
    """Interactive setup wizard for LinkedIn OAuth"""
    print("=" * 70)
    print("LinkedIn API Setup Wizard")
    print("=" * 70)
    print()
    
    # Step 1: Check for credentials
    client_id = os.getenv('LINKEDIN_CLIENT_ID')
    client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("❌ LinkedIn credentials not found!")
        print()
        print("To set up LinkedIn API access:")
        print()
        print("1. Go to: https://www.linkedin.com/developers/apps")
        print("2. Click 'Create app'")
        print("3. Fill in app details:")
        print("   - App name: HEDIS GSD Publisher (or any name)")
        print("   - LinkedIn Page: Create a test page if needed")
        print("   - App logo: Optional")
        print("4. After creating app:")
        print("   - Go to 'Auth' tab")
        print("   - Copy 'Client ID' and 'Client Secret'")
        print("   - Add Redirect URL: http://localhost:8888/callback")
        print("   - Request permissions: w_member_social, r_liteprofile")
        print()
        print("5. Set environment variables:")
        print()
        print("   Windows:")
        print("   set LINKEDIN_CLIENT_ID=your_client_id")
        print("   set LINKEDIN_CLIENT_SECRET=your_client_secret")
        print()
        print("   Or add to .env file:")
        print("   LINKEDIN_CLIENT_ID=your_client_id")
        print("   LINKEDIN_CLIENT_SECRET=your_client_secret")
        print()
        
        # Prompt for credentials
        print("Enter credentials now (or press Enter to skip):")
        client_id_input = input("LinkedIn Client ID: ").strip()
        client_secret_input = input("LinkedIn Client Secret: ").strip()
        
        if client_id_input and client_secret_input:
            client_id = client_id_input
            client_secret = client_secret_input
            os.environ['LINKEDIN_CLIENT_ID'] = client_id
            os.environ['LINKEDIN_CLIENT_SECRET'] = client_secret
            print("✅ Credentials set for this session")
            print()
        else:
            print("Skipping setup. Run this script again after setting credentials.")
            return
    else:
        print("✅ LinkedIn credentials found!")
        print(f"Client ID: {client_id[:20]}...")
        print()
    
    # Step 2: Initialize OAuth handler
    oauth = LinkedInOAuth(client_id=client_id, client_secret=client_secret)
    
    # Step 3: Generate authorization URL
    print("=" * 70)
    print("Step 1: Authorize the App")
    print("=" * 70)
    print()
    
    auth_url = oauth.get_authorization_url()
    print("Opening authorization URL in your browser...")
    print()
    print("Authorization URL:")
    print(auth_url)
    print()
    
    # Open browser
    try:
        webbrowser.open(auth_url)
        print("✅ Browser opened. Please authorize the app.")
    except:
        print("⚠️ Could not open browser automatically.")
        print("Please copy the URL above and open it manually.")
    
    print()
    print("After authorizing:")
    print("1. You'll be redirected to: http://localhost:8888/callback?code=...")
    print("2. Copy the FULL redirect URL from your browser")
    print("   (The page won't load, but the URL contains the code)")
    print()
    
    # Step 4: Get authorization code
    print("=" * 70)
    print("Step 2: Get Authorization Code")
    print("=" * 70)
    print()
    
    redirect_url = input("Paste the redirect URL here: ").strip()
    
    if not redirect_url:
        print("❌ No URL provided. Exiting.")
        return
    
    # Parse authorization code from URL
    try:
        parsed = urlparse(redirect_url)
        params = parse_qs(parsed.query)
        
        if 'code' not in params:
            print("❌ Authorization code not found in URL")
            print("Make sure you copied the FULL redirect URL")
            return
        
        auth_code = params['code'][0]
        print(f"✅ Authorization code extracted: {auth_code[:20]}...")
        print()
    except Exception as e:
        print(f"❌ Error parsing URL: {e}")
        return
    
    # Step 5: Exchange code for token
    print("=" * 70)
    print("Step 3: Get Access Token")
    print("=" * 70)
    print()
    
    try:
        token_data = oauth.exchange_code_for_token(auth_code)
        access_token = token_data['access_token']
        expires_in = token_data.get('expires_in', 'Unknown')
        
        print(f"✅ Access token obtained!")
        print(f"Token: {access_token[:30]}...")
        print(f"Expires in: {expires_in} seconds ({expires_in // 86400} days)")
        print()
        
        # Step 6: Test token
        print("=" * 70)
        print("Step 4: Test Token")
        print("=" * 70)
        print()
        
        if oauth.test_token(access_token):
            print("✅ Token is valid and working!")
            print()
            
            # Step 7: Save token
            print("=" * 70)
            print("Step 5: Save Token")
            print("=" * 70)
            print()
            
            save_choice = input("Save token to file? (y/n): ").strip().lower()
            
            if save_choice == 'y':
                token_file = oauth.save_token_to_file(token_data)
                print(f"✅ Token saved to: {token_file}")
                print()
                print("⚠️ IMPORTANT: Add to .gitignore:")
                print("   .linkedin_token.json")
                print()
            
            # Step 8: Set environment variable
            print("=" * 70)
            print("Step 6: Set Environment Variable")
            print("=" * 70)
            print()
            print("To use automatic posting, set:")
            print()
            print("Windows (PowerShell):")
            print(f"$env:LINKEDIN_ACCESS_TOKEN=\"{access_token}\"")
            print()
            print("Windows (CMD):")
            print(f"set LINKEDIN_ACCESS_TOKEN={access_token}")
            print()
            print("Or add to .env file:")
            print(f"LINKEDIN_ACCESS_TOKEN={access_token}")
            print()
            
            # Create batch file to set token
            batch_file = Path(__file__).parent.parent / 'set_linkedin_token.bat'
            with open(batch_file, 'w') as f:
                f.write(f"@echo off\n")
                f.write(f"REM LinkedIn Access Token (expires in {expires_in // 86400} days)\n")
                f.write(f"set LINKEDIN_ACCESS_TOKEN={access_token}\n")
                f.write(f"echo ✅ LinkedIn access token set for this session\n")
                f.write(f"echo To use: call set_linkedin_token.bat before running publish scripts\n")
            
            print(f"✅ Created: {batch_file}")
            print("   Run this before publishing: call set_linkedin_token.bat")
            print()
            
            print("=" * 70)
            print("✅ Setup Complete!")
            print("=" * 70)
            print()
            print("Next steps:")
            print("1. Run: call set_linkedin_token.bat")
            print("2. Test posting: python scripts/publish_to_linkedin.py --milestone 1 --dry-run")
            print("3. Real post: python scripts/publish_to_linkedin.py --milestone 1")
            print()
            print("⚠️ Token expires in ~60 days. Re-run this script when it expires.")
            
        else:
            print("❌ Token test failed. Please try again.")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.exception("Token exchange failed")


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='LinkedIn OAuth 2.0 Setup Helper'
    )
    parser.add_argument(
        '--test-token',
        action='store_true',
        help='Test existing access token'
    )
    parser.add_argument(
        '--token',
        type=str,
        help='Access token to test'
    )
    
    args = parser.parse_args()
    
    if args.test_token:
        token = args.token or os.getenv('LINKEDIN_ACCESS_TOKEN')
        
        if not token:
            print("❌ No token provided")
            print("Usage: python linkedin_oauth_setup.py --test-token --token YOUR_TOKEN")
            print("Or set LINKEDIN_ACCESS_TOKEN environment variable")
            return 1
        
        oauth = LinkedInOAuth()
        if oauth.test_token(token):
            print("✅ Token is valid!")
            return 0
        else:
            print("❌ Token is invalid or expired")
            return 1
    else:
        # Run interactive setup
        interactive_setup()
        return 0


if __name__ == "__main__":
    sys.exit(main())

