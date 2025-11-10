"""Convert DOCX resume to PDF"""
from docx2pdf import convert
import os

def convert_resume():
    """Convert the latest resume to PDF"""
    
    input_file = "reports/Robert_Reichert_Resume_LATEST.docx"
    output_file = "reports/Robert_Reichert_Resume_LATEST.pdf"
    
    print(f"Converting {input_file} to PDF...")
    
    try:
        convert(input_file, output_file)
        print(f"✅ PDF created: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Note: You may need to install: pip install docx2pdf")
        return False

if __name__ == "__main__":
    convert_resume()

