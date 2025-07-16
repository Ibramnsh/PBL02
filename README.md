# PBL02-PABW4A1

# Cars CRUD API

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)

API sederhana yang dibangun menggunakan FastAPI untuk mengelola data mobil. Proyek ini mendukung operasi CRUD (Create, Read, Update, Delete) penuh dan memiliki fitur untuk mengunggah data mobil secara massal melalui file CSV.

## 🚀 Instalasi & Persiapan

Ikuti langkah-langkah berikut untuk menjalankan proyek ini di lingkungan lokal Anda.

### Prasyarat
- Python 3.9 atau yang lebih baru

### Langkah-langkah Instalasi

1.  **Clone repositori ini:**
    ```bash
    git clone [URL_REPOSITORI_ANDA]
    cd [NAMA_FOLDER_REPOSITORI]
    ```

2.  **Buat dan aktifkan *virtual environment* (dianjurkan):**
    ```bash
    # Membuat venv
    python -m venv venv

    # Mengaktifkan venv (Windows)
    .\venv\Scripts\activate

    # Mengaktifkan venv (macOS/Linux)
    source venv/bin/activate
    ```

3.  **Instal semua dependensi yang dibutuhkan:**
    Gunakan file `requirements.txt` yang sudah disediakan.
    ```bash
    pip install -r requirements.txt
    ```

---

## ▶️ Menjalankan Aplikasi

Setelah instalasi selesai, jalankan server pengembangan menggunakan **Uvicorn**:

```bash
uvicorn main:app --reload
