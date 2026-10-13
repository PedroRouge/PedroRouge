import base64
from PIL import Image, ImageOps, ImageEnhance
import numpy as np

def generate_whoami_card():
    # 1. Base64 encode avatar
    avatar_path = 'avatar.png'
    im_avatar = Image.open(avatar_path).convert('RGB')
    im_avatar = im_avatar.resize((260, 260), Image.Resampling.LANCZOS)
    im_avatar.save('avatar_square.jpg', quality=95)
    with open('avatar_square.jpg', 'rb') as f:
        b64_avatar = base64.b64encode(f.read()).decode('utf-8')

    # 2. Generate clean ASCII of Pedro
    im_prepped = Image.open('scripts/source-prepped.png')
    w, h = im_prepped.size
    face = im_prepped.crop((int(w * 0.22), int(h * 0.02), int(w * 0.78), int(h * 0.38)))

    cols = 28
    rows = 18
    face_resized = face.resize((cols, rows), Image.Resampling.LANCZOS)
    arr = np.array(face_resized)

    RAMP = ' .:-=+*#%@'
    ascii_lines = []
    for r in range(rows):
        line = []
        for c in range(cols):
            val = arr[r, c]
            if val > 240:
                line.append(' ')
            else:
                idx = int((240 - val) / 240 * len(RAMP))
                line.append(RAMP[min(idx, len(RAMP) - 1)])
        # Escape XML characters
        escaped = ''.join(line).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        ascii_lines.append(escaped)

    # 3. SVG parameters
    width = 880
    height = 240

    info_rows = [
        ('Name', 'Pedro'),
        ('Role', 'Future Systems Graduate'),
        ('Focus', 'Backend · DevOps · Architecture'),
        ('Stack', 'Python · Docker · Linux · Git · C++'),
        ('Location', 'Argentina'),
        ('Status', 'Building high-performance systems 🚀')
    ]

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
        '  <defs>',
        '    <clipPath id="circleAvatar">',
        '      <circle cx="770" cy="132" r="52"/>',
        '    </clipPath>',
        '    <filter id="greenGlow">',
        '      <feDropShadow dx="0" dy="0" stdDeviation="2" flood-color="#39d353" flood-opacity="0.4"/>',
        '    </filter>',
        '  </defs>',
        '  <style>',
        "    .term-title { font-family: 'SF Mono', 'Courier New', monospace; font-size: 14px; font-weight: 600; fill: #58a6ff; }",
        "    .term-cmd { fill: #39d353; font-weight: 700; }",
        "    .ascii-text { font-family: 'SF Mono', 'Courier New', monospace; font-size: 9.5px; fill: #39d353; letter-spacing: 1px; }",
        "    .info-key { font-family: 'SF Mono', 'Courier New', monospace; font-size: 12.5px; font-weight: bold; fill: #58a6ff; }",
        "    .info-val { font-family: 'SF Mono', 'Courier New', monospace; font-size: 12.5px; fill: #c9d1d9; }",
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
        '    pedro@github ~ $ <tspan class="term-cmd">whoami</tspan>',
        '  </text>',
        '',
        '  <!-- 1. Left Column: Pedro ASCII Portrait -->',
        '  <g class="ascii-text" transform="translate(30, 85)" xml:space="preserve">'
    ]

    line_height = 8.0
    for i, line in enumerate(ascii_lines):
        svg.append(f'    <text x="0" y="{i * line_height}">{line}</text>')

    svg.extend([
        '  </g>',
        '',
        '  <!-- 2. Middle Column: Identity Details -->',
        '  <g transform="translate(245, 96)">'
    ])

    for i, (k, v) in enumerate(info_rows):
        y = i * 22
        svg.append(f'    <text x="0" y="{y}" class="info-key">{k}:</text>')
        svg.append(f'    <text x="85" y="{y}" class="info-val">{v}</text>')

    svg.extend([
        '  </g>',
        '',
        '  <!-- 3. Right Column: Pedro Circular Photo -->',
        '  <g>',
        '    <!-- Background circular shadow & border -->',
        '    <circle cx="770" cy="132" r="55" fill="#161b22" stroke="#39d353" stroke-width="2.5" filter="url(#greenGlow)"/>',
        f'    <image href="data:image/jpeg;base64,{b64_avatar}" x="718" y="80" width="104" height="104" clip-path="url(#circleAvatar)"/>',
        '  </g>',
        '</svg>'
    ])

    with open('whoami.svg', 'w', encoding='utf-8') as f:
        f.write('\n'.join(svg))

    print('Successfully generated whoami.svg!')

if __name__ == '__main__':
    generate_whoami_card()
