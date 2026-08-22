import os

def main():
    output_path = 'info-card.svg'

    # You can customize these lines to tell your story
    rows = [
        ('Role', 'Software Developer & Builder'),
        ('Stack', 'Python, JavaScript, Git'),
        ('Focus', 'Automation & Creative Coding'),
        ('Location', 'Argentina'),
        ('Status', 'Building awesome things')
    ]

    width = 460
    height = 200

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
        '  <style>',
        '    text {',
        '      font-family: monospace;',
        '      font-size: 13px;',
        '    }',
        '    .title {',
        '      fill: #ff7b72;',
        '      font-weight: bold;',
        '    }',
        '    .key {',
        '      fill: #79c0ff;',
        '    }',
        '    .val {',
        '      fill: #c9d1d9;',
        '    }',
        '    .card-row {',
        '      animation: fadeIn 0.8s ease forwards;',
        '      opacity: 0;',
        '    }',
        '    @keyframes fadeIn {',
        '      to { opacity: 1; }',
        '    }',
        '  </style>',
        '  <rect width="100%" height="100%" fill="#0d1117" rx="6"/>',
        '  <g transform="translate(20, 30)">',
        '    <text x="0" y="0" class="title">pedro@github:~</text>'
    ]

    for i, (key, val) in enumerate(rows):
        y = 35 + (i * 28)
        delay = 0.2 + (i * 0.15)
        svg_lines.append(f'    <g class="card-row" style="animation-delay: {delay}s;">')
        svg_lines.append(f'      <text x="0" y="{y}" class="key">{key}:</text>')
        svg_lines.append(f'      <text x="110" y="{y}" class="val">{val}</text>')
        svg_lines.append(f'    </g>')

    svg_lines.append('  </g>')
    svg_lines.append('</svg>')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(svg_lines))

    print(f'Successfully generated {output_path}')

if __name__ == '__main__':
    main()
