import os
from PIL import Image, ImageDraw, ImageFont

def generate_icons():
    icons_dir = os.path.join(os.path.dirname(__file__), 'static', 'icons')
    os.makedirs(icons_dir, exist_ok=True)

    sizes = [192, 512]
    for size in sizes:
        # Create green circle image
        img = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Draw rounded background
        margin = int(size * 0.05)
        draw.rounded_rectangle([margin, margin, size - margin, size - margin], radius=int(size * 0.22), fill=(27, 67, 50, 255))
        
        # Inner emerald accent
        inner_m = int(size * 0.1)
        draw.rounded_rectangle([inner_m, inner_m, size - inner_m, size - inner_m], radius=int(size * 0.18), outline=(82, 183, 136, 255), width=max(2, int(size * 0.02)))

        # Draw leaf/plant symbol
        center_x = size // 2
        center_y = size // 2
        stem_top = center_y - int(size * 0.25)
        stem_bottom = center_y + int(size * 0.25)
        
        # Stem
        draw.line([(center_x, stem_top), (center_x, stem_bottom)], fill=(212, 163, 115, 255), width=max(3, int(size * 0.03)))

        # Left Leaf
        leaf_left = [
            (center_x, center_y),
            (center_x - int(size * 0.22), center_y - int(size * 0.12)),
            (center_x, center_y - int(size * 0.18))
        ]
        draw.polygon(leaf_left, fill=(74, 222, 128, 255))

        # Right Leaf
        leaf_right = [
            (center_x, center_y + int(size * 0.05)),
            (center_x + int(size * 0.22), center_y - int(size * 0.08)),
            (center_x, center_y - int(size * 0.12))
        ]
        draw.polygon(leaf_right, fill=(34, 197, 94, 255))

        # Save icon
        out_path = os.path.join(icons_dir, f'icon-{size}.png')
        img.save(out_path, 'PNG')
        print(f"Generated {out_path}")

if __name__ == '__main__':
    generate_icons()
