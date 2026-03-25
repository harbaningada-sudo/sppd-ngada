import streamlit as st
import pandas as pd
from datetime import datetime
import logo  

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Ngada Pro", layout="wide")

if 'arsip_register' not in st.session_state:
    st.session_state.arsip_register = []

# CSS UNTUK PRESISI CETAK FULL LEGAL
st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    .stApp { background-color: #525659 !important; }
    .main-container { display: flex; flex-direction: column; align-items: center; width: 100%; padding: 10px 0; }

    .kertas { 
        background-color: white !important; width: 215.9mm; height: 330mm; 
        padding: 10mm 15mm; margin-bottom: 20px; color: black !important; 
        font-family: Arial, sans-serif; box-sizing: border-box; box-shadow: 0 0 20px rgba(0,0,0,0.8);
        font-size: 10.5pt; page-break-after: always; overflow: hidden; position: relative;
    }

    /* KHUSUS KOP GARUDA LUAR DAERAH */
    .kop-garuda { text-align: center; margin-bottom: 10px; line-height: 1.0; }
    .kop-garuda img { width: 75px; margin-bottom: 5px; }
    .kop-garuda h2 { margin: 0; font-size: 16pt; font-weight: bold; letter-spacing: 2px; }

    .kop-table { width: 100%; border: none !important; border-bottom: 3.5pt solid black !important; margin-bottom: 5px; }
    .kop-table td { border: none !important; padding: 0 !important; vertical-align: middle; }
    .kop-teks { text-align: center; line-height: 1.0 !important; } 
    .kop-teks h3, .kop-teks h2, .kop-teks p { margin: 0; line-height: 1.0 !important; padding: 1px 0; }
    
    .judul-rapat { text-align: center; line-height: 1.0 !important; margin-top: 5px; }
    .judul-rapat h3 { margin: 0; font-weight: bold; text-decoration: underline; }

    .tabel-border { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; table-layout: fixed; }
    .tabel-border td { border: 1pt solid black !important; padding: 4px 8px !important; vertical-align: top; color: black !important; font-size: 10pt; line-height: 1.0 !important; }
    
    .visum-table { width: 100%; border: none !important; border-collapse: collapse; margin: 0 !important; }
    .visum-table td { border: none !important; padding: 0 !important; font-size: 10pt; line-height: 1.0 !important; color: black !important; vertical-align: top; }

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
    # PEMISAH JALUR UTAMA
    mode_wilayah = st.selectbox("Pilih Jenis Perjalanan", ["Dalam Daerah", "Luar Daerah"])
    
    opsi_cetak = st.multiselect("Pilih Dokumen", ["SPT", "SPD Depan", "SPD Belakang"], default=["SPT", "SPD Depan", "SPD Belakang"])
    
    with st.expander("👤 DATA PEGAWAI", expanded=True):
        if 'jml' not in st.session_state: st.session_state.jml = 1
        c1, c2 = st.columns(2)
        if c1.button("➕ Tambah"): st.session_state.jml += 1
        if c2.button("➖ Hapus") and st.session_state.jml > 1: st.session_state.jml -= 1
        
        daftar = []
        for i in range(st.session_state.jml):
            daftar.append({
                "nama": st.text_input(f"Nama {i+1}", f"Nama {i+1}", key=f"n{i}"),
                "nip": st.text_input(f"NIP", "19XXXXXXXXXXXXXX", key=f"nip{i}"),
                "gol": st.text_input(f"Gol", "III/a", key=f"g{i}"),
                "jab": st.text_input(f"Jabatan", "Pelaksana", key=f"j{i}"),
                "spd": st.text_input(f"No SPD", f"530 /02/2026", key=f"spd{i}")
            })

    with st.expander("📄 DATA UTAMA"):
        no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
        maksud = st.text_area("Maksud Perjalanan", "Dalam rangka mendampingi...")
        tujuan = st.text_input("Tujuan", "Kecamatan Riung")
        tgl_bkt = st.text_input("Tgl Berangkat", "17 Maret 2026")
        tgl_kbl = st.text_input("Tgl Pulang", "17 Maret 2026")
        anggaran = st.text_input("Dasar Anggaran", "DPA Bagian Perekonomian dan SDA 2026")

    if mode_wilayah == "Luar Daerah":
        with st.expander("🏢 KHUSUS LUAR DAERAH"):
            instansi_tujuan = st.text_input("Instansi Tujuan", "Kantor Gubernur NTT")
            pjb_tujuan = st.text_input("Nama Pejabat Tujuan", "Nama Pejabat")
            gol_tujuan = st.text_input("Gol Tujuan", "IV/c")
            nip_tujuan = st.text_input("NIP Pejabat Tujuan", "19XXXXXXXXXXXXXX")

    st.subheader("🖋️ TANDA TANGAN")
    pjb = st.text_input("Nama Pejabat", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
    gol_pjb = st.text_input("Pangkat/Gol", "Pembina Utama Muda - IV/c")
    jab_ttd = st.text_input("Jabatan Utama", "Pj. Sekretaris Daerah")
    ub = st.text_input("Ub.", "Asisten Perekonomian dan Pembangunan")
    nip_ttd = st.text_input("NIP", "19710328 199203 1 011")

    if st.button("🖨️ PROSES CETAK"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

# --- KOMPONEN ---
def get_ttd(space): 
    return f'''<div style="margin-left:55%; margin-top:10px; line-height:1.0; text-align:center;"><b>An. BUPATI NGADA</b><br>{jab_ttd},<br>{f"Ub. {ub}," if ub else ""}<div style="height:{space}px;"></div><b><u>{pjb}</u></b><br>{gol_pjb}<br>NIP. {nip_ttd}</div>'''

kop_pemda = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>BAJAWA</p></td><td width="15%"></td></tr></table>'''

html_out = '<div class="main-container">'

# ==========================================
# JALUR 1: DALAM DAERAH (KODE ASLI ANDA)
# ==========================================
if mode_wilayah == "Dalam Daerah":
    if "SPT" in opsi_cetak:
        p_rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{i+1}.</td><td width='20%'>Nama</td><td width='5%'>:</td><td><b>{p['nama']}</b></td></tr><tr><td></td><td></td><td></td><td>Pangkat/Gol</td><td>:</td><td>{p['gol']}</td></tr><tr><td></td><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr><tr><td></td><td></td><td></td><td>Jabatan</td><td>:</td><td>{p['jab']}</td></tr>" for i, p in enumerate(daftar)])
        html_out += f'<div class="kertas">{kop_pemda}<div class="judul-rapat"><h3>SURAT PERINTAH TUGAS</h3><p>NOMOR : {no_spt}</p></div><div class="isi-surat-spt"><table class="visum-table"><tr><td width="12%">Dasar</td><td width="5%">:</td><td>{anggaran}</td></tr></table><p class="text-center text-bold" style="margin:10px 0;">M E M E R I N T A H K A N</p><table class="visum-table">{p_rows}</table><table class="visum-table" style="margin-top:10px;"><tr><td width="12%">Untuk</td><td width="5%">:</td><td>{maksud} ke {tujuan}</td></tr></table></div>{get_ttd(90)}</div>'
    for p in daftar:
        if "SPD Depan" in opsi_cetak:
            html_out += f'''<div class="kertas">{kop_pemda}<div style="margin-left:60%; line-height:1.0;">Kode No: 094<br>Nomor: {p["spd"]}</div><div class="judul-rapat"><h3>SURAT PERJALANAN DINAS</h3></div><table class="tabel-border"><tr><td class="col-no">1.</td><td width="42%">Pejabat pemberi perintah</td><td><b>BUPATI NGADA</b></td></tr><tr><td class="col-no">2.</td><td>Nama Pegawai</td><td><b>{p['nama']}</b></td></tr><tr><td class="col-no">4.</td><td>Maksud Perjalanan</td><td>{maksud}</td></tr><tr><td class="col-no">6.</td><td>Tempat Tujuan</td><td>{tujuan}</td></tr></table>{get_ttd(75)}</div>'''
    if "SPD Belakang" in opsi_cetak:
        ttd_bk = get_ttd(65)
        def rv(n, l, v, d): return f'''<table class="visum-table"><tr><td width="10%">{n}</td><td width="35%">{l}</td><td width="5%">:</td><td>{v}</td></tr><tr><td></td><td>Pada Tanggal</td><td>:</td><td>{d}</td></tr></table>'''
        html_out += f'''<div class="kertas"><table class="tabel-border" style="height:88%;"><tr><td width="50%"></td><td style="padding:10px;">{rv("I.", "Berangkat dari", "Bajawa", tgl_bkt)}<br>{ttd_bk}</td></tr><tr><td>{rv("II.", "Tiba di", tujuan, tgl_bkt)}</td><td style="padding:10px;">{rv("", "Berangkat dari", tujuan, tgl_kbl)}</td></tr><tr><td>{rv("V.", "Tiba Kembali", "Bajawa", tgl_kbl)}</td><td style="padding:10px;"><p style="font-style:italic;">Telah diperiksa...</p>{ttd_bk}</td></tr></table></div>'''

# ==========================================
# JALUR 2: LUAR DAERAH (KODE BARU LOGO GARUDA)
# ==========================================
else:
    if "SPT" in opsi_cetak:
        p_rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{i+1}.</td><td width='20%'>Nama</td><td width='5%'>:</td><td><b>{p['nama']}</b></td></tr><tr><td></td><td></td><td></td><td>Pangkat/Gol</td><td>:</td><td>{p['gol']}</td></tr><tr><td></td><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr><tr><td></td><td></td><td></td><td>Jabatan</td><td>:</td><td>{p['jab']}</td></tr>" for i, p in enumerate(daftar)])
        html_out += f'''<div class="kertas">
            <div class="kop-garuda"><img src="data:image/png;base64,{logo.GARUDA}"><h2>BUPATI NGADA</h2></div>
            <div class="judul-rapat"><h3>SURAT PERINTAH TUGAS</h3><p>NOMOR : {no_spt}</p></div>
            <div class="isi-surat-spt">
                <table class="visum-table"><tr><td width="12%">Dasar</td><td width="5%">:</td><td>{anggaran}</td></tr></table>
                <p class="text-center text-bold" style="margin:10px 0;">M E M E R I N T A H K A N</p>
                <table class="visum-table">{p_rows}</table>
                <div style="height:25px;"></div>
                <table class="visum-table"><tr><td width="12%">Untuk</td><td width="5%">:</td><td>{maksud} ke {tujuan}</td></tr></table>
            </div>{get_ttd(90)}</div>'''
    for p in daftar:
        if "SPD Depan" in opsi_cetak:
            html_out += f'''<div class="kertas">{kop_pemda}<div style="margin-left:60%; line-height:1.0;">Kode No: 094<br>Nomor: {p["spd"]}</div><div class="judul-rapat"><h3>SURAT PERJALANAN DINAS</h3></div><table class="tabel-border"><tr><td class="col-no">1.</td><td width="42%">Pejabat pemberi perintah</td><td><b>BUPATI NGADA</b></td></tr><tr><td class="col-no">2.</td><td>Nama Pegawai</td><td><b>{p['nama']}</b></td></tr><tr><td class="col-no">4.</td><td>Maksud Perjalanan</td><td>{maksud}</td></tr></table>{get_ttd(75)}</div>'''
    if "SPD Belakang" in opsi_cetak:
        ttd_bk = get_ttd(65)
        ttd_tujuan_ld = f'''<div style="text-align:center; line-height:1.0; font-size:10pt;"><br><b>Mengesahkan</b><br>{instansi_tujuan}<div style="height:60px;"></div><b><u>{pjb_tujuan}</u></b><br>{gol_tujuan}<br>NIP. {nip_tujuan}</div>'''
        def rv_ld(n, l, v, d): return f'''<table class="visum-table"><tr><td width="10%">{n}</td><td width="35%">{l}</td><td width="5%">:</td><td>{v}</td></tr><tr><td></td><td>Pada Tanggal</td><td>:</td><td>{d}</td></tr></table>'''
        html_out += f'''<div class="kertas"><table class="tabel-border" style="height:88%;"><tr><td width="50%"></td><td style="padding:10px;">{rv_ld("I.", "Berangkat dari", "Bajawa", tgl_bkt)}<br>{ttd_bk}</td></tr><tr><td><table class="visum-table"><tr><td width="10%">II.</td><td width="35%">Tiba di</td><td>: {tujuan}</td></tr></table></td><td style="padding:10px;">{rv_ld("", "Berangkat dari", tujuan, tgl_kbl)}<br>{ttd_tujuan_ld}</td></tr><tr><td>{rv_ld("V.", "Tiba Kembali", "Bajawa", tgl_kbl)}</td><td style="padding:10px;"><p style="font-style:italic;">Telah diperiksa...</p>{ttd_bk}</td></tr></table></div>'''

html_out += '</div>'
st.markdown(html_out, unsafe_allow_html=True)
