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

# Pastikan kolom datetime
df['dteday'] = pd.to_datetime(df['dteday'])

# HEADER
st.title("📊 Bike Sharing Analysis Dashboard")
st.markdown(
    "Dashboard ini menampilkan hasil analisis penggunaan sepeda "
    "berdasarkan faktor suhu, waktu, musim, serta analisis RFM dan clustering."
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

col_left_hr, col_right_hr = st.columns(2)

with col_left_hr:
    fig, ax = plt.subplots(figsize=(10, 5))
    df.groupby("hr")["cnt"].sum().plot(ax=ax)
    ax.set_xlabel("Jam")
    ax.set_ylabel("Total Pengguna")
    ax.set_title("Total Penggunaan Sepeda per Jam")
    ax.grid(True)
    st.pyplot(fig)

with col_right_hr:
    st.markdown("**Statistik Deskriptif per Jam:**")
    st.dataframe(df.groupby("hr")["cnt"].describe())

    st.markdown("**Insight:** Pola penggunaan menunjukkan dua puncak utama "
                "pada pagi dan sore hari, yang mengindikasikan penggunaan sepeda "
                "sebagai moda transportasi aktivitas harian.")

# Tambahan: Boxplot untuk variabilitas
fig_box, ax_box = plt.subplots(figsize=(12, 6))
sns.boxplot(x='hr', y='cnt', data=df, ax=ax_box)
ax_box.set_title('Distribusi Jumlah Pengguna Sepeda Berdasarkan Jam')
ax_box.set_xlabel('Jam dalam Sehari')
ax_box.set_ylabel('Jumlah Pengguna (cnt)')
st.pyplot(fig_box)

st.divider()

# ANALISIS MUSIM (GEOSPATIAL ADAPTIF)
st.subheader("Distribusi Penggunaan Sepeda Berdasarkan Musim")

if 'season' in df.columns:
    # Map season jika numeric
    if pd.api.types.is_numeric_dtype(df['season']):
        season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
        df['season_name'] = df['season'].map(season_map)
        group_col = 'season_name'
    else:
        group_col = 'season'
    
    season_data = df.groupby(group_col)["cnt"].sum().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(data=season_data, x=group_col, y="cnt", ax=ax)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Total Pengguna")
    ax.set_title("Distribusi Penggunaan Sepeda per Musim")
    st.pyplot(fig)

    # Insight tambahan
    max_season = season_data.loc[season_data['cnt'].idxmax(), group_col]
    st.markdown(
        f"**Insight:** Musim dengan penggunaan tertinggi adalah **{max_season}**. "
        "Musim tertentu menunjukkan konsentrasi penggunaan "
        "yang lebih tinggi. Walaupun dataset tidak memiliki koordinat geografis, "
        "musim digunakan sebagai pendekatan analisis spasial konseptual."
    )
else:
    st.warning("Kolom 'season' tidak ditemukan dalam data. Melewati analisis musim, RFM, dan clustering.")

st.divider()

# RFM ANALYSIS (jika season ada)
if 'season' in df.columns:
    st.subheader("RFM Analysis Berdasarkan Musim")
    
    latest_date = df['dteday'].max()
    rfm = df.groupby('season').agg({
        'dteday': lambda x: (latest_date - x.max()).days,
        'cnt': ['count', 'sum']
    })
    rfm.columns = ['Recency', 'Frequency', 'Monetary']
    rfm = rfm.reset_index()
    
    st.dataframe(rfm)
    
    st.markdown("**Insight RFM:** Analisis ini mengelompokkan perilaku penggunaan berdasarkan Recency (jarak hari terakhir), Frequency (frekuensi), dan Monetary (total penggunaan).")

    st.divider()

    # CLUSTERING
    st.subheader("Clustering Penggunaan Sepeda Berdasarkan Monetary")
    
    rfm['UsageCluster'] = pd.qcut(rfm['Monetary'], q=3, labels=['Low Usage', 'Medium Usage', 'High Usage'])
    st.dataframe(rfm)
    
    st.markdown("**Insight Clustering:** Pengelompokan ini menggunakan binning pada nilai Monetary untuk mengidentifikasi musim dengan tingkat penggunaan rendah, sedang, dan tinggi.")

st.divider()

# CONCLUSION
st.subheader("Kesimpulan Analisis")
st.markdown(
    "- **Pengaruh Suhu:** Suhu yang nyaman mendorong lebih banyak orang untuk menyewa sepeda, sehingga strategi pemasaran dapat difokuskan pada musim panas dan hari-hari yang lebih hangat.\n"
    "- **Pola Waktu:** Pemahaman tentang pola penyewaan berdasarkan waktu membantu dalam perencanaan operasional dan pengelolaan armada sepeda, terutama untuk menghadapi jam sibuk.\n"
    "- **Musim dan RFM:** Musim dengan penggunaan rendah berpotensi menjadi target promosi atau penyesuaian layanan."
)

st.caption("Dashboard dideploy menggunakan Streamlit Cloud.")