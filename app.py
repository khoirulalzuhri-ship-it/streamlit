import streamlit as st

class KategoriNode:
    def __init__(self, nama_kategori):
        self.nama = nama_kategori
        self.sub_kategori = []

    def tambah_sub(self, node_kategori):
        self.sub_kategori.append(node_kategori)

    def dapatkan_tree_string(self, level=0):
        indentasi = "    " * level
        simbol = "↳ " if level > 0 else "📦 "
        print(f"{indentasi}{simbol}{self.nama}")
        
        for sub in self.sub_kategori:
            sub.dapatkan_tree_string(level + 1)
        return hasil

    def cari_node(self, target_nama):
        # Mencari node spesifik untuk menambahkan anak di bawahnya
        if self.nama.lower() == target_nama.lower():
            return self
            
        for sub in self.sub_kategori:
            hasil = sub.cari_node(target_nama)
            if hasil:
                return hasil
                
        return None

    def cari_jalur(self, target, path=""):
        # Mencari jalur lengkap (breadcrumb) seperti studi kasus sebelumnya
        jalur_saat_ini = path + " > " + self.nama if path else self.nama
        
        if self.nama.lower() == target.lower():
            return jalur_saat_ini
            
        for sub in self.sub_kategori:
            hasil = sub.cari_jalur(target, jalur_saat_ini)
            if hasil:
                return hasil
                
        return None

# ==========================================
# PROGRAM UTAMA (STREAMLIT UI)
# ==========================================
st.set_page_config(page_title="Struktur kategori", page_icon="📦")

st.title(" Membuat Struktur Kategori ")
st.write(" Applikasi interaktif untuk mensimulasikan struktur data dengan tree.")

# inisialisasi session state untuk menyimpan struktur tree agar tidak hilang saat halaman di refresh

if 'root' not in st.session_state:
    st.session_state.root = None

#jika root belum dibuat, tampilkan form pembuatan root
if st.session_state.root is None:
    st.info("Sistem belum memiliki kategori utama. Silahkan buat terlebih dahulu.")
    nama_root = st.text_input("Masukkan nama kategori utama (root): ", value="Toko Saya")

    if st.button("Buat kategori utama", type="primary"):
        st.session_state.root = KategoriNode(nama_root)
        st.rerun() #refresh halaman

#jika root sudah ada, tampilkan menu utama menggunakan tabs
else:
    root = st.session_state.root

    #mengganti menu CLI dengan sistem tab yang lebih modern
    tab1, tab2, tab3 = st.tabs(["📁Lihat Struktur", "➕Tambah Sub-Kategori", "🔍Cari Jalur"])

    #tab 1 lihat struktur
    with tab1:
        st.subheader("Struktur kategori saat ini")
        tree_teks = root.dapatkan_tree_string()
        #menggunkan st.code agar format indentasi (spasi) tetap rapi
        st.code(tree_teks, language="text")

    #
    with tab2:
        st.subheader("Tambah Cabang Baru")
        induk_nama = st.text_input ("Masukkan nama kategori induk tempat cabang ditambahkan : ")
        anak_nama = st.text_input ("Nama sub-kategori baru : ")

        if st.button("Tambah kategori"):
            if induk_nama and anak_nama:
                induk_node = root.cari_node(induk_nama)
                if induk_node:
                    induk_node.tambah_sub(KategoriNode(anak_nama))
                    st.success(f"Berhasil menambahkan {anak_nama} di bawah '{induk_node.nama}' !")
                else:
                    st.error (f"kategori {induk_nama} tidak ditemukan! Pastikan ejaannya benar.")
            else:
                st.warning("Harap isi kedua kolom di atas.")

    with tab3:
        st.subheader("Pencarian BreadCrumb")
        target_cari = st.text_input("Nama kategori yang ingin dicari jalurnya")
        
        if st.button ("Cari Jalur"):
            if target_cari:
                hasil = root.cari_jalur(target_cari)
                if hasil:
                    st.success("Ditemukan")
                    st.info(f"jalur : {hasil}")
                else:
                    st.error(f"Kategori {target_cari} tidak ditemukan dalam sistem")

#tombol reset
st.divider()
if st.button ("Reset sistem / mulai dari awal"):
    st.session_state.root = None
    st.rerun()
