"""
Fungsi untuk mengirim gambar ke API Cerebrium untuk enhancement
Dibuat sesuai spesifikasi task2.md
"""

import base64
import requests
from typing import Tuple, Union


def enhance_image_cerebrium(image_path: str, task: str, api_endpoint: str) -> Tuple[bool, Union[bytes, str]]:
    """
    Mengirim gambar lokal ke API Cerebrium untuk diproses dan mengembalikan hasil
    
    Args:
        image_path (str): Path lengkap menuju file gambar di komputer lokal
        task (str): Tugas yang ingin dilakukan ("upscale", "face_restore", "full_enhance", "denoise", "crop_5r")
        api_endpoint (str): URL lengkap ke endpoint predict Cerebrium
    
    Returns:
        Tuple[bool, Union[bytes, str]]: 
            - (True, image_bytes) jika berhasil
            - (False, error_message) jika gagal
    """
    
    try:
        # 1. Baca file gambar dan konversi ke base64
        print(f"Membaca gambar dari: {image_path}")
        
        try:
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
                image_base64 = base64.b64encode(image_data).decode('utf-8')
        except FileNotFoundError:
            return False, f"File gambar tidak ditemukan: {image_path}"
        except Exception as e:
            return False, f"Error membaca file gambar: {str(e)}"
        
        # 2. Buat payload JSON
        payload = {
            "image_base64": image_base64,
            "task": task
        }
        
        # 3. Setup headers
        headers = {
            "Content-Type": "application/json"
        }
        
        print(f"Mengirim request ke API dengan task: {task}")
        
        # 4. Kirim POST request ke API Cerebrium
        try:
            response = requests.post(
                api_endpoint,
                json=payload,
                headers=headers,
                timeout=120  # 120 detik timeout
            )
        except requests.exceptions.Timeout:
            return False, "Request timeout - API tidak merespons dalam 120 detik"
        except requests.exceptions.ConnectionError:
            return False, f"Tidak dapat terhubung ke API endpoint: {api_endpoint}"
        except Exception as e:
            return False, f"Error saat mengirim request: {str(e)}"
        
        # 5. Periksa status code
        if response.status_code != 200:
            try:
                error_detail = response.json()
                return False, f"API error (status {response.status_code}): {error_detail}"
            except:
                return False, f"API error (status {response.status_code}): {response.text}"
        
        # 6. Parse respons JSON
        try:
            response_data = response.json()
        except Exception as e:
            return False, f"Error parsing JSON response: {str(e)}"
        
        # 7. Ekstrak data gambar dari respons
        if "processed_image" not in response_data:
            return False, "Response tidak mengandung 'processed_image'"
        
        processed_image_data = response_data["processed_image"]
        
        # 8. Ekstrak base64 string dari format "data:image/png;base64,..."
        try:
            if processed_image_data.startswith("data:image/"):
                # Hapus prefix "data:image/png;base64," atau serupa
                base64_string = processed_image_data.split(",", 1)[1]
            else:
                # Asumsikan sudah pure base64
                base64_string = processed_image_data
            
            # Konversi base64 ke bytes
            image_bytes = base64.b64decode(base64_string)
            
        except Exception as e:
            return False, f"Error decoding base64 image: {str(e)}"
        
        print(f"Berhasil memproses gambar. Ukuran hasil: {len(image_bytes)} bytes")
        return True, image_bytes
        
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"


def save_processed_image(image_bytes: bytes, output_path: str) -> bool:
    """
    Helper function untuk menyimpan hasil gambar yang sudah diproses
    
    Args:
        image_bytes (bytes): Data gambar dalam format bytes
        output_path (str): Path untuk menyimpan gambar hasil
    
    Returns:
        bool: True jika berhasil, False jika gagal
    """
    try:
        with open(output_path, 'wb') as output_file:
            output_file.write(image_bytes)
        print(f"Gambar berhasil disimpan ke: {output_path}")
        return True
    except Exception as e:
        print(f"Error menyimpan gambar: {str(e)}")
        return False


# Contoh penggunaan
if __name__ == "__main__":
    # Contoh penggunaan fungsi
    image_path = "work/gambar_01.jpg"
    task = "full_enhance"
    api_endpoint = "https://your-cerebrium-endpoint.com/predict"
    
    # Panggil fungsi
    success, result = enhance_image_cerebrium(image_path, task, api_endpoint)
    
    if success:
        # Simpan hasil
        output_path = "work/gambar_01_enhanced.jpg"
        if save_processed_image(result, output_path):
            print("Proses enhancement berhasil!")
        else:
            print("Enhancement berhasil tapi gagal menyimpan file")
    else:
        print(f"Enhancement gagal: {result}")