import streamlit as st
import pandas as pd
from datetime import datetime
import logo  # Pastikan file logo.py ada di folder yang sama
from io import BytesIO

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Sistem SPD Ngada Pro", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Inisialisasi data agar tidak error saat reload
if 'jml' not in st.session_state:
    st.session_state.jml = 1

# 2. CSS UNTUK TAMPILAN KERTAS (Legal 215.9 x 330mm)
st.markdown("""
<style>
    header, footer, .stDeployButton { visibility: hidden; display: none !important; }
    [data-testid="stMainViewContainer"] { background-color: #525659 !important; }
    .main-container { display: flex; flex-direction: column; align-items: center; width: 100%; padding: 20px 0; }
    .kertas { 
        background-color: white !important; 
        width: 215.9mm; height: 330mm; 
        padding: 10mm 15mm; margin-bottom: 25px; 
        color: black !important; font-family: Arial, sans-serif; 
        box-sizing: border-box; box-shadow: 0 0 20px rgba(0,0,0,0.5);
        font-size: 10.5pt; position: relative; overflow: hidden;
    }
    .kop-table { width: 100%; border-bottom: 3.5pt solid black !important; margin-bottom: 10px; border-collapse: collapse; }
    .kop-teks { text-align: center; line-height: 1.1 !important; color: black !important; }
    .visum-table { width: 100%; border-collapse: collapse; }
    .visum-table td { border: none !important; padding: 2px 0; font-size: 10pt; color: black !important; vertical-align: top; }
    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }
    @media print {
        [data-testid="stSidebar"], .stButton { display: none !important; }
        [data-testid="stMainViewContainer"] { background-color: white !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; }
        @page { size: legal portrait; margin: 0; }
    }
</style>
""", unsafe_allow_html=True)

# 3. SIDEBAR NAVIGASI (INPUTAN)
with st.sidebar:
    st.header("📋 NAVIGASI SPD")
    wilayah = st.selectbox("Wilayah", ["Dalam Daerah", "Luar Daerah"])
    
    with st.expander("👤 DATA PEGAWAI", expanded=True):
        c1, c2 = st.columns(2)
        if c1.button("➕ Tambah"): st.session_state.jml += 1
        if c2.button("➖ Hapus") and st.session_state.jml > 1: st.session_state.jml -= 1
        
        pegawai = []
        for i in range(st.session_state.jml):
            pegawai.append({
                "nama": st.text_input(f"Nama {i+1}", f"NAMA PEGAWAI {i+1}", key=f"nm_{i}"),
                "nip": st.text_input(f"NIP {i+1}", "19...", key=f"np_{i}"),
                "jab": st.text_input(f"Jabatan {i+1}", "Pelaksana", key=f"jb_{i}")
            })

    with st.expander("📄 DETAIL SURAT"):
        no_spt = st.text_input("No SPT", "094/Prokopim/557/02/2026")
        maksud = st.text_area("Maksud", "Mendampingi Bupati...")
        tujuan = st.text_input("Tujuan", "Riung")
        lama = st.text_input("Lama", "1 (Satu) hari")
        anggaran = st.text_area("Dasar", "DPA Bagian Perekonomian 2026")

    with st.expander("🖋️ PENANDA TANGAN"):
        ttd_status = st.selectbox("Status", ["An. BUPATI NGADA", "BUPATI NGADA"])
        pjb_nama = st.text_input("Nama Pejabat", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
        pjb_jab = st.text_input("Jabatan", "Pj. Sekretaris Daerah")
        pjb_nip = st.text_input("NIP", "19710328 199203 1 011")

    if st.button("🖨️ PRINT SURAT"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

# 4. RENDER SURAT KE LAYAR UTAMA
# Kop Surat
kop_html = f"""
<table class="kop-table">
    <tr>
        <td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="70"></td>
        <td class="kop-teks">
            <h3>PEMERINTAH KABUPATEN NGADA</h3>
            <h2>SEKRETARIAT DAERAH</h2>
            <p>BAJAWA</p>
        </td>
        <td width="15%"></td>
    </tr>
</table>"""

# List Pegawai
rows = ""
for i, p in enumerate(pegawai):
    rows += f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td>{i+1}. Nama: <b>{p['nama']}</b><br>NIP: {p['nip']}</td></tr>"

# Tanda Tangan
jab_final = f"{pjb_jab},<br>" if ttd_status == "An. BUPATI NGADA" else ""
ttd_html = f"""
<div style="margin-left:55%; margin-top:30px; text-align:center; line-height:1.2;">
    <b>{ttd_status}</b><br>{jab_final}
    <div style="height:70px;"></div>
    <b><u>{pjb_nama}</u></b><br>NIP. {pjb_nip}
</div>"""

# Gabungan Final
html_full = f"""
<div class="main-container">
    <div class="kertas">
        {kop_html}
        <div class="text-center" style="margin-top:10px;">
            <h3 class="underline">SURAT PERINTAH TUGAS</h3>
            <p>Nomor: {no_spt}</p>
        </div>
        <table class="visum-table">
            <tr><td width="12%">Dasar</td><td width="5%">:</td><td>{anggaran}</td></tr>
            <tr style="height:15px;"><td></td></tr>
            {rows}
            <tr style="height:15px;"><td></td></tr>
            <tr><td>Untuk</td><td>:</td><td>{maksud} ke {tujuan} selama {lama}.</td></tr>
        </table>
        {ttd_html}
    </div>
</div>"""

# TAMPILKAN
st.markdown(html_full, unsafe_allow_html=True)
