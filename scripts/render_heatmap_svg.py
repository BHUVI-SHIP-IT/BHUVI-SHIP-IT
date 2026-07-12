import json
import os

COLORS = {
    0: "#161b22",
    1: "#0e4429",
    2: "#006d32",
    3: "#26a641",
    4: "#39d353"
}

def render_heatmap_svg(input_path="data/contributions.json", output_path="contrib-heatmap.svg"):
    if not os.path.exists(input_path):
        print(f"File {input_path} not found.")
        return
        
    with open(input_path, "r") as f:
        data = json.load(f)
        
    # Data is ordered by date.
    # We want to lay it out in columns of 7.
    
    cell_size = 11
    gap = 4
    
    # Calculate SVG dimensions
    cols = (len(data) // 7) + 1
    width = cols * (cell_size + gap) + 20
    height = 7 * (cell_size + gap) + 20
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
    <rect width="100%" height="100%" fill="none" />
    <g transform="translate(10, 10)">
'''
    
    for i, day in enumerate(data):
        col = i // 7
        row = i % 7
        
        x = col * (cell_size + gap)
        y = row * (cell_size + gap)
        
        level = day.get('level', 0)
        color = COLORS.get(level, COLORS[0])
        
        # Staggered animation based on column
        begin_time = col * 0.05
        
        svg += f'''        <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="{color}" rx="2" opacity="0">
            <animate attributeName="opacity" values="0;1" begin="{begin_time}s" dur="1s" fill="freeze" />
        </rect>
'''

    svg += '''    </g>
</svg>'''

    with open(output_path, "w") as f:
        f.write(svg)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    render_heatmap_svg()
