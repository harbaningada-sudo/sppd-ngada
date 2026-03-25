import streamlit as st
import pandas as pd
from datetime import datetime
import logo  # Pastikan di file logo.py ada variabel GARUDA dan PEMDA

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Ngada Pro", layout="wide")

# 2. INISIALISASI DATABASE REGISTER
if 'arsip_register' not in st.session_state:
    st.session_state.arsip_register = []

# CSS UNTUK PRESISI CETAK FULL LEGAL & LANDSCAPE REGISTER
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
    .kertas-landscape { width: 355.6mm !important; height: 215.9mm !important; padding: 15mm !important; }

    /* KOP KHUSUS GARUDA (SPT) */
    .kop-garuda { text-align: center; margin-bottom: 15px; line-height: 1.0; }
    .kop-garuda img { width: 70px; margin-bottom: 8px; }
    .kop-garuda h2 { margin: 0; font-size: 14pt; font-weight: bold; letter-spacing: 2px; }

    /* KOP PEMDA (SPD) */
    .kop-table { width: 100%; border: none !important; border-bottom: 3.5pt solid black !important; margin-bottom: 5px; }
    .kop-teks { text-align: center; line-height: 1.0 !important; } 
    .kop-teks h3, .kop-teks h2 { margin: 0; line-height: 1.0 !important; padding: 1px 0; }

    .judul-rapat { text-align: center; line-height: 1.0 !important; margin-top: 5px; }
    .judul-rapat h3 { margin: 0; line-height: 1.0 !important; font-weight: bold; text-decoration: underline; }
    
    .isi-surat-spt { line-height: 1.5 !important; margin-top: 15px; }

    .tabel-border { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; table-layout: fixed; }
    .tabel-border td { border: 1pt solid black !important; padding: 4px 8px !important; vertical-align: top; color: black !important; font-size: 10pt; line-height: 1.1 !important; }
    .col-no { width: 35px !important; text-align: left !important; }

    .visum-table { width: 100%; border: none !important; border-collapse: collapse; margin: 0 !important; }
    .visum-table td { border: none !important; padding: 0 !important; font-size: 10pt; line-height: 1.2; color: black !important; vertical-align: top; }

    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }

    @media print {
        [data-testid="stSidebar"], .stButton, .no-print { display: none !important; }
        .stApp, .main-container { background-color: white !important; padding: 0 !important; margin: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; width: 215.9mm !important; height: 330mm !important; }
        @page { size: legal portrait; margin: 0; }
        .register-page { @page { size: legal landscape; } }
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 PANEL KONTROL")
    tab_menu = st.radio("Menu", ["Input & Cetak", "Kelola Register"])
    
    if tab_menu == "Input & Cetak":
        jenis_perjalanan = st.selectbox("Jenis SPT/SPD", ["Dalam Daerah", "Luar Daerah"])
        opsi_cetak = st.multiselect("Pilih Dokumen", ["SPT", "SPD Depan", "SPD Belakang", "Register"], default=["SPT", "SPD Depan", "SPD Belakang"])
        
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
                    "spd": st.text_input(f"No SPD", f"530 /02/2026", key=f"spd{i}"),
                    "lembar": st.text_input(f"Lembar ke", "I", key=f"lbr{i}")
                })

        with st.expander("📄 DATA UTAMA"):
            no_spt = st.text_input("Nomor SPT", "094/Prokopim/4724/12/2025")
            maksud = st.text_area("Maksud Perjalanan", "Dalam rangka mengikuti Seminar Nasional...")
            tujuan = st.text_input("Tujuan", "Labuan Bajo, Kabupaten Manggarai Barat")
            tgl_bkt = st.text_input("Tanggal Berangkat", "15 Desember 2025")
            tgl_kbl = st.text_input("Tanggal Pulang", "18 Desember 2025")
            anggaran = st.text_input("Dasar Anggaran", "Surat Balai Besar Konservasi Sumber Daya Alam NTT Nomor: UN.14/K.5...")

        st.subheader("🖋️ PENANDA TANGAN")
        ttd_label = st.selectbox("Label Jabatan", ["BUPATI NGADA", "WAKIL BUPATI NGADA", "An. BUPATI NGADA"])
        pjb_nama = st.text_input("Nama Pejabat", "BERNADINUS DHEY NGEBU, SP")
        pjb_gol = st.text_input("Pangkat/Gol Pejabat", "Pembina Utama Madya")
        pjb_nip = st.text_input("NIP Pejabat", "19650101 198603 1 045")

        if st.button("🖨️ PROSES CETAK & SIMPAN"):
            for p in daftar:
                st.session_state.arsip_register.append({
                    "Nama": p['nama'], "No SPT": no_spt, "No SPD": p['spd'],
                    "Berangkat": tgl_bkt, "Pulang": tgl_kbl, "Ket": jenis_perjalanan
                })
            st.components.v1.html("<script>setTimeout(function(){ window.parent.print(); }, 1200);</script>", height=0)

# --- FUNGSI RENDER ---
def render_ttd(space=70):
    return f'''<div style="margin-left:55%; text-align:center; line-height:1.2;">
        <b>{ttd_label}</b><br><div style="height:{space}px;"></div>
        <b><u>{pjb_nama}</u></b><br>{pjb_gol}<br>NIP. {pjb_nip}</div>'''

html_out = '<div class="main-container">'

if tab_menu == "Input & Cetak":
    # 1. SPT (Logic Garuda vs Pemda)
    if "SPT" in opsi_cetak:
        # Jika Luar Daerah pakai Logo Garuda (sesuai gambar github)
        kop_spt = f'<div class="kop-garuda"><img src="data:image/png;base64,{logo.GARUDA}"><h2>{ttd_label}</h2></div>' if jenis_perjalanan == "Luar Daerah" else f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>BAJAWA</p></td><td width="15%"></td></tr></table>'''
        
        p_rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{i+1}.</td><td width='20%'>Nama</td><td width='5%'>:</td><td><b>{p['nama']}</b></td></tr><tr><td></td><td></td><td></td><td>Pangkat/Gol</td><td>:</td><td>{p['gol']}</td></tr><tr><td></td><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr><tr><td></td><td></td><td></td><td>Jabatan</td><td>:</td><td>{p['jab']}</td></tr>" for i, p in enumerate(daftar)])
        
        html_out += f'''<div class="kertas">{kop_spt}
            <div class="judul-rapat"><h3>SURAT PERINTAH TUGAS</h3><p>NOMOR : {no_spt}</p></div>
            <div class="isi-surat-spt">
                <table class="visum-table"><tr><td width="12%">Dasar</td><td width="3%">:</td><td>{anggaran}</td></tr></table>
                <p class="text-center text-bold" style="margin:15px 0; letter-spacing:4px;">M E M E R I N T A H K A N</p>
                <table class="visum-table">{p_rows}</table>
                <table class="visum-table" style="margin-top:15px;"><tr><td width="12%">Untuk</td><td width="3%">:</td><td>{maksud} ke {tujuan}</td></tr></table>
            </div>
            <div style="margin-top:30px; margin-left:50%;">
                <table class="visum-table"><tr><td width="40%">Ditetapkan di</td><td width="5%">:</td><td>Bajawa</td></tr><tr><td>Pada Tanggal</td><td>:</td><td>{datetime.now().strftime('%d %B %Y')}</td></tr></table><br>
                {render_ttd(80)}
            </div>
        </div>'''

    # 2. SPD DEPAN
    kop_pemda = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p class="text-bold">BAJAWA</p></td><td width="15%"></td></tr></table>'''
    for p in daftar:
        if "SPD Depan" in opsi_cetak:
            html_out += f'''<div class="kertas">{kop_pemda}<div style="margin-left:60%; line-height:1.0;"><table class="visum-table"><tr><td width="40%">Lembar ke</td><td width="5%">:</td><td>{p["lembar"]}</td></tr><tr><td>Kode No</td><td>:</td><td>094/Prokopim</td></tr><tr><td>Nomor</td><td>:</td><td>{p["spd"]}</td></tr></table></div><div class="judul-rapat" style="margin-top:5px;"><h3>SURAT PERJALANAN DINAS</h3><h3>(SPD)</h3></div><table class="tabel-border" style="margin-top:10px;">
                <tr><td class="col-no">1.</td><td width="42%">Pejabat pemberi perintah</td><td colspan="3"><b>BUPATI NGADA</b></td></tr>
                <tr><td class="col-no">2.</td><td>Nama Pegawai diperintah</td><td colspan="3"><b>{p['nama']}</b></td></tr>
                <tr><td class="col-no" rowspan="3">3.</td><td>a. Pangkat/Golongan</td><td colspan="3">{p['gol']}</td></tr>
                <tr><td>b. Jabatan</td><td colspan="3">{p['jab']}</td></tr>
                <tr><td>c. Tingkat Peraturan</td><td colspan="3">-</td></tr>
                <tr><td class="col-no">4.</td><td>Maksud Perjalanan Dinas</td><td colspan="3">{maksud}</td></tr>
                <tr><td class="col-no">5.</td><td>Alat angkut</td><td colspan="3">Mobil Dinas</td></tr>
                <tr><td class="col-no" rowspan="2">6.</td><td>a. Tempat Berangkat</td><td colspan="3">Bajawa</td></tr>
                <tr><td>b. Tempat Tujuan</td><td colspan="3">{tujuan}</td></tr>
                <tr><td class="col-no" rowspan="3">7.</td><td>Lamanya Perjalanan Dinas</td><td colspan="3">...</td></tr>
                <tr><td>a. Tanggal Berangkat</td><td colspan="3">{tgl_bkt}</td></tr>
                <tr><td>b. Tanggal Harus Kembali</td><td colspan="3">{tgl_kbl}</td></tr>
                <tr><td class="col-no">10.</td><td>Keterangan lain-lain</td><td colspan="3">-</td></tr>
            </table><div style="margin-top:15px;">{render_ttd(60)}</div></div>'''

    # 3. SPD BELAKANG (VISUM DALAM DAERAH)
    if "SPD Belakang" in opsi_cetak:
        ttd_bk = render_ttd(65)
        def rv(num, label, val, d_v): return f'''<table class="visum-table"><tr><td width="10%">{num}</td><td width="35%">{label}</td><td width="5%">:</td><td>{val}</td></tr><tr><td></td><td>Pada Tanggal</td><td>:</td><td>{d_v}</td></tr></table>'''

        html_out += f'''<div class="kertas"><table class="tabel-border" style="height:90%;">
            <tr style="height: 220px;"><td width="50%"></td><td style="padding:10px;">{rv("I.", "Berangkat dari", "Bajawa", tgl_bkt)}<table class="visum-table"><tr><td width="10%"></td><td width="35%">Ke</td><td width="5%">:</td><td>{tujuan}</td></tr></table>{ttd_bk}</td></tr>
            <tr style="height: 180px;"><td>{rv("II.", "Tiba di", tujuan, tgl_bkt)}</td><td><table class="visum-table"><tr><td width="10%"></td><td width="35%">Berangkat dari</td><td width="5%">:</td><td>{tujuan}</td></tr><tr><td></td><td>Ke</td><td>:</td><td>Bajawa</td></tr><tr><td></td><td>Pada Tanggal</td><td>:</td><td>{tgl_kbl}</td></tr></table></td></tr>
            <tr style="height: 180px;"><td>{rv("III.", "Tiba di", "", "")}</td><td></td></tr>
            <tr style="height: 220px;"><td>{rv("V.", "Tiba Kembali", "Bajawa", tgl_kbl)}</td><td style="padding:10px;"><p style="font-style:italic; font-size:9.2pt; line-height:1.2;">Telah diperiksa, dengan keterangan bahwa perjalanan tersebut atas perintahnya...</p>{ttd_bk}</td></tr>
        </table><div style="border:1pt solid black; border-top:none; padding:8px; font-size:10.5pt;"><b>VI. Catatan Lain-lain</b></div><div style="border:1pt solid black; border-top:none; padding:8px; font-size:8.8pt; text-align:justify; color:black; line-height:1.2;"><b>VII. Perhatian :</b> Pejabat yang menerbitkan SPD... bertanggung jawab...</div></div>'''

html_out += '</div>'
st.markdown(html_out, unsafe_allow_html=True)
