import base64
from PIL import Image
import numpy as np

def generate_whoami_card():
    # 1. Base64 encode avatar photo (Pedro)
    avatar_path = 'avatar.png'
    im_avatar = Image.open(avatar_path).convert('RGB')
    im_avatar = im_avatar.resize((260, 260), Image.Resampling.LANCZOS)
    im_avatar.save('avatar_square.jpg', quality=95)
    with open('avatar_square.jpg', 'rb') as f:
        b64_avatar = base64.b64encode(f.read()).decode('utf-8')

    # 2. Base64 encode blended puppy ASCII image
    puppy = Image.open('puppy-ascii.png').convert('RGB')
    p_thumb = puppy.resize((124, 166), Image.Resampling.LANCZOS)
    arr = np.array(p_thumb, dtype=np.float32)
    diff = np.mean(arr, axis=2)
    target_bg = np.array([13.0, 17.0, 23.0])
    mask = np.clip((diff - 22.0) / 30.0, 0.0, 1.0)[:, :, np.newaxis]
    blended = arr * mask + target_bg * (1.0 - mask)
    out_thumb = Image.fromarray(np.clip(blended, 0, 255).astype(np.uint8))
    out_thumb.save('puppy-embedded.png')
    with open('puppy-embedded.png', 'rb') as f:
        b64_puppy = base64.b64encode(f.read()).decode('utf-8')

    # 3. SVG parameters
    width = 880
    height = 250

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
        '      <circle cx="775" cy="138" r="54"/>',
        '    </clipPath>',
        '    <filter id="greenGlow">',
        '      <feDropShadow dx="0" dy="0" stdDeviation="2.5" flood-color="#39d353" flood-opacity="0.5"/>',
        '    </filter>',
        '  </defs>',
        '  <style>',
        "    .term-title { font-family: 'SF Mono', 'Courier New', monospace; font-size: 14px; font-weight: 600; fill: #58a6ff; }",
        "    .term-cmd { fill: #39d353; font-weight: 700; }",
        "    .info-key { font-family: 'SF Mono', 'Courier New', monospace; font-size: 13px; font-weight: bold; fill: #58a6ff; }",
        "    .info-val { font-family: 'SF Mono', 'Courier New', monospace; font-size: 13px; fill: #c9d1d9; }",
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
        '  <!-- 1. Left Column: Matrix Green ASCII Puppy -->',
        f'  <image href="data:image/png;base64,{b64_puppy}" x="35" y="70" width="124" height="166"/>',
        '',
        '  <!-- 2. Middle Column: Identity Details -->',
        '  <g transform="translate(195, 100)">'
    ]

    for i, (k, v) in enumerate(info_rows):
        y = i * 23
        svg.append(f'    <text x="0" y="{y}" class="info-key">{k}:</text>')
        svg.append(f'    <text x="85" y="{y}" class="info-val">{v}</text>')

    svg.extend([
        '  </g>',
        '',
        '  <!-- 3. Right Column: Pedro Circular Photo -->',
        '  <g>',
        '    <!-- Background circular shadow & border -->',
        '    <circle cx="775" cy="138" r="57" fill="#161b22" stroke="#39d353" stroke-width="2.5" filter="url(#greenGlow)"/>',
        f'    <image href="data:image/jpeg;base64,{b64_avatar}" x="721" y="84" width="108" height="108" clip-path="url(#circleAvatar)"/>',
        '  </g>',
        '</svg>'
    ])

    with open('whoami.svg', 'w', encoding='utf-8') as f:
        f.write('\n'.join(svg))

    print('Successfully generated whoami.svg with Matrix ASCII puppy!')

if __name__ == '__main__':
    generate_whoami_card()
