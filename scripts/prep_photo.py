import sys
import cv2
import numpy as np
from PIL import Image
from rembg import remove

def main():
    if len(sys.argv) < 2:
        print('Usage: python prep_photo.py <source-photo.jpg>')
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = 'scripts/source-prepped.png'

    print(f'Loading {input_path} and removing background...')
    input_image = Image.open(input_path)
    output_image = remove(input_image)

    # Convert to OpenCV format (BGR)
    np_image = np.array(output_image)
    if np_image.shape[2] == 4:
        # Alpha channel to white background composite
        alpha = np_image[:, :, 3] / 255.0
        rgb = np_image[:, :, :3]
        background = np.ones_like(rgb, dtype=np.uint8) * 255
        composite = (rgb * alpha[:, :, np.newaxis] + background * (1 - alpha[:, :, np.newaxis])).astype(np.uint8)
    else:
        composite = np_image[:, :, :3]

    gray = cv2.cvtColor(composite, cv2.COLOR_BGR2GRAY)

    # Boost local contrast using CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    cv2.imwrite(output_path, enhanced)
    print(f'Saved prepped photo to {output_path}')

if __name__ == '__main__':
    main()
