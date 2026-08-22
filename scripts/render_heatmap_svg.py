import json
import os
from datetime import datetime

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def main():
    input_path = 'data/contributions.json'
    output_path = 'contrib-heatmap.svg'

    if not os.path.exists(input_path):
        print(f'Error: {input_path} not found. Run fetch_contributions.py first.')
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    days = data.get('days', [])
    total_contribs = sum(d.get('count', 0) for d in days)

    width = 720
    height = 160

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
        '  <style>',
        '    text {',
        '      font-family: monospace;',
        '      font-size: 11px;',
        '      fill: #8b949e;',
        '    }',
        '    .cell {',
        '      rx: 2;',
        '      ry: 2;',
        '      animation: fadeIn 0.6s ease forwards;',
        '      opacity: 0;',
        '    }',
        '    @keyframes fadeIn {',
        '      to { opacity: 1; }',
        '    }',
        '  </style>',
        '  <rect width="100%" height="100%" fill="#0d1117" rx="6"/>',
        f'  <text x="20" y="30">{total_contribs} contributions in the last year</text>',
        '  <g transform="translate(20, 50)">'
    ]

    # Simple grid rendering layout
    cell_size = 11
    cell_gap = 3
    step = cell_size + cell_gap

    for i, d in enumerate(days):
        col = i // 7
        row = i % 7
        x = col * step
        y = row * step
        level = min(max(d.get('level', 0), 0), 5)
        color = PALETTE[level]
        delay = (col * 0.01) + (row * 0.02)

        svg_lines.append(f'    <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="{color}" class="cell" style="animation-delay: {delay:.2f}s;"/>')

    svg_lines.append('  </g>')
    svg_lines.append('</svg>')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(svg_lines))

    print(f'Successfully generated {output_path}')

if __name__ == '__main__':
    main()
