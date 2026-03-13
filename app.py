import streamlit as st
from datetime import datetime

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Cetak SPT Prokopim Ngada", layout="wide")

# CSS AGRESIF UNTUK MENGHAPUS JARAK ATAS
st.markdown("""
<style>
    /* Menghilangkan elemen UI bawaan */
    header, footer, #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* MEMAKSA HALAMAN MEPET KE ATAS (0 PIXEL) */
    .stApp {
        margin-top: -60px !important;
    }
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }
    
    .main { background-color: #525659; }
    
    .kertas-a4 {
        background-color: white;
        width: 210mm;
        min-height: 297mm;
        padding: 10mm 20mm 20mm 25mm;
        margin: 0 auto !important;
        color: black;
        font-family: "Arial", sans-serif;
        font-size: 11pt;
        box-shadow: 0 0 15px rgba(0,0,0,0.5);
        box-sizing: border-box;
    }

    /* KOP SURAT MEPET */
    .kop-header { 
        text-align: center; 
        border-bottom: 3px solid black; 
        padding-bottom: 2px; 
        margin-bottom: 15px;
        line-height: 1.1;
    }
    
    .tabel-data { width: 100%; border-collapse: collapse; margin-bottom: 10px; }
    .tabel-data td { border: none !important; padding: 2px 0; vertical-align: top; }
    .text-center { text-align: center; }
    .text-bold { font-weight: bold; }
    .text-underline { text-decoration: underline; }
    .text-justify { text-align: justify; }

    @media print {
        .stSidebar, .stButton { display: none !important; }
        .stApp { margin-top: 0 !important; }
        .main { background-color: white !important; }
        .kertas-a4 { box-shadow: none !important; margin: 0 !important; }
    }
</style>
""", unsafe_allow_html=True)

# 2. PANEL INPUT SIDEBAR
with st.sidebar:
    st.header("📋 INPUT DATA SPT")
    no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
    dasar = st.text_area("Dasar (DPA)", "DPA Bagian Perekonomian dan SDA Setda Ngada Tahun Anggaran 2026")
    st.markdown("---")
    nama = st.text_input("Nama Pegawai", "Dr. Nicolaus Noywuli, S.Pt., M.Si")
    nip = st.text_input("NIP", "19720921 200012 1 004")
    gol = st.text_input("Pangkat/Gol", "Pembina Utama Muda - IV/c")
    jabatan = st.text_area("Jabatan", "Asisten Perekonomian dan Pembangunan Setda Ngada")
    st.markdown("---")
    untuk = st.text_area("Untuk (Kegiatan)", "Mendampingi Kunjungan Kementerian PPPA")
    tgl_tetap = st.date_input("Tanggal Penetapan", datetime(2026, 2, 12))
    nama_sekda = st.text_input("Nama Pj. Sekda", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
    nip_sekda = st.text_input("NIP Pj. Sekda", "19710328 199203 1 011")

# FORMAT TANGGAL
bulan_list = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
tgl_indo = f"{tgl_tetap.day} {bulan_list[tgl_tetap.month-1]} {tgl_tetap.year}"

# 3. RENDER KERTAS
st.write('<div class="kertas-a4">', unsafe_allow_html=True)

st.markdown(f"""
<div class="kop-header">
    <h3 class="text-bold" style="margin:0; font-size: 14pt;">PEMERINTAH KABUPATEN NGADA</h3>
    <h3 class="text-bold" style="margin:0; font-size: 14pt;">SEKRETARIAT DAERAH</h3>
    <p style="margin:0; font-size:10pt;">Jln. Soekarno - Hatta No. 1 Telp (0384) 21012</p>
    <h3 class="text-bold" style="margin:0; font-size: 14pt;">BAJAWA</h3>
</div>

<h3 class="text-center text-bold text-underline" style="margin-top: 10px; margin-bottom:0;">SURAT PERINTAH TUGAS</h3>
<p class="text-center" style="margin-top:0;">NOMOR : {no_spt}</p>

<br>

<table class="tabel-data">
    <tr><td width="15%">Dasar</td><td width="2%">:</td><td class="text-justify">{dasar}</td></tr>
</table>

<p class="text-center" style="letter-spacing: 3px; margin: 15px 0;">M E M E R I N T A H K A N</p>

<table class="tabel-data">
    <tr><td width="15%">Kepada</td><td width="5%">: 1.</td><td width="15%">Nama</td><td width="2%">:</td><td class="text-bold">{nama}</td></tr>
    <tr><td></td><td></td><td>Pangkat/Gol</td><td>:</td><td>{gol}</td></tr>
    <tr><td></td><td></td><td>NIP</td><td>:</td><td>{nip}</td></tr>
    <tr><td></td><td></td><td>Jabatan</td><td>:</td><td>{jabatan}</td></tr>
</table>

<br>

<table class="tabel-data">
    <tr><td width="15%">Untuk</td><td width="2%">:</td><td class="text-justify">{untuk}</td></tr>
</table>

<div style="margin-left:50%; margin-top:30px;">
    <table class="tabel-data">
        <tr><td width="45%">Ditetapkan di</td><td>:</td><td>Bajawa</td></tr>
        <tr><td>Pada Tanggal</td><td>:</td><td>{tgl_indo}</td></tr>
    </table>
    <div style="margin: 15px 0 0 25px;">
        <p class="text-bold" style="margin:0;">An. BUPATI NGADA</p>
        <p style="margin:0;">Pj. Sekretaris Daerah,</p>
        <br><br><br><br>
        <p class="text-bold text-underline" style="margin:0;">{nama_sekda}</p>
        <p style="margin:0;">{gol}</p>
        <p style="margin:0;">NIP. {nip_sekda}</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.write('</div>', unsafe_allow_html=True)
