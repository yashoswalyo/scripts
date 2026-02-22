"""
This script helped to convert 100 GB+ photos to 10 GB, in short time
"""
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image, ImageOps

INPUT_DIR = r"/path/to/photos/folder"
DRIVE_DIR = r"compressed"
MAX_DIM = 4096  # height, width to 2096
MAX_WORKERS = 4   # Tune this (6–12 is usually ideal)

os.makedirs(DRIVE_DIR, exist_ok=True)


def process_image(filename):
    try:
        path = os.path.join(INPUT_DIR, filename)
        img = Image.open(path)

        # Fix EXIF rotation
        img = ImageOps.exif_transpose(img)

        width, height = img.size

        # Preserve aspect ratio
        if max(width, height) <= MAX_DIM:
            new_w, new_h = width, height
            drive_img = img.copy()
        else:
            if width > height:
                new_w = MAX_DIM
                new_h = int(height * MAX_DIM / width)
            else:
                new_h = MAX_DIM
                new_w = int(width * MAX_DIM / height)

            drive_img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

        drive_path = os.path.join(DRIVE_DIR, filename)
        drive_img.save(
            drive_path,
            "JPEG",
            quality=90,
            optimize=True,
            progressive=True
        )

        return f"Processed: {filename} → {new_w}×{new_h}"

    except Exception as e:
        return f"❌ Failed: {filename} — {e}"


def main():
    files = [
        f for f in os.listdir(INPUT_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".arw"))
    ]

    print(f"Processing {len(files)} images using {MAX_WORKERS} threads...\n")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_image, f): f for f in files}

        for future in as_completed(futures):
            result = future.result()
            print(result, flush=True)


if __name__ == "__main__":
    main()
