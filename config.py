"""
Konfigurasi untuk auto photo processing workflow
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# -------- CLOUDFLARE R2 CONFIG --------
R2_BUCKET = os.getenv("CLOUDFLARE_R2_BUCKET_NAME")
R2_ENDPOINT = os.getenv("CLOUDFLARE_R2_ENDPOINT")
R2_ACCESS_KEY = os.getenv("CLOUDFLARE_R2_ACCESS_KEY_ID")
R2_SECRET_KEY = os.getenv("CLOUDFLARE_R2_SECRET_ACCESS_KEY")
PUBLIC_DOMAIN = "https://photos.hafiportrait.photography"

# -------- CEREBRIUM API CONFIG --------
# PENTING: Ganti 'your-app-name' dengan nama app Cerebrium Anda yang sebenarnya
CEREBRIUM_API = "https://your-app-name.cerebrium.ai/predict"

# Task yang akan digunakan untuk semua foto
ENHANCEMENT_TASK = "full_enhance"  # upscale + denoise + face_restore

# -------- DIRECTORY CONFIG --------
INPUT_DIR = "input"
BACKUP_DIR = "backup"
RAW_BACKUP_DIR = "backup/raw"  # Folder khusus untuk RAW files
JPG_BACKUP_DIR = "backup/jpg"  # Folder khusus untuk JPG files
WORK_DIR = "work"
ENHANCED_DIR = "enhanced"

# -------- PROCESSING CONFIG --------
# Watermark settings
ENABLE_WATERMARK = True
WATERMARK_FILE = "watermark.png"  # Put your PNG watermark file here

# File naming
OUTPUT_PREFIX = "HFI-event"  # Prefix untuk nama file hasil

# Upload retry settings
MAX_UPLOAD_RETRIES = 3
UPLOAD_RETRY_DELAY = 5  # seconds

# File processing settings
FILE_STABILITY_CHECKS = 3
FILE_STABILITY_INTERVAL = 0.5  # seconds
IMAGE_OPEN_RETRIES = 5

# Supported file formats
SUPPORTED_FORMATS = (".jpg", ".jpeg", ".png", ".cr2", ".nef", ".arw", ".dng")

# -------- LOG FILES --------
COUNTER_FILE = ".counter.txt"
URLS_FILE = "urls.txt"
ERROR_LOG = "error.log"
FAILED_UPLOADS_LOG = "failed_uploads.txt"