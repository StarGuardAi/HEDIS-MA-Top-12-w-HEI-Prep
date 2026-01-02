# AI Executive Insights Setup Guide

This guide explains how to configure and use the AI-powered executive insights generator for the HEDIS Portfolio Optimizer.

## Overview

The AI Insights Generator analyzes HEDIS portfolio data and generates natural language executive summaries with:
- **Executive Summary**: High-level findings in conversational language
- **Actionable Recommendations**: Specific, prioritized actions with numbers and timelines
- **Why This Matters**: Business impact explanations for non-technical executives

## Features

- ✅ Pulls real metrics from your HEDIS portfolio database
- ✅ Generates natural language summaries like:
  > "Your HbA1c testing program shows 93% predicted closure rate with $285K potential. 
  > Recommend prioritizing 847 members in the next 30 days for maximum ROI."
- ✅ Supports both OpenAI GPT and Anthropic Claude APIs
- ✅ Desktop and mobile-optimized views
- ✅ Actionable recommendations with specific numbers and timelines
- ✅ "Why this matters" explanations for executives

## API Provider Setup

You can use either OpenAI or Anthropic Claude API. Choose one:

### Option 1: OpenAI API

1. **Get API Key**: Sign up at [OpenAI Platform](https://platform.openai.com/) and create an API key

2. **Set Environment Variable** (Recommended for local development):
   ```bash
   # Windows PowerShell
   $env:OPENAI_API_KEY="sk-your-key-here"
   
   # Windows CMD
   set OPENAI_API_KEY=sk-your-key-here
   
   # Linux/Mac
   export OPENAI_API_KEY="sk-your-key-here"
   ```

3. **Or Use Streamlit Secrets** (Recommended for Streamlit Cloud):
   Create `.streamlit/secrets.toml`:
   ```toml
   [openai]
   api_key = "sk-your-key-here"
   ```

### Option 2: Anthropic Claude API

1. **Get API Key**: Sign up at [Anthropic Console](https://console.anthropic.com/) and create an API key

2. **Set Environment Variable**:
   ```bash
   # Windows PowerShell
   $env:ANTHROPIC_API_KEY="sk-ant-your-key-here"
   
   # Windows CMD
   set ANTHROPIC_API_KEY=sk-ant-your-key-here
   
   # Linux/Mac
   export ANTHROPIC_API_KEY="sk-ant-your-key-here"
   ```

3. **Or Use Streamlit Secrets**:
   Create `.streamlit/secrets.toml`:
   ```toml
   [anthropic]
   api_key = "sk-ant-your-key-here"
   ```

## Installation

1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

   Or install AI packages separately:
   ```bash
   pip install openai anthropic
   ```

## Usage

### Desktop Version

1. Navigate to the **"🤖 AI Executive Insights"** page in the dashboard
2. Select your date range and focus area (Portfolio Overview, Top Opportunity, or Specific Measure)
3. Click **"✨ Generate AI Insights"**
4. Review the generated:
   - Executive Summary
   - Actionable Recommendations
   - Why This Matters explanation

### Mobile Version

1. Navigate to the **"Mobile AI Insights"** page
2. Select date range and focus
3. Tap **"✨ Generate AI Insights"**
4. View optimized mobile-friendly insights

## How It Works

1. **Data Extraction**: Pulls real metrics from your database:
   - Portfolio summary (investment, closures, ROI, net benefit)
   - Measure-level performance
   - Member prioritization data
   - Activity metrics
   - Budget variance
   - Top opportunities

2. **AI Analysis**: Sends formatted metrics to AI API with prompt:
   - Analyzes performance patterns
   - Identifies key opportunities
   - Generates specific recommendations
   - Explains business impact

3. **Insights Generation**: Returns structured insights:
   - Natural language summary
   - Prioritized recommendations with numbers
   - Executive-friendly explanations

## Example Output

### Executive Summary
> "Your HEDIS portfolio shows strong performance with a 4.2 ROI ratio and $1.2M net benefit. The HbA1c testing program is your top opportunity, with 93% predicted closure rate and $285K potential revenue."

### Recommendations
1. Prioritize 847 members in the HbA1c testing program over the next 30 days for maximum ROI
2. Increase investment in low-touch activities showing 85%+ success rates
3. Reallocate budget from underperforming measures to top 3 opportunities
4. Focus on members with highest predicted closure rates in next quarter

### Why This Matters
> "Optimizing HEDIS performance directly impacts Star Ratings and revenue. Each closure represents $100 in revenue, and prioritizing high-ROI measures maximizes your return on intervention investment while improving member health outcomes."

## Configuration Options

### Model Selection

By default, the system uses:
- OpenAI: `gpt-4o-mini` (cost-effective)
- Anthropic: `claude-3-haiku-20240307` (fast and efficient)

You can modify the model in `utils/ai_insights_generator.py`:
```python
# For OpenAI
generate_executive_insights(metrics, provider="openai", model="gpt-4")

# For Anthropic
generate_executive_insights(metrics, provider="anthropic", model="claude-3-opus-20240229")
```

### Customizing Prompts

Edit the prompt templates in `utils/ai_insights_generator.py` to customize:
- Summary length and style
- Number of recommendations
- Explanation depth
- Tone and language

## Troubleshooting

### "No AI API provider configured"
- Check that you've set either `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`
- Verify the API key is correct and has credits/quota
- For Streamlit Cloud, ensure secrets are configured correctly

### "API error" or "Rate limit exceeded"
- Check your API account has sufficient credits
- Verify API key permissions
- Try a different model (e.g., use `gpt-4o-mini` instead of `gpt-4`)
- Wait a few minutes and retry

### "No data found"
- Verify database connection is working
- Check date range includes data
- Ensure Phase 3 data is loaded in database

### Import errors
- Install missing packages: `pip install openai anthropic`
- Check Python version (3.8+ required)

## Cost Considerations

### OpenAI Pricing (as of 2024)
- `gpt-4o-mini`: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- Typical insight generation: ~$0.001-0.01 per request

### Anthropic Pricing (as of 2024)
- `claude-3-haiku`: ~$0.25 per 1M input tokens, ~$1.25 per 1M output tokens
- Typical insight generation: ~$0.001-0.01 per request

**Tip**: Both providers offer free tiers for testing. Start with the free tier to evaluate.

## Security Best Practices

1. **Never commit API keys to git**
   - Use environment variables or Streamlit secrets
   - Add `.streamlit/secrets.toml` to `.gitignore`

2. **Rotate API keys regularly**
   - Update keys if exposed
   - Use separate keys for development and production

3. **Monitor API usage**
   - Set usage limits in API provider dashboard
   - Review costs regularly

## Support

For issues or questions:
- 📧 **Email**: reichert.starguardai@gmail.com
- 🔗 **LinkedIn**: [sentinel-analytics](https://www.linkedin.com/in/sentinel-analytics/)
- 💻 **GitHub**: [HEDIS-MA-Top-12-w-HEI-Prep](https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep/blob/main/README.md)
- 🎨 **Portfolio**: [Canva Portfolio](https://www.canva.com/design/DAG2WzhiLwM/N_iXUe3eEKL3dzQ2M_0PgQ/edit)

---

**AI Executive Insights** | Powered by OpenAI GPT or Anthropic Claude | Part of HEDIS Portfolio Optimizer

