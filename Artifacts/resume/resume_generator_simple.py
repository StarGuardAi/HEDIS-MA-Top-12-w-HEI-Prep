#!/usr/bin/env python3
"""
Simple Resume Generator for Robert Reichert
Converts markdown resume content to HTML and plain text.
For PDF, use browser Print to PDF from HTML file.
"""

from pathlib import Path
from datetime import datetime
import re

# Read markdown content
script_dir = Path(__file__).parent
markdown_file = script_dir / "resume_content.md"
output_html = script_dir / "resume_output.html"
output_txt = script_dir / "resume_plain_text.txt"

print("="*60)
print("Robert Reichert - Resume Generator (Simple)")
print("="*60)
print()

# Read markdown
print(f"Reading {markdown_file}...")
with open(markdown_file, 'r', encoding='utf-8') as f:
    markdown_content = f.read()

# Simple HTML conversion
print("Converting to HTML...")
html_content = markdown_content

# Convert markdown headers to HTML
html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
html_content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html_content, flags=re.MULTILINE)

# Convert bold
html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)

# Convert links
html_content = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html_content)

# Convert horizontal rules
html_content = html_content.replace('---', '<hr>')

# Convert lists (simple - detect bullet points)
html_content = re.sub(r'^- (.+)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)

# Wrap list items in ul tags
html_content = re.sub(r'(<li>.+?</li>\n?)+', lambda m: '<ul>' + m.group(0) + '</ul>', html_content, flags=re.DOTALL)

# Convert line breaks (but not inside lists)
html_content = html_content.replace('\n', '<br>\n')

# Remove br tags inside ul elements
import re as re2
html_content = re2.sub(r'(<ul>.*?</ul>)', lambda m: m.group(0).replace('<br>\n', '\n'), html_content, flags=re2.DOTALL)

# Full HTML document
full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Robert Reichert - Resume</title>
    <style>
        @page {{
            size: letter;
            margin: 0.3in;
        }}
        body {{
            font-family: 'Calibri', 'Arial', sans-serif;
            font-size: 9pt;
            line-height: 1.15;
            color: #333;
            max-width: 8.5in;
            margin: 0 auto;
            padding: 0;
        }}
        h1 {{
            font-size: 15pt;
            color: #1e3a5f;
            margin-bottom: 1pt;
            border-bottom: 1px solid #1e3a5f;
            padding-bottom: 1pt;
        }}
        h2 {{
            font-size: 10pt;
            color: #1e3a5f;
            margin-top: 4pt;
            margin-bottom: 1pt;
            border-bottom: 1px solid #ccc;
            padding-bottom: 0pt;
        }}
        h3 {{
            font-size: 9.5pt;
            color: #4b5563;
            margin-top: 3pt;
            margin-bottom: 1pt;
        }}
        p, ul, li {{
            margin: 1pt 0;
        }}
        ul {{
            padding-left: 18pt;
        }}
        li {{
            margin: 0pt 0;
        }}
        strong {{
            color: #1e3a5f;
            font-weight: bold;
        }}
        a {{
            color: #3b82f6;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        hr {{
            border: none;
            border-top: 1px solid #ccc;
            margin: 2pt 0;
        }}
        @media print {{
            body {{
                padding: 0;
            }}
            a {{
                color: #333;
                text-decoration: none;
            }}
        }}
        .footer {{
            margin-top: 3pt;
            font-size: 7pt;
            color: #999;
            text-align: center;
            border-top: 1px solid #eee;
            padding-top: 1pt;
        }}
    </style>
</head>
<body>
    {html_content}
    <div class="footer">
        Generated: {datetime.now().strftime('%B %d, %Y')} | sentinel-analytics.my.canva.site
    </div>
</body>
</html>"""

# Save HTML
print(f"Writing {output_html}...")
with open(output_html, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"✓ HTML resume generated: {output_html}")

# Generate plain text
print(f"Generating plain text...")
text = markdown_content
# Remove markdown headers
text = re.sub(r'^#+\s*(.+)$', r'\1\n', text, flags=re.MULTILINE)
# Remove markdown links
text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
# Remove markdown formatting
text = text.replace('**', '')
text = text.replace('*', '')
# Remove horizontal rules
text = text.replace('---', '')
# Clean up extra spaces
text = re.sub(r'\n{3,}', '\n\n', text)

with open(output_txt, 'w', encoding='utf-8') as f:
    f.write(text)

print(f"✓ Plain text resume generated: {output_txt}")

print()
print("="*60)
print("✓ Resume generation complete!")
print()
print("TO CREATE PDF:")
print("1. Open resume_output.html in your browser")
print("2. Press Ctrl+P (or Cmd+P on Mac)")
print("3. Select 'Print to PDF' as destination")
print("4. Save as resume_output.pdf")
print("="*60)

