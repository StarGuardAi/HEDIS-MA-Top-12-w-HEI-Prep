"""
Generate LinkedIn-ready timeline infographic image
Creates a high-resolution PNG image suitable for Buffer/LinkedIn upload
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
from datetime import datetime

def create_linkedin_timeline_image(output_path="timeline_infographic.png"):
    """
    Create a professional timeline infographic image for LinkedIn
    Returns the path to the saved image
    LinkedIn optimal size: 1200x627px (1.91:1 ratio)
    """
    
    # Create figure with high DPI for LinkedIn (recommended: 1200x627px or higher)
    # Using 16:9 ratio for better visual appeal
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)  # 2400x1350px final size
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    
    # Timeline data
    timeline_data = [
        {
            "month": "Month 1-2",
            "title": "Core Data Architecture",
            "subtitle": "Synthetic Data Generation",
            "description": "PostgreSQL schema • Data modeling • Synthetic HEDIS data",
            "color": "#4A3D6F",
            "start": 0,
            "end": 2
        },
        {
            "month": "Month 2-3",
            "title": "Dashboard Development",
            "subtitle": "Visualization & UI",
            "description": "Streamlit dashboard • Plotly charts • Responsive design",
            "color": "#6F5F96",
            "start": 2,
            "end": 3
        },
        {
            "month": "Month 3-4",
            "title": "Predictive Models",
            "subtitle": "ML Integration",
            "description": "Gap closure predictions • ROI models • Scenario analysis",
            "color": "#8B7BA8",
            "start": 3,
            "end": 4
        },
        {
            "month": "Month 4-5",
            "title": "AI Context Engineering",
            "subtitle": "Chatbot & RAG",
            "description": "Local LLM • Context engineering • Agentic RAG • Secure AI",
            "color": "#A896C0",
            "start": 4,
            "end": 5
        },
        {
            "month": "Month 5-6",
            "title": "Production Hardening",
            "subtitle": "Mobile Optimization",
            "description": "Mobile responsiveness • Performance • Security • Deployment",
            "color": "#C5B3D8",
            "start": 5,
            "end": 6
        }
    ]
    
    # Set up axes
    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(-1, len(timeline_data) + 1)
    ax.axis('off')
    
    # Draw timeline phases
    y_positions = []
    for i, phase in enumerate(timeline_data):
        y_pos = len(timeline_data) - i - 0.5
        y_positions.append(y_pos)
        
        # Draw timeline bar
        width = phase["end"] - phase["start"]
        rect = FancyBboxPatch(
            (phase["start"], y_pos - 0.3),
            width, 0.6,
            boxstyle="round,pad=0.02",
            linewidth=0,
            facecolor=phase["color"],
            edgecolor=None,
            zorder=2
        )
        ax.add_patch(rect)
        
        # Add month label above
        ax.text(
            (phase["start"] + phase["end"]) / 2,
            y_pos + 0.4,
            phase["month"],
            ha='center',
            va='bottom',
            fontsize=11,
            fontweight='bold',
            color=phase["color"],
            fontfamily='Arial'
        )
        
        # Add title
        ax.text(
            (phase["start"] + phase["end"]) / 2,
            y_pos,
            phase["title"],
            ha='center',
            va='center',
            fontsize=14,
            fontweight='bold',
            color='#FFFFFF',
            fontfamily='Arial',
            zorder=3
        )
        
        # Add subtitle
        ax.text(
            (phase["start"] + phase["end"]) / 2,
            y_pos - 0.35,
            phase["subtitle"],
            ha='center',
            va='top',
            fontsize=10,
            color='#666666',
            fontfamily='Arial',
            style='italic'
        )
    
    # Draw main timeline line
    ax.plot([0, 6], [-0.5, -0.5], color='#4ade80', linewidth=6, zorder=1)
    
    # Draw start and end markers
    ax.scatter([0, 6], [-0.5, -0.5], s=400, c='#4ade80', 
               edgecolors='#FFFFFF', linewidths=3, zorder=3)
    
    # Add START and 6 MONTHS labels
    ax.text(0, -0.9, 'START', ha='center', va='top',
           fontsize=12, fontweight='bold', color='#4ade80', fontfamily='Arial')
    ax.text(6, -0.9, '6 MONTHS', ha='center', va='top',
           fontsize=12, fontweight='bold', color='#4ade80', fontfamily='Arial')
    
    # Add main title
    ax.text(3, len(timeline_data) + 0.6,
           'How Long Did It Take to Build StarGuard AI?',
           ha='center', va='bottom',
           fontsize=24, fontweight='bold', color='#4A3D6F', fontfamily='Arial')
    
    ax.text(3, len(timeline_data) + 0.3,
           '6 Months of Evenings & Weekends',
           ha='center', va='bottom',
           fontsize=16, color='#666666', fontfamily='Arial')
    
    # Add experience note box
    experience_box = FancyBboxPatch(
        (0.5, -0.3),
        5, 0.5,
        boxstyle="round,pad=0.05",
        linewidth=2,
        facecolor='#E8F5E9',
        edgecolor='#4ade80',
        zorder=1
    )
    ax.add_patch(experience_box)
    
    ax.text(3, -0.05,
           '22 Years of Healthcare Data Experience',
           ha='center', va='center',
           fontsize=14, fontweight='bold', color='#2E7D32', fontfamily='Arial')
    
    ax.text(3, -0.25,
           'Condensed into a portfolio showing thinking, not just coding',
           ha='center', va='center',
           fontsize=11, color='#1B5E20', fontfamily='Arial', style='italic')
    
    # Add architecture decisions at bottom
    arch_y = -0.8
    arch_texts = [
        ('PostgreSQL', '#4A3D6F'),
        ('Streamlit', '#6F5F96'),
        ('Local LLM', '#8B7BA8')
    ]
    
    for i, (text, color) in enumerate(arch_texts):
        x_pos = 1.5 + i * 1.5
        ax.text(x_pos, arch_y, text, ha='center', va='top',
               fontsize=10, fontweight='bold', color=color, fontfamily='Arial')
        ax.text(x_pos, arch_y - 0.15, 'Architecture', ha='center', va='top',
               fontsize=8, color='#999999', fontfamily='Arial')
    
    # Add hashtags at very bottom
    hashtags = "#BuildProcess #Portfolio #HealthcareAnalytics #Development #DataScience"
    ax.text(3, arch_y - 0.4, hashtags, ha='center', va='top',
           fontsize=9, color='#999999', fontfamily='Arial')
    
    # Add StarGuard AI branding (without emoji to avoid font issues)
    ax.text(6.2, len(timeline_data) + 0.6, 'StarGuard AI',
           ha='right', va='bottom',
           fontsize=12, fontweight='bold', color='#4A3D6F', fontfamily='Arial')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', 
                facecolor='white', edgecolor='none', format='png',
                pad_inches=0.2)
    plt.close()
    
    print(f"Timeline infographic created: {output_path}")
    print(f"  Size: 2400x1350px (16:9 ratio, LinkedIn optimized)")
    return output_path


if __name__ == "__main__":
    output_file = create_linkedin_timeline_image("timeline_infographic.png")
    print(f"Timeline infographic saved to: {output_file}")
