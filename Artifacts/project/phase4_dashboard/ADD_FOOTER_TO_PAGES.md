# Add Footer Value Proposition to All Pages

## Quick Script to Add Footer

Run this Python script to add the footer to all pages:

```python
import os
import re

pages_dir = "pages"
footer_code = '''
# Value Proposition Footer
st.markdown("---")
from utils.value_proposition import render_footer_value_proposition
render_footer_value_proposition()

'''

# Patterns to find where to insert footer
patterns = [
    r'st\.markdown\("---"\)\s+st\.info\(""".*?Demonstration Portfolio Project',
    r'# Footer',
    r'# Disclaimer',
    r'st\.markdown\("---"\)\s*$'
]

for filename in os.listdir(pages_dir):
    if filename.endswith('.py') and not filename.startswith('__'):
        filepath = os.path.join(pages_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if footer already added
        if 'render_footer_value_proposition' in content:
            continue
        
        # Try to find insertion point
        inserted = False
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
            if match:
                pos = match.start()
                content = content[:pos] + footer_code + content[pos:]
                inserted = True
                break
        
        if inserted:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Added footer to {filename}")
```

## Manual Addition

For each page file, add this before the existing footer/disclaimer:

```python
# Value Proposition Footer
st.markdown("---")
from utils.value_proposition import render_footer_value_proposition
render_footer_value_proposition()
```

## Pages Already Updated

- ✅ `app.py` (main page) - Sidebar and Footer
- ✅ `pages/1_📊_ROI_by_Measure.py` - Footer added
- ✅ `pages/18_🤖_Secure_AI_Chatbot.py` - Footer added

## Pages That Need Footer

All other pages in the `pages/` directory need the footer added before their existing footer/disclaimer sections.










