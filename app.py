import streamlit as st
import pandas as pd
from datetime import datetime
import logo  # Memastikan file logo.py ada di folder yang sama
from io import BytesIO

# 1. KONFIGURASI DASAR
st.set_page_config(page_title="Sistem SPD Ngada Pro", layout="wide")

# --- INISIALISASI SESSION STATE (Kunci agar inputan tidak hilang) ---
if 'jml_pegawai' not in st.session_state: st.session_state.jml_pegawai = 1
if 'arsip_register' not in st.session_state: st.session_state.arsip_register = []

# 2. CSS KERTAS PRESISI (LEGAL)
st.markdown("""
<style>
    header, footer, .stDeployButton { visibility: hidden; display: none !important; }
    .stApp { background-color: #525659 !important; }
    
    .main-container { 
        display: flex; flex-direction: column; align-items: center; 
        width: 100%; padding: 20px 0; 
    }

    .kertas { 
        background-color: white !important; 
        width: 215.9mm; height: 330mm; 
        padding: 15mm 20mm; margin-bottom: 25px; 
        color: black !important; font-family: Arial, sans-serif; 
        box-sizing: border-box; box-shadow: 0 0 20px rgba(0,0,0,0.5);
        font-size: 10.5pt; position: relative; flex-shrink: 0;
    }

    /* Tabel Kop */
    .kop-table { width: 100%; border-bottom: 3.5pt solid black !important; margin-bottom: 10px; }
    .kop-teks { text-align: center; line-height: 1.1; }
    .kop-teks h3, .kop-teks h2 { margin: 0; padding: 2px 0; }

    /* Tabel Isi */
    .tabel-border { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; }
    .tabel-border td { border: 1pt solid black !important; padding: 5px 8px; vertical-align: top; color: black !important; font-size: 9.5pt; }
    .visum-table { width: 100%; border-collapse: collapse; margin: 0; }
    .visum-table td { padding: 2px 0; vertical-align: top; font-size: 10pt; color: black !important; }

    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }

    @media print {
        @page { size: legal portrait; margin: 0; }
        .stApp { background-color: white !important; }
        [data-testid="stSidebar"], .stButton, .no-print { display: none !important; }
        .main-container { padding: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; }
    }
</style>
""", unsafe_allow_html=True)

# 3. NAVIGASI INPUT (SIDEBAR)
with st.sidebar:
    st.header("📋 NAVIGASI INPUT")
    tab_menu = st.radio("Menu Utama", ["Input & Cetak", "Kelola Register"])
    
    if tab_menu == "Input & Cetak":
        wilayah = st.selectbox("Jenis Wilayah", ["Dalam Daerah", "Luar Daerah"])
        docs = st.multiselect("Pilih Dokumen", ["SPT", "SPD Depan", "SPD Belakang"], default=["SPT", "SPD Depan"])
        
        # --- INPUT NAMA YANG BERTUGAS ---
        st.subheader("👤 PEGAWAI BERTUGAS")
        c1, c2 = st.columns(2)
        if c1.button("➕ Tambah"): st.session_state.jml_pegawai += 1
        if c2.button("➖ Hapus") and st.session_state.jml_pegawai > 1: st.session_state.jml_pegawai -= 1
        
        daftar_petugas = []
        for i in range(st.session_state.jml_pegawai):
            with st.expander(f"Data Pegawai {i+1}", expanded=(i==0)):
                p = {
                    "nama": st.text_input("Nama Lengkap", key=f"n_{i}"),
                    "nip": st.text_input("NIP", key=f"nip_{i}"),
                    "gol": st.text_input("Pangkat / Gol", "III/a", key=f"g_{i}"),
                    "jab": st.text_input("Jabatan", key=f"j_{i}"),
                    "spd": st.text_input("No SPD", f"530 /02/2026", key=f"s_{i}"),
                    "lembar": st.text_input("Lembar Ke", "I", key=f"l_{i}")
                }
                daftar_petugas.append(p)

        # --- INPUT DATA PERJALANAN ---
        with st.expander("📄 DATA PERJALANAN", expanded=False):
            no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
            kode_spd = st.text_input("Kode No SPD", "094/Prokopim")
            maksud = st.text_area("Maksud Perjalanan", "Dalam rangka...")
            tujuan = st.text_input("Tujuan", "Riung")
            tgl_bkt = st.text_input("Tgl Berangkat", "17 Maret 2026")
            tgl_kbl = st.text_input("Tgl Kembali", "18 Maret 2026")
            lama = st.text_input("Lama Hari", "2 (Dua) hari")
            anggaran = st.text_area("Dasar Anggaran", "DPA Bagian Perekonomian 2026")

        # --- INPUT PENANDA TANGAN ---
        with st.expander("🖋️ PENANDA TANGAN", expanded=False):
            ttd_label = st.selectbox("Label Atas", ["An. BUPATI NGADA", "WAKIL BUPATI NGADA", "BUPATI NGADA"])
            jab_ttd = st.text_input("Jabatan Penandatangan", "Pj. Sekretaris Daerah")
            ub = st.text_input("Atas Nama (Ub.)", "Asisten Perekonomian dan Pembangunan")
            pjb_nama = st.text_input("Nama Pejabat", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
            pjb_nip = st.text_input("NIP Pejabat", "19710328 199203 1 011")
            pjb_gol = st.text_input("Golongan Pejabat", "Pembina Utama Muda, IV/c")

        if st.button("🖨️ PROSES & CETAK"):
            # Masukkan ke Register
            for p in daftar_petugas:
                st.session_state.arsip_register.append({"Nama": p['nama'], "SPT": no_spt, "Tujuan": tujuan, "Tgl": tgl_bkt})
            # Script Print
            st.components.v1.html("<script>window.parent.print();</script>", height=0)

# --- FUNGSI GENERATE TTD ---
def generate_ttd(space=70):
    # Logika tampil/sembunyi Ub. dan Jabatan tambahan
    jab_final = f"{jab_ttd},<br>" if ttd_label == "An. BUPATI NGADA" else ""
    ub_final = f"Ub. {ub},<br>" if (ub and ttd_label == "An. BUPATI NGADA") else ""
    
    return f'''
    <div style="margin-left:55%; margin-top:20px; text-align:center; line-height:1.2;">
        <b>{ttd_label}</b><br>{jab_final}{ub_final}
        <div style="height:{space}px;"></div>
        <b><u>{pjb_nama}</u></b><br>{pjb_gol}<br>NIP. {pjb_nip}
    </div>'''

# 4. AREA TAMPILAN KERTAS (UTAMA)
html_output = '<div class="main-container">'

if tab_menu == "Input & Cetak":
    # KOP PEMDA KAB. NGADA
    kop_pemda = f'''
    <table class="kop-table">
        <tr>
            <td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td>
            <td class="kop-teks">
                <h3>PEMERINTAH KABUPATEN NGADA</h3>
                <h2>SEKRETARIAT DAERAH</h2>
                <p>Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834</p>
                <p class="text-bold">BAJAWA</p>
            </td>
            <td width="15%"></td>
        </tr>
    </table>'''

    # --- RENDER SPT ---
    if "SPT" in docs:
        kop_spt = f'<div class="text-center" style="margin-bottom:15px;"><img src="data:image/png;base64,{logo.GARUDA}" width="75"><br><h2>BUPATI NGADA</h2></div>' if wilayah == "Luar Daerah" else kop_pemda
        
        petugas_list = ""
        for i, p in enumerate(daftar_petugas):
            petugas_list += f'''
            <tr><td width="12%">Kepada</td><td width="5%">:</td><td width="5%">{i+1}.</td><td width="18%">Nama</td><td>: <b>{p['nama']}</b></td></tr>
            <tr><td colspan="3"></td><td>NIP</td><td>: {p['nip']}</td></tr>
            <tr><td colspan="3"></td><td>Jabatan</td><td>: {p['jab']}</td></tr>'''

        html_output += f'''
        <div class="kertas">
            {kop_spt}
            <div class="judul-rapat"><h3 class="underline">SURAT PERINTAH TUGAS</h3><p>Nomor: {no_spt}</p></div>
            <table class="visum-table" style="margin-top:10px;"><tr><td width="12%">Dasar</td><td width="5%">:</td><td>{anggaran}</td></tr></table>
            <p class="text-center text-bold" style="margin:10px 0;">MEMERINTAHKAN:</p>
            <table class="visum-table">{petugas_list}</table>
            <table class="visum-table" style="margin-top:20px;"><tr><td width="12%">Untuk</td><td width="5%">:</td><td>{maksud} ke {tujuan} selama {lama}.</td></tr></table>
            {generate_ttd(80)}
        </div>'''

    # --- RENDER SPD (PER PEGAWAI) ---
    if "SPD Depan" in docs:
        for p in daftar_petugas:
            html_output += f'''
            <div class="kertas">
                {kop_pemda}
                <div style="margin-left:60%; font-size:9pt; line-height:1.2;">
                    Lembar ke: {p['lembar']}<br>Kode No: {kode_spd}<br>Nomor SPD: {p['spd']}
                </div>
                <div class="judul-rapat"><h3 class="underline">SURAT PERJALANAN DINAS (SPD)</h3></div>
                <table class="tabel-border" style="margin-top:10px;">
                    <tr><td width="5%" class="text-center">1</td><td width="40%">Pejabat pemberi perintah</td><td>BUPATI NGADA</td></tr>
                    <tr><td class="text-center">2</td><td>Nama pegawai diperintah</td><td><b>{p['nama']}</b></td></tr>
                    <tr><td class="text-center" rowspan="2">3</td><td>a. Pangkat dan Golongan</td><td>{p['gol']}</td></tr>
                    <tr><td>b. Jabatan / Instansi</td><td>{p['jab']}</td></tr>
                    <tr><td class="text-center">4</td><td>Maksud Perjalanan Dinas</td><td>{maksud}</td></tr>
                    <tr><td class="text-center">5</td><td>Alat angkut yang dipergunakan</td><td>Mobil Dinas</td></tr>
                    <tr><td class="text-center" rowspan="2">6</td><td>a. Tempat Berangkat</td><td>Bajawa</td></tr>
                    <tr><td>b. Tempat Tujuan</td><td>{tujuan}</td></tr>
                    <tr><td class="text-center" rowspan="3">7</td><td>a. Lamanya perjalanan dinas</td><td>{lama}</td></tr>
                    <tr><td>b. Tanggal berangkat</td><td>{tgl_bkt}</td></tr>
                    <tr><td>c. Tanggal harus kembali</td><td>{tgl_kbl}</td></tr>
                    <tr><td class="text-center">8</td><td>Pembebanan Anggaran</td><td>{anggaran}</td></tr>
                </table>
                {generate_ttd(60)}
            </div>'''

html_output += '</div>'
st.markdown(html_output, unsafe_allow_html=True)

# 5. KELOLA REGISTER
if tab_menu == "Kelola Register":
    st.sidebar.markdown("---")
    if st.session_state.arsip_register:
        st.subheader("📂 RIWAYAT INPUT")
        st.table(pd.DataFrame(st.session_state.arsip_register))
        if st.button("🗑️ Kosongkan Data"):
            st.session_state.arsip_register = []
            st.rerun()
