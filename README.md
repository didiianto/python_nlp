# python nlp

# Virtual Environment Setup on Windows

Ikuti langkah-langkah berikut untuk membuat dan mengaktifkan virtual environment di Windows.

### 1. Buat Virtual Environment
Buka Command Prompt di folder proyek Anda, lalu jalankan perintah berikut:
```bash
python -m venv nama_venv
```

### 2. Aktifkan Virtual Environment
Setelah membuat virtual environment, aktifkan dengan menjalankan perintah berikut:
```bash
nama_venv\Scripts\activate
```

### 3. Menonaktifkan Virtual Environment
Setelah selesai bekerja, Anda bisa menonaktifkan virtual environment dengan menjalankan perintah:
```bash
deactivate
```


# Install Library yang Dibutuhkan

Untuk menjalankan aplikasi ini, Anda perlu menginstal beberapa library Python. Gunakan perintah berikut untuk menginstalnya:

```bash
pip install Flask nltk scikit-learn pandas numpy
```

# Jalankan Aplikasi Flask
```bash
python search.py
```

# Cek di Browser: Setelah dijalankan, buka browser dan akses http://127.0.0.1:5000 atau sesuai port yang diinginkan untuk melihat aplikasi Flask Anda.