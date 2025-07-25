#!/usr/bin/env python3
"""
Simple script to create placeholder icons for the Chrome extension.
This fixes the "Could not load icon" error.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    """Create a simple icon with the specified size."""
    # Create image with blue background
    img = Image.new('RGBA', (size, size), (0, 123, 255, 255))  # Bootstrap blue
    draw = ImageDraw.Draw(img)
    
    # Add a simple download arrow symbol
    if size >= 32:
        # Draw download arrow
        center = size // 2
        arrow_size = size // 3
        
        # Arrow shaft (vertical line)
        draw.rectangle([center-2, center-arrow_size, center+2, center+arrow_size//2], fill='white')
        
        # Arrow head (triangle)
        points = [
            (center-arrow_size//2, center),
            (center+arrow_size//2, center),
            (center, center+arrow_size//2)
        ]
        draw.polygon(points, fill='white')
    
    # Save the icon
    icons_dir = os.path.join(os.path.dirname(__file__), 'icons')
    os.makedirs(icons_dir, exist_ok=True)
    
    filepath = os.path.join(icons_dir, filename)
    img.save(filepath, 'PNG')
    print(f"✅ Created {filename} ({size}x{size})")

def main():
    """Create all required icon sizes."""
    print("🎨 Creating Chrome extension icons...")
    
    # Required icon sizes
    sizes = [
        (16, 'icon16.png'),
        (32, 'icon32.png'),
        (48, 'icon48.png'),
        (128, 'icon128.png')
    ]
    
    for size, filename in sizes:
        create_icon(size, filename)
    
    print("🎉 All icons created successfully!")
    print("You can now reload the Chrome extension.")

if __name__ == '__main__':
    try:
        main()
    except ImportError:
        print("❌ PIL (Pillow) not found. Installing...")
        import subprocess
        subprocess.run(['pip', 'install', 'pillow'])
        print("✅ Pillow installed. Please run the script again.")
    except Exception as e:
        print(f"❌ Error creating icons: {e}")
        print("💡 You can also just create any PNG files named icon16.png, icon32.png, icon48.png, icon128.png in the icons/ folder") 