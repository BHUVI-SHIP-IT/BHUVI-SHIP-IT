import os
import cv2
import numpy as np

# Config
CONTRAST = 1.2
GAMMA = 1.0
WHITE_FLOOR = 200 # Pixels brighter than this become spaces
ROW_DUR = "2s"
STAGGER = 0.05
WIDTH = 370
CHARS = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

def make_ascii_svg(input_path="source-prepped.png", output_path="avi-ascii.svg"):
    STATIC = os.environ.get("STATIC", "0") == "1"
    
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Could not read source-prepped.png. Run prep_photo.py first.")
        return

    # Extract alpha
    if img.shape[2] == 4:
        alpha = img[:, :, 3]
        gray = img[:, :, 0] # It's grayscale so B=G=R
    else:
        alpha = np.ones(img.shape[:2], dtype=np.uint8) * 255
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Adjust contrast and gamma
    gray = cv2.convertScaleAbs(gray, alpha=CONTRAST, beta=0)
    inv_gamma = 1.0 / GAMMA
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    gray = cv2.LUT(gray, table)

    # Resize for ASCII (character aspect ratio is roughly 2:1 height:width)
    target_cols = 50
    h, w = gray.shape
    aspect_ratio = h / w
    target_rows = int(target_cols * aspect_ratio * 0.5)
    
    gray = cv2.resize(gray, (target_cols, target_rows))
    alpha = cv2.resize(alpha, (target_cols, target_rows))
    
    char_len = len(CHARS)
    
    rows_text = []
    for y in range(target_rows):
        row_str = ""
        for x in range(target_cols):
            if alpha[y, x] < 128 or gray[y, x] > WHITE_FLOOR:
                row_str += " "
            else:
                intensity = gray[y, x]
                # Map intensity to char (darker = more dense)
                idx = int((1.0 - (intensity / 255.0)) * (char_len - 1))
                # HTML escape
                char = CHARS[idx]
                if char == '<': char = '&lt;'
                elif char == '>': char = '&gt;'
                elif char == '&': char = '&amp;'
                elif char == '"': char = '&quot;'
                row_str += char
        rows_text.append(row_str)

    # Generate SVG
    svg_h = target_rows * 12
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {svg_h}" width="{WIDTH}" height="{svg_h}">
    <style>
        .ascii {{
            font-family: 'Courier New', Courier, monospace;
            font-size: 10px;
            fill: #8b949e;
            white-space: pre;
        }}
    </style>
    <rect width="100%" height="100%" fill="none" />
    <g class="ascii">
'''
    
    for i, row in enumerate(rows_text):
        y_pos = (i + 1) * 12
        begin_time = i * STAGGER
        
        if STATIC:
            svg_content += f'        <text x="0" y="{y_pos}">{row}</text>\n'
        else:
            svg_content += f'        <text x="0" y="{y_pos}" opacity="0">\n'
            svg_content += f'            {row}\n'
            svg_content += f'            <animate attributeName="opacity" values="0;1" begin="{begin_time}s" dur="{ROW_DUR}" fill="freeze" />\n'
            svg_content += f'        </text>\n'

    svg_content += '''    </g>
</svg>'''

    with open(output_path, "w") as f:
        f.write(svg_content)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    make_ascii_svg()
