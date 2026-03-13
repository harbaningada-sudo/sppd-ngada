import streamlit as st
from datetime import datetime

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Cetak SPT Prokopim Ngada", layout="wide")

st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    .main { background-color: #525659; }
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

# 3. RENDER TAMPILAN MENGGUNAKAN KOMPONEN HTML KHUSUS
surat_html = f"""
<div style="background-color: #525659; padding: 20px; display: flex; justify-content: center;">
    <div style="background-color: white; width: 210mm; min-height: 297mm; padding: 15mm 20mm 20mm 25mm; color: black; font-family: Arial, sans-serif; font-size: 11pt; box-shadow: 0 0 15px rgba(0,0,0,0.5); box-sizing: border-box;">
        
        <div style="text-align: center; border-bottom: 3px solid black; padding-bottom: 2px; margin-bottom: 15px; line-height: 1.1;">
            <h3 style="margin:0; font-weight: bold; font-size: 14pt;">PEMERINTAH KABUPATEN NGADA</h3>
            <h3 style="margin:0; font-weight: bold; font-size: 14pt;">SEKRETARIAT DAERAH</h3>
            <p style="margin:0; font-size:10pt;">Jln. Soekarno - Hatta No. 1 Telp (0384) 21012</p>
            <h3 style="margin:0; font-weight: bold; font-size: 14pt;">BAJAWA</h3>
        </div>

        <h3 style="text-align: center; font-weight: bold; text-decoration: underline; margin-top: 10px; margin-bottom: 0;">SURAT PERINTAH TUGAS</h3>
        <p style="text-align: center; margin-top: 0;">NOMOR : {no_spt}</p>

        <br>

        <table style="width: 100%; border-collapse: collapse; margin-bottom: 10px;">
            <tr><td style="width: 15%; vertical-align: top;">Dasar</td><td style="width: 2%; vertical-align: top;">:</td><td style="text-align: justify; vertical-align: top;">{dasar}</td></tr>
        </table>

        <p style="text-align: center; letter-spacing: 3px; margin: 15px 0; font-weight: bold;">M E M E R I N T A H K A N</p>

        <table style="width: 100%; border-collapse: collapse; margin-bottom: 10px;">
            <tr><td style="width: 15%; vertical-align: top;">Kepada</td><td style="width: 5%; vertical-align: top;">: 1.</td><td style="width: 15%; vertical-align: top;">Nama</td><td style="width: 2%; vertical-align: top;">:</td><td style="font-weight: bold; vertical-align: top;">{nama}</td></tr>
            <tr><td></td><td></td><td style="vertical-align: top;">Pangkat/Gol</td><td style="vertical-align: top;">:</td><td style="vertical-align: top;">{gol}</td></tr>
            <tr><td></td><td></td><td style="vertical-align: top;">NIP</td><td style="vertical-align: top;">:</td><td style="vertical-align: top;">{nip}</td></tr>
            <tr><td></td><td></td><td style="vertical-align: top;">Jabatan</td><td style="vertical-align: top;">:</td><td style="vertical-align: top;">{jabatan}</td></tr>
        </table>

        <br>

        <table style="width: 100%; border-collapse: collapse; margin-bottom: 10px;">
            <tr><td style="width: 15%; vertical-align: top;">Untuk</td><td style="width: 2%; vertical-align: top;">:</td><td style="text-align: justify; vertical-align: top;">{untuk}</td></tr>
        </table>

        <div style="margin-left: 50%; margin-top: 30px;">
            <table style="width: 100%; border-collapse: collapse;">
                <tr><td style="width: 45%; vertical-align: top;">Ditetapkan di</td><td style="vertical-align: top;">:</td><td style="vertical-align: top;">Bajawa</td></tr>
                <tr><td style="vertical-align: top;">Pada Tanggal</td><td style="vertical-align: top;">:</td><td style="vertical-align: top;">{tgl_indo}</td></tr>
            </table>
            <div style="margin: 15px 0 0 25px;">
                <p style="font-weight: bold; margin:0;">An. BUPATI NGADA</p>
                <p style="margin:0;">Pj. Sekretaris Daerah,</p>
                <br><br><br><br>
                <p style="font-weight: bold; text-decoration: underline; margin:0;">{nama_sekda}</p>
                <p style="margin:0;">{gol}</p>
                <p style="margin:0;">NIP. {nip_sekda}</p>
            </div>
        </div>
    </div>
</div>
"""

# Memanggil komponen HTML secara murni
st.components.v1.html(surat_html, height=1200, scrolling=True)
