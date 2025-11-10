#!/usr/bin/env python3
"""Generate visual skill matrix as Markdown table"""

from pathlib import Path

skills_matrix = {
    'Machine Learning': {
        'XGBoost': '●●●●○',
        'LightGBM': '●●●●○',
        'scikit-learn': '●●●●○',
        'Feature Engineering': '●●●●○',
        'SHAP Explainability': '●●●○○',
        'Model Evaluation': '●●●●○',
        'Imbalanced Learning': '●●●○○',
    },
    'Backend Development': {
        'FastAPI': '●●●○○',
        'Python': '●●●●○',
        'Pandas': '●●●●○',
        'NumPy': '●●●○○',
        'RESTful APIs': '●●●○○',
        'Data Processing': '●●●●○',
    },
    'Frontend Development': {
        'Streamlit': '●●●○○',
        'Plotly': '●●●○○',
        'Data Visualization': '●●●○○',
        'Interactive Dashboards': '●●●○○',
    },
    'Healthcare Domain': {
        'HEDIS Specifications': '●●●●○',
        'CMS Star Ratings': '●●●●○',
        'Clinical Validation': '●●●●○',
        'Healthcare Data': '●●●●○',
        'Regulatory Compliance': '●●●○○',
    },
    'Data Engineering': {
        'ETL Pipelines': '●●●●○',
        'Feature Engineering': '●●●●○',
        'Data Validation': '●●●○○',
        'Database Design': '●●●○○',
    },
    'DevOps': {
        'Docker': '●●●○○',
        'CI/CD Concepts': '●●○○○',
        'Deployment': '●●●○○',
    }
}


def generate_markdown_matrix():
    """Generate markdown table for skill matrix"""
    markdown = "## 📊 Visual Skill Proficiency Matrix\n\n"
    markdown += "Legend: ●●●●● Expert | ●●●●○ Advanced | ●●●○○ Intermediate | ●●○○○ Beginner\n\n"
    markdown += "| Category | Skill | Proficiency |\n"
    markdown += "|----------|-------|-------------|\n"
    
    for category, skills in skills_matrix.items():
        for i, (skill, level) in enumerate(skills.items()):
            if i == 0:
                rowspan = len(skills)
                markdown += f"| **{category}** | {skill} | {level} |\n"
            else:
                markdown += f"| | {skill} | {level} |\n"
        markdown += "| | | |\n"  # Empty row for spacing
    
    return markdown


def generate_html_matrix():
    """Generate HTML table for skill matrix"""
    html = """
<table>
  <thead>
    <tr>
      <th>Category</th>
      <th>Skill</th>
      <th>Proficiency</th>
    </tr>
  </thead>
  <tbody>
"""
    
    for category, skills in skills_matrix.items():
        first = True
        for skill, level in skills.items():
            if first:
                rowspan = len(skills)
                html += f"    <tr><td rowspan='{rowspan}'><b>{category}</b></td>"
                first = False
            else:
                html += "    <tr>"
            
            html += f"<td>{skill}</td><td>{level}</td></tr>\n"
    
    html += """  </tbody>
</table>
"""
    
    return html


if __name__ == "__main__":
    # Generate markdown version
    markdown_matrix = generate_markdown_matrix()
    print("✅ Markdown Skill Matrix:")
    print()
    print(markdown_matrix)
    
    # Save to file
    output_dir = Path("docs")
    output_dir.mkdir(exist_ok=True)
    
    markdown_path = output_dir / "skill-matrix.md"
    with open(markdown_path, 'w', encoding='utf-8') as f:
        f.write(markdown_matrix)
    
    print(f"✅ Markdown matrix saved to {markdown_path}")
    
    # Generate HTML version
    html_matrix = generate_html_matrix()
    html_path = output_dir / "skill-matrix.html"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_matrix)
    
    print(f"✅ HTML matrix saved to {html_path}")
    print()
    print("💡 You can include the markdown version in README.md")
    print("   Or embed the HTML version in documentation")

