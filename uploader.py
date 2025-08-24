"""
Upload functionality untuk Cloudflare R2
"""

import boto3
import time
from config import (
    R2_BUCKET, R2_ENDPOINT, R2_ACCESS_KEY, R2_SECRET_KEY, 
    PUBLIC_DOMAIN, MAX_UPLOAD_RETRIES, UPLOAD_RETRY_DELAY
)
from utils import log_failed_upload, log_public_url


# Initialize R2 client
s3 = boto3.client(
    "s3",
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY,
    region_name="auto"
)


def upload_to_r2(local_file_path, remote_filename):
    """
    Upload file ke Cloudflare R2 dengan retry mechanism
    
    Args:
        local_file_path (str): Path file lokal yang akan diupload
        remote_filename (str): Nama file di R2
    
    Returns:
        tuple: (success: bool, public_url: str or error_message: str)
    """
    upload_success = False
    
    for upload_attempt in range(MAX_UPLOAD_RETRIES):
        try:
            print(f"☁️ Uploading to R2 (attempt {upload_attempt + 1}/{MAX_UPLOAD_RETRIES})...")
            
            # Upload file
            s3.upload_file(local_file_path, R2_BUCKET, remote_filename)
            
            # Generate public URL
            public_url = f"{PUBLIC_DOMAIN}/{remote_filename}"
            print(f"✅ Uploaded → {public_url}")
            
            # Log public URL
            log_public_url(public_url)
            
            upload_success = True
            return True, public_url
            
        except Exception as upload_error:
            print(f"⚠️ Upload attempt {upload_attempt + 1} failed: {upload_error}")
            
            if upload_attempt < MAX_UPLOAD_RETRIES - 1:
                print(f"🔄 Retrying in {UPLOAD_RETRY_DELAY} seconds...")
                time.sleep(UPLOAD_RETRY_DELAY)
            else:
                print(f"❌ Upload failed after {MAX_UPLOAD_RETRIES} attempts")
                # Log failed upload
                log_failed_upload(remote_filename, str(upload_error))
                return False, str(upload_error)
    
    return False, "Upload failed after all retries"


def check_r2_connection():
    """
    Test koneksi ke R2
    
    Returns:
        bool: True jika koneksi berhasil
    """
    try:
        # List buckets untuk test koneksi
        response = s3.list_buckets()
        print(f"✅ R2 connection successful. Found {len(response['Buckets'])} buckets")
        return True
    except Exception as e:
        print(f"❌ R2 connection failed: {e}")
        return False