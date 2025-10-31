# 🔐 Manual GitHub Authentication Guide

**Issue:** The interactive authentication script isn't working well.  
**Solution:** Authenticate manually with these simple steps.

---

## ✅ **EASIEST METHOD: Use PowerShell Directly**

### **Step 1: Open PowerShell in this directory**

Right-click in the project folder → "Open in Terminal" or "Open PowerShell here"

### **Step 2: Add GitHub CLI to PATH**

```powershell
$env:Path += ";C:\Program Files\GitHub CLI"
```

### **Step 3: Authenticate**

```powershell
gh auth login
```

### **Step 4: Follow these selections:**

When prompted, use **arrow keys** and **Enter**:

1. **Where do you use GitHub?**  
   → Select: `GitHub.com` (press Enter)

2. **What is your preferred protocol?**  
   → Select: `HTTPS` (press Enter)

3. **Authenticate Git with your GitHub credentials?**  
   → Select: `Yes` (press Enter)

4. **How would you like to authenticate?**  
   → Select: `Login with a web browser` (press Enter)

5. **You'll see a code like:** `A1B2-C3D4`  
   → **Copy this code**

6. **Press Enter**  
   → Your browser will open automatically

7. **In the browser:**  
   → Paste the code  
   → Click "Authorize GitHub CLI"  
   → Done! ✅

### **Step 5: Verify authentication:**

```powershell
gh auth status
```

Should show: `✓ Logged in to github.com as YOUR_USERNAME`

---

## 🔄 **ALTERNATIVE: Use Personal Access Token**

If the browser method doesn't work:

### **Step 1: Create a token**

1. Visit: https://github.com/settings/tokens?type=beta
2. Click: **"Generate new token"** (Fine-grained token)
3. Settings:
   - **Token name:** `HEDIS GSD Project`
   - **Expiration:** 90 days
   - **Repository access:** Only select repositories → `hedis-gsd-prediction-engine`
   - **Permissions:**
     - Contents: **Read and write** ✅
     - Metadata: Read-only (auto-selected)
4. Click: **"Generate token"**
5. **COPY the token** (format: `github_pat_...`)

### **Step 2: Authenticate with the token**

In PowerShell:

```powershell
# Paste your token in place of YOUR_TOKEN_HERE
$token = "github_pat_YOUR_TOKEN_HERE"
$token | gh auth login --with-token
```

### **Step 3: Verify**

```powershell
gh auth status
```

---

## ✅ **After Successful Authentication**

Once you see the success message, you're ready to publish!

### **Publish Milestone 1:**
```powershell
.\publish_all.bat
```
Enter: `1`

### **Publish Milestone 2:**
```powershell
.\publish_all.bat
```
Enter: `2`

### **Push to GitHub:**
```bash
git push origin main
```

---

## 🚨 **Troubleshooting**

### **Issue: "gh: command not found"**

**Fix:** Run this first in your PowerShell session:
```powershell
$env:Path += ";C:\Program Files\GitHub CLI"
```

Then try authentication again.

---

### **Issue: "Failed to authenticate"**

**Fix 1:** Try the token method (above)

**Fix 2:** Logout and try again:
```powershell
gh auth logout
gh auth login
```

---

### **Issue: "Permission denied" when pushing**

**Fix:** After authenticating with `gh`, also configure git:
```powershell
gh auth setup-git
```

---

## 📋 **Quick Reference**

```powershell
# Check if authenticated
gh auth status

# Login (interactive)
gh auth login

# Login (with token)
echo YOUR_TOKEN | gh auth login --with-token

# Setup git credentials
gh auth setup-git

# Logout
gh auth logout
```

---

## ✨ **What Happens After Authentication**

Once authenticated, all these will work automatically:

- ✅ `publish_all.bat` - Creates GitHub releases
- ✅ `publish_github.bat` - Updates README and badges
- ✅ GitHub CLI commands in scripts
- ✅ `git push` to GitHub

---

## 🎯 **Expected Output After Success**

```
✓ Logged in to github.com account YOUR_USERNAME (keyring)
✓ Git operations protocol: https
✓ Token: gho_************************************
✓ Token scopes: gist, read:org, repo, workflow
```

---

**Ready to publish after you see the success message!** 🚀

**Recommended:** Use the first method (browser login) - it's the simplest once you're in PowerShell directly.



---
*This file is maintained by Sentinel Analytics. For inquiries, contact reichert.sentinel.ai@gmail.com.*
