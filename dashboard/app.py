import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
@st.cache_data
def load_data():
    day_df = pd.read_csv('./data/day.csv')
    hour_df = pd.read_csv('./data/hour.csv')
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    return day_df, hour_df

day_df, hour_df = load_data()

# Sidebar for filters
st.sidebar.header('Filters')
season = st.sidebar.selectbox('Select Season', ['All'] + list(day_df['season'].unique()))
hour_filter = st.sidebar.slider('Select Hour Range', 0, 23, (0, 23))
demand_filter = st.sidebar.selectbox('Select Demand Cluster', ['All', 'High Demand', 'Medium Demand', 'Low Demand'])

# Filter data
if season != 'All':
    day_df = day_df[day_df['season'] == season]
    hour_df = hour_df[hour_df['season'] == season]
hour_df = hour_df[(hour_df['hr'] >= hour_filter[0]) & (hour_df['hr'] <= hour_filter[1])]

# Apply clustering for filtering
day_df['temp_bin'] = pd.cut(day_df['temp'], bins=3, labels=['Low Temp', 'Med Temp', 'High Temp'])
day_df['hum_bin'] = pd.cut(day_df['hum'], bins=3, labels=['Low Hum', 'Med Hum', 'High Hum'])
day_df['wind_bin'] = pd.cut(day_df['windspeed'], bins=3, labels=['Low Wind', 'Med Wind', 'High Wind'])

def demand_cluster(row):
    if row['temp_bin'] == 'High Temp' and row['hum_bin'] in ['Low Hum', 'Med Hum'] and row['wind_bin'] == 'Low Wind':
        return 'High Demand'
    elif row['temp_bin'] == 'Med Temp' and row['wind_bin'] != 'High Wind':
        return 'Medium Demand'
    else:
        return 'Low Demand'

day_df['demand'] = day_df.apply(demand_cluster, axis=1)
if demand_filter != 'All':
    day_df = day_df[day_df['demand'] == demand_filter]

# Dashboard Title
st.title('Bike Sharing Dashboard')

# Key Metrics
st.subheader('Key Metrics')
col1, col2 = st.columns(2)
col1.metric('Average Daily Rentals', int(day_df['cnt'].mean()))
col2.metric('Total Rentals', day_df['cnt'].sum())

# Visualizations
st.subheader('Hourly Rentals Pattern')
fig1, ax1 = plt.subplots()
sns.lineplot(x='hr', y='cnt', data=hour_df, hue='workingday', ci=None, ax=ax1)
st.pyplot(fig1)

st.subheader('Rentals by Weekday')
fig2, ax2 = plt.subplots()
sns.barplot(x='weekday', y='cnt', data=day_df, ax=ax2)
st.pyplot(fig2)

st.subheader('Weather Impact: Rentals vs Temperature')
fig3, ax3 = plt.subplots()
sns.scatterplot(x='temp', y='cnt', data=day_df, ax=ax3)
st.pyplot(fig3)

# Demand Cluster
st.subheader('Demand Clusters (Clustering Manual)')
cluster_group = day_df.groupby('demand')['cnt'].mean()
fig4, ax4 = plt.subplots()
sns.barplot(x=cluster_group.index, y=cluster_group.values, ax=ax4)
st.pyplot(fig4)

# RFM Analysis
st.subheader('RFM Analysis (Adaptasi untuk Hari)')
day_df = day_df.sort_values('dteday')
max_date = day_df['dteday'].max()
day_df['recency'] = (max_date - day_df['dteday']).dt.days
high_rental_threshold = day_df['cnt'].quantile(0.75)
day_df['is_high_rental'] = day_df['cnt'] > high_rental_threshold
rfm_df = day_df.groupby('yr').agg({
    'recency': 'min',
    'is_high_rental': 'sum',
    'cnt': 'sum'
}).reset_index()
rfm_df.columns = ['year', 'recency', 'frequency', 'monetary']
rfm_df['r_score'] = pd.qcut(rfm_df['recency'].rank(method='first'), 4, labels=[4,3,2,1])
rfm_df['f_score'] = pd.qcut(rfm_df['frequency'].rank(method='first'), 4, labels=[1,2,3,4])
rfm_df['m_score'] = pd.qcut(rfm_df['monetary'].rank(method='first'), 4, labels=[1,2,3,4])
rfm_df['rfm_score'] = rfm_df['r_score'].astype(str) + rfm_df['f_score'].astype(str) + rfm_df['m_score'].astype(str)
st.dataframe(rfm_df)

# Raw Data View
if st.checkbox('Show Raw Data'):
    st.subheader('Day Data')
    st.dataframe(day_df.head())
    st.subheader('Hour Data')
    st.dataframe(hour_df.head())