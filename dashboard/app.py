import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# CONFIG
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide"
)

sns.set_style("whitegrid")

# LOAD DATA
@st.cache_data
def load_data():
    return pd.read_csv("dashboard/main_data.csv")

df = load_data()
df["dteday"] = pd.to_datetime(df["dteday"])

# SIDEBAR FILTER
st.sidebar.header("Filter Data")

min_date = df["dteday"].min()
max_date = df["dteday"].max()

date_range = st.sidebar.date_input(
    "Rentang Tanggal",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

filtered_df = df[
    (df["dteday"] >= pd.to_datetime(date_range[0])) &
    (df["dteday"] <= pd.to_datetime(date_range[1]))
]

# HEADER
st.title("🚲 Bike Sharing Dashboard")
st.markdown(
    """
Dashboard ini menyajikan analisis data penyewaan sepeda dengan fokus pada:
- Pengaruh **suhu**
- Pola **waktu (jam)**
- Segmentasi tingkat penggunaan harian

Analisis dilakukan berdasarkan data historis yang tersedia.
"""
)

# KPI
col1, col2, col3 = st.columns(3)

col1.metric("Total Pengguna", int(filtered_df["cnt"].sum()))
col2.metric("Rata-rata Harian", int(filtered_df["cnt"].mean()))
col3.metric("Jumlah Hari", filtered_df["dteday"].nunique())

st.divider()

# TEMPERATURE ANALYSIS
st.subheader("🌡️ Pengaruh Suhu terhadap Jumlah Pengguna")

fig, ax = plt.subplots()
sns.scatterplot(
    data=filtered_df,
    x="temp",
    y="cnt",
    alpha=0.6,
    ax=ax
)

ax.set_xlabel("Suhu (Normalisasi)")
ax.set_ylabel("Jumlah Pengguna")
ax.set_title("Hubungan Suhu dan Jumlah Pengguna")

st.pyplot(fig)

corr = filtered_df["temp"].corr(filtered_df["cnt"])

st.markdown(
    f"""
**Insight:**  
Terdapat hubungan positif antara suhu dan jumlah pengguna
(**korelasi = {corr:.2f}**).  
Pada suhu yang lebih hangat, jumlah penyewaan cenderung meningkat.
"""
)

st.divider()

# HOURLY USAGE PATTERN
st.subheader("⏰ Pola Penggunaan Berdasarkan Jam")

hourly_avg = filtered_df.groupby("hr")["cnt"].mean()

fig, ax = plt.subplots(figsize=(10, 4))
hourly_avg.plot(ax=ax)
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Jumlah Pengguna")
ax.set_title("Rata-rata Penggunaan Sepeda per Jam")
ax.grid(True)

st.pyplot(fig)

st.markdown(
    """
**Insight:**  
Terlihat dua puncak utama penggunaan pada pagi dan sore hari.
Hal ini mengindikasikan bahwa sepeda sering digunakan sebagai
sarana transportasi harian (berangkat dan pulang aktivitas).
"""
)

st.divider()

# MANUAL CLUSTERING (NON-ML)
st.subheader("📊 Segmentasi Tingkat Penggunaan Harian (Clustering Manual)")

daily_usage = (
    filtered_df
    .groupby("dteday")["cnt"]
    .sum()
    .reset_index()
)

def usage_category(x):
    if x < 1000:
        return "Rendah"
    elif x < 3000:
        return "Sedang"
    else:
        return "Tinggi"

daily_usage["kategori"] = daily_usage["cnt"].apply(usage_category)

fig, ax = plt.subplots()
sns.countplot(
    data=daily_usage,
    x="kategori",
    order=["Rendah", "Sedang", "Tinggi"],
    ax=ax
)

ax.set_xlabel("Kategori Penggunaan")
ax.set_ylabel("Jumlah Hari")
ax.set_title("Distribusi Hari Berdasarkan Tingkat Penggunaan")

st.pyplot(fig)

st.markdown(
    """
**Insight:**  
Mayoritas hari berada pada kategori **Sedang**, yang menunjukkan pola penggunaan
yang relatif stabil. Hari dengan kategori **Tinggi** dapat menjadi fokus
untuk optimalisasi kapasitas layanan.
"""
)

st.divider()

# CONCLUSION
st.subheader("📌 Kesimpulan")

st.markdown(
    """
- Suhu memiliki pengaruh terhadap peningkatan jumlah pengguna.
- Pola waktu menunjukkan penggunaan tinggi pada jam-jam tertentu.
- Segmentasi manual membantu memahami tingkat intensitas penggunaan harian.

Dashboard ini mendukung pengambilan keputusan berbasis data
dalam pengelolaan sistem bike sharing.
"""
)

st.caption("Dashboard interaktif ini dibangun menggunakan Streamlit dan dideploy di Streamlit Cloud.")
