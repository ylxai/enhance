"""
Contoh penggunaan fungsi enhance_image_cerebrium
Menunjukkan berbagai skenario penggunaan
"""

import os
from enhance_image_cerebrium import enhance_image_cerebrium, save_processed_image


def process_single_image():
    """Contoh memproses satu gambar"""
    print("=== Memproses Satu Gambar ===")
    
    # Konfigurasi
    image_path = "work/foto_wedding.jpg"
    task = "crop_5r"  # Crop ke ukuran 5R untuk foto wedding
    api_endpoint = "https://your-app-name.cerebrium.ai/predict"
    
    # Proses gambar
    success, result = enhance_image_cerebrium(image_path, task, api_endpoint)
    
    if success:
        # Simpan hasil dengan nama yang menunjukkan task
        base_name = os.path.splitext(image_path)[0]
        output_path = f"{base_name}_{task}.jpg"
        
        if save_processed_image(result, output_path):
            print(f"✅ Berhasil! Hasil disimpan di: {output_path}")
        else:
            print("❌ Enhancement berhasil tapi gagal menyimpan")
    else:
        print(f"❌ Enhancement gagal: {result}")


def process_multiple_tasks():
    """Contoh memproses gambar yang sama dengan berbagai task"""
    print("\n=== Memproses Dengan Berbagai Task ===")
    
    image_path = "work/portrait.jpg"
    api_endpoint = "https://your-app-name.cerebrium.ai/predict"
    
    # Daftar task yang ingin dicoba
    tasks = ["upscale", "face_restore", "denoise", "full_enhance"]
    
    for task in tasks:
        print(f"\nMemproses dengan task: {task}")
        
        success, result = enhance_image_cerebrium(image_path, task, api_endpoint)
        
        if success:
            # Buat nama file output
            base_name = os.path.splitext(image_path)[0]
            output_path = f"{base_name}_{task}.jpg"
            
            if save_processed_image(result, output_path):
                print(f"✅ {task}: Berhasil disimpan di {output_path}")
            else:
                print(f"❌ {task}: Gagal menyimpan file")
        else:
            print(f"❌ {task}: {result}")


def batch_process_folder():
    """Contoh memproses semua gambar dalam folder"""
    print("\n=== Batch Processing Folder ===")
    
    input_folder = "work/input_images"
    output_folder = "work/output_images"
    task = "full_enhance"
    api_endpoint = "https://your-app-name.cerebrium.ai/predict"
    
    # Buat folder output jika belum ada
    os.makedirs(output_folder, exist_ok=True)
    
    # Ekstensi file gambar yang didukung
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    
    # Cari semua file gambar di folder input
    if not os.path.exists(input_folder):
        print(f"❌ Folder input tidak ditemukan: {input_folder}")
        return
    
    image_files = []
    for file in os.listdir(input_folder):
        if any(file.lower().endswith(ext) for ext in image_extensions):
            image_files.append(file)
    
    if not image_files:
        print(f"❌ Tidak ada file gambar ditemukan di: {input_folder}")
        return
    
    print(f"Ditemukan {len(image_files)} file gambar")
    
    # Proses setiap file
    success_count = 0
    for i, filename in enumerate(image_files, 1):
        print(f"\n[{i}/{len(image_files)}] Memproses: {filename}")
        
        input_path = os.path.join(input_folder, filename)
        
        success, result = enhance_image_cerebrium(input_path, task, api_endpoint)
        
        if success:
            # Buat nama file output
            name, ext = os.path.splitext(filename)
            output_filename = f"{name}_{task}{ext}"
            output_path = os.path.join(output_folder, output_filename)
            
            if save_processed_image(result, output_path):
                print(f"✅ Berhasil: {output_filename}")
                success_count += 1
            else:
                print(f"❌ Gagal menyimpan: {filename}")
        else:
            print(f"❌ Gagal memproses: {filename} - {result}")
    
    print(f"\n=== Selesai ===")
    print(f"Berhasil: {success_count}/{len(image_files)} file")


def test_all_tasks():
    """Test semua task yang tersedia"""
    print("\n=== Test Semua Task ===")
    
    image_path = "work/test_image.jpg"
    api_endpoint = "https://your-app-name.cerebrium.ai/predict"
    
    # Semua task yang tersedia
    all_tasks = ["upscale", "face_restore", "denoise", "crop_5r", "full_enhance"]
    
    print(f"Testing dengan gambar: {image_path}")
    
    for task in all_tasks:
        print(f"\n🧪 Testing task: {task}")
        
        success, result = enhance_image_cerebrium(image_path, task, api_endpoint)
        
        if success:
            print(f"✅ {task}: Berhasil ({len(result)} bytes)")
        else:
            print(f"❌ {task}: {result}")


if __name__ == "__main__":
    print("🚀 Contoh Penggunaan enhance_image_cerebrium")
    print("=" * 50)
    
    # Ganti dengan endpoint Cerebrium Anda yang sebenarnya
    print("⚠️  PENTING: Ganti 'your-app-name' dengan nama app Cerebrium Anda!")
    print()
    
    # Jalankan contoh-contoh
    try:
        # process_single_image()
        # process_multiple_tasks()
        # batch_process_folder()
        test_all_tasks()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Proses dihentikan oleh user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
    
    print("\n✨ Selesai!")