import os
from PIL import Image

RAMP = " .:-=+*cs#%@"
COLS = 100
ROWS = 53

def main():
    input_path = 'scripts/source-prepped.png'
    output_path = 'avi-ascii.svg'

    if not os.path.exists(input_path):
        print(f'Error: {input_path} not found. Run prep_photo.py first.')
        return

    print('Converting image to ASCII grid...')
    image = Image.open(input_path).convert('L')
    image = image.resize((COLS, ROWS), Image.Resampling.LANCZOS)

    pixels = list(image.getdata())
    lines = []
    for r in range(ROWS):
        row_pixels = pixels[r * COLS:(r + 1) * COLS]
        line = ''.join([RAMP[p * (len(RAMP) - 1) // 255] for p in row_pixels])
        lines.append(line)

    # Build SVG content with SMIL animation
    char_width = 8
    char_height = 14
    width = COLS * char_width
    height = ROWS * char_height

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
        '  <style>',
        '    text {',
        '      font-family: monospace;',
        '      font-size: 12px;',
        '      fill: #c9d1d9;',
        '    }',
        '    .wipe {',
        '      animation: reveal 2.5s steps(100, end) forwards;',
        '      opacity: 0;',
        '    }',
        '    @keyframes reveal {',
        '      0% { opacity: 0; clip-path: inset(0 100% 0 0); }',
        '      100% { opacity: 1; clip-path: inset(0 0 0 0); }',
        '    }',
        '  </style>',
        '  <rect width="100%" height="100%" fill="#0d1117" rx="6"/>',
        '  <g transform="translate(10, 20)">'
    ]

    for i, line in enumerate(lines):
        # Escape XML special characters
        escaped_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
        delay = f'{i * 0.03:.2f}s'
        svg_lines.append(f'    <text x="0" y="{i * char_height}" class="wipe" style="animation-delay: {delay};">{escaped_line}</text>')

    svg_lines.append('  </g>')
    svg_lines.append('</svg>')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(svg_lines))

    print(f'Successfully generated {output_path}')

if __name__ == '__main__':
    main()
