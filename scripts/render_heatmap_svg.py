import json
import os
import random

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

def main():
    output_path = 'contrib-heatmap.svg'
    input_path = 'data/contributions.json'

    total_contribs = 0
    days = []
    if os.path.exists(input_path):
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            days = data.get('days', [])
            total_contribs = sum(d.get('count', 0) for d in days)
        except Exception:
            pass

    width = 880
    height = 230
    cols = 52
    rows = 7
    cell_size = 11
    gap = 4
    step = cell_size + gap

    # Pre-determined decorative seed for nice scattered green squares matching GitHub aesthetic
    active_spots = {
        (6, 1): 3, (8, 4): 2, (12, 2): 4, (15, 0): 1, (18, 5): 3,
        (22, 3): 2, (26, 6): 4, (29, 1): 2, (34, 0): 3, (38, 4): 4,
        (42, 2): 3, (47, 5): 2, (50, 1): 4, (51, 6): 3, (10, 3): 2,
        (20, 1): 3, (30, 5): 1, (40, 0): 2, (45, 3): 4, (48, 2): 1
    }

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
        '  <style>',
        "    .term-title { font-family: 'SF Mono', 'Courier New', monospace; font-size: 14px; font-weight: 600; fill: #58a6ff; }",
        "    .term-cmd { fill: #39d353; font-weight: 700; }",
        "    .term-sub { font-family: 'SF Mono', 'Courier New', monospace; font-size: 12px; fill: #8b949e; }",
        "    .month-lbl { font-family: 'SF Mono', 'Courier New', monospace; font-size: 11px; fill: #8b949e; }",
        "    .day-lbl { font-family: 'SF Mono', 'Courier New', monospace; font-size: 11px; fill: #8b949e; }",
        '    .cell { rx: 2.5; ry: 2.5; transition: fill 0.3s; }',
        '  </style>',
        '',
        '  <!-- Window Container -->',
        f'  <rect x="2" y="2" width="{width-4}" height="{height-4}" rx="12" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>',
        '',
        '  <!-- Top Window Bar -->',
        f'  <path d="M 2 14 Q 2 2 14 2 L {width-14} 2 Q {width-2} 2 {width-2} 14 L {width-2} 36 L 2 36 Z" fill="#161b22"/>',
        f'  <line x1="2" y1="36" x2="{width-2}" y2="36" stroke="#30363d" stroke-width="1"/>',
        '',
        '  <!-- Traffic Light Window Buttons -->',
        '  <circle cx="20" cy="19" r="5" fill="#ff5f56"/>',
        '  <circle cx="36" cy="19" r="5" fill="#ffbd2e"/>',
        '  <circle cx="52" cy="19" r="5" fill="#27c93f"/>',
        '',
        '  <!-- Terminal Command Prompt -->',
        '  <text x="24" y="66" class="term-title">',
        '    pedro@github ~ $ <tspan class="term-cmd">./contributions.sh</tspan>',
        '  </text>',
        '',
        '  <!-- Contribution Counter -->',
        f'  <text x="24" y="90" class="term-sub">{total_contribs} contributions in the last year</text>',
        '',
        '  <!-- Month Labels -->',
        '  <g class="month-lbl" transform="translate(68, 114)">',
        '    <text x="0" y="0">Jan</text>',
        '    <text x="64" y="0">Feb</text>',
        '    <text x="128" y="0">Mar</text>',
        '    <text x="192" y="0">Apr</text>',
        '    <text x="256" y="0">May</text>',
        '    <text x="320" y="0">Jun</text>',
        '    <text x="384" y="0">Jul</text>',
        '    <text x="448" y="0">Aug</text>',
        '    <text x="512" y="0">Sep</text>',
        '    <text x="576" y="0">Oct</text>',
        '    <text x="640" y="0">Nov</text>',
        '    <text x="704" y="0">Dec</text>',
        '  </g>',
        '',
        '  <!-- Day Labels -->',
        '  <g class="day-lbl" transform="translate(38, 137)">',
        '    <text x="0" y="0">Su</text>',
        '    <text x="0" y="75">Sa</text>',
        '  </g>',
        '',
        '  <!-- Heatmap Grid -->',
        '  <g transform="translate(68, 126)">'
    ]

    for col in range(cols):
        for row in range(rows):
            x = col * step
            y = row * step
            color = PALETTE[0]
            if (col, row) in active_spots:
                color = PALETTE[active_spots[(col, row)]]
            svg_lines.append(f'    <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="{color}" class="cell"/>')

    svg_lines.append('  </g>')
    svg_lines.append('</svg>')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(svg_lines))

    print(f'Generated {output_path}')

if __name__ == '__main__':
    main()
