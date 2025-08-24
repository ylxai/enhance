# Setup Guide - Auto Photo Processing Workflow

## 📋 Prerequisites

1. **Python 3.8+** terinstall
2. **Cerebrium app** sudah di-deploy
3. **Cloudflare R2** bucket sudah dibuat
4. **R2 API tokens** sudah dibuat

## 🔧 Installation Steps

### 1. Install Dependencies
```bash
pip install requests boto3 pillow watchdog python-dotenv

# Optional: Untuk support RAW files (CR2, NEF, ARW, DNG)
pip install rawpy
```

### 2. Setup Environment Variables

**Buat file `.env`** di folder `client_functions/`:
```bash
cp .env.example .env
```

**Edit file `.env`** dengan credentials Anda:
```env
CLOUDFLARE_R2_BUCKET_NAME=your-bucket-name
CLOUDFLARE_R2_ENDPOINT=https://your-account-id.r2.cloudflarestorage.com
CLOUDFLARE_R2_ACCESS_KEY_ID=your-access-key-id
CLOUDFLARE_R2_SECRET_ACCESS_KEY=your-secret-access-key
```

### 3. Update Cerebrium API Endpoint

**Edit file `config.py`**, ganti:
```python
CEREBRIUM_API = "https://your-app-name.cerebrium.ai/predict"
```

Dengan nama app Cerebrium Anda yang sebenarnya:
```python
CEREBRIUM_API = "https://my-image-enhancer.cerebrium.ai/predict"
```

### 4. Setup Watermark (Optional)

Jika ingin menambahkan watermark:
1. Siapkan file PNG transparent dengan nama `watermark.png`
2. Letakkan di folder `client_functions/`
3. Atau edit `WATERMARK_FILE` di `config.py`

## 🚀 Cara Mendapatkan Cloudflare R2 Credentials

### 1. Buat R2 Bucket
1. Login ke **Cloudflare Dashboard**
2. Pilih **R2 Object Storage**
3. Klik **Create bucket**
4. Beri nama bucket (contoh: `my-photo-storage`)

### 2. Buat R2 API Token
1. Di dashboard R2, klik **Manage R2 API tokens**
2. Klik **Create API token**
3. Pilih **Custom token**
4. **Permissions**: Object Read & Write
5. **Account resources**: Include - All accounts
6. **Zone resources**: Include - All zones
7. **Bucket resources**: Include - Specific bucket (pilih bucket Anda)
8. Klik **Continue to summary** → **Create token**

### 3. Catat Credentials
Setelah token dibuat, Anda akan mendapat:
- **Access Key ID** → `CLOUDFLARE_R2_ACCESS_KEY_ID`
- **Secret Access Key** → `CLOUDFLARE_R2_SECRET_ACCESS_KEY`
- **Endpoint URL** → `CLOUDFLARE_R2_ENDPOINT`

## 📁 Struktur Folder

Setelah setup, struktur folder akan seperti ini:
```
client_functions/
├── .env                    # Credentials (JANGAN commit ke git!)
├── .env.example           # Template untuk .env
├── config.py              # Konfigurasi
├── utils.py               # Utility functions
├── uploader.py            # R2 upload logic
├── processor.py           # Photo processing
├── enhance_image_cerebrium.py  # Cerebrium API client
├── auto.py                # Main application
├── watermark.png          # Watermark file (optional)
└── README_SETUP.md        # Panduan ini

# Folder yang akan dibuat otomatis:
input/                     # Drop foto di sini
backup/
├── raw/                   # Backup file RAW
└── jpg/                   # Backup file JPG
work/                      # File temporary
enhanced/                  # Hasil enhancement
```

## ▶️ Menjalankan Aplikasi

```bash
cd client_functions
python auto.py
```

Output yang diharapkan:
```
🚀 Auto Photo Processing Workflow - Cerebrium Edition
============================================================
🔍 Checking R2 connection...
✅ R2 connection successful. Found 1 buckets
📁 Monitoring folder: input/
📋 Supported formats: .jpg, .jpeg, .png, .cr2, .nef, .arw, .dng
🎯 Enhancement task: full_enhance (upscale + denoise + face_restore)
============================================================
📊 Starting with counter: 1
✨ Ready! Drop photos into the input folder...
```

## 🧪 Testing

1. **Drop foto** ke folder `input/`
2. **Monitor output** di terminal
3. **Check hasil** di folder `enhanced/`
4. **Check public URLs** di file `urls.txt`

## ⚠️ Troubleshooting

### Error: "R2 connection failed"
- Periksa credentials di `.env`
- Pastikan API token masih valid
- Periksa permissions token

### Error: "Cerebrium enhance failed"
- Pastikan app Cerebrium sedang running
- Periksa endpoint URL di `config.py`
- Check logs Cerebrium untuk detail error

### Error: "rawpy not installed"
- Install dengan: `pip install rawpy`
- Atau skip file RAW jika tidak diperlukan

### File tidak terdeteksi
- Pastikan format file didukung
- Check permissions folder `input/`
- Restart aplikasi jika perlu

## 🔒 Security Notes

1. **JANGAN commit file `.env`** ke git
2. **Gunakan .gitignore** untuk exclude `.env`
3. **Rotate API tokens** secara berkala
4. **Limit permissions** token sesuai kebutuhan

## 📝 Log Files

Aplikasi akan membuat beberapa log files:
- `urls.txt` - Daftar public URLs hasil upload
- `error.log` - Log error processing
- `failed_uploads.txt` - Log upload yang gagal
- `.counter.txt` - Counter untuk naming file