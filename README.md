# Dashboard Bike Sharing

## Deskripsi
Dashboard ini menggunakan data dari sistem penyewaan sepeda untuk menganalisis pengaruh suhu terhadap jumlah pengguna dan variasi jumlah pengguna sepanjang waktu dalam satu hari. Dashboard ini dibangun menggunakan Streamlit.

## Prerequisites
Sebelum menjalankan dashboard, pastikan Anda memiliki lingkungan pengembangan yang siap dan telah menginstal semua dependensi. Berikut adalah langkah-langkah yang perlu dilakukan:

1. **Instalasi Python**: Pastikan Python 3.x sudah terpasang di sistem Anda.
2. **Instalasi Dependensi**: Anda perlu menginstal semua paket yang diperlukan. Gunakan perintah berikut untuk menginstal paket-paket yang dibutuhkan:
   ```bash
   pip install -r requirements.txt
   ```

## Cara Menjalankan Dashboard

1. **Navigasi ke Folder Dashboard**: Buka terminal atau command prompt, dan navigasikan ke direktori `dashboard` tempat berkas `dashboard.py` berada. Anda dapat melakukannya dengan perintah:
   ```bash
   cd path/to/your/submission/dashboard
   ```

2. **Menjalankan Streamlit**: Setelah berada di dalam folder yang benar, jalankan perintah berikut untuk memulai dashboard:
   ```bash
   streamlit run dashboard.py
   ```

3. **Akses Dashboard**: Setelah menjalankan perintah di atas, buka browser Anda dan kunjungi alamat yang ditunjukkan di terminal (biasanya `http://localhost:8501`) untuk melihat dashboard.

## Struktur Berkas
- `dashboard.py`: Skrip utama yang berisi kode untuk menjalankan dashboard.
- `main_data.csv`: Berkas data yang digunakan dalam dashboard.
- `requirements.txt`: Daftar dependensi yang diperlukan untuk menjalankan dashboard.

