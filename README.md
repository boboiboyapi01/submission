# Proyek Analisis Data: Bike Sharing Dataset

## Deskripsi
Proyek ini bertujuan untuk menganalisis Bike Sharing Dataset (periode 2011–2012) guna memahami pola penyewaan sepeda serta pengaruh faktor cuaca dan waktu.

Analisis dilakukan menggunakan Jupyter Notebook (notebook.ipynb) dengan tahapan lengkap, meliputi:
- Data wrangling dan data cleaning
- Exploratory Data Analysis (EDA)
- Visualisasi data
- Analisis lanjutan berupa clustering manual (tanpa menggunakan algoritma machine learning)
- Insight dan rekomendasi bisnis

Selain itu, proyek ini juga menyediakan dashboard interaktif berbasis Streamlit untuk eksplorasi data secara dinamis.

## Dataset
Dataset yang digunakan dalam proyek ini terdiri dari:
- day.csv, yaitu data agregasi penyewaan sepeda harian
- hour.csv, yaitu data agregasi penyewaan sepeda per jam

Dataset ini digunakan sebagai dasar analisis pada notebook dan dashboard.

## Dashboard Interaktif
Dashboard interaktif hasil analisis data telah dideploy menggunakan Streamlit Cloud dan dapat diakses melalui tautan berikut:

https://submission-d9fqcxeccsztw8wf5xdcva.streamlit.app/

Catatan: Jika tautan tidak dapat diakses, kemungkinan deployment sebelumnya sudah kedaluwarsa dan aplikasi dapat dideploy ulang melalui Streamlit Cloud.

## Prerequisites
Proyek ini membutuhkan:
- Python versi 3.10 atau lebih baru
- Library Python sesuai dengan file requirements.txt

Pastikan seluruh dependensi telah terinstal sebelum menjalankan notebook maupun dashboard.

## Cara Menjalankan Dashboard Secara Lokal
1. Masuk ke direktori proyek:
   cd path/to/your/project

2. Instal seluruh dependensi:
   pip install -r requirements.txt

3. Jalankan aplikasi Streamlit:
   streamlit run app.py

4. Buka browser dan akses alamat lokal yang ditampilkan (umumnya http://localhost:8501).

## Catatan Akhir
Proyek ini disusun untuk memenuhi kriteria penilaian kelas Analisis Data, dengan fokus pada:
- Dokumentasi analisis yang jelas
- Visualisasi data yang efektif
- Analisis lanjutan non–machine learning
- Dashboard interaktif yang dapat diakses secara online
