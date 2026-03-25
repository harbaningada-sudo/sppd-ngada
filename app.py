import streamlit as st
import pandas as pd
from datetime import datetime
import logo  # Pastikan file logo.py ada variabel GARUDA dan PEMDA

# 1. SETUP HALAMAN
st.set_page_config(page_title="Sistem SPD Ngada Pro", layout="wide")

if 'arsip_register' not in st.session_state:
    st.session_state.arsip_register = []

# CSS UNTUK PRESISI CETAK LEGAL
st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    .stApp { background-color: #525659 !important; }
    .main-container { display: flex; flex-direction: column; align-items: center; width: 100%; padding: 10px 0; }

    /* KERTAS LEGAL */
    .kertas { 
        background-color: white !important; width: 215.9mm; height: 330mm; 
        padding: 12mm 15mm; margin-bottom: 20px; color: black !important; 
        font-family: Arial, sans-serif; box-sizing: border-box; box-shadow: 0 0 20px rgba(0,0,0,0.8);
        font-size: 10.5pt; page-break-after: always; overflow: hidden; position: relative;
    }

    /* KOP GARUDA KHUSUS SPT LUAR DAERAH */
    .kop-garuda { text-align: center; margin-bottom: 15px; line-height: 1.0; width: 100%; }
    .kop-garuda img { width: 70px; margin-bottom: 8px; }
    .kop-garuda h2 { margin: 0; font-size: 15pt; font-weight: bold; letter-spacing: 2px; }

    /* KOP STANDAR PEMDA NGADA */
    .kop-table { width: 100%; border: none !important; border-bottom: 3.5pt solid black !important; margin-bottom: 5px; }
    .kop-teks { text-align: center; line-height: 1.0 !important; } 
    .kop-teks h3, .kop-teks h2 { margin: 0; padding: 1px 0; }

    .judul-rapat { text-align: center; line-height: 1.1; margin-top: 10px; }
    .judul-rapat h3 { margin: 0; font-weight: bold; text-decoration: underline; }
    
    .tabel-border { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; table-layout: fixed; }
    .tabel-border td { border: 1pt solid black !important; padding: 4px 8px; vertical-align: top; color: black !important; line-height: 1.1; }
    .col-no { width: 35px !important; text-align: left !important; }

    .visum-table { width: 100%; border: none !important; border-collapse: collapse; margin: 0 !important; }
    .visum-table td { border: none !important; padding: 0 !important; font-size: 10pt; line-height: 1.2; vertical-align: top; color: black; }

    .ttd-box { text-align: center; line-height: 1.2; width: 280px; margin-left: auto; margin-top: 15px; }

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
    opsi_cetak = st.multiselect("Pilih Dokumen", ["SPT", "SPD Depan", "SPD Belakang"], default=["SPT", "SPD Depan", "SPD Belakang"])
    
    with st.expander("👤 DATA PEGAWAI", expanded=True):
        if 'jml' not in st.session_state: st.session_state.jml = 1
        c1, c2 = st.columns(2)
        if c1.button("➕ Tambah"): st.session_state.jml += 1
        if c2.button("➖ Hapus") and st.session_state.jml > 1: st.session_state.jml -= 1
        
        daftar = []
        for i in range(st.session_state.jml):
            st.markdown(f"**Pegawai {i+1}**")
            daftar.append({
                "nama": st.text_input(f"Nama", f"Nama {i+1}", key=f"n{i}"),
                "nip": st.text_input(f"NIP", "19XXXXXXXXXXXXXX", key=f"nip{i}"),
                "gol": st.text_input(f"Gol", "III/a", key=f"g{i}"),
                "jab": st.text_input(f"Jabatan", "Pelaksana", key=f"j{i}"),
                "spd": st.text_input(f"No SPD", f"530 /.../2026", key=f"spd{i}")
            })

    with st.expander("📄 DATA UTAMA"):
        no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
        tujuan = st.text_input("Tujuan", "Labuan Bajo")
        maksud = st.text_area("Maksud", "Dalam rangka mengikuti...")
        anggaran = st.text_input("Dasar Anggaran", "DPA Bagian Perekonomian dan SDA 2026")

    st.subheader("🖋️ PENANDA TANGAN ASAL")
    pjb = st.text_input("Pejabat", "BERNADINUS DHEY NGEBU, SP")
    gol_pjb = st.text_input("Gol Pejabat", "Pembina Utama Madya")
    nip_pjb = st.text_input("NIP Pejabat", "19650101 198603 1 045")

    if st.button("🖨️ PROSES CETAK"):
        st.components.v1.html("<script>setTimeout(function(){ window.parent.print(); }, 1000);</script>", height=0)

# --- FUNGSI RENDER TTD ---
def get_ttd(label="An. BUPATI NGADA", space=75):
    return f'''<div class="ttd-box"><b>{label}</b><br><div style="height:{space}px;"></div><b><u>{pjb}</u></b><br>{gol_pjb}<br>NIP. {nip_pjb}</div>'''

# --- KONSTRUKSI HTML ---
html_out = '<div class="main-container">'

# 1. SPT (KOP GARUDA - LUAR DAERAH)
if "SPT" in opsi_cetak:
    p_rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{i+1}.</td><td width='18%'>Nama</td><td width='5%'>:</td><td><b>{p['nama']}</b></td></tr><tr><td></td><td></td><td></td><td>Pangkat/Gol</td><td>:</td><td>{p['gol']}</td></tr><tr><td></td><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr><tr><td></td><td></td><td></td><td>Jabatan</td><td>:</td><td>{p['jab']}</td></tr>" for i, p in enumerate(daftar)])
    html_out += f'''<div class="kertas">
        <div class="kop-garuda"><img src="data:image/png;base64,{logo.GARUDA}"><h2>BUPATI NGADA</h2></div>
        <div class="judul-rapat"><h3>SURAT PERINTAH TUGAS</h3><p>NOMOR : {no_spt}</p></div>
        <div style="line-height:1.5; margin-top:15px;">
            <table class="visum-table"><tr><td width="12%">Dasar</td><td width="5%">:</td><td>{anggaran}</td></tr></table>
            <p class="text-center" style="font-weight:bold; letter-spacing:4px; margin:15px 0;">M E M E R I N T A H K A N</p>
            <table class="visum-table">{p_rows}</table>
            <table class="visum-table" style="margin-top:10px;"><tr><td width="12%">Untuk</td><td width="5%">:</td><td>{maksud} ke {tujuan}</td></tr></table>
        </div>
        <div style="margin-top:30px; margin-left:55%;">
            <table class="visum-table">
                <tr><td width="40%">Ditetapkan di</td><td width="5%">:</td><td>Bajawa</td></tr>
                <tr><td>Pada Tanggal</td><td>:</td><td>{datetime.now().strftime('%d %B %Y')}</td></tr>
            </table>
            {get_ttd("WAKIL BUPATI NGADA", 85)}
        </div>
    </div>'''

# 2. SPD DEPAN (KOP PEMDA)
kop_p = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>BAJAWA</p></td><td width="15%"></td></tr></table>'''
for p in daftar:
    if "SPD Depan" in opsi_cetak:
        html_out += f'''<div class="kertas">{kop_p}
            <div style="margin-left:65%; line-height:1.2;">Kode No: 094<br>Nomor: {p['spd']}</div>
            <div class="judul-rapat"><h3>SURAT PERJALANAN DINAS</h3><h3>(SPD)</h3></div>
            <table class="tabel-border" style="margin-top:10px;">
                <tr><td class="col-no">1.</td><td width="42%">Pejabat pemberi perintah</td><td colspan="3"><b>BUPATI NGADA</b></td></tr>
                <tr><td class="col-no">2.</td><td>Nama Pegawai diperintah</td><td colspan="3"><b>{p['nama']}</b></td></tr>
                <tr><td class="col-no">4.</td><td>Maksud Perjalanan</td><td colspan="3">{maksud}</td></tr>
                <tr><td class="col-no">6.</td><td>Tempat Tujuan</td><td colspan="3">{tujuan}</td></tr>
            </table>
            <div style="margin-top:20px; margin-left:55%;">{get_ttd("An. BUPATI NGADA", 65)}</div>
        </div>'''

# 3. SPD BELAKANG (VISUM LUAR DAERAH)
if "SPD Belakang" in opsi_cetak:
    ttd_asal = get_ttd("An. BUPATI NGADA", 65)
    def rv(num, label, val): return f'''<table class="visum-table"><tr><td width="10%">{num}</td><td width="35%">{label}</td><td width="5%">:</td><td>{val}</td></tr></table>'''
    
    html_out += f'''<div class="kertas"><table class="tabel-border" style="height:90%;">
        <tr style="height: 220px;"><td width="50%"></td><td style="padding:10px;">{rv("I.", "Berangkat dari", "Bajawa")}<br>{ttd_asal}</td></tr>
        <tr style="height: 190px;"><td>{rv("II.", "Tiba di", tujuan)}</td><td style="padding:10px;">{rv("", "Berangkat dari", tujuan)}</td></tr>
        <tr style="height: 220px;"><td>{rv("V.", "Tiba Kembali", "Bajawa")}</td><td style="padding:10px;"><p style="font-style:italic; font-size:9.2pt; line-height:1.2;">Telah diperiksa...</p>{ttd_asal}</td></tr>
    </table></div>'''

html_out += '</div>'

# BAGIAN PALING PENTING: Render Markdown
st.markdown(html_out, unsafe_allow_html=True)
