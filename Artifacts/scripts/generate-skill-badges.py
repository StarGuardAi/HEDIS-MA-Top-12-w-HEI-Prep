#!/usr/bin/env python3
"""Generate skill badges for README from SKILLS_DEMONSTRATED.md"""

import re
from pathlib import Path


def parse_skills(skills_md_path):
    """Parse SKILLS_DEMONSTRATED.md and extract skill counts"""
    with open(skills_md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract skill categories from the Quick Skill Summary table
    category_pattern = r'\|\s*\*\*(.*?)\*\*\s*\|\s*(\d+)\s*\|\s*(.*?)\s*\|'
    matches = re.findall(category_pattern, content)
    
    skill_counts = {}
    for category, count, level in matches:
        skill_counts[category.strip()] = int(count)
    
    return skill_counts


def generate_skill_summary_badges(skill_counts):
    """Generate markdown badges for skill counts"""
    badges = []
    
    color_map = {
        'Machine Learning': 'red',
        'Backend Development': 'blue',
        'Frontend Development': '61DAFB',
        'Data Engineering': 'green',
        'Healthcare Domain': '009688',
        'DevOps': 'orange',
        'Database Design': '4169E1',
    }
    
    for category, count in skill_counts.items():
        # Clean category name for badge URL
        category_clean = category.replace(' ', '%20')
        color = color_map.get(category, 'gray')
        badge = f"![{category}](https://img.shields.io/badge/{category_clean}-{count}%20skills-{color})"
        badges.append(badge)
    
    return '\n'.join(badges)


def calculate_total_skills(skill_counts):
    """Calculate total number of skills"""
    return sum(skill_counts.values())


if __name__ == "__main__":
    skills_path = Path("SKILLS_DEMONSTRATED.md")
    
    if not skills_path.exists():
        print("❌ SKILLS_DEMONSTRATED.md not found")
        print(f"   Current directory: {Path.cwd()}")
        print(f"   Looking for: {skills_path.absolute()}")
        exit(1)
    
    skill_counts = parse_skills(skills_path)
    total_skills = calculate_total_skills(skill_counts)
    badges = generate_skill_summary_badges(skill_counts)
    
    print("✅ Skill badges generated:")
    print()
    print(badges)
    print()
    print(f"📊 Total Skills: {total_skills}")
    print()
    print("💡 Add these to README.md after the title section")
    print()
    print("Example usage:")
    print("```markdown")
    print("## 🔖 Professional Badges")
    print()
    print(badges.split('\n')[0])  # Show first badge as example
    print("```")

