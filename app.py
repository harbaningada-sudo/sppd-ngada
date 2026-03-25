import streamlit as st
import pandas as pd
from datetime import datetime
import logo 

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Ngada Pro", layout="wide")

# 2. INISIALISASI DATABASE REGISTER
if 'arsip_register' not in st.session_state:
    st.session_state.arsip_register = []

# CSS UNTUK PRESISI CETAK
st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    .stApp { background-color: #525659 !important; }
    .main-container { display: flex; flex-direction: column; align-items: center; width: 100%; padding: 10px 0; }

    .kertas { 
        background-color: white !important; width: 215.9mm; height: 330mm; 
        padding: 10mm 20mm; margin-bottom: 20px; color: black !important; 
        font-family: Arial, sans-serif; box-sizing: border-box; box-shadow: 0 0 20px rgba(0,0,0,0.8);
        font-size: 10.5pt; page-break-after: always; overflow: hidden; position: relative;
    }
    
    /* KOP KHUSUS GARUDA (SPT) */
    .kop-garuda { text-align: center; margin-bottom: 15px; line-height: 1.0; }
    .kop-garuda img { width: 65px; margin-bottom: 8px; }
    .kop-garuda h2 { margin: 0; font-size: 14pt; font-weight: bold; letter-spacing: 2px; }

    /* JUDUL & ISI */
    .judul-rapat { text-align: center; line-height: 1.1; margin-top: 5px; }
    .judul-rapat h3 { margin: 0; font-weight: bold; text-decoration: underline; }
    .isi-surat-spt { line-height: 1.5; margin-top: 15px; }
    .visum-table { width: 100%; border: none; border-collapse: collapse; }
    .visum-table td { padding: 1px 0; vertical-align: top; color: black; }

    /* TABEL SPD DEPAN */
    .tabel-border { width: 100%; border-collapse: collapse; border: 1pt solid black; table-layout: fixed; }
    .tabel-border td { border: 1pt solid black; padding: 4px 8px; vertical-align: top; color: black; font-size: 10pt; line-height: 1.1; }

    /* FIX PENANDATANGAN (CENTERED IN COLUMN) */
    .ttd-container { margin-left: 55%; width: 45%; text-align: center; line-height: 1.2; margin-top: 20px; }
    .ttd-pejabat { font-weight: bold; text-decoration: underline; display: inline-block; margin-top: 60px; }

    @media print {
        [data-testid="stSidebar"], .stButton, .no-print { display: none !important; }
        .stApp, .main-container { background-color: white !important; padding: 0 !important; margin: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; width: 215.9mm !important; height: 330mm !important; }
        @page { size: legal portrait; margin: 0; }
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 PANEL KONTROL")
    tab_menu = st.radio("Menu", ["Input & Cetak", "Kelola Register"])
    
    if tab_menu == "Input & Cetak":
        jenis_perjalanan = st.selectbox("Jenis SPT/SPD", ["Dalam Daerah", "Luar Daerah"])
        opsi_cetak = st.multiselect("Pilih Dokumen", ["SPT", "SPD Depan", "SPD Belakang"], default=["SPT", "SPD Depan", "SPD Belakang"])
        
        with st.expander("👤 DATA PEGAWAI", expanded=True):
            if 'jml' not in st.session_state: st.session_state.jml = 1
            if st.button("➕ Tambah Pegawai"): st.session_state.jml += 1
            
            daftar = []
            for i in range(st.session_state.jml):
                daftar.append({
                    "nama": st.text_input(f"Nama P-{i+1}", f"Nama {i+1}", key=f"n{i}"),
                    "nip": st.text_input(f"NIP P-{i+1}", "19XXXXXXXXXXXXXX", key=f"nip{i}"),
                    "gol": st.text_input(f"Gol P-{i+1}", "III/a", key=f"g{i}"),
                    "jab": st.text_input(f"Jab P-{i+1}", "Pelaksana", key=f"j{i}"),
                    "spd": st.text_input(f"No SPD P-{i+1}", f"530 /02/2026", key=f"spd{i}")
                })

        with st.expander("📄 DATA UTAMA"):
            no_spt = st.text_input("Nomor SPT", "094/Prokopim/4724/12/2025")
            tujuan = st.text_input("Tujuan", "Labuan Bajo")
            maksud = st.text_area("Maksud", "Dalam rangka mengikuti...")
            tgl_ttd = st.text_input("Tanggal Ditetapkan", datetime.now().strftime('%d %B %Y'))

        st.subheader("🖋️ PENANDA TANGAN")
        ttd_label = st.selectbox("Jabatan Penanda Tangan", ["BUPATI NGADA", "WAKIL BUPATI NGADA", "An. BUPATI NGADA"])
        pjb_nama = st.text_input("Nama Pejabat", "BERNADINUS DHEY NGEBU, SP")
        pjb_gol = st.text_input("Pangkat/Gol Pejabat", "Pembina Utama Madya")
        pjb_nip = st.text_input("NIP Pejabat", "19650101 198603 1 045")

        if st.button("🖨️ PROSES CETAK"):
            st.components.v1.html("<script>setTimeout(function(){ window.parent.print(); }, 1000);</script>", height=0)

# --- FUNGSI RENDER PENANDATANGAN ---
def render_ttd_section():
    return f'''
    <div class="ttd-container">
        <b>{ttd_label}</b><br>
        <span class="ttd-pejabat">{pjb_nama}</span><br>
        {pjb_gol}<br>
        NIP. {pjb_nip}
    </div>'''

html_out = '<div class="main-container">'

if tab_menu == "Input & Cetak":
    # 1. SPT
    if "SPT" in opsi_cetak:
        kop_spt = f'<div class="kop-garuda"><img src="data:image/png;base64,{logo.GARUDA}"><h2>{ttd_label.replace("An. ", "")}</h2></div>'
        p_rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{i+1}.</td><td width='18%'>Nama</td><td width='3%'>:</td><td><b>{p['nama']}</b></td></tr><tr><td></td><td></td><td></td><td>Pangkat/Gol</td><td>:</td><td>{p['gol']}</td></tr><tr><td></td><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr><tr><td></td><td></td><td></td><td>Jabatan</td><td>:</td><td>{p['jab']}</td></tr>" for i, p in enumerate(daftar)])
        
        html_out += f'''<div class="kertas">{kop_spt}
            <div class="judul-rapat"><h3>SURAT PERINTAH TUGAS</h3><p>NOMOR : {no_spt}</p></div>
            <div class="isi-surat-spt">
                <table class="visum-table"><tr><td width="12%">Dasar</td><td width="3%">:</td><td>DPA Bagian Perekonomian dan SDA 2026</td></tr></table>
                <p class="text-center text-bold" style="margin:15px 0; letter-spacing:4px;">M E M E R I N T A H K A N</p>
                <table class="visum-table">{p_rows}</table>
                <table class="visum-table" style="margin-top:15px;"><tr><td width="12%">Untuk</td><td width="3%">:</td><td>{maksud} ke {tujuan}</td></tr></table>
            </div>
            <div style="margin-left:55%; margin-top:30px;">
                <table class="visum-table">
                    <tr><td width="40%">Ditetapkan di</td><td width="5%">:</td><td>Bajawa</td></tr>
                    <tr><td>Pada Tanggal</td><td>:</td><td>{tgl_ttd}</td></tr>
                </table>
            </div>
            {render_ttd_section()}
        </div>'''

    # 2. SPD DEPAN (Standard Kop Pemda)
    kop_pemda = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>BAJAWA</p></td><td width="15%"></td></tr></table>'''
    for p in daftar:
        if "SPD Depan" in opsi_cetak:
            html_out += f'''<div class="kertas">{kop_pemda}<div style="margin-left:60%; line-height:1.0;">Kode No: 094<br>Nomor: {p['spd']}</div><div class="judul-rapat"><h3>SURAT PERJALANAN DINAS</h3><h3>(SPD)</h3></div>
                <table class="tabel-border" style="margin-top:10px;">
                    <tr><td class="col-no">1.</td><td width="42%">Pejabat pemberi perintah</td><td>BUPATI NGADA</td></tr>
                    <tr><td class="col-no">2.</td><td>Nama Pegawai</td><td><b>{p['nama']}</b></td></tr>
                    <tr><td class="col-no">3.</td><td>Pangkat / Jabatan</td><td>{p['gol']} / {p['jab']}</td></tr>
                    <tr><td class="col-no">4.</td><td>Maksud Perjalanan</td><td>{maksud}</td></tr>
                    <tr><td class="col-no">6.</td><td>Tempat Tujuan</td><td>{tujuan}</td></tr>
                    <tr><td class="col-no">10.</td><td>Keterangan</td><td>-</td></tr>
                </table>
                <div style="margin-top:10px; margin-left:55%;">
                    <table class="visum-table">
                        <tr><td width="40%">Dikeluarkan di</td><td width="5%">:</td><td>Bajawa</td></tr>
                        <tr><td>Pada Tanggal</td><td>:</td><td>{tgl_ttd}</td></tr>
                    </table>
                </div>
                {render_ttd_section()}
            </div>'''

html_out += '</div>'
st.markdown(html_out, unsafe_allow_html=True)
