import streamlit as st
import pandas as pd
from datetime import datetime
import logo  # Memanggil logo.py di repository kamu

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Ngada Pro - Register Mode", layout="wide")

# 2. INISIALISASI DATABASE (Session State)
# Di masa depan, bagian ini bisa dihubungkan ke Google Sheets/st.connection
if 'db_register' not in st.session_state:
    st.session_state.db_register = []

# CSS UNTUK PRESISI CETAK (Sama seperti sebelumnya)
st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    .main-container { display: flex; flex-direction: column; align-items: center; width: 100%; padding: 5px 0; }
    .kertas { 
        background-color: white !important; width: 215.9mm; height: 330mm; 
        padding: 12mm 15mm; margin-bottom: 20px; color: black !important; 
        font-family: Arial, sans-serif; box-sizing: border-box; box-shadow: 0 0 20px rgba(0,0,0,0.8);
        font-size: 10pt; page-break-after: always; overflow: hidden;
    }
    .kertas-landscape { width: 330mm !important; height: 215.9mm !important; padding: 15mm !important; }
    .tabel-border { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; }
    .tabel-border th, .tabel-border td { border: 1pt solid black !important; padding: 5px; color: black !important; }
    @media print {
        [data-testid="stSidebar"], .stButton, .no-print { display: none !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; }
        @page { size: legal landscape; margin: 0; }
    }
</style>
""", unsafe_allow_html=True)

# 3. SIDEBAR PANEL KONTROL
with st.sidebar:
    st.header("📋 PANEL KONTROL")
    menu = st.radio("Pilih Menu", ["Input Data & Cetak", "Lihat & Kelola Register"])
    
    if menu == "Input Data & Cetak":
        with st.expander("👤 DATA PEGAWAI", expanded=True):
            if 'jml' not in st.session_state: st.session_state.jml = 1
            c1, c2 = st.columns(2)
            if c1.button("➕ Tambah"): st.session_state.jml += 1
            if c2.button("➖ Hapus") and st.session_state.jml > 1: st.session_state.jml -= 1
            daftar = []
            for i in range(st.session_state.jml):
                n = st.text_input(f"Nama P-{i+1}", f"Nama {i+1}", key=f"n{i}")
                ni = st.text_input(f"NIP P-{i+1}", "19XXXXXXXXXXXXXX", key=f"nip{i}")
                s = st.text_input(f"No SPD P-{i+1}", f"530 /02/2026", key=f"spd{i}")
                daftar.append({"nama": n, "nip": ni, "spd": s})

        with st.expander("📄 DATA UTAMA"):
            no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
            tujuan = st.text_input("Tujuan", "Kecamatan Riung")
            tgl_bkt = st.date_input("Tanggal Berangkat", datetime.now())
            tgl_kbl = st.date_input("Tanggal Pulang", datetime.now())
            lama = st.text_input("Lama Hari", "1 (Satu) hari")
            ket = st.text_input("Keterangan", "-")

        if st.button("🖨️ PROSES CETAK & SIMPAN"):
            # SIMPAN KE DATABASE REGISTER
            for p in daftar:
                data_baru = {
                    "Tanggal Input": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Nama": p['nama'],
                    "Nomor SPT": no_spt,
                    "Nomor SPD": p['spd'],
                    "Tujuan": tujuan,
                    "Tgl Berangkat": tgl_bkt.strftime("%d/%m/%Y"),
                    "Tgl Pulang": tgl_kbl.strftime("%d/%m/%Y"),
                    "Lama": lama,
                    "Keterangan": ket
                }
                st.session_state.db_register.append(data_baru)
            
            st.success("Data disimpan ke Register!")
            st.components.v1.html("<script>setTimeout(function(){ window.parent.print(); }, 1000);</script>", height=0)

# 4. HALAMAN KELOLA REGISTER
if menu == "Lihat & Kelola Register":
    st.title("📂 Register Riwayat SPT/SPD")
    
    if not st.session_state.db_register:
        st.warning("Belum ada data yang disimpan.")
    else:
        # Tampilkan Tabel dalam bentuk DataFrame agar mudah dilihat
        df = pd.DataFrame(st.session_state.db_register)
        
        # Opsi Hapus Data
        st.subheader("Kelola Data")
        index_hapus = st.number_input("Masukkan nomor baris yang ingin dihapus (mulai dari 0)", min_value=0, max_value=len(df)-1, step=1)
        if st.button("🗑️ Hapus Baris Terpilih"):
            st.session_state.db_register.pop(index_hapus)
            st.rerun()

        if st.button("🧹 Kosongkan Semua Riwayat"):
            st.session_state.db_register = []
            st.rerun()

        # TAMPILAN FORMAT CETAK REGISTER (LANDSCAPE)
        st.markdown("---")
        st.subheader("Pratinjau Cetak Register")
        
        html_reg = f'''
        <div class="kertas-landscape" style="background:white; color:black; padding:20px;">
            <h3 class="text-center text-bold">REGISTER SURAT PERJALANAN DINAS</h3>
            <br>
            <table class="tabel-border" style="width:100%;">
                <thead>
                    <tr style="background:#f2f2f2;">
                        <th>No</th>
                        <th>Nama</th>
                        <th>Nomor SPT</th>
                        <th>Nomor SPD</th>
                        <th>Tgl Berangkat</th>
                        <th>Tgl Pulang</th>
                        <th>Lama</th>
                        <th>Keterangan</th>
                    </tr>
                </thead>
                <tbody>
        '''
        for idx, row in df.iterrows():
            html_reg += f'''
                <tr>
                    <td class="text-center">{idx + 1}</td>
                    <td>{row['Nama']}</td>
                    <td>{row['Nomor SPT']}</td>
                    <td>{row['Nomor SPD']}</td>
                    <td>{row['Tgl Berangkat']}</td>
                    <td>{row['Tgl Pulang']}</td>
                    <td>{row['Lama']}</td>
                    <td>{row['Keterangan']}</td>
                </tr>
            '''
        html_reg += "</tbody></table></div>"
        st.markdown(html_reg, unsafe_allow_html=True)
        
        if st.button("🖨️ Cetak Tabel Register"):
             st.components.v1.html("<script>window.parent.print();</script>", height=0)

# --- LOGIKA TAMPILAN SURAT (Sama seperti kode sebelumnya) ---
if menu == "Input Data & Cetak":
    st.info("Silakan isi data di sidebar lalu klik tombol cetak.")
