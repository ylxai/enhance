"""
Auto Photo Processing Workflow - Revisi untuk Cerebrium API
Monitoring folder input, process foto, enhance dengan Cerebrium, upload ke R2
"""

import os
import time
from PIL import ImageFile
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Import modules yang sudah dipisah
from config import INPUT_DIR, SUPPORTED_FORMATS
from utils import load_counter, save_counter
from processor import process_photo
from uploader import check_r2_connection

# Setup PIL untuk handle truncated images
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Buat semua direktori yang diperlukan
from config import BACKUP_DIR, RAW_BACKUP_DIR, JPG_BACKUP_DIR, WORK_DIR, ENHANCED_DIR

for directory in [INPUT_DIR, BACKUP_DIR, RAW_BACKUP_DIR, JPG_BACKUP_DIR, WORK_DIR, ENHANCED_DIR]:
    os.makedirs(directory, exist_ok=True)


class PhotoHandler(FileSystemEventHandler):
    """Handler untuk monitoring file baru di input directory"""
    
    def __init__(self):
        self.counter = load_counter()
        print(f"📊 Starting with counter: {self.counter}")
    
    def on_created(self, event):
        """Handle file baru yang dibuat di input directory"""
        if event.is_directory:
            return
        
        # Check if file is supported format
        file_path = event.src_path.lower()
        if file_path.endswith(SUPPORTED_FORMATS):
            print(f"📸 Detected: {os.path.basename(event.src_path)}")
            
            # Process photo
            success = process_photo(event.src_path, self.counter)
            
            if success:
                self.counter += 1
                save_counter(self.counter)
                print(f"✅ Photo processed successfully. Next counter: {self.counter}")
            else:
                print(f"❌ Photo processing failed")


def main():
    """Main function untuk menjalankan monitoring"""
    print("🚀 Auto Photo Processing Workflow - Cerebrium Edition")
    print("=" * 60)
    
    # Check R2 connection
    print("🔍 Checking R2 connection...")
    if not check_r2_connection():
        print("⚠️ Warning: R2 connection failed. Files will be saved locally only.")
    
    # Check Cerebrium API endpoint
    from config import CEREBRIUM_API
    if "your-app-name" in CEREBRIUM_API:
        print("⚠️ WARNING: Please update CEREBRIUM_API in config.py with your actual app name!")
        print(f"   Current: {CEREBRIUM_API}")
    
    print(f"📁 Monitoring folder: {INPUT_DIR}/")
    print(f"📋 Supported formats: {', '.join(SUPPORTED_FORMATS)}")
    print("🎯 Enhancement task: full_enhance (upscale + denoise + face_restore)")
    print("=" * 60)
    
    # Setup file monitoring
    event_handler = PhotoHandler()
    observer = Observer()
    observer.schedule(event_handler, INPUT_DIR, recursive=False)
    observer.start()
    
    try:
        print("✨ Ready! Drop photos into the input folder...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping monitoring...")
        observer.stop()
    
    observer.join()
    print("👋 Goodbye!")


if __name__ == "__main__":
    main()
