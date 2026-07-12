import os

HOST = "bhuvi@ship-it"

ROWS = [
    ("OS", "Arch Linux (Just kidding, it's Ubuntu)"),
    ("Role", "Software Dev Engineer | Backend | AI/ML"),
    ("Location", "Chennai, India 📍"),
    ("Experience", "CoinSwitch, Brakes India, Alldigi-tech"),
    ("Projects", "Trace Ops AI, DeepSolve, Debatron, ForensIQ"),
    ("LeetCode", "776+ solved, 1915 peak rating 🧠"),
    ("Languages", "Python, SQL, Swift, JS, C++, C, Java, TS"),
    ("AI / ML", "PyTorch, OpenCV, LangChain, LlamaIndex, CrewAI"),
    ("Backend", "Node.js, Express, Django, Flask, FastAPI"),
    ("Cloud and DevOps", "Docker, K8s, Azure, AWS, GCP, GitHub Actions"),
    ("Databases", "PostgreSQL, MongoDB, Firebase, Neo4j, IceBerg"),
    ("Achievements", "Hackfinity Winner, SIH Top 50, AIVENTRA 3rd")
]

H = 500
W = 490

def make_info_card(output_path="info-card.svg"):
    # Generate the Neofetch style SVG
    header = f"{HOST}"
    separator = "-" * len(header)
    
    # SVG setup
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
    <style>
        .text {{
            font-family: 'Courier New', Courier, monospace;
            font-size: 14px;
            fill: #c9d1d9;
            white-space: pre;
        }}
        .key {{
            fill: #58a6ff;
            font-weight: bold;
        }}
        .title {{
            fill: #58a6ff;
            font-weight: bold;
        }}
        .container {{
            fill: #0d1117;
            stroke: #30363d;
            stroke-width: 1;
            rx: 6px;
        }}
    </style>
    <rect class="container" width="100%" height="100%" />
    <g class="text" transform="translate(20, 30)">
        <text class="title" x="0" y="0">{header}</text>
        <text x="0" y="20">{separator}</text>
'''
    
    y_pos = 50
    for key, val in ROWS:
        # Align keys to be 15 chars wide
        padded_key = f"{key}:".ljust(15)
        # Handle long values by truncating or keeping them (they should fit in W=490)
        svg += f'''
        <text x="0" y="{y_pos}"><tspan class="key">{padded_key}</tspan> {val}</text>'''
        y_pos += 25
        
    svg += '''
    </g>
</svg>'''

    with open(output_path, "w") as f:
        f.write(svg)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    make_info_card()
