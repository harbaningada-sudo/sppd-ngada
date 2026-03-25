import streamlit as st
import pandas as pd
from datetime import datetime
import logo  # Memanggil file logo.py di repository kamu

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Ngada Pro", layout="wide")

# INISIALISASI DATABASE REGISTER
if 'arsip_register' not in st.session_state:
    st.session_state.arsip_register = []

# CSS UNTUK PRESISI CETAK FULL LEGAL & LANDSCAPE REGISTER
st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    .stApp { background-color: #525659 !important; }
    .main-container { display: flex; flex-direction: column; align-items: center; width: 100%; padding: 10px 0; }

    /* KERTAS UMUM (PORTRAIT LEGAL) */
    .kertas { 
        background-color: white !important; width: 215.9mm; height: 330mm; 
        padding: 10mm 15mm; margin-bottom: 20px; color: black !important; 
        font-family: Arial, sans-serif; box-sizing: border-box; box-shadow: 0 0 20px rgba(0,0,0,0.8);
        font-size: 10.5pt; page-break-after: always; overflow: hidden; position: relative;
    }

    /* KHUSUS KOP GARUDA (LUAR DAERAH) */
    .kop-garuda { text-align: center; margin-bottom: 10px; line-height: 1.0; width: 100%; }
    .kop-garuda img { width: 70px; margin-bottom: 5px; }
    .kop-garuda h2 { margin: 0; font-size: 16pt; font-weight: bold; letter-spacing: 2px; }

    /* KOP PEMDA */
    .kop-table { width: 100%; border: none !important; border-bottom: 3.5pt solid black !important; margin-bottom: 5px; }
    .kop-table td { border: none !important; padding: 0 !important; vertical-align: middle; }
    .kop-teks { text-align: center; line-height: 1.0 !important; } 
    .kop-teks h3, .kop-teks h2, .kop-teks p { margin: 0; line-height: 1.0 !important; padding: 1px 0; }
    
    .judul-rapat { text-align: center; line-height: 1.0 !important; margin-top: 5px; }
    .judul-rapat h3, .judul-rapat p { margin: 0; line-height: 1.0 !important; }

    /* TABEL SPD DEPAN */
    .tabel-border { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; table-layout: fixed; }
    .tabel-border td { border: 1pt solid black !important; padding: 4px 8px !important; vertical-align: top; color: black !important; font-size: 10pt; line-height: 1.1 !important; }
    .col-no { width: 30px !important; text-align: center !important; }

    /* TABEL VISUM BELAKANG */
    .visum-table { width: 100%; border: none !important; border-collapse: collapse; margin: 0 !important; }
    .visum-table td { border: none !important; padding: 0 !important; font-size: 10pt; line-height: 1.2; color: black !important; vertical-align: top; }

    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }

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
    wilayah = st.selectbox("Jenis Wilayah", ["Dalam Daerah", "Luar Daerah"])
    
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
                "jab": st.text_input(f"Jab P-{i+1}", "Pelaksana", key=f"j{i}"),
                "spd": st.text_input(f"No SPD P-{i+1}", f"530 /02/2026", key=f"spd{i}"),
                "lembar": st.text_input(f"Lembar ke P-{i+1}", "I", key=f"lbr{i}")
            })

    with st.expander("📄 DATA UTAMA"):
        no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
        kode_spd = st.text_input("Kode No SPD", "094/Prokopim")
        default_dasar = "DPA Bagian Perekonomian dan SDA Setda Ngada Tahun Anggaran 2026" if wilayah == "Dalam Daerah" else ""
        anggaran = st.text_area("Dasar SPT", value=default_dasar)
        maksud = st.text_area("Maksud Perjalanan", "Dalam rangka mendampingi...")
        tujuan = st.text_input("Tujuan", "Kecamatan Riung")
        alat = st.text_input("Alat Angkut", "Mobil Dinas")
        lama = st.text_input("Lama Hari", "1 (Satu) hari")
        tgl_bkt = st.text_input("Tanggal Berangkat", "17 Maret 2026")
        tgl_kbl = st.text_input("Tanggal Pulang", "17 Maret 2026")

    st.subheader("🖋️ TANDA TANGAN")
    ttd_label = st.selectbox("Label Jabatan", ["An. BUPATI NGADA", "WAKIL BUPATI NGADA", "BUPATI NGADA"])
    pjb = st.text_input("Nama Pejabat", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
    gol_pjb = st.text_input("Pangkat/Gol", "Pembina Utama Muda - IV/c")
    jab_ttd = st.text_input("Jabatan Utama", "Pj. Sekretaris Daerah")
    ub = st.text_input("Ub.", "Asisten Perekonomian dan Pembangunan")
    nip_ttd = st.text_input("NIP", "19710328 199203 1 011")

    if st.button("🖨️ PROSES CETAK"):
        st.components.v1.html("<script>setTimeout(function(){ window.parent.print(); }, 1200);</script>", height=0)

# --- FUNGSI TTD ---
def get_ttd(space): 
    label_final = f"<b>{ttd_label}</b>"
    jab_final = f"{jab_ttd}," if ttd_label == "An. BUPATI NGADA" else ""
    ub_final = f"Ub. {ub}," if (ub and ttd_label == "An. BUPATI NGADA") else ""
    return f'''<div style="margin-left:55%; margin-top:10px; line-height:1.2; text-align:center;">{label_final}<br>{jab_final}<br>{ub_final}<div style="height:{space}px;"></div><b><u>{pjb}</u></b><br>{gol_pjb}<br>NIP. {nip_ttd}</div>'''

html_out = '<div class="main-container">'

# 1. SPD DEPAN (Template Diperbaiki)
kop_pemda = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p class="text-bold">BAJAWA</p></td><td width="15%"></td></tr></table>'''

for p in daftar:
    html_out += f'''<div class="kertas">{kop_pemda}
        <div style="margin-left:60%; line-height:1.2;">
            <table class="visum-table">
                <tr><td width="40%">Lembar ke</td><td width="5%">:</td><td>{p["lembar"]}</td></tr>
                <tr><td>Kode No</td><td>:</td><td>{kode_spd}</td></tr>
                <tr><td>Nomor</td><td>:</td><td>{p["spd"]}</td></tr>
            </table>
        </div>
        <div class="judul-rapat" style="margin-top:10px;">
            <h3 class="text-bold underline">SURAT PERJALANAN DINAS</h3>
            <h3 class="text-bold">(SPD)</h3>
        </div>
        <table class="tabel-border" style="margin-top:15px;">
            <tr><td class="col-no">1.</td><td width="45%">Pejabat pemberi perintah</td><td colspan="2"><b>BUPATI NGADA</b></td></tr>
            <tr><td class="col-no">2.</td><td>Nama Pegawai diperintah</td><td colspan="2"><b>{p['nama']}</b></td></tr>
            <tr><td class="col-no" rowspan="3">3.</td><td>a. Pangkat/Golongan</td><td colspan="2">{p['gol']}</td></tr>
            <tr><td>b. Jabatan</td><td colspan="2">{p['jab']}</td></tr>
            <tr><td>c. Tingkat Menurut Peraturan</td><td colspan="2">-</td></tr>
            <tr><td class="col-no">4.</td><td>Maksud Perjalanan Dinas</td><td colspan="2">{maksud}</td></tr>
            <tr><td class="col-no">5.</td><td>Alat angkut</td><td colspan="2">{alat}</td></tr>
            <tr><td class="col-no" rowspan="2">6.</td><td>a. Tempat Berangkat</td><td colspan="2">Bajawa</td></tr>
            <tr><td>b. Tempat Tujuan</td><td colspan="2">{tujuan}</td></tr>
            <tr><td class="col-no" rowspan="3">7.</td><td>Lamanya Perjalanan Dinas</td><td colspan="2">{lama}</td></tr>
            <tr><td>a. Tanggal Berangkat</td><td colspan="2">{tgl_bkt}</td></tr>
            <tr><td>b. Tanggal Harus Kembali</td><td colspan="2">{tgl_kbl}</td></tr>
            <tr><td class="col-no">9.</td><td>Pembebanan Anggaran</td><td colspan="2">Bagian Perekonomian dan SDA</td></tr>
            <tr><td class="col-no">10.</td><td>Keterangan lain-lain</td><td colspan="2">-</td></tr>
        </table>
        {get_ttd(75)}
    </div>'''

# 2. SPD BELAKANG (Logika Luar Daerah Diperbaiki)
def rv(num, label, val, d_v, is_n=True):
    n_c = f'<td width="10%">{num}</td>' if is_n else ""
    return f'''<table class="visum-table"><tr>{n_c}<td width="35%">{label}</td><td width="5%">:</td><td>{val}</td></tr><tr>{"<td></td>" if is_n else ""}<td>Pada Tanggal</td><td>:</td><td>{d_v}</td></tr></table>'''

# Logika kolom II Kiri (Tiba di)
kolom_kiri_ii = rv("II.", "Tiba di", tujuan, tgl_bkt) if wilayah == "Dalam Daerah" else f'<table class="visum-table"><tr><td width="10%">II.</td><td width="35%">Tiba di</td><td width="5%">:</td><td>{tujuan}</td></tr></table>'
ttd_bk = get_ttd(65)

html_out += f'''<div class="kertas"><table class="tabel-border" style="height:88%;">
    <tr style="height: 220px;"><td width="50%"></td><td style="padding:10px;">{rv("I.", "Berangkat dari", "Bajawa", tgl_bkt)}<table class="visum-table"><tr><td width="10%"></td><td width="35%">Ke</td><td width="5%">:</td><td>{tujuan}</td></tr></table>{ttd_bk}</td></tr>
    <tr style="height: 190px;"><td>{kolom_kiri_ii}</td><td style="padding:10px;">{rv("", "Berangkat dari", tujuan, tgl_kbl, False)}<table class="visum-table"><tr><td width="35%">Ke</td><td width="5%">:</td><td>Bajawa</td></tr></table></td></tr>
    <tr style="height: 190px;"><td>{rv("III.", "Tiba di", "", "", True)}</td><td style="padding:10px;">{rv("", "Berangkat dari", "", "", False)}</td></tr>
    <tr style="height: 220px;"><td>{rv("V.", "Tiba Kembali", "Bajawa", tgl_kbl)}</td><td style="padding:10px;"><p style="font-style:italic; font-size:9.2pt; line-height:1.2; margin-top:5px;">Telah diperiksa, dengan keterangan bahwa perjalanan tersebut atas perintahnya dan semata-mata untuk kepentingan jabatan</p>{ttd_bk}</td></tr>
</table>
<div style="border:1pt solid black; border-top:none; padding:8px; font-size:8.6pt; text-align:justify; color:black; line-height:1.2;"><b>VII. Perhatian :</b><br>Pejabat yang menerbitkan SPD, pegawai yang melakukan perjalanan dinas... bertanggung jawab...</div></div>'''

html_out += '</div>'
st.markdown(html_out, unsafe_allow_html=True)
