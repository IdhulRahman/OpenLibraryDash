import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import os
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")  # Set wide layout
st.title('Dashboard Data Oplib')

FOLDER_PATH = "Data"

@st.cache_data
def load_data(file):
    file_path = os.path.join(FOLDER_PATH, file)
    data = pd.read_csv(file_path)
    if file == "data riset peminjaman(2018-2024).csv":
        data = data.drop(columns=['author', 'member_id'], errors='ignore')
    elif file == "Akses File (2024).csv":
        data[['date', 'time']] = data['created_at'].str.split(' ', expand=True)
        data = data.drop(columns=['created_at', 'name', 'member_id'], errors='ignore')
    elif file == "data riset pengunjung(2018-2024).csv":
        data[['date', 'time']] = data['attended_at'].str.split(' ', expand=True)
        data = data.drop(columns=['attended_at', 'member_id'], errors='ignore')
    return data

def visualize_pengunjung_tren(data):
    data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
    data['month'] = data['date'].dt.month
    data['year'] = data['date'].dt.year
    Tren_pengunjung = data.groupby(['year', 'month']).size().reset_index(name='Jumlah Pengunjung')
    Tren_pengunjung['year_month'] = Tren_pengunjung['year'].astype(str) + '-' + Tren_pengunjung['month'].astype(str).str.zfill(2)
    fig = px.line(Tren_pengunjung, x='year_month', y='Jumlah Pengunjung', title='Tren Pengunjung Oplib Tahun ke Tahun', markers=True)
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

def visualize_pengunjung_jam(data):
    data['date'] = pd.to_datetime(data['date'])
    data['time'] = pd.to_datetime(data['time'], format='%H:%M:%S').dt.time
    data['day_name'] = data['date'].dt.day_name()
    data['hour'] = pd.to_datetime(data['time'].apply(lambda x: x.strftime('%H:%M:%S')), format='%H:%M:%S').dt.hour
    akses_jam = data.groupby(['day_name', 'hour']).size().reset_index(name='count')
    waktu_sibuk = akses_jam.loc[akses_jam.groupby('day_name')['count'].idxmax()]
    fig = go.Figure()
    for day in waktu_sibuk['day_name'].unique():
        day_data = akses_jam[akses_jam['day_name'] == day]
        fig.add_trace(go.Scatter(
            x=day_data['hour'],
            y=day_data['count'],
            mode='lines+markers',
            name=day
        ))
    fig.update_layout(
        xaxis_title='Jam',
        yaxis_title='Jumlah Pengunjung',
        title='Jumlah Pengunjung Berdasarkan Jam',
        xaxis=dict(
            tickvals=list(range(24)),
            ticktext=[f'{i:02d}:00' for i in range(24)]
        ),
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    st.subheader('Jam Tersibuk untuk Setiap Hari:')
    st.write(waktu_sibuk[['day_name', 'hour', 'count']])

def visualize_peminjaman_tren(data):
    data['rent_date'] = pd.to_datetime(data['rent_date'], format='%Y-%m-%d')
    data['month'] = data['rent_date'].dt.month
    data['year'] = data['rent_date'].dt.year
    Tren_Pinjaman = data.groupby(['year', 'month']).size().reset_index(name='Jumlah Peminjaman')
    Tren_Pinjaman['year_month'] = Tren_Pinjaman['year'].astype(str) + '-' + Tren_Pinjaman['month'].astype(str).str.zfill(2)
    fig = px.line(Tren_Pinjaman, x='year_month', y='Jumlah Peminjaman', title='Tren Peminjaman Tahun ke Tahun', markers=True)
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

def visualize_fav_books(data):
    FavBooks = data.groupby(['nama_prodi', 'title']).size().reset_index(name='count')
    Buku = FavBooks.loc[FavBooks.groupby('nama_prodi')['count'].idxmax()].reset_index(drop=True)
    selected_departments = st.multiselect('Pilih Jurusan:', options=Buku['nama_prodi'].unique(), default=Buku['nama_prodi'].unique())
    filtered_data = Buku[Buku['nama_prodi'].isin(selected_departments)]
    
    def plot_pivot(dataframe, title):
        pivot_data = dataframe.pivot_table(values='count', index='title', columns='nama_prodi', fill_value=0)
        fig, ax = plt.subplots(figsize=(10, 7))
        pivot_data.plot(kind='barh', stacked=True, ax=ax)
        ax.set_xlabel('Jumlah Buku')
        ax.set_ylabel('Judul Buku')
        ax.set_title(title)
        ax.legend(title='Jurusan', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True)
        plt.tight_layout()
        st.pyplot(fig)
    
    if not filtered_data.empty:
        plot_pivot(filtered_data, 'Judul Buku Yang Paling Sering Dipinjam')
    else:
        st.write("Data Tidak Tersedia")

def visualize_akses_tren(data):
    data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
    data['month'] = data['date'].dt.month
    data['year'] = data['date'].dt.year
    Tren_Akses_File = data.groupby(['year', 'month']).size().reset_index(name='Jumlah Pengunjung')
    Tren_Akses_File['year_month'] = Tren_Akses_File['year'].astype(str) + '-' + Tren_Akses_File['month'].astype(str).str.zfill(2)
    fig = px.line(Tren_Akses_File, x='year_month', y='Jumlah Pengunjung', title='Tren Akses File', markers=True)
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

def visualize_akses_jam(data):
    data['date'] = pd.to_datetime(data['date'])
    data['time'] = pd.to_datetime(data['time'], format='%H:%M:%S').dt.time
    data['day_name'] = data['date'].dt.day_name()
    data['hour'] = pd.to_datetime(data['time'].apply(lambda x: x.strftime('%H:%M:%S')), format='%H:%M:%S').dt.hour
    akses_jam = data.groupby(['day_name', 'hour']).size().reset_index(name='count')
    waktu_sibuk = akses_jam.loc[akses_jam.groupby('day_name')['count'].idxmax()]
    fig = go.Figure()
    for day in waktu_sibuk['day_name'].unique():
        day_data = akses_jam[akses_jam['day_name'] == day]
        fig.add_trace(go.Scatter(
            x=day_data['hour'],
            y=day_data['count'],
            mode='lines+markers',
            name=day
        ))
    fig.update_layout(
        xaxis_title='Waktu',
        yaxis_title='Jumlah Akses',
        title='Jam Tersibuk Setiap Hari',
        xaxis=dict(
            tickvals=list(range(24)),
            ticktext=[f'{i:02d}:00' for i in range(24)]
        ),
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    st.subheader('Jam Tersibuk untuk Setiap Hari:')
    st.write(waktu_sibuk[['day_name', 'hour', 'count']])

with st.sidebar:
    upload_file = st.selectbox(
        "Select Data:",
        [
            "Akses File (2024).csv",
            "data riset peminjaman(2018-2024).csv",
            "data riset pengunjung(2018-2024).csv"
        ]
    )

df = load_data(upload_file).dropna().reset_index(drop=True)
df.index += 1

with st.expander("Data Overview"):
    st.dataframe(df)

if upload_file == "data riset pengunjung(2018-2024).csv":
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("Visualisasi Tren"):
            visualize_pengunjung_tren(df)
    with col2:
        with st.expander("Visualisasi Rerata Jumlah Pengunjung (Jam)"):
            visualize_pengunjung_jam(df)

elif upload_file == "data riset peminjaman(2018-2024).csv":
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("Visualisasi Tren"):
            visualize_peminjaman_tren(df)
    with col2:
        with st.expander("Buku Favorit Setiap Jurusan"):
            visualize_fav_books(df)

elif upload_file == "Akses File (2024).csv":
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("Visualisasi Tren"):
            visualize_akses_tren(df)
    with col2:
        with st.expander("Jumlah Pengunjung Disetiap Jam"):
            visualize_akses_jam(df)
