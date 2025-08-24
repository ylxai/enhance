"""
Utility functions untuk auto photo processing workflow
"""

import os
import time
from PIL import Image
from config import (
    COUNTER_FILE, FILE_STABILITY_CHECKS, FILE_STABILITY_INTERVAL, 
    IMAGE_OPEN_RETRIES, WATERMARK_FILE
)


def load_counter():
    """Load counter dari file"""
    if os.path.exists(COUNTER_FILE):
        try:
            return int(open(COUNTER_FILE).read().strip())
        except:
            return 1
    return 1


def save_counter(n):
    """Save counter ke file"""
    with open(COUNTER_FILE, "w") as f:
        f.write(str(n))


def wait_until_complete(path, checks=FILE_STABILITY_CHECKS, interval=FILE_STABILITY_INTERVAL):
    """
    Tunggu sampai file selesai di-copy/transfer
    Mengecek stabilitas ukuran file
    """
    last_size = -1
    stable_count = 0
    for _ in range(20):
        try:
            size = os.path.getsize(path)
        except FileNotFoundError:
            size = 0
        if size == last_size and size > 0:
            stable_count += 1
            if stable_count >= checks:
                return True
        else:
            stable_count = 0
            last_size = size
        time.sleep(interval)
    return False


def safe_open_image(path, retries=IMAGE_OPEN_RETRIES):
    """
    Buka gambar dengan retry mechanism
    Untuk menangani file yang masih dalam proses transfer
    """
    for i in range(retries):
        try:
            img = Image.open(path)
            img.load()
            return img
        except Exception as e:
            print(f"⏳ File belum siap {os.path.basename(path)}, retry {i+1}/{retries}: {e}")
            time.sleep(0.5)
    raise RuntimeError(f"Gagal membuka gambar setelah {retries}x percobaan: {os.path.basename(path)}")


def add_watermark(img: Image.Image, watermark_path: str = WATERMARK_FILE) -> Image.Image:
    """
    Tambahkan watermark PNG transparent di bagian bawah foto
    """
    if not os.path.exists(watermark_path):
        print(f"⚠️ Watermark file not found: {watermark_path}")
        return img

    try:
        # Load watermark
        watermark = Image.open(watermark_path).convert("RGBA")

        # Calculate watermark size (15% of image width)
        img_width, img_height = img.size
        watermark_width = int(img_width * 0.15)

        # Maintain aspect ratio
        watermark_ratio = watermark.size[1] / watermark.size[0]
        watermark_height = int(watermark_width * watermark_ratio)

        # Resize watermark
        watermark = watermark.resize((watermark_width, watermark_height), Image.Resampling.LANCZOS)

        # Position watermark (bottom center, with offset)
        offset_from_bottom = 50  # pixels from bottom
        x_position = (img_width - watermark_width) // 2
        y_position = img_height - watermark_height - offset_from_bottom

        # Convert main image to RGBA for transparency support
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # Create a transparent overlay
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        overlay.paste(watermark, (x_position, y_position), watermark)

        # Composite the images
        watermarked = Image.alpha_composite(img, overlay)

        # Convert back to RGB
        final_img = Image.new('RGB', watermarked.size, (255, 255, 255))
        final_img.paste(watermarked, mask=watermarked.split()[-1])

        print(f"🏷️ Watermark added: {watermark_width}x{watermark_height} at ({x_position}, {y_position})")
        return final_img

    except Exception as e:
        print(f"⚠️ Watermark failed: {e}")
        return img


def log_error(filename, error):
    """Log error ke file"""
    from config import ERROR_LOG
    with open(ERROR_LOG, "a") as f:
        f.write(f"{filename}: {error}\n")


def log_failed_upload(filename, error):
    """Log failed upload ke file"""
    from config import FAILED_UPLOADS_LOG
    with open(FAILED_UPLOADS_LOG, "a") as f:
        f.write(f"{filename}: {error}\n")


def log_public_url(url):
    """Log public URL ke file"""
    from config import URLS_FILE
    with open(URLS_FILE, "a") as f:
        f.write(url + "\n")