import streamlit as st
import pandas as pd
from datetime import datetime
import logo  # Pastikan file logo.py kamu berisi variabel PEMDA (base64 logo)

# 1. SETUP
st.set_page_config(page_title="Cetak SPT Ngada", layout="wide")

# Database Register
if 'db_reg' not in st.session_state: st.session_state.db_reg = []

st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .main-container { display: flex; flex-direction: column; align-items: center; color: black; }
    
    /* KERTAS LEGAL */
    .kertas { 
        background: white !important; width: 215.9mm; min-height: 330mm; 
        padding: 15mm 20mm; margin-bottom: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.5);
        font-family: "Arial", sans-serif; font-size: 11pt; line-height: 1.5;
    }

    /* KOP SURAT RAPI */
    .kop-table { width: 100%; border-bottom: 3pt solid black; margin-bottom: 10px; border-collapse: collapse; }
    .kop-table td { vertical-align: middle; padding-bottom: 5px; }
    .kop-teks { text-align: center; line-height: 1.1; }
    .kop-teks h3 { margin: 0; font-size: 14pt; font-weight: bold; }
    .kop-teks h2 { margin: 0; font-size: 16pt; font-weight: bold; }
    .kop-teks p { margin: 0; font-size: 10pt; }

    /* JUDUL SPT */
    .judul-spt { text-align: center; margin-top: 15px; margin-bottom: 20px; line-height: 1.1; }
    .judul-spt b { text-decoration: underline; font-size: 12pt; }
    
    .memerintahkan { text-align: center; letter-spacing: 4px; margin: 20px 0; font-weight: bold; }

    /* TABEL IDENTITAS (Titik Dua Sejajar) */
    .identitas-table { width: 100%; border: none; margin-left: 0; }
    .identitas-table td { vertical-align: top; padding: 1px 0; }

    /* TANDA TANGAN */
    .ttd-box { margin-left: 55%; margin-top: 30px; line-height: 1.2; text-align: left; }
    .ttd-pejabat { margin-top: 70px; text-align: left; line-height: 1.1; }
    .ttd-pejabat u { font-weight: bold; }

    @media print {
        [data-testid="stSidebar"], .stButton { display: none !important; }
        .stApp { background: white !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; width: 215.9mm; height: 330mm; }
        @page { size: legal; margin: 0; }
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 INPUT SPT")
    no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
    dasar = st.text_area("Dasar (DPA)", "DPA Bagian Perekonomian dan SDA Setda Ngada Tahun Anggaran 2026")
    
    st.subheader("👤 DATA PEGAWAI")
    nama = st.text_input("Nama & Gelar", "Dr. Nicolaus Noywuli, S.Pt., M.Si")
    pangkat = st.text_input("Pangkat/Gol", "Pembina Utama Muda - IV/c")
    nip = st.text_input("NIP", "19720921 200012 1 004")
    jabatan = st.text_area("Jabatan", "Asisten Perekonomian dan Pembangunan Setda Ngada")
    
    st.subheader("📍 TUJUAN")
    untuk = st.text_area("Untuk (Keperluan)", "Dalam Rangka Mendampingi Kunjungan Kementerian Pemberdayaan Perempuan dan Perlindungan Anak (PPPA) di Desa Naruwolo Kec. Jerebuu")
    
    st.subheader("🖋️ PENANDATANGAN")
    tgl_ttd = st.text_input("Tanggal Ditetapkan", "12 Februari 2026")
    an = st.text_input("An. Jabatan", "An. BUPATI NGADA")
    jab_an = st.text_input("Jabatan Penandatangan", "Pj. Sekretaris Daerah,")
    
    nama_pjb = st.text_input("Nama Pejabat TTD", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
    pangkat_pjb = st.text_input("Pangkat Pejabat TTD", "Pembina Utama Muda - IV/c")
    nip_pjb = st.text_input("NIP Pejabat TTD", "19710328 199203 1 011")

    if st.button("🖨️ CETAK SPT"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

# --- KONSTRUKSI SURAT ---
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

spt_html = f'''
<div class="main-container">
    <div class="kertas">
        {kop_html}
        
        <div class="judul-spt">
            <b>SURAT PERINTAH TUGAS</b><br>
            NOMOR : {no_spt}
        </div>

        <table class="identitas-table">
            <tr>
                <td width="15%">Dasar</td>
                <td width="3%">:</td>
                <td>{dasar}</td>
            </tr>
        </table>

        <div class="memerintahkan">MEMERINTAHKAN</div>

        <table class="identitas-table">
            <tr>
                <td width="15%">Kepada</td>
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

        <table class="identitas-table" style="margin-top:20px;">
            <tr>
                <td width="15%">Untuk</td>
                <td width="3%">:</td>
                <td>{untuk}</td>
            </tr>
        </table>

        <div class="ttd-box">
            <table class="visum-table" style="width:100%">
                <tr><td width="40%">Ditetapkan di</td><td width="5%">:</td><td>Bajawa</td></tr>
                <tr><td>Pada Tanggal</td><td>:</td><td>{tgl_ttd}</td></tr>
            </table>
            <br>
            <b>{an}</b><br>
            {jab_an}
            
            <div class="ttd-pejabat">
                <u>{nama_pjb}</u><br>
                {pangkat_pjb}<br>
                NIP. {nip_pjb}
            </div>
        </div>
    </div>
</div>
'''

st.markdown(spt_html, unsafe_allow_html=True)
