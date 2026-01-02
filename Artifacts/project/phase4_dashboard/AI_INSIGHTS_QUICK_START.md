# AI Executive Insights - Quick Start

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies
```bash
pip install openai anthropic
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

### 2. Set API Key

**Option A: Environment Variable (Recommended)**
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-your-key-here"

# Windows CMD
set OPENAI_API_KEY=sk-your-key-here

# Linux/Mac
export OPENAI_API_KEY="sk-your-key-here"
```

**Option B: Streamlit Secrets (For Streamlit Cloud)**
Create `.streamlit/secrets.toml`:
```toml
[openai]
api_key = "sk-your-key-here"
```

### 3. Run Dashboard
```bash
streamlit run app.py
```

Navigate to **"🤖 AI Executive Insights"** page and click **"✨ Generate AI Insights"**

## 📋 What You'll Get

1. **Executive Summary**: Natural language overview of your HEDIS portfolio performance
2. **Actionable Recommendations**: Specific, prioritized actions with numbers and timelines
3. **Why This Matters**: Business impact explanation for executives

## 💡 Example Output

**Summary:**
> "Your HEDIS portfolio shows strong performance with a 4.2 ROI ratio and $1.2M net benefit. The HbA1c testing program is your top opportunity, with 93% predicted closure rate and $285K potential revenue."

**Recommendations:**
1. Prioritize 847 members in the HbA1c testing program over the next 30 days for maximum ROI
2. Increase investment in low-touch activities showing 85%+ success rates
3. Reallocate budget from underperforming measures to top 3 opportunities

**Why This Matters:**
> "Optimizing HEDIS performance directly impacts Star Ratings and revenue. Each closure represents $100 in revenue, and prioritizing high-ROI measures maximizes your return on intervention investment."

## 🔧 Troubleshooting

**"No AI API provider configured"**
- Check that you've set `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`
- Restart the Streamlit app after setting environment variables

**"API error"**
- Verify API key is correct
- Check account has sufficient credits
- Try a different model (see `AI_INSIGHTS_SETUP.md`)

## 📚 More Information

See `AI_INSIGHTS_SETUP.md` for:
- Detailed setup instructions
- Model selection options
- Cost considerations
- Security best practices
- Customization options

---

**Ready to generate insights?** Open the dashboard and navigate to the AI Executive Insights page!

