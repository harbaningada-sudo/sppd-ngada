import streamlit as st
import pandas as pd
from datetime import datetime
import logo 

# 1. KONFIGURASI
st.set_page_config(page_title="Cetak SPT Ngada", layout="wide")

# CSS UNTUK PRESISI CETAK (Sesuai Gambar Template)
st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    .main-container { display: flex; flex-direction: column; align-items: center; color: black; background-color: #525659; padding: 20px 0; }
    
    /* KERTAS LEGAL */
    .kertas { 
        background: white !important; width: 215.9mm; min-height: 330mm; 
        padding: 15mm 20mm; margin-bottom: 20px; box-shadow: 0 0 20px rgba(0,0,0,0.5);
        font-family: "Arial", sans-serif; font-size: 11pt; line-height: 1.5; color: black !important;
    }

    /* KOP SURAT */
    .kop-table { width: 100%; border-bottom: 3.5pt solid black; margin-bottom: 10px; border-collapse: collapse; }
    .kop-teks { text-align: center; line-height: 1.1; color: black !important; }
    .kop-teks h3 { margin: 0; font-size: 14pt; }
    .kop-teks h2 { margin: 0; font-size: 16pt; }
    .kop-teks p { margin: 0; font-size: 10pt; }

    /* JUDUL */
    .judul-spt { text-align: center; margin: 15px 0; line-height: 1.2; color: black !important; }
    .judul-spt b { text-decoration: underline; font-size: 12pt; }
    .memerintahkan { text-align: center; letter-spacing: 5px; margin: 15px 0; font-weight: bold; color: black !important; }

    /* TABEL IDENTITAS */
    .identitas-table { width: 100%; border: none; border-collapse: collapse; margin-bottom: 10px; }
    .identitas-table td { vertical-align: top; padding: 2px 0; color: black !important; }

    /* TANDA TANGAN */
    .ttd-box { margin-left: 55%; margin-top: 30px; line-height: 1.2; color: black !important; }
    .ttd-pejabat { margin-top: 70px; line-height: 1.1; }

    @media print {
        [data-testid="stSidebar"], .stButton { display: none !important; }
        .main-container { background: none !important; padding: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; width: 215.9mm; height: 330mm; }
        @page { size: legal; margin: 0; }
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 INPUT DATA SPT")
    no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
    dasar = st.text_area("Dasar (DPA)", "DPA Bagian Perekonomian dan SDA Setda Ngada Tahun Anggaran 2026")
    
    st.subheader("👤 PEGAWAI")
    nama = st.text_input("Nama & Gelar", "Dr. Nicolaus Noywuli, S.Pt., M.Si")
    pangkat = st.text_input("Pangkat/Gol", "Pembina Utama Muda - IV/c")
    nip = st.text_input("NIP", "19720921 200012 1 004")
    jabatan = st.text_area("Jabatan", "Asisten Perekonomian dan Pembangunan Setda Ngada")
    
    st.subheader("📍 TUJUAN")
    untuk = st.text_area("Untuk", "Dalam Rangka Mendampingi Kunjungan Kementerian PPPA di Desa Naruwolo Kec. Jerebuu")
    
    st.subheader("🖋️ PENANDATANGAN")
    tgl_ttd = st.text_input("Tanggal", "12 Februari 2026")
    pjb_ttd = st.text_input("Pejabat TTD", "Yohanes C. Watu Ngebu, S.Sos., M.Si")

    if st.button("🖨️ CETAK SEKARANG"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

# --- TEMPLATE SURAT (RENDER HTML) ---
kop_html = f'''
<table class="kop-table">
    <tr>
        <td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="80"></td>
        <td class="kop-teks">
            <h3>PEMERINTAH KABUPATEN NGADA</h3>
            <h2>SEKRETARIAT DAERAH</h2>
            <p>Jln. Soekarno - Hatta No. 1 Telp (0384) 21012</p>
            <p><b>BAJAWA</b></p>
        </td>
    </tr>
</table>
'''

# ISI SURAT
spt_content = f'''
<div class="kertas">
    {kop_html}
    
    <div class="judul-spt">
        <b>SURAT PERINTAH TUGAS</b><br>
        NOMOR : {no_spt}
    </div>

    <table class="identitas-table">
        <tr>
            <td width="12%">Dasar</td>
            <td width="3%">:</td>
            <td>{dasar}</td>
        </tr>
    </table>

    <div class="memerintahkan">MEMERINTAHKAN</div>

    <table class="identitas-table">
        <tr>
            <td width="12%">Kepada</td>
            <td width="3%">:</td>
            <td width="4%">1.</td>
            <td width="18%">Nama</td>
            <td width="3%">:</td>
            <td><b>{nama}</b></td>
        </tr>
        <tr>
            <td></td><td></td><td></td>
            <td>Pangkat/Gol</td><td>:</td>
            <td>{pangkat}</td>
        </tr>
        <tr>
            <td></td><td></td><td></td>
            <td>NIP</td><td>:</td>
            <td>{nip}</td>
        </tr>
        <tr>
            <td></td><td></td><td></td>
            <td>Jabatan</td><td>:</td>
            <td>{jabatan}</td>
        </tr>
    </table>

    <table class="identitas-table" style="margin-top:15px;">
        <tr>
            <td width="12%">Untuk</td>
            <td width="3%">:</td>
            <td>{untuk}</td>
        </tr>
    </table>

    <div class="ttd-box">
        <table style="width:100%; border:none; line-height:1.1;">
            <tr><td width="40%">Ditetapkan di</td><td width="5%">:</td><td>Bajawa</td></tr>
            <tr><td>Pada Tanggal</td><td>:</td><td>{tgl_ttd}</td></tr>
        </table>
        <br>
        <b>An. BUPATI NGADA</b><br>
        Pj. Sekretaris Daerah,
        
        <div class="ttd-pejabat">
            <b><u>{pjb_ttd}</u></b><br>
            Pembina Utama Muda - IV/c<br>
            NIP. 19710328 199203 1 011
        </div>
    </div>
</div>
'''

# BAGIAN PALING PENTING: Render Markdown
st.markdown(f'<div class="main-container">{spt_content}</div>', unsafe_allow_html=True)
