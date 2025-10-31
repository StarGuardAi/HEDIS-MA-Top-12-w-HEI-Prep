# Repository Transfer Instructions

## Current Status

- **Current Location:** [reichert-science-intelligence/HEDIS-MA-Top-12-w-HEI-Prep](https://github.com/reichert-science-intelligence/HEDIS-MA-Top-12-w-HEI-Prep)
- **Target Organization:** [StarGuardAi](https://github.com/StarGuardAi)
- **Local Remote:** Already configured to point to `StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep.git`

## Why Commands Hang

Commands may hang due to:
1. **GitHub CLI waiting for prompts** - Some commands need interactive confirmation
2. **Network timeouts** - Slow or unstable connections to GitHub API
3. **Authentication checks** - Verifying permissions before transfer

## Transfer Methods

### Option 1: GitHub CLI Command (Recommended)

Run this command directly in your terminal:

```powershell
gh repo transfer reichert-science-intelligence/HEDIS-MA-Top-12-w-HEI-Prep StarGuardAi --yes
```

**Note:** If it hangs, press `Ctrl+C` and try Option 2.

### Option 2: Via GitHub Web Interface

1. Go to: https://github.com/reichert-science-intelligence/HEDIS-MA-Top-12-w-HEI-Prep/settings
2. Scroll down to "Danger Zone"
3. Click "Transfer ownership"
4. Enter `StarGuardAi` as the new owner
5. Type the repository name to confirm
6. Click "I understand, transfer this repository"

### Option 3: Batch File

Run the provided batch file:
```batch
.\transfer-repo.bat
```

## Prerequisites

1. **You must be an owner** of `reichert-science-intelligence` organization
2. **You must be an owner** of `StarGuardAi` organization  
3. **GitHub CLI authenticated**: Run `gh auth login` if needed
4. **Sufficient permissions** in both organizations

## After Transfer

Once transferred, verify:
1. Visit: https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep
2. Confirm the repository is visible in [StarGuardAi organization](https://github.com/StarGuardAi)
3. The local remote URL is already configured correctly (see `.git/config`)

## Troubleshooting Hanging Commands

If `gh` commands hang:

1. **Check authentication:**
   ```powershell
   gh auth status
   ```

2. **Try interactive mode:**
   ```powershell
   gh auth login
   ```

3. **Use web interface instead** (Option 2 above) - This is more reliable for transfers

4. **Check network:** Ensure stable connection to GitHub

## Verification

After transfer completes:
- ✅ Repository visible at https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep
- ✅ [StarGuardAi organization](https://github.com/StarGuardAi) shows the repository
- ✅ Local git remote already points to correct URL

