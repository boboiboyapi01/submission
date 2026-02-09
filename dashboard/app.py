import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load Data
@st.cache_data
def load_data():
    try:
        day_path = './data/day.csv'
        hour_path = './data/hour.csv'
        
        day_df = pd.read_csv(day_path)
        hour_df = pd.read_csv(hour_path)
        
        day_df['dteday'] = pd.to_datetime(day_df['dteday'])
        hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
        
        return day_df, hour_df
    except FileNotFoundError as e:
        st.error(f"File tidak ditemukan: {e}. Pastikan folder 'data' berisi day.csv dan hour.csv.")
        st.stop()

day_df, hour_df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")
season = st.sidebar.selectbox("Pilih Musim (Season)", ["All"] + list(day_df["season"].unique()))
hour_range = st.sidebar.slider("Rentang Jam", 0, 23, (0, 23))
demand_filter = st.sidebar.selectbox("Tingkat Permintaan", ["All", "Permintaan Tinggi", "Permintaan Sedang", "Permintaan Rendah"])

# Apply filters
filtered_day = day_df.copy()
filtered_hour = hour_df.copy()

if season != "All":
    filtered_day = filtered_day[filtered_day["season"] == season]
    filtered_hour = filtered_hour[filtered_hour["season"] == season]

filtered_hour = filtered_hour[
    (filtered_hour["hr"] >= hour_range[0]) & (filtered_hour["hr"] <= hour_range[1])
]

# Clustering Manual (sama seperti notebook)
filtered_day["temp_bin"] = pd.cut(filtered_day["temp"], bins=3, labels=["Rendah", "Sedang", "Tinggi"])
filtered_day["hum_bin"] = pd.cut(filtered_day["hum"], bins=3, labels=["Rendah", "Sedang", "Tinggi"])
filtered_day["wind_bin"] = pd.cut(filtered_day["windspeed"], bins=3, labels=["Rendah", "Sedang", "Tinggi"])

def demand_level(row):
    if row["temp_bin"] == "Tinggi" and row["hum_bin"] != "Tinggi" and row["wind_bin"] == "Rendah":
        return "Permintaan Tinggi"
    elif row["temp_bin"] == "Sedang":
        return "Permintaan Sedang"
    else:
        return "Permintaan Rendah"

filtered_day["demand_level"] = filtered_day.apply(demand_level, axis=1)

if demand_filter != "All":
    filtered_day = filtered_day[filtered_day["demand_level"] == demand_filter]

# Dashboard Utama
st.title("Bike Sharing Dashboard (2011–2012)")

st.markdown("""
Analisis pola penyewaan sepeda berdasarkan waktu dan faktor cuaca selama periode 2011–2012.  
Dashboard ini mendukung filtering musim, jam, dan tingkat permintaan.
""")

# Key Metrics
st.subheader("Metrik Utama")
col1, col2, col3 = st.columns(3)
col1.metric("Rata-rata Penyewaan Harian", f"{int(filtered_day['cnt'].mean()):,}")
col2.metric("Total Penyewaan", f"{filtered_day['cnt'].sum():,}")
col3.metric("Jumlah Hari Tersaring", len(filtered_day))

# Visual 1: Pola per Jam (Working vs Non-Working)
st.subheader("Pola Penyewaan per Jam: Hari Kerja vs Akhir Pekan")
hourly_working = filtered_hour.groupby(["hr", "workingday"])["cnt"].mean().unstack()
hourly_working = hourly_working.rename(columns={0: "Akhir Pekan", 1: "Hari Kerja"})

fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.lineplot(data=hourly_working, linewidth=2.5, ax=ax1)
ax1.set_title("Rata-rata Penyewaan per Jam")
ax1.set_xlabel("Jam")
ax1.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig1)

st.info("Insight: Puncak penyewaan di hari kerja terjadi jam 8 pagi (~350–380 unit) dan jam 17–18 sore (~450–500 unit) → pola komuter.")

# Visual 2: Penyewaan per Hari dalam Seminggu
st.subheader("Rata-rata Penyewaan per Hari dalam Seminggu")
weekday_map = {0: "Minggu", 1: "Senin", 2: "Selasa", 3: "Rabu", 4: "Kamis", 5: "Jumat", 6: "Sabtu"}
weekday_avg = filtered_day.groupby("weekday")["cnt"].mean().reset_index()
weekday_avg["weekday"] = weekday_avg["weekday"].map(weekday_map)

fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.barplot(x="weekday", y="cnt", data=weekday_avg, ax=ax2, palette="viridis")
ax2.set_title("Rata-rata Penyewaan per Hari")
ax2.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig2)

# Visual 3: Pengaruh Suhu
st.subheader("Pengaruh Suhu terhadap Penyewaan")
fig3, ax3 = plt.subplots(figsize=(8, 5))
sns.scatterplot(x="temp", y="cnt", data=filtered_day, alpha=0.6, ax=ax3)
ax3.set_title("Penyewaan vs Suhu (normalized)")
ax3.set_xlabel("Suhu (normalized)")
ax3.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig3)

st.info("Insight: Suhu memiliki korelasi positif terkuat (~0.63). Penyewaan meningkat signifikan saat suhu >0.6 (sekitar 20–25°C+).")

# Demand Cluster
st.subheader("Tingkat Permintaan (Clustering Manual)")
cluster_group = filtered_day.groupby("demand_level")["cnt"].mean().reset_index()

fig4, ax4 = plt.subplots(figsize=(7, 5))
sns.barplot(x="demand_level", y="cnt", data=cluster_group, ax=ax4, palette="Set2")
ax4.set_title("Rata-rata Penyewaan per Tingkat Permintaan")
ax4.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig4)

# RFM Adaptasi
st.subheader("RFM Adaptasi (Segmentasi Tahun Berdasarkan Demand)")
filtered_day = filtered_day.sort_values("dteday")
max_date = filtered_day["dteday"].max()
filtered_day["recency"] = (max_date - filtered_day["dteday"]).dt.days

high_threshold = filtered_day["cnt"].quantile(0.75)
filtered_day["is_high"] = filtered_day["cnt"] > high_threshold

rfm = filtered_day.groupby("yr").agg({
    "recency": "min",
    "is_high": "sum",
    "cnt": "sum"
}).reset_index()
rfm.columns = ["Tahun", "Recency (hari terakhir high)", "Frequency (hari high)", "Monetary (total penyewaan)"]

rfm["r_score"] = pd.qcut(rfm["Recency (hari terakhir high)"].rank(method="first"), 2, labels=[2, 1])
rfm["f_score"] = pd.qcut(rfm["Frequency (hari high)"].rank(method="first"), 2, labels=[1, 2])
rfm["m_score"] = pd.qcut(rfm["Monetary (total penyewaan)"].rank(method="first"), 2, labels=[1, 2])
rfm["RFM Score"] = rfm["r_score"].astype(str) + rfm["f_score"].astype(str) + rfm["m_score"].astype(str)

st.dataframe(rfm.style.highlight_max(color="#d4edda"))

# Raw Data
if st.checkbox("Tampilkan Data Mentah"):
    st.subheader("Data Harian (Day)")
    st.dataframe(filtered_day.head(10))
    st.subheader("Data Per Jam (Hour)")
    st.dataframe(filtered_hour.head(10))

st.markdown("---")
st.caption("Dashboard dibuat untuk proyek Analisis Data Bike Sharing – Dicoding 2026")