import streamlit as st
import pandas as pd
from datetime import datetime
import logo  # Pastikan file logo.py ada
from io import BytesIO

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Ngada Pro", layout="wide")

# --- INISIALISASI STATE ---
if 'jml' not in st.session_state: st.session_state.jml = 1
if 'arsip_register' not in st.session_state: st.session_state.arsip_register = []

# 2. CSS FIX (Agar Sidebar tidak hilang)
st.markdown("""
<style>
    /* Hanya sembunyikan header bawaan Streamlit, JANGAN sembunyikan sidebar */
    header, footer, .stDeployButton { visibility: hidden; display: none !important; }
    
    /* Warna background area kerja */
    .stMainView { background-color: #525659 !important; }
    
    /* Container Kertas di Tengah */
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
        font-size: 10.5pt; position: relative;
    }

    /* Tabel & Kop */
    .kop-table { width: 100%; border-bottom: 3.5pt solid black !important; margin-bottom: 10px; }
    .kop-teks { text-align: center; line-height: 1.1; }
    .visum-table { width: 100%; border-collapse: collapse; }
    .visum-table td { padding: 2px 0; vertical-align: top; font-size: 10pt; color: black !important; }
    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }

    /* CSS SAAT PRINT */
    @media print {
        @page { size: legal portrait; margin: 0; }
        [data-testid="stSidebar"], .stButton, .no-print { display: none !important; }
        .stMainView { background-color: white !important; }
        .main-container { padding: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; }
    }
</style>
""", unsafe_allow_html=True)

# 3. NAVIGASI INPUT (DI SIDEBAR - PASTI MUNCUL)
with st.sidebar:
    st.header("📋 PANEL NAVIGASI")
    wilayah = st.selectbox("Jenis Wilayah", ["Dalam Daerah", "Luar Daerah"])
    
    # --- INPUT PEGAWAI ---
    st.subheader("👤 PEGAWAI")
    c1, c2 = st.columns(2)
    if c1.button("➕ Tambah"): st.session_state.jml += 1
    if c2.button("➖ Hapus") and st.session_state.jml > 1: st.session_state.jml -= 1
    
    daftar = []
    for i in range(st.session_state.jml):
        with st.expander(f"Pegawai {i+1}", expanded=(i==0)):
            daftar.append({
                "nama": st.text_input("Nama", value=f"NAMA PEGAWAI {i+1}", key=f"nm_{i}"),
                "nip": st.text_input("NIP", value="19...", key=f"np_{i}"),
                "gol": st.text_input("Gol", "III/a", key=f"gl_{i}"),
                "jab": st.text_input("Jabatan", key=f"jb_{i}"),
                "spd": st.text_input("No SPD", f"530 /02/2026", key=f"sd_{i}")
            })

    # --- INPUT DATA SURAT ---
    with st.expander("📄 DATA SURAT"):
        no_spt = st.text_input("No SPT", "094/Prokopim/557/02/2026")
        maksud = st.text_area("Maksud", "Mendampingi Bupati...")
        tujuan = st.text_input("Tujuan", "Kecamatan Riung")
        lama = st.text_input("Lama Hari", "1 (Satu) hari")
        tgl_bkt = st.text_input("Tgl Berangkat", "17 Maret 2026")
        anggaran = st.text_area("Dasar", "DPA Bagian Perekonomian 2026")

    # --- INPUT PENANDA TANGAN ---
    with st.expander("🖋️ PENANDA TANGAN"):
        ttd_label = st.selectbox("Status", ["An. BUPATI NGADA", "BUPATI NGADA"])
        pjb_nama = st.text_input("Nama Pejabat", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
        jab_ttd = st.text_input("Jabatan Utama", "Pj. Sekretaris Daerah")
        ub = st.text_input("Ub.", "Asisten Perekonomian")
        nip_ttd = st.text_input("NIP", "19710328 199203 1 011")

    if st.button("🖨️ CETAK SEKARANG"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

# --- FUNGSI RENDER TTD ---
def get_ttd_html():
    jab_h = f"{jab_ttd},<br>" if ttd_label == "An. BUPATI NGADA" else ""
    ub_h = f"Ub. {ub},<br>" if (ub and ttd_label == "An. BUPATI NGADA") else ""
    return f'''
    <div style="margin-left:55%; margin-top:20px; text-align:center; line-height:1.2;">
        <b>{ttd_label}</b><br>{jab_h}{ub_h}
        <div style="height:75px;"></div>
        <b><u>{pjb_nama}</u></b><br>NIP. {nip_ttd}
    </div>'''

# 4. TAMPILAN KERTAS DI LAYAR UTAMA
kop_pemda = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>BAJAWA</p></td><td width="15%"></td></tr></table>'''

html_out = '<div class="main-container">'

# KERTAS SPT
p_rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{i+1}.</td><td width='20%'>Nama</td><td>: <b>{p['nama']}</b></td></tr><tr><td colspan='3'></td><td>NIP</td><td>: {p['nip']}</td></tr>" for i, p in enumerate(daftar)])

html_out += f'''
<div class="kertas">
    {kop_pemda}
    <div class="judul-rapat"><h3 class="underline text-center">SURAT PERINTAH TUGAS</h3><p class="text-center">Nomor: {no_spt}</p></div>
    <table class="visum-table"><tr><td width="12%">Dasar</td><td width="5%">:</td><td>{anggaran}</td></tr></table>
    <p class="text-center text-bold" style="margin:10px 0;">MEMERINTAHKAN:</p>
    <table class="visum-table">{p_rows}</table>
    <table class="visum-table" style="margin-top:20px;"><tr><td width="12%">Untuk</td><td width="5%">:</td><td>{maksud} ke {tujuan} selama {lama}.</td></tr></table>
    {get_ttd_html()}
</div>'''

html_out += '</div>'

# TAMPILKAN KE LAYAR
st.markdown(html_out, unsafe_allow_html=True)
