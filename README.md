# Dashboard Analisis Bike Sharing

## Deskripsi
Dashboard interaktif ini dibuat untuk menganalisis data Bike Sharing Dataset. Dashboard menampilkan:

- Pola penyewaan sepeda berdasarkan jam dan hari dalam seminggu  
- Pengaruh faktor cuaca (suhu, kelembaban, kecepatan angin) terhadap jumlah penyewaan  
- Segmentasi tingkat permintaan (demand clustering) berdasarkan kondisi cuaca  
- Metrik kunci dan visualisasi yang membantu memahami perilaku pengguna  

Dashboard dibangun menggunakan **Streamlit** dan dapat dijalankan secara lokal atau di-deploy ke Streamlit Cloud.

## Demo Dashboard (jika sudah di-deploy)
Jika Anda telah mendeploy ulang dashboard ini ke Streamlit Cloud, tautan biasanya akan berbentuk:  
`https://submission-d9fqcxeccsztw8wf5xdcva.streamlit.app/`

**Catatan**: Tautan lama mungkin sudah tidak aktif. Silakan deploy ulang aplikasi Anda untuk mendapatkan link baru.

## Prerequisites
Pastikan Anda memiliki:

1. **Python** 3.11 atau 3.12 (direkomendasikan)  
   → Versi 3.13 juga bisa, tapi 3.11/3.12 paling stabil untuk library data science saat ini.

2. Semua dependensi terinstal. Jalankan perintah berikut di terminal:
   ```bash
   pip install -r requirements.txt