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
PUBLIC_DOMAIN = os.getenv("CLOUDFLARE_R2_PUBLIC_URL", "https://photos.hafiportrait.photography")

# -------- CEREBRIUM API CONFIG --------
CEREBRIUM_API = "https://api.aws.us-east-1.cerebrium.ai/v4/p-82c79058/image-enhancement-v2/predict"
CEREBRIUM_AUTH_TOKEN = os.getenv("CEREBRIUM_AUTH_TOKEN")

# -------- AI ENHANCEMENT CONFIG --------
# Available tasks: upscale, face_restore, full_enhance, denoise, crop_5r
ENHANCEMENT_TASK = "general"  # Real-ESRGAN + GFPGAN + Denoise pipeline

# Task options untuk different scenarios:
TASK_OPTIONS = {
    "portraits": "full_enhance",      # Real-ESRGAN + GFPGAN + Denoise (best for faces)
    "landscapes": "upscale",          # Real-ESRGAN only (best for scenery)
    "wedding": "crop_5r",             # Crop to 5R ratio for wedding photos
    "damaged": "face_restore",        # GFPGAN only for damaged faces
    "noisy": "denoise",               # Denoise only for noisy images
    "general": "full_enhance"         # Default: complete AI pipeline
}

# Current active task (change this to switch enhancement type)
ACTIVE_TASK_TYPE = "general"  # Use portraits setting by default

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
