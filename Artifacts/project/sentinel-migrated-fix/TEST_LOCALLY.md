# 🧪 How to Test Your Portfolio Locally

## Quick Methods

### Method 1: View Landing Page (HTML)

**Option A: Simple HTTP Server**
```bash
# In your project directory
python -m http.server 8000

# Then open:
http://localhost:8000
```

**Option B: Double-Click**
- Just double-click `index.html` in your file explorer
- Opens in your default browser
- Some features may not work (relative paths)

**Option C: Use the Batch File**
```bash
# Windows:
TEST_LOCALLY.bat

# This will:
# - Open http://localhost:8000
# - Start a local server
```

---

### Method 2: Test Streamlit Changes

**Start Streamlit App:**
```bash
streamlit run streamlit_app.py

# Opens at:
http://localhost:8501
```

**What to Check:**
- ✅ Business Impact section appears at top
- ✅ "How This Solves Real Problems" expander works
- ✅ Contact CTA buttons at bottom work
- ✅ All 10 pages still accessible
- ✅ No errors or warnings

---

### Method 3: Test Both Together

**Terminal 1 (Landing Page):**
```bash
python -m http.server 8000
# Opens: http://localhost:8000
```

**Terminal 2 (Streamlit):**
```bash
streamlit run streamlit_app.py
# Opens: http://localhost:8501
```

**Test the Connection:**
1. Open landing page: http://localhost:8000
2. Click "Try Live Demo" button
3. Update the link to: `http://localhost:8501`
4. Verify it opens Streamlit

---

## What to Look For

### Landing Page (HTML) Checks:
- ✅ Logo/branding looks professional
- ✅ Hero section loads instantly
- ✅ All stats display correctly ($13-27M, 12 measures, etc.)
- ✅ Featured project section visible
- ✅ Problem/Solution/Results cards readable
- ✅ "Try Live Demo" button works
- ✅ "View Code" button works
- ✅ Contact section at bottom
- ✅ Mobile responsive (resize browser window)

### Streamlit Changes to Verify:
- ✅ Page title: "HEDIS MA Analytics Tool"
- ✅ Icon: 📊 (not 🏥)
- ✅ Menu → About: mentions "Reducing HEDIS reporting complexity"
- ✅ Business Impact section at top of home page
- ✅ "How This Solves Real Problems" expander works
- ✅ Contact CTA buttons at bottom of home page
- ✅ Email and LinkedIn links work
- ✅ All other pages still function

---

## Quick Visual Checklist

### Landing Page Should Show:
```
✓ Professional hero section
✓ "Transform Healthcare Data Into Business Intelligence"
✓ "$13-27M Value" stats
✓ Featured project section
  - Challenge card
  - Solution card
  - Results card
✓ "Try Live Demo" button
✓ "View Code" button
✓ Case studies (Humana/Centene)
✓ Contact section
```

### Streamlit Home Page Should Show:
```
✓ "📊 Business Impact" section at top
✓ Time savings: "3 hours to 15 minutes"
✓ "💼 How This Solves Real Problems" expander
✓ All original content still visible
✓ Contact CTA buttons at bottom
✓ Email button (opens mailto)
✓ LinkedIn button (opens LinkedIn)
```

---

## Common Issues & Fixes

### Issue: "Module not found" error
**Fix:**
```bash
pip install streamlit
```

### Issue: HTML doesn't load CSS
**Fix:** Using local server instead of file://
```bash
python -m http.server 8000
```

### Issue: Links don't work in HTML
**Fix:** Update links to actual URLs in index.html
```html
<!-- Change to your actual Streamlit URL -->
href="https://hedis-ma-top-12-w-hei-prep.streamlit.app/"
```

### Issue: Streamlit won't start
**Fix:**
```bash
streamlit --version
# If not installed:
pip install streamlit plotly pandas numpy
```

---

## Screenshot Checklist

Before deploying, take screenshots of:

1. **Landing Page:**
   - Full page (desktop view)
   - Mobile view (resize to 375px wide)
   - Hero section
   - Featured project section

2. **Streamlit:**
   - Business Impact section
   - Expanded "How This Solves Real Problems"
   - Contact CTA buttons

**Save screenshots for:**
- LinkedIn posts
- Portfolio documentation
- Before/after comparisons

---

## Deploy After Testing

Once you've verified everything works locally:

1. **Deploy Landing Page:**
   ```bash
   # Push to GitHub, then:
   # - Go to vercel.com
   # - Import repository
   # - Deploy
   ```

2. **Deploy Streamlit Changes:**
   ```bash
   # Your Streamlit Cloud auto-updates on git push
   git add streamlit_app.py
   git commit -m "Add business context and contact CTAs"
   git push origin main
   ```

---

## Testing on Mobile

**iPhone/Android Testing:**
1. Find your computer's local IP address:
   ```bash
   # Windows:
   ipconfig
   
   # Mac/Linux:
   ifconfig
   ```

2. On your phone, open:
   ```
   http://192.168.1.XXX:8000
   ```

3. Test:
   - Landing page looks good on mobile
   - All buttons are tap-able
   - Text is readable without zooming
   - Navigation works

---

## ✅ Ready to Deploy Checklist

Before going live, verify:

### Landing Page:
- [ ] Loads in <2 seconds
- [ ] Mobile responsive (test on phone)
- [ ] All links work
- [ ] Contact information correct
- [ ] Professional appearance

### Streamlit:
- [ ] Business context visible
- [ ] Contact CTAs work
- [ ] All 10 pages accessible
- [ ] No errors in console

### Both:
- [ ] Streamlit URLs in landing page are correct
- [ ] Consistent branding
- [ ] Professional throughout

---

## 🚀 Deploy When Ready

**Quick Deploy (5 minutes):**

1. **Test locally** (follow steps above)
2. **Fix any issues** you find
3. **Deploy to Vercel:**
   - Go to https://vercel.com
   - Import repository
   - Deploy!

4. **Update Streamlit:**
   ```bash
   git push origin main
   # Streamlit Cloud auto-deploys
   ```

5. **Share on LinkedIn:**
   ```
   🚀 Just launched my portfolio!
   
   Landing: [your-vercel-url]
   Demo: [your-streamlit-url]
   
   Features: Business impact, interactive demos, production-ready
   ```

---

**Time to test:** 5 minutes  
**Time to deploy:** 3 minutes  
**Total:** Less than 10 minutes to go live!

🎉 **Start with Method 1 to view your landing page locally!**



---
*This file is maintained by Sentinel Analytics. For inquiries, contact reichert.sentinel.ai@gmail.com.*
