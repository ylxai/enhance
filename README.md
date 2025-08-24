# Fungsi Client untuk Cerebrium Image Enhancement API

Folder ini berisi fungsi Python untuk berinteraksi dengan API Cerebrium image enhancement yang telah di-deploy.

## File yang Tersedia

### 1. `enhance_image_cerebrium.py`
Fungsi utama untuk mengirim gambar ke API Cerebrium dan menerima hasil enhancement.

### 2. `example_usage.py`
Contoh penggunaan lengkap dengan berbagai skenario.

### 3. `README.md`
Dokumentasi ini.

## Instalasi Dependencies

```bash
pip install requests
```

## Penggunaan Dasar

```python
from enhance_image_cerebrium import enhance_image_cerebrium, save_processed_image

# Konfigurasi
image_path = "path/to/your/image.jpg"
task = "full_enhance"
api_endpoint = "https://your-app-name.cerebrium.ai/predict"

# Proses gambar
success, result = enhance_image_cerebrium(image_path, task, api_endpoint)

if success:
    # Simpan hasil
    save_processed_image(result, "output/enhanced_image.jpg")
    print("Berhasil!")
else:
    print(f"Gagal: {result}")
```

## Task yang Tersedia

| Task | Deskripsi |
|------|-----------|
| `upscale` | Memperbesar gambar 4x dengan kualitas tinggi |
| `face_restore` | Memperbaiki dan memperhalus wajah |
| `denoise` | Menghilangkan noise dari gambar |
| `crop_5r` | Auto crop ke ukuran 5R untuk foto wedding |
| `full_enhance` | Kombinasi upscale + denoise + face restore |

## Parameter Fungsi

### `enhance_image_cerebrium(image_path, task, api_endpoint)`

**Input:**
- `image_path` (str): Path lengkap ke file gambar lokal
- `task` (str): Jenis enhancement yang diinginkan
- `api_endpoint` (str): URL endpoint API Cerebrium

**Output:**
- `(True, image_bytes)` jika berhasil
- `(False, error_message)` jika gagal

## Contoh Penggunaan Lanjutan

### 1. Proses Satu Gambar
```python
success, result = enhance_image_cerebrium(
    image_path="work/foto.jpg",
    task="crop_5r",
    api_endpoint="https://your-app.cerebrium.ai/predict"
)
```

### 2. Proses Multiple Tasks
```python
tasks = ["upscale", "face_restore", "denoise"]
for task in tasks:
    success, result = enhance_image_cerebrium(image_path, task, api_endpoint)
    if success:
        save_processed_image(result, f"output_{task}.jpg")
```

### 3. Batch Processing
```python
import os

input_folder = "input_images"
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.png')):
        image_path = os.path.join(input_folder, filename)
        success, result = enhance_image_cerebrium(image_path, "full_enhance", api_endpoint)
        if success:
            output_path = f"output/{filename}"
            save_processed_image(result, output_path)
```

## Error Handling

Fungsi menangani berbagai jenis error:

- **File tidak ditemukan**: `FileNotFoundError`
- **Connection error**: Tidak bisa terhubung ke API
- **Timeout**: Request lebih dari 120 detik
- **API error**: Status code bukan 200
- **Invalid response**: Response tidak sesuai format

## Tips Penggunaan

1. **Pastikan endpoint benar**: Ganti `your-app-name` dengan nama app Cerebrium Anda
2. **Ukuran file**: API dapat menangani file gambar berukuran besar
3. **Timeout**: Default 120 detik, sesuaikan jika diperlukan
4. **Format gambar**: Mendukung JPG, PNG, BMP, TIFF
5. **Hasil**: Selalu dalam format PNG base64

## Troubleshooting

### Error: "File gambar tidak ditemukan"
- Periksa path file gambar
- Pastikan file exists dan readable

### Error: "Tidak dapat terhubung ke API"
- Periksa koneksi internet
- Pastikan endpoint URL benar
- Pastikan API Cerebrium sedang running

### Error: "Request timeout"
- Gambar terlalu besar
- API sedang overload
- Tingkatkan timeout jika diperlukan

### Error: "API error (status 500)"
- Ada error di server API
- Cek logs Cerebrium untuk detail error

## Contoh Lengkap

Lihat file `example_usage.py` untuk contoh penggunaan yang lebih lengkap dan detail.

## Support

Jika ada masalah atau pertanyaan, periksa:
1. Logs Cerebrium app
2. Network connectivity
3. File permissions
4. API endpoint URL