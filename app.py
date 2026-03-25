import streamlit as st
import pandas as pd
from datetime import datetime
import logo  # Memanggil file logo.py di repository kamu

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Ngada Pro", layout="wide")

# INISIALISASI DATABASE REGISTER
if 'arsip_register' not in st.session_state:
    st.session_state.arsip_register = []

# CSS UNTUK PRESISI CETAK FULL LEGAL
st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    .stApp { background-color: #525659 !important; }
    .main-container { display: flex; flex-direction: column; align-items: center; width: 100%; padding: 10px 0; }

    /* KERTAS LEGAL PORTRAIT */
    .kertas { 
        background-color: white !important; width: 215.9mm; height: 330mm; 
        padding: 12mm 18mm; margin-bottom: 20px; color: black !important; 
        font-family: Arial, sans-serif; box-sizing: border-box; box-shadow: 0 0 20px rgba(0,0,0,0.8);
        font-size: 10.5pt; page-break-after: always; overflow: hidden; position: relative;
    }

    /* KOP GARUDA (KHUSUS SPT LUAR DAERAH) */
    .kop-garuda { text-align: center; margin-bottom: 10px; line-height: 1.0; }
    .kop-garuda img { width: 75px; margin-bottom: 5px; }
    .kop-garuda h2 { margin: 0; font-size: 16pt; font-weight: bold; letter-spacing: 2px; }

    /* KOP PEMDA (UNTUK SPD DEPAN) */
    .kop-table { width: 100%; border: none !important; border-bottom: 3.5pt solid black !important; margin-bottom: 8px; }
    .kop-teks { text-align: center; line-height: 1.1 !important; } 
    .kop-teks h3 { margin: 0; font-size: 13pt; }
    .kop-teks h2 { margin: 0; font-size: 15pt; }

    /* JUDUL & TEKS */
    .judul-rapat { text-align: center; line-height: 1.0 !important; margin-top: 10px; margin-bottom: 15px; }
    .judul-rapat h3 { margin: 0; font-weight: bold; text-decoration: underline; font-size: 12pt; }
    .memerintahkan { text-align: center; font-weight: bold; letter-spacing: 5px; margin: 15px 0; }

    /* TABEL STANDAR */
    .tabel-border { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; table-layout: fixed; }
    .tabel-border td { border: 1pt solid black !important; padding: 5px 8px; vertical-align: top; line-height: 1.1; }
    .col-no { width: 35px !important; text-align: left !important; }

    /* TABEL VISUM TANPA BORDER */
    .visum-table { width: 100%; border: none !important; border-collapse: collapse; }
    .visum-table td { border: none !important; padding: 1px 0; font-size: 10.5pt; line-height: 1.2; vertical-align: top; }

    .underline { text-decoration: underline; }
    .text-bold { font-weight: bold; }

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
        opsi_cetak = st.multiselect("Pilih Dokumen", ["SPT", "SPD Depan", "SPD Belakang"], default=["SPT", "SPD Depan", "SPD Belakang"])
        
        with st.expander("👤 DATA PEGAWAI", expanded=True):
            if 'jml' not in st.session_state: st.session_state.jml = 1
            c1, c2 = st.columns(2)
            if c1.button("➕ Tambah"): st.session_state.jml += 1
            if c2.button("➖ Hapus") and st.session_state.jml > 1: st.session_state.jml -= 1
            
            daftar = []
            for i in range(st.session_state.jml):
                daftar.append({
                    "nama": st.text_input(f"Nama P-{i+1}", f"Nama {i+1}", key=f"n{i}"),
                    "nip": st.text_input(f"NIP P-{i+1}", "19XXXXXXXXXXXXXX", key=f"nip{i}"),
                    "gol": st.text_input(f"Gol P-{i+1}", "III/a", key=f"g{i}"),
                    "jab": st.text_input(f"Jabatan P-{i+1}", "Pelaksana", key=f"j{i}"),
                    "spd": st.text_input(f"No SPD P-{i+1}", f"530/.../2026", key=f"spd{i}")
                })

        with st.expander("📄 DATA UTAMA"):
            no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
            maksud = st.text_area("Maksud Tugas", "Dalam rangka mendampingi...")
            tujuan = st.text_input("Tempat Tujuan", "Labuan Bajo")
            tgl_bkt = st.text_input("Tgl Berangkat", "17 Maret 2026")
            tgl_kbl = st.text_input("Tgl Pulang", "20 Maret 2026")
            anggaran = st.text_input("Dasar Anggaran", "DPA Bagian Perekonomian dan SDA Setda Ngada 2026")

        with st.expander("🏢 PENGESAH TUJUAN"):
            instansi_tujuan = st.text_input("Instansi Tujuan", "Kantor Bupati Manggarai Barat")
            pjb_tujuan = st.text_input("Nama Pejabat Tujuan", "Nama Pejabat")
            gol_tujuan = st.text_input("Gol Pejabat Tujuan", "Pembina Utama Muda, IV/c")
            nip_tujuan = st.text_input("NIP Pejabat Tujuan", "19XXXXXXXXXXXXXX")

        st.subheader("🖋️ TANDA TANGAN ASAL")
        ttd_label = st.selectbox("Label Jabatan", ["BUPATI NGADA", "WAKIL BUPATI NGADA", "An. BUPATI NGADA"])
        pjb_asal = st.text_input("Nama Pejabat Asal", "BERNADINUS DHEY NGEBU, SP")
        gol_asal = st.text_input("Gol Pejabat Asal", "Pembina Utama Madya")
        nip_asal = st.text_input("NIP Pejabat Asal", "19650101 198603 1 045")

        if st.button("🖨️ PROSES CETAK"):
            st.components.v1.html("<script>setTimeout(function(){ window.parent.print(); }, 1200);</script>", height=0)

# --- FUNGSI RENDER TANDA TANGAN ---
def render_ttd_statis(nama, gol, nip, label, space=75):
    return f'''
    <div style="text-align:center; line-height:1.2; width:280px; margin-left:auto;">
        <b>{label}</b><br><div style="height:{space}px;"></div>
        <b><u>{nama}</u></b><br>{gol}<br>NIP. {nip}
    </div>'''

html_out = '<div class="main-container">'

if tab_menu == "Input & Cetak":
    # 1. SPT (LOGIKA LUAR DAERAH - LOGO GARUDA)
    if "SPT" in opsi_cetak:
        p_rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{i+1}.</td><td width='18%'>Nama</td><td width='5%'>:</td><td><b>{p['nama']}</b></td></tr><tr><td></td><td></td><td></td><td>Pangkat/Gol</td><td>:</td><td>{p['gol']}</td></tr><tr><td></td><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr><tr><td></td><td></td><td></td><td>Jabatan</td><td>:</td><td>{p['jab']}</td></tr>" for i, p in enumerate(daftar)])
        html_out += f'''<div class="kertas">
            <div class="kop-garuda"><img src="data:image/png;base64,{logo.GARUDA}"><h2>BUPATI NGADA</h2></div>
            <div class="judul-rapat"><h3>SURAT PERINTAH TUGAS</h3><p>NOMOR : {no_spt}</p></div>
            <div style="line-height:1.5;">
                <table class="visum-table"><tr><td width="12%">Dasar</td><td width="5%">:</td><td>{anggaran}</td></tr></table>
                <div class="memerintahkan">M E M E R I N T A H K A N</div>
                <table class="visum-table">{p_rows}</table>
                <table class="visum-table" style="margin-top:10px;"><tr><td width="12%">Untuk</td><td width="5%">:</td><td>{maksud} ke {tujuan}</td></tr></table>
            </div>
            <div style="margin-top:30px; margin-left:55%;">
                <table class="visum-table">
                    <tr><td width="40%">Ditetapkan di</td><td width="5%">:</td><td>Bajawa</td></tr>
                    <tr><td>Pada Tanggal</td><td>:</td><td>{datetime.now().strftime('%d %B %Y')}</td></tr>
                </table>
                <br>
                {render_ttd_statis(pjb_asal, gol_asal, nip_asal, ttd_label, 85)}
            </div>
        </div>'''

    # 2. SPD DEPAN (KOP PEMDA)
    kop_pemda = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>BAJAWA</p></td><td width="15%"></td></tr></table>'''
    for p in daftar:
        if "SPD Depan" in opsi_cetak:
            html_out += f'''<div class="kertas">{kop_pemda}
                <div style="margin-left:65%; line-height:1.2;">Kode No: 094<br>Nomor: {p['spd']}</div>
                <div class="judul-rapat" style="margin-top:10px;"><h3>SURAT PERJALANAN DINAS</h3><h3>(SPD)</h3></div>
                <table class="tabel-border">
                    <tr><td class="col-no">1.</td><td width="42%">Pejabat pemberi perintah</td><td colspan="3"><b>BUPATI NGADA</b></td></tr>
                    <tr><td class="col-no">2.</td><td>Nama Pegawai diperintah</td><td colspan="3"><b>{p['nama']}</b></td></tr>
                    <tr><td class="col-no">4.</td><td>Maksud Perjalanan</td><td colspan="3">{maksud}</td></tr>
                    <tr><td class="col-no">6.</td><td>Tempat Tujuan</td><td colspan="3">{tujuan}</td></tr>
                    <tr><td class="col-no">7.</td><td>Lamanya Perjalanan</td><td colspan="3">3 (Tiga) hari</td></tr>
                </table>
                <div style="margin-top:20px;">{render_ttd_statis(pjb_asal, gol_asal, nip_asal, "An. BUPATI NGADA", 65)}</div>
            </div>'''

    # 3. SPD BELAKANG (POIN II KIRI KOSONG)
    if "SPD Belakang" in opsi_cetak:
        ttd_asal = render_ttd_statis(pjb_asal, gol_asal, nip_asal, "An. BUPATI NGADA", 60)
        ttd_tujuan = f'''<div style="text-align:center; line-height:1.2; font-size:10pt;"><br><b>Mengesahkan</b><br>{instansi_tujuan}<div style="height:60px;"></div><b><u>{pjb_tujuan}</u></b><br>{gol_tujuan}<br>NIP. {nip_tujuan}</div>'''
        
        def rv(num, label, val, d_v, is_n=True):
            n_c = f'<td width="10%">{num}</td>' if is_n else ""
            return f'''<table class="visum-table"><tr>{n_c}<td width="35%">{label}</td><td width="5%">:</td><td>{val}</td></tr><tr>{"<td></td>" if is_n else ""}<td>Pada Tanggal</td><td>:</td><td>{d_v}</td></tr></table>'''

        html_out += f'''<div class="kertas"><table class="tabel-border" style="height:88%;">
            <tr style="height: 220px;"><td width="50%"></td><td style="padding:10px;">{rv("I.", "Berangkat dari", "Bajawa", tgl_bkt)}<table class="visum-table"><tr><td width="10%"></td><td width="35%">Ke</td><td width="5%">:</td><td>{tujuan}</td></tr></table>{ttd_asal}</td></tr>
            <tr style="height: 190px;"><td>{rv("II.", "Tiba di", tujuan, tgl_bkt)}<br></td><td style="padding:10px;">{rv("", "Berangkat dari", tujuan, tgl_kbl, False)}<table class="visum-table"><tr><td width="35%">Ke</td><td width="5%">:</td><td>Bajawa</td></tr></table>{ttd_tujuan}</td></tr>
            <tr style="height: 220px;"><td>{rv("V.", "Tiba Kembali", "Bajawa", tgl_kbl)}</td><td style="padding:10px;"><p style="font-style:italic; font-size:9.2pt; line-height:1.2;">Telah diperiksa...</p>{ttd_asal}</td></tr>
        </table>
        <div style="border:1pt solid black; border-top:none; padding:8px; font-size:10.5pt;"><b>VI. Catatan Lain-lain</b></div>
        <div style="border:1pt solid black; border-top:none; padding:8px; font-size:8.5pt; text-align:justify; line-height:1.2;"><b>VII. Perhatian :</b> Pejabat yang menerbitkan SPD... bertanggung jawab...</div></div>'''

html_out += '</div>'
st.markdown(html_out, unsafe_allow_html=True)
