import streamlit as st
import pandas as pd
from datetime import datetime
import logo  # Pastikan file logo.py tersedia
from io import BytesIO

# 1. KONFIGURASI HALAMAN (Wajib paling atas)
st.set_page_config(page_title="SPD Ngada", layout="wide", initial_sidebar_state="expanded")

# --- INISIALISASI SESSION STATE ---
if 'jml' not in st.session_state: st.session_state.jml = 1

# 2. CSS KHUSUS (Hanya untuk Kertas, Tidak mengganggu Sidebar)
st.markdown("""
<style>
    /* Mengatur background area utama saja */
    [data-testid="stMainViewContainer"] {
        background-color: #525659 !important;
    }
    
    /* Container Kertas */
    .main-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        padding: 20px 0;
    }

    /* KERTAS LEGAL */
    .kertas {
        background-color: white !important;
        width: 215.9mm;
        height: 330mm;
        padding: 15mm 20mm;
        margin-bottom: 25px;
        color: black !important;
        font-family: Arial, sans-serif;
        box-sizing: border-box;
        box-shadow: 0 0 15px rgba(0,0,0,0.5);
        font-size: 10.5pt;
        position: relative;
    }

    /* Tabel Kop */
    .kop-table { width: 100%; border-bottom: 3.5pt solid black !important; margin-bottom: 10px; border-collapse: collapse; }
    .kop-teks { text-align: center; line-height: 1.1; }
    .visum-table { width: 100%; border-collapse: collapse; }
    .visum-table td { padding: 2px 0; vertical-align: top; color: black !important; }
    
    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }

    /* CSS Saat Cetak */
    @media print {
        header, [data-testid="stSidebar"], .stButton, .no-print { display: none !important; }
        [data-testid="stMainViewContainer"] { background-color: white !important; }
        .main-container { padding: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; }
        @page { size: legal portrait; margin: 0; }
    }
</style>
""", unsafe_allow_html=True)

# 3. NAVIGASI INPUT (DI SIDEBAR)
# Kita pastikan input ini muncul duluan
with st.sidebar:
    st.header("📋 PANEL INPUT")
    
    # --- INPUT DATA PEGAWAI ---
    st.subheader("👤 PEGAWAI")
    col_t, col_h = st.columns(2)
    if col_t.button("➕ Tambah"): st.session_state.jml += 1
    if col_h.button("➖ Hapus") and st.session_state.jml > 1: st.session_state.jml -= 1
    
    data_pegawai = []
    for i in range(st.session_state.jml):
        with st.expander(f"Pegawai {i+1}", expanded=(i==0)):
            p = {
                "nama": st.text_input("Nama", key=f"nm_{i}"),
                "nip": st.text_input("NIP", key=f"np_{i}"),
                "jab": st.text_input("Jabatan", key=f"jb_{i}")
            }
            data_pegawai.append(p)

    # --- INPUT DETAIL SURAT ---
    with st.expander("📄 DETAIL SURAT"):
        no_spt = st.text_input("No SPT", "094/Prokopim/557/02/2026")
        maksud = st.text_area("Maksud", "Dampingi Bupati...")
        tujuan = st.text_input("Tujuan", "Riung")
        lama = st.text_input("Lama Hari", "1 (Satu) hari")
        anggaran = st.text_area("Dasar", "DPA Bagian Perekonomian 2026")

    # --- INPUT PENANDA TANGAN ---
    with st.expander("🖋️ PENANDA TANGAN"):
        ttd_label = st.selectbox("Status", ["An. BUPATI NGADA", "BUPATI NGADA"])
        pjb_nama = st.text_input("Nama Pejabat", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
        jab_ttd = st.text_input("Jabatan", "Pj. Sekretaris Daerah")
        ub = st.text_input("Ub.", "Asisten Perekonomian")
        nip_ttd = st.text_input("NIP", "19710328 199203 1 011")

    if st.button("🖨️ CETAK SEKARANG"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

# 4. PROSES RENDER KERTAS (DI HALAMAN UTAMA)
# Kop Surat
kop_html = f'''
<table class="kop-table">
    <tr>
        <td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td>
        <td class="kop-teks">
            <h3>PEMERINTAH KABUPATEN NGADA</h3>
            <h2>SEKRETARIAT DAERAH</h2>
            <p>BAJAWA</p>
        </td>
        <td width="15%"></td>
    </tr>
</table>'''

# Isi Baris Pegawai
pegawai_rows = ""
for i, p in enumerate(data_pegawai):
    pegawai_rows += f'''
    <tr>
        <td width="12%">Kepada</td><td width="5%">:</td><td width="5%">{i+1}.</td><td width="20%">Nama</td><td>: <b>{p['nama']}</b></td>
    </tr>
    <tr><td colspan="3"></td><td>NIP</td><td>: {p['nip']}</td></tr>
    '''

# Tanda Tangan Logic
jab_final = f"{jab_ttd},<br>" if ttd_label == "An. BUPATI NGADA" else ""
ub_final = f"Ub. {ub},<br>" if (ub and ttd_label == "An. BUPATI NGADA") else ""

ttd_html = f'''
<div style="margin-left:55%; margin-top:20px; text-align:center; line-height:1.2;">
    <b>{ttd_label}</b><br>{jab_final}{ub_final}
    <div style="height:70px;"></div>
    <b><u>{pjb_nama}</u></b><br>NIP. {nip_ttd}
</div>'''

# Gabungkan Semua ke HTML Final
html_final = f'''
<div class="main-container">
    <div class="kertas">
        {kop_html}
        <div class="text-center"><h3 class="underline">SURAT PERINTAH TUGAS</h3><p>Nomor: {no_spt}</p></div>
        <table class="visum-table"><tr><td width="12%">Dasar</td><td width="5%">:</td><td>{anggaran}</td></tr></table>
        <p class="text-center text-bold" style="margin:10px 0;">MEMERINTAHKAN:</p>
        <table class="visum-table">{pegawai_rows}</table>
        <table class="visum-table" style="margin-top:20px;"><tr><td width="12%">Untuk</td><td width="5%">:</td><td>{maksud} ke {tujuan} selama {lama}.</td></tr></table>
        {ttd_html}
    </div>
</div>
'''

# TAMPILKAN
st.markdown(html_final, unsafe_allow_html=True)
