"""
Photo processing logic
"""

import os
import shutil
from PIL import Image
from config import (
    RAW_BACKUP_DIR, JPG_BACKUP_DIR, WORK_DIR, ENHANCED_DIR,
    ENABLE_WATERMARK, CEREBRIUM_API, ENHANCEMENT_TASK, OUTPUT_PREFIX
)
from utils import wait_until_complete, safe_open_image, add_watermark, log_error
from uploader import upload_to_r2
from enhance_image_cerebrium import enhance_image_cerebrium


def process_raw_file(input_path, base_name):
    """
    Process RAW file (CR2, NEF, ARW, DNG)
    
    Args:
        input_path (str): Path ke file RAW
        base_name (str): Base name tanpa extension
    
    Returns:
        PIL.Image: Converted image atau None jika gagal
    """
    print(f"📷 RAW file detected: {os.path.basename(input_path)}")
    
    # Backup RAW file (copy original)
    raw_backup_path = os.path.join(RAW_BACKUP_DIR, os.path.basename(input_path))
    shutil.copy2(input_path, raw_backup_path)
    print(f"📂 RAW Backup → {raw_backup_path}")
    
    # Convert RAW to JPG for processing (requires rawpy)
    try:
        import rawpy
        with rawpy.imread(input_path) as raw:
            rgb = raw.postprocess()
        img = Image.fromarray(rgb)
        print(f"✅ RAW conversion successful")
        return img
    except ImportError:
        print("⚠️ rawpy not installed, skipping RAW processing")
        print("   Install with: pip install rawpy")
        return None
    except Exception as e:
        print(f"⚠️ RAW conversion failed: {e}")
        return None


def process_regular_image(input_path):
    """
    Process regular image file (JPG, PNG)
    
    Args:
        input_path (str): Path ke file gambar
    
    Returns:
        PIL.Image: Loaded image
    """
    return safe_open_image(input_path)


def backup_jpg(img, base_name):
    """
    Backup processed JPG
    
    Args:
        img (PIL.Image): Image to backup
        base_name (str): Base name untuk file
    
    Returns:
        str: Path ke backup file
    """
    jpg_backup_path = os.path.join(JPG_BACKUP_DIR, base_name + ".jpg")
    img.convert("RGB").save(jpg_backup_path, "JPEG", quality=95)
    print(f"📂 JPG Backup → {jpg_backup_path}")
    return jpg_backup_path


def prepare_for_api(img, base_name):
    """
    Prepare image untuk dikirim ke API (add watermark, save)
    
    Args:
        img (PIL.Image): Image to process
        base_name (str): Base name untuk file
    
    Returns:
        str: Path ke file yang siap dikirim ke API
    """
    # Add watermark if enabled
    if ENABLE_WATERMARK:
        img = add_watermark(img)
    
    # Save final processed image for API
    work_path = os.path.join(WORK_DIR, f"{base_name}_processed.jpg")
    img.convert("RGB").save(work_path, "JPEG", quality=95)
    print(f"🛠️ Processed image ready → {work_path}")
    
    return work_path


def enhance_with_cerebrium(work_path):
    """
    Enhance image menggunakan Cerebrium API
    
    Args:
        work_path (str): Path ke file yang akan di-enhance
    
    Returns:
        tuple: (success: bool, enhanced_bytes: bytes or error_message: str)
    """
    print(f"🚀 Sending {os.path.basename(work_path)} to Cerebrium API...")
    
    success, result = enhance_image_cerebrium(
        image_path=work_path,
        task=ENHANCEMENT_TASK,
        api_endpoint=CEREBRIUM_API
    )
    
    if success:
        print(f"✅ Cerebrium API enhancement successful! Size: {len(result)} bytes")
        return True, result
    else:
        print(f"❌ Cerebrium API enhancement failed: {result}")
        return False, result


def save_enhanced_image(enhanced_bytes, counter):
    """
    Save enhanced image ke disk
    
    Args:
        enhanced_bytes (bytes): Enhanced image data
        counter (int): Counter untuk naming
    
    Returns:
        str: Path ke enhanced file
    """
    enhance_name = f"{OUTPUT_PREFIX}_{counter:03d}.jpg"
    enhance_path = os.path.join(ENHANCED_DIR, enhance_name)
    
    with open(enhance_path, "wb") as out:
        out.write(enhanced_bytes)
    
    print(f"✨ Enhanced → {enhance_path}")
    return enhance_path, enhance_name


def process_photo(input_path, counter):
    """
    Main photo processing function
    
    Args:
        input_path (str): Path ke file input
        counter (int): Counter untuk naming
    
    Returns:
        bool: True jika berhasil, False jika gagal
    """
    fname = os.path.basename(input_path)
    base, ext = os.path.splitext(fname)
    ext = ext.lower().replace("jpeg", "jpg")
    
    # Deteksi file type
    is_raw = ext in [".cr2", ".nef", ".arw", ".dng"]
    
    try:
        # Wait until file transfer complete
        wait_until_complete(input_path)
        
        # Process based on file type
        if is_raw:
            img = process_raw_file(input_path, base)
            if img is None:
                return False
        else:
            img = process_regular_image(input_path)
        
        # Backup JPG
        backup_jpg(img, base)
        
        # Prepare for API
        work_path = prepare_for_api(img, base)
        
        # Enhance with Cerebrium
        success, enhanced_bytes = enhance_with_cerebrium(work_path)
        if not success:
            raise RuntimeError(f"Enhancement failed: {enhanced_bytes}")
        
        # Save enhanced image
        enhance_path, enhance_name = save_enhanced_image(enhanced_bytes, counter)
        
        # Upload to R2
        upload_success, result = upload_to_r2(enhance_path, enhance_name)
        
        if not upload_success:
            print(f"⚠️ File saved locally but upload failed: {enhance_path}")
            print(f"   Error: {result}")
            print(f"   You can manually upload later or check failed_uploads.txt")
        
        return True
        
    except Exception as e:
        error_msg = f"Error memproses {fname}: {e}"
        print(f"❌ {error_msg}")
        log_error(fname, str(e))
        return False