#!/usr/bin/env python3
"""
Resume Generator for Robert Reichert
Converts markdown resume content to PDF format.
"""

import os
import sys
from pathlib import Path

try:
    from markdown import markdown
    from weasyprint import HTML, CSS
except ImportError:
    print("Installing required packages...")
    os.system(f"{sys.executable} -m pip install markdown weasyprint")

from markdown import markdown
from weasyprint import HTML, CSS
from datetime import datetime

# Resume styling
RESUME_CSS = """
@page {
    size: letter;
    margin: 0.5in;
}

body {
    font-family: 'Calibri', 'Arial', sans-serif;
    font-size: 11pt;
    line-height: 1.4;
    color: #333;
    max-width: 8.5in;
    margin: 0 auto;
}

h1 {
    font-size: 20pt;
    color: #1e3a5f;
    margin-bottom: 5pt;
    border-bottom: 2px solid #1e3a5f;
    padding-bottom: 5pt;
}

h2 {
    font-size: 14pt;
    color: #1e3a5f;
    margin-top: 15pt;
    margin-bottom: 8pt;
    border-bottom: 1px solid #ccc;
    padding-bottom: 3pt;
}

h3 {
    font-size: 12pt;
    color: #4b5563;
    margin-top: 12pt;
    margin-bottom: 5pt;
}

p {
    margin: 5pt 0;
}

ul {
    margin: 5pt 0;
    padding-left: 20pt;
}

li {
    margin: 3pt 0;
}

strong {
    color: #1e3a5f;
    font-weight: bold;
}

header {
    text-align: center;
    margin-bottom: 20pt;
}

.section {
    margin-bottom: 15pt;
}

.subsection {
    margin-bottom: 10pt;
}

.print-only {
    display: block;
}

@media print {
    .no-print {
        display: none;
    }
}
"""

def generate_resume_pdf():
    """Generate PDF resume from markdown content."""
    
    # Paths
    script_dir = Path(__file__).parent
    markdown_file = script_dir / "resume_content.md"
    output_pdf = script_dir / "resume_output.pdf"
    output_html = script_dir / "resume_output.html"
    
    # Read markdown content
    print("Reading resume content...")
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convert markdown to HTML
    print("Converting markdown to HTML...")
    html_content = markdown(markdown_content, extensions=['extra', 'nl2br', 'sane_lists'])
    
    # Wrap in full HTML document
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Robert Reichert - Resume</title>
        <style>{RESUME_CSS}</style>
    </head>
    <body>
        {html_content}
        <div class="print-only" style="margin-top: 20pt; font-size: 9pt; color: #999; text-align: center;">
            Generated: {datetime.now().strftime('%B %d, %Y')} | sentinel-analytics.my.canva.site
        </div>
    </body>
    </html>
    """
    
    # Save HTML (for preview)
    print(f"Saving HTML to {output_html}...")
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    # Generate PDF
    print(f"Generating PDF to {output_pdf}...")
    try:
        html_doc = HTML(string=full_html)
        html_doc.write_pdf(output_pdf)
        print(f"✓ Resume PDF generated successfully: {output_pdf}")
        
        # Get file size
        size_kb = output_pdf.stat().st_size / 1024
        print(f"✓ File size: {size_kb:.1f} KB")
        
    except Exception as e:
        print(f"✗ Error generating PDF: {e}")
        print("\nTroubleshooting:")
        print("1. Install weasyprint: pip install weasyprint")
        print("2. Install system dependencies:")
        print("   Windows: winget install GTK3_Runtime")
        print("   Linux: apt-get install python3-cffi python3-brotli")
        print("   macOS: brew install cairo pango gdk-pixbuf libffi")
        return False
    
    return True

def generate_plain_text_resume():
    """Generate plain text resume for copy-paste applications."""
    
    script_dir = Path(__file__).parent
    markdown_file = script_dir / "resume_content.md"
    output_txt = script_dir / "resume_plain_text.txt"
    
    print(f"Generating plain text resume to {output_txt}...")
    
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple markdown to plain text conversion
    text = content
    # Remove markdown headers
    text = text.replace('# ', '')
    text = text.replace('## ', '')
    text = text.replace('### ', '')
    # Remove markdown links
    import re
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Remove markdown formatting
    text = text.replace('**', '')
    text = text.replace('*', '')
    # Remove horizontal rules
    text = text.replace('---', '')
    
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"✓ Plain text resume generated: {output_txt}")
    return True

if __name__ == "__main__":
    print("="*60)
    print("Robert Reichert - Resume Generator")
    print("="*60)
    print()
    
    # Generate PDF
    pdf_success = generate_resume_pdf()
    
    # Generate plain text
    txt_success = generate_plain_text_resume()
    
    print()
    print("="*60)
    if pdf_success and txt_success:
        print("✓ All resume formats generated successfully!")
    else:
        print("⚠ Some formats had errors. Check output above.")
    print("="*60)

