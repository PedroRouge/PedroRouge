import json
import os
from datetime import datetime, timedelta

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

def main():
    output_path = 'contrib-heatmap.svg'
    input_path = 'data/contributions.json'

    if not os.path.exists(input_path):
        print(f'Error: {input_path} not found. Run fetch_contributions.py first.')
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    days = data.get('days', [])
    total_contribs = data.get('total_contributions') if data.get('total_contributions') is not None else sum(d.get('count', 0) for d in days)

    if not days:
        print('Error: no days found in data/contributions.json')
        return

    width = 880
    height = 250
    cell_size = 11
    gap = 4
    step = cell_size + gap

    # Determine start date and layout
    first_date = datetime.strptime(days[0]['date'], '%Y-%m-%d')
    start_x = 56
    start_y = 124

    # Calculate month header positions
    months_seen = set()
    month_positions = []
    for i, d in enumerate(days):
        dt = datetime.strptime(d['date'], '%Y-%m-%d')
        col = i // 7
        m_name = dt.strftime('%b')
        if dt.day <= 7 and m_name not in months_seen:
            months_seen.add(m_name)
            month_positions.append((m_name, start_x + col * step))

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
        '  <style>',
        "    .term-title { font-family: 'SF Mono', 'Courier New', monospace; font-size: 14px; font-weight: 600; fill: #58a6ff; }",
        "    .term-cmd { fill: #39d353; font-weight: 700; }",
        "    .term-sub { font-family: 'SF Mono', 'Courier New', monospace; font-size: 12px; fill: #8b949e; }",
        "    .month-lbl { font-family: 'SF Mono', 'Courier New', monospace; font-size: 10.5px; fill: #8b949e; }",
        "    .day-lbl { font-family: 'SF Mono', 'Courier New', monospace; font-size: 10px; fill: #8b949e; }",
        '    .cell { rx: 2.5; ry: 2.5; }',
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
        '  <!-- Real Contribution Counter -->',
        f'  <text x="24" y="88" class="term-sub">{total_contribs} contributions in the last year</text>',
        '',
        '  <!-- Month Labels -->'
    ]

    for m_name, mx in month_positions:
        svg_lines.append(f'  <text x="{mx}" y="110" class="month-lbl">{m_name}</text>')

    svg_lines.extend([
        '',
        '  <!-- Day Labels -->',
        '  <g class="day-lbl">',
        f'    <text x="{start_x - 22}" y="{start_y + 10}">Su</text>',
        f'    <text x="{start_x - 22}" y="{start_y + 98}">Sa</text>',
        '  </g>',
        '',
        '  <!-- Real Heatmap Grid -->'
    ])

    for i, d in enumerate(days):
        col = i // 7
        row = i % 7
        x = start_x + col * step
        y = start_y + row * step
        level = min(max(d.get('level', 0), 0), 4)
        color = PALETTE[level]
        date_str = d.get('date', '')
        cnt = d.get('count', 0)
        svg_lines.append(f'  <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="{color}" class="cell"><title>{cnt} contributions on {date_str}</title></rect>')

    svg_lines.append('</svg>')

    for p in ['contrib-heatmap.svg', 'contrib-heatmap-live.svg']:
        with open(p, 'w', encoding='utf-8') as f:
            f.write('\n'.join(svg_lines))

    print(f'Successfully rendered contrib-heatmap.svg & contrib-heatmap-live.svg with {total_contribs} REAL contributions across {len(days)} days!')

if __name__ == '__main__':
    main()
