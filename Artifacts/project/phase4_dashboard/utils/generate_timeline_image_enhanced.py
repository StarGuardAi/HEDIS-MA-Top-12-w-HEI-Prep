"""
Generate Enhanced LinkedIn-ready timeline infographic image
Professional design optimized for Buffer/LinkedIn upload
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

def create_enhanced_timeline_image(output_path="timeline_infographic_linkedin.png"):
    """
    Create a professional timeline infographic image optimized for LinkedIn
    LinkedIn optimal: 1200x627px (1.91:1 ratio) or 16:9 for better engagement
    """
    
    # Create figure - LinkedIn optimized size
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)  # 2400x1350px
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    
    # Timeline data
    timeline_data = [
        {
            "month": "Month 1-2",
            "title": "Core Data Architecture",
            "subtitle": "Synthetic Data Generation",
            "details": "PostgreSQL • Data Modeling • Synthetic HEDIS Data",
            "color": "#4A3D6F",
            "start": 0,
            "end": 2
        },
        {
            "month": "Month 2-3",
            "title": "Dashboard Development",
            "subtitle": "Visualization & UI",
            "details": "Streamlit • Plotly Charts • Responsive Design",
            "color": "#6F5F96",
            "start": 2,
            "end": 3
        },
        {
            "month": "Month 3-4",
            "title": "Predictive Models",
            "subtitle": "ML Integration",
            "details": "Gap Closure Predictions • ROI Models • Scenario Analysis",
            "color": "#8B7BA8",
            "start": 3,
            "end": 4
        },
        {
            "month": "Month 4-5",
            "title": "AI Context Engineering",
            "subtitle": "Chatbot & RAG",
            "details": "Local LLM • Context Engineering • Agentic RAG • Secure AI",
            "color": "#A896C0",
            "start": 4,
            "end": 5
        },
        {
            "month": "Month 5-6",
            "title": "Production Hardening",
            "subtitle": "Mobile Optimization",
            "details": "Mobile Responsiveness • Performance • Security • Deployment",
            "color": "#C5B3D8",
            "start": 5,
            "end": 6
        }
    ]
    
    # Set up axes with better spacing to prevent overlap
    # Calculate dynamic y limits based on content
    phase_spacing = 1.2
    total_height = len(timeline_data) * phase_spacing + 3  # Top title + phases + bottom content
    ax.set_xlim(-0.8, 6.8)
    ax.set_ylim(-2.5, total_height)
    ax.axis('off')
    
    # Add subtle background gradient effect
    gradient = np.linspace(0, 1, 256).reshape(1, -1)
    gradient = np.vstack((gradient, gradient))
    
    # Draw timeline phases with enhanced design and proper spacing
    # Increased vertical spacing between phases to prevent overlap
    phase_spacing = 1.2  # Space between each phase
    bar_height = 0.5     # Height of the colored bar
    
    for i, phase in enumerate(timeline_data):
        # Calculate y position with proper spacing
        y_pos = (len(timeline_data) - i) * phase_spacing - 0.5
        
        # Draw main timeline bar with shadow effect
        width = phase["end"] - phase["start"]
        
        # Shadow
        shadow = FancyBboxPatch(
            (phase["start"] + 0.05, y_pos - bar_height/2 - 0.05),
            width, bar_height + 0.1,
            boxstyle="round,pad=0.03",
            linewidth=0,
            facecolor='#E0E0E0',
            edgecolor=None,
            zorder=1,
            alpha=0.3
        )
        ax.add_patch(shadow)
        
        # Main bar
        rect = FancyBboxPatch(
            (phase["start"], y_pos - bar_height/2),
            width, bar_height,
            boxstyle="round,pad=0.03",
            linewidth=2,
            facecolor=phase["color"],
            edgecolor='#FFFFFF',
            zorder=2
        )
        ax.add_patch(rect)
        
        # Add month label above bar (with more space)
        ax.text(
            (phase["start"] + phase["end"]) / 2,
            y_pos + bar_height/2 + 0.4,
            phase["month"],
            ha='center',
            va='bottom',
            fontsize=13,
            fontweight='bold',
            color=phase["color"],
            fontfamily='Arial'
        )
        
        # Add title (white text on colored bar) - ensure it fits
        ax.text(
            (phase["start"] + phase["end"]) / 2,
            y_pos,
            phase["title"],
            ha='center',
            va='center',
            fontsize=15,
            fontweight='bold',
            color='#FFFFFF',
            fontfamily='Arial',
            zorder=3,
            wrap=True  # Allow text wrapping if needed
        )
        
        # Add subtitle below bar (with more space)
        ax.text(
            (phase["start"] + phase["end"]) / 2,
            y_pos - bar_height/2 - 0.3,
            phase["subtitle"],
            ha='center',
            va='top',
            fontsize=11,
            color='#666666',
            fontfamily='Arial',
            style='italic'
        )
        
        # Add details below subtitle (with more space)
        ax.text(
            (phase["start"] + phase["end"]) / 2,
            y_pos - bar_height/2 - 0.55,
            phase["details"],
            ha='center',
            va='top',
            fontsize=9,
            color='#999999',
            fontfamily='Arial'
        )
    
    # Calculate timeline line position (below all phases)
    timeline_y = -1.5
    
    # Draw main timeline line (green accent)
    ax.plot([0, 6], [timeline_y, timeline_y], color='#4ade80', linewidth=8, zorder=1, alpha=0.8)
    
    # Draw start and end markers
    for x_pos in [0, 6]:
        circle = plt.Circle((x_pos, timeline_y), 0.15, 
                           facecolor='#4ade80',
                           edgecolor='#FFFFFF', linewidth=4, zorder=3)
        ax.add_patch(circle)
    
    # Add START and 6 MONTHS labels (with more space)
    ax.text(0, timeline_y - 0.3, 'START', ha='center', va='top',
           fontsize=13, fontweight='bold', color='#4ade80', fontfamily='Arial')
    ax.text(6, timeline_y - 0.3, '6 MONTHS', ha='center', va='top',
           fontsize=13, fontweight='bold', color='#4ade80', fontfamily='Arial')
    
    # Add main title at top (with more space from phases)
    title_y = len(timeline_data) * phase_spacing + 0.8
    ax.text(3, title_y,
           'How Long Did It Take to Build StarGuard AI?',
           ha='center', va='bottom',
           fontsize=26, fontweight='bold', color='#4A3D6F', fontfamily='Arial')
    
    ax.text(3, title_y - 0.5,
           '6 Months of Evenings & Weekends',
           ha='center', va='bottom',
           fontsize=17, color='#666666', fontfamily='Arial')
    
    # Add experience highlight box (positioned below timeline line)
    experience_y = timeline_y - 0.6
    experience_box = FancyBboxPatch(
        (0.3, experience_y - 0.3),
        5.4, 0.6,
        boxstyle="round,pad=0.08",
        linewidth=3,
        facecolor='#E8F5E9',
        edgecolor='#4ade80',
        zorder=1
    )
    ax.add_patch(experience_box)
    
    ax.text(3, experience_y,
           '22 Years of Healthcare Data Experience',
           ha='center', va='center',
           fontsize=15, fontweight='bold', color='#2E7D32', fontfamily='Arial')
    
    ax.text(3, experience_y - 0.2,
           'Condensed into a portfolio showing thinking, not just coding',
           ha='center', va='center',
           fontsize=11, color='#1B5E20', fontfamily='Arial', style='italic')
    
    # Add architecture decisions section (with proper spacing)
    arch_y = experience_y - 0.8
    arch_texts = [
        ('PostgreSQL', 'Proven at Scale', '#4A3D6F'),
        ('Streamlit', 'Rapid Development', '#6F5F96'),
        ('Local LLM', 'Zero PHI Exposure', '#8B7BA8')
    ]
    
    # Add architecture label first
    ax.text(3, arch_y + 0.4, 'Architecture Decisions Reflect Experience',
           ha='center', va='bottom',
           fontsize=11, fontweight='bold', color='#4A3D6F', fontfamily='Arial')
    
    for i, (tech, desc, color) in enumerate(arch_texts):
        x_pos = 1.2 + i * 2.2
        
        # Tech name
        ax.text(x_pos, arch_y, tech, ha='center', va='top',
               fontsize=12, fontweight='bold', color=color, fontfamily='Arial')
        
        # Description
        ax.text(x_pos, arch_y - 0.2, desc, ha='center', va='top',
               fontsize=9, color='#666666', fontfamily='Arial')
    
    # Add hashtags at very bottom (with more space)
    hashtags = "#BuildProcess #Portfolio #HealthcareAnalytics #Development #DataScience"
    ax.text(3, arch_y - 0.5, hashtags, ha='center', va='top',
           fontsize=10, color='#999999', fontfamily='Arial')
    
    # Add StarGuard AI branding in top right (with proper spacing)
    ax.text(6.5, title_y, 'StarGuard AI',
           ha='right', va='bottom',
           fontsize=14, fontweight='bold', color='#4A3D6F', fontfamily='Arial')
    
    # Add decorative elements
    # Top border accent
    top_border = Rectangle((0, title_y + 0.2), 6.5, 0.08, 
                          facecolor='#4A3D6F', edgecolor='none', zorder=0)
    ax.add_patch(top_border)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', 
                facecolor='white', edgecolor='none', format='png',
                pad_inches=0.3)
    plt.close()
    
    print(f"Enhanced timeline infographic created: {output_path}")
    print(f"  Size: 2400x1350px (16:9 ratio, LinkedIn optimized)")
    print(f"  Ready for Buffer/LinkedIn upload!")
    return output_path


if __name__ == "__main__":
    output_file = create_enhanced_timeline_image("timeline_infographic_linkedin.png")
    print(f"\nImage saved to: {output_file}")
