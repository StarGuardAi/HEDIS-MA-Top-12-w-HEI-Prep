"""
Display timeline infographic image
Opens the generated timeline image for viewing
"""

import os
import sys
from pathlib import Path

def display_timeline_image():
    """Display the timeline infographic image"""
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.parent
    image_path = script_dir / "timeline_infographic_linkedin.png"
    
    if not image_path.exists():
        print(f"Image not found at: {image_path}")
        # Try the basic version
        image_path = script_dir / "timeline_infographic.png"
        if not image_path.exists():
            print(f"Image not found at: {image_path}")
            print("\nGenerating timeline image first...")
            from generate_timeline_image_enhanced import create_enhanced_timeline_image
            image_path = Path(create_enhanced_timeline_image(str(script_dir / "timeline_infographic_linkedin.png")))
    
    print(f"\n{'='*60}")
    print(f"Timeline Infographic")
    print(f"{'='*60}")
    print(f"\nImage location: {image_path}")
    print(f"File size: {image_path.stat().st_size / 1024:.2f} KB")
    print(f"\nOpening image...")
    
    # Try to open the image with the default system viewer
    try:
        if sys.platform == "win32":
            os.startfile(str(image_path))
        elif sys.platform == "darwin":  # macOS
            os.system(f"open '{image_path}'")
        else:  # Linux
            os.system(f"xdg-open '{image_path}'")
        print("Image opened successfully!")
    except Exception as e:
        print(f"Could not open image automatically: {e}")
        print(f"\nPlease manually open: {image_path}")
    
    return str(image_path)


if __name__ == "__main__":
    display_timeline_image()
