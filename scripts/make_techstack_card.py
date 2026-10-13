def generate_techstack_card():
    width = 880
    height = 200

    badges_row1 = [
        ("Python", "#3776AB", "white"),
        ("Linux", "#FCC624", "#111111"),
        ("Bash", "#4EAA25", "white"),
        ("Docker", "#2496ED", "white"),
        ("Git", "#F05032", "white"),
    ]

    badges_row2 = [
        ("C++", "#00599C", "white"),
        ("PostgreSQL", "#4169E1", "white"),
        ("GitHub Actions", "#2088FF", "white"),
        ("VS Code", "#007ACC", "white"),
        ("Markdown", "#000000", "white"),
    ]

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
        '  <style>',
        "    .term-title { font-family: 'SF Mono', 'Courier New', monospace; font-size: 14px; font-weight: 600; fill: #58a6ff; }",
        "    .term-cmd { fill: #39d353; font-weight: 700; }",
        "    .badge-txt { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 11px; font-weight: bold; }",
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
        '  <!-- Terminal Command -->',
        '  <text x="24" y="66" class="term-title">',
        '    pedro@github ~ $ <tspan class="term-cmd">tech-stack --list</tspan>',
        '  </text>',
        '',
        '  <!-- Badges Row 1 -->'
    ]

    def render_row(badges, y_pos):
        # Calculate total width to center
        badge_w = 110
        badge_h = 32
        gap = 14
        total_w = len(badges) * badge_w + (len(badges) - 1) * gap
        start_x = (width - total_w) // 2

        row_lines = []
        for i, (name, bg, fg) in enumerate(badges):
            bx = start_x + i * (badge_w + gap)
            row_lines.append(f'  <g transform="translate({bx}, {y_pos})">')
            row_lines.append(f'    <rect width="{badge_w}" height="{badge_h}" rx="6" fill="{bg}" stroke="#30363d" stroke-width="1"/>')
            row_lines.append(f'    <text x="{badge_w//2}" y="20" fill="{fg}" text-anchor="middle" class="badge-txt">{name}</text>')
            row_lines.append('  </g>')
        return row_lines

    svg.extend(render_row(badges_row1, 95))
    svg.extend(['', '  <!-- Badges Row 2 -->'])
    svg.extend(render_row(badges_row2, 140))
    svg.append('</svg>')

    with open('tech-stack.svg', 'w', encoding='utf-8') as f:
        f.write('\n'.join(svg))

    print('Successfully generated tech-stack.svg!')

if __name__ == '__main__':
    generate_techstack_card()
