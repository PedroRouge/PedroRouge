import os

def main():
    output_path = 'info-card.svg'

    rows = [
        ('Name', 'Pedro'),
        ('Role', 'Future Systems Graduate'),
        ('Focus', 'Backend, DevOps, Architecture'),
        ('Stack', 'Python, C++, Docker, Linux, Git'),
        ('Location', 'Argentina'),
        ('Status', 'Ready to deploy')
    ]

    width = 480
    height = 220

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
        '  <style>',
        '    text { font-family: "SF Mono", monospace, monospace; font-size: 13px; }',
        '    .title { fill: #39d353; font-weight: bold; }',
        '    .key { fill: #58a6ff; font-weight: 600; }',
        '    .val { fill: #c9d1d9; }',
        '  </style>',
        '  <rect width="100%" height="100%" fill="#0d1117" rx="8" stroke="#30363d" stroke-width="1.5"/>',
        '  <g transform="translate(24, 34)">',
        '    <text x="0" y="0" class="title">pedro@github:~ $ whoami</text>'
    ]

    for i, (key, val) in enumerate(rows):
        y = 30 + (i * 26)
        svg_lines.append(f'    <text x="0" y="{y}" class="key">{key}:</text>')
        svg_lines.append(f'    <text x="90" y="{y}" class="val">{val}</text>')

    svg_lines.append('  </g>')
    svg_lines.append('</svg>')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(svg_lines))

    print(f'Successfully generated {output_path}')

if __name__ == '__main__':
    main()
