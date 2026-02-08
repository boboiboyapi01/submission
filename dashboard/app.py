import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide"
)

# LOAD DATA
@st.cache_data
def load_data():
    return pd.read_csv("dashboard/main_data.csv")

df = load_data()

# HEADER
st.title("📊 Bike Sharing Analysis Dashboard")
st.markdown(
    "Dashboard ini menampilkan hasil analisis penggunaan sepeda "
    "berdasarkan faktor suhu, waktu, dan musim."
)

# KPI
col1, col2, col3 = st.columns(3)
col1.metric("Total Pengguna", int(df["cnt"].sum()))
col2.metric("Rata-rata Harian", int(df["cnt"].mean()))
col3.metric("Hari Tercatat", df.shape[0])

st.divider()

# ANALISIS SUHU
st.subheader("Pengaruh Suhu terhadap Jumlah Pengguna")

col_left, col_right = st.columns(2)

with col_left:
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x="temp", y="cnt", ax=ax)
    ax.set_xlabel("Suhu (Normalisasi)")
    ax.set_ylabel("Jumlah Pengguna")
    ax.set_title("Hubungan Suhu dan Jumlah Pengguna")
    st.pyplot(fig)

with col_right:
    correlation = df["temp"].corr(df["cnt"])
    st.markdown("**Insight:**")
    st.write(
        f"Terdapat korelasi positif antara suhu dan jumlah pengguna "
        f"dengan nilai korelasi **{correlation:.2f}**. "
        "Semakin hangat suhu, semakin tinggi kecenderungan penggunaan sepeda."
    )

st.divider()

# ANALISIS WAKTU (JAM)
st.subheader("Pola Penggunaan Sepeda Berdasarkan Jam")

fig, ax = plt.subplots(figsize=(10, 5))
df.groupby("hr")["cnt"].sum().plot(ax=ax)
ax.set_xlabel("Jam")
ax.set_ylabel("Total Pengguna")
ax.set_title("Total Penggunaan Sepeda per Jam")
ax.grid(True)
st.pyplot(fig)

st.markdown(
    "**Insight:** Pola penggunaan menunjukkan dua puncak utama "
    "pada pagi dan sore hari, yang mengindikasikan penggunaan sepeda "
    "sebagai moda transportasi aktivitas harian."
)

st.divider()

# ANALISIS MUSIM (GEOSPATIAL ADAPTIF)
st.subheader("Distribusi Penggunaan Sepeda Berdasarkan Musim")

fig, ax = plt.subplots()
df.groupby("season")["cnt"].sum().plot(kind="bar", ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Total Pengguna")
ax.set_title("Distribusi Penggunaan Sepeda per Musim")
st.pyplot(fig)

st.markdown(
    "**Insight:** Musim tertentu menunjukkan konsentrasi penggunaan "
    "yang lebih tinggi. Walaupun dataset tidak memiliki koordinat geografis, "
    "musim digunakan sebagai pendekatan analisis spasial konseptual."
)

st.caption("Dashboard dideploy menggunakan Streamlit Cloud.")
