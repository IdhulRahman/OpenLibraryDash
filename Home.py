import streamlit as st
from PIL import Image

# Set up the page
st.set_page_config(page_title="Perpustakaan Online", layout="wide")

# Define a function to display the library home page
def show_home_page():
    st.title("Selamat Datang di Perpustakaan Online 📚")
    
    st.markdown("""
        <style>
        .welcome-message {
            font-size: 1.2em;
            background-color: #f9f9f9;
            padding: 10px;
            border-radius: 5px;
        }
        .content {
            display: flex;
            flex-direction: row;
            justify-content: space-between;
        }
        .left-col, .right-col {
            width: 48%;
        }
        .image-container {
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="welcome-message">
        Selamat datang di perpustakaan online! Di sini, Anda dapat mencari buku, 
        melihat koleksi terbaru, dan mendapatkan informasi tentang buku-buku yang tersedia.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        ## Temukan Koleksi Kami
        Jelajahi berbagai koleksi buku yang tersedia di perpustakaan kami. Anda dapat mencari buku berdasarkan judul, pengarang, atau kategori. Kami juga menyediakan koleksi terbaru yang selalu diperbarui setiap bulan.
        
        - **Buku Terbaru**: Koleksi buku terbaru yang baru saja tiba di perpustakaan kami.
        - **Kategori**: Cari buku berdasarkan kategori yang Anda minati.
        - **Pengarang Terkenal**: Temukan buku dari pengarang terkenal di seluruh dunia.
        
        Jangan lupa untuk memeriksa **tren peminjaman** dan **jam tersibuk** di perpustakaan kami!
        """)

    with col2:
        st.image("Library.jpg", caption="OpenLibraryDash", use_column_width=True)

    st.markdown("---")

    with st.container():
        st.markdown("### Statistik Perpustakaan")
        
        col3, col4 = st.columns(2)

        with col3:
            st.metric(label="Jumlah Pengunjung", value="5,234", delta="24%")
            st.metric(label="Buku Dipinjam", value="1,932", delta="12%")

        with col4:
            st.metric(label="Buku Tersedia", value="12,456", delta="5%")
            st.metric(label="Anggota Baru", value="123", delta="8%")

    st.markdown("---")

    st.markdown("""
    ### Temukan Lebih Banyak:
    - [Lihat Tren Peminjaman dan Hal Data Menarik](Data_Visualisation)
    - [Gunakan ChatLib Untuk Membantu Anda Berkeliling](ChatBot)
    """)

if __name__ == "__main__":
    show_home_page()
