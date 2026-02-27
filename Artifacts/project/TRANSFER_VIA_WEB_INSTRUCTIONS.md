# Transfer Repository to StarGuardAi Organization - Web Interface

## Current Status
- **Source:** [reichert-science-intelligence/HEDIS-MA-Top-12-w-HEI-Prep](https://github.com/reichert-science-intelligence/HEDIS-MA-Top-12-w-HEI-Prep)
- **Target:** [StarGuardAi](https://github.com/StarGuardAi)
- **Note:** GitHub CLI doesn't support transfer - must use web interface

## Step-by-Step Transfer Instructions

### Step 1: Navigate to Repository Settings
1. Go to: https://github.com/reichert-science-intelligence/HEDIS-MA-Top-12-w-HEI-Prep
2. Click the **"Settings"** tab (at the top of the repository page)
   - If you don't see Settings, you need to be an owner or admin of the `reichert-science-intelligence` organization

### Step 2: Go to Danger Zone
1. Scroll down to the bottom of the Settings page
2. Find the **"Danger Zone"** section (red warning area at the bottom)

### Step 3: Transfer Repository
1. Click **"Transfer ownership"** button (in the Danger Zone section)
2. In the "Transfer ownership" dialog:
   - **New owner:** Enter `StarGuardAi` (the organization name)
   - **Repository name:** Enter `HEDIS-MA-Top-12-w-HEI-Prep` to confirm
   - Click **"I understand, transfer this repository"**

### Step 4: Confirmation
1. GitHub will send a confirmation email
2. The transfer may take a few moments to complete
3. Once complete, you'll be redirected to: https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep

## Prerequisites

Before transferring, ensure:
- ✅ You are an **owner** of the `reichert-science-intelligence` organization
- ✅ You are an **owner** of the `StarGuardAi` organization
- ✅ You have transfer permissions enabled in the `StarGuardAi` organization settings

## After Transfer

Once the transfer completes:

1. **Verify transfer:**
   - Visit: https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep
   - Confirm it shows `StarGuardAi` as the owner

2. **Update local git remote** (if needed):
   ```powershell
   git remote set-url origin https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep.git
   ```

3. **Check StarGuardAi organization:**
   - Visit: https://github.com/StarGuardAi
   - The repository should now be visible in the organization

## Troubleshooting

### "Settings" tab not visible:
- You need to be an owner/admin of `reichert-science-intelligence` organization
- Go to organization settings and ensure you have the correct role

### "Transfer ownership" button grayed out:
- Check that you're an owner of both organizations
- Verify transfer permissions are enabled in organization settings

### Organization name not found:
- Ensure the exact organization name is `StarGuardAi` (case-sensitive)
- You can verify at: https://github.com/StarGuardAi

## Alternative: Using GitHub API

If you have API access and prefer automation, you can use:

```powershell
# PowerShell example using GitHub API
$headers = @{
    "Authorization" = "token YOUR_TOKEN"
    "Accept" = "application/vnd.github.v3+json"
}

$body = @{
    new_owner = "StarGuardAi"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://api.github.com/repos/reichert-science-intelligence/HEDIS-MA-Top-12-w-HEI-Prep/transfer" -Method POST -Headers $headers -Body $body
```

But the web interface method above is recommended as it's simpler and more reliable.

