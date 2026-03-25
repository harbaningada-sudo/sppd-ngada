import streamlit as st
import pandas as pd
from datetime import datetime
import logo  # Pastikan file logo.py kamu punya variabel GARUDA dan PEMDA

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

    .kertas { 
        background-color: white !important; width: 215.9mm; height: 330mm; 
        padding: 10mm 15mm; margin-bottom: 20px; color: black !important; 
        font-family: Arial, sans-serif; box-sizing: border-box; box-shadow: 0 0 20px rgba(0,0,0,0.8);
        font-size: 10.5pt; page-break-after: always; overflow: hidden; position: relative;
    }

    /* KOP GARUDA (KHUSUS SPT LUAR DAERAH) */
    .kop-garuda { text-align: center; margin-bottom: 15px; line-height: 1.0; width: 100%; }
    .kop-garuda img { width: 70px; margin-bottom: 8px; }
    .kop-garuda h2 { margin: 0; font-size: 16pt; font-weight: bold; letter-spacing: 2px; text-transform: uppercase; }

    /* KOP PEMDA (UNTUK SPD) */
    .kop-table { width: 100%; border: none !important; border-bottom: 3.5pt solid black !important; margin-bottom: 5px; }
    .kop-table td { border: none !important; padding: 0 !important; vertical-align: middle; }
    .kop-teks { text-align: center; line-height: 1.0 !important; } 
    .kop-teks h3, .kop-teks h2 { margin: 0; line-height: 1.0 !important; padding: 1px 0; }
    
    .judul-rapat { text-align: center; line-height: 1.0 !important; margin-top: 5px; }
    .judul-rapat h3 { margin: 0; line-height: 1.0 !important; font-weight: bold; text-decoration: underline; }
    .isi-surat-spt { line-height: 1.5 !important; margin-top: 10px; }

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
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 PANEL KONTROL")
    # Fokus Luar Daerah
    st.info("Mode: SPT/SPD Luar Daerah")
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
                "spd": st.text_input(f"No SPD P-{i+1}", f"530/.../2026", key=f"spd{i}"),
                "lembar": st.text_input(f"Lembar ke P-{i+1}", "I", key=f"lbr{i}")
            })

    with st.expander("📄 DATA UTAMA"):
        no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
        kode_spd = st.text_input("Kode No SPD", "094/Prokopim")
        maksud = st.text_area("Maksud Tugas", "Dalam rangka mendampingi...")
        tujuan = st.text_input("Tempat Tujuan", "Labuan Bajo")
        alat = st.text_input("Alat Angkut", "Mobil Dinas")
        lama = st.text_input("Lama Hari", "3 (Tiga) hari")
        tgl_bkt = st.text_input("Tanggal Berangkat", "17 Maret 2026")
        tgl_kbl = st.text_input("Tanggal Pulang", "20 Maret 2026")
        anggaran = st.text_input("Dasar Anggaran", "DPA Bagian Perekonomian dan SDA Setda Ngada 2026")

    with st.expander("🏢 PENGESAH TUJUAN"):
        instansi_tujuan = st.text_input("Instansi Tujuan", "Kantor Gubernur NTT")
        pjb_tujuan = st.text_input("Pejabat Pengesah", "Nama Pejabat")
        gol_tujuan = st.text_input("Gol Pejabat Tujuan", "Pembina Utama Muda, IV/c")
        nip_tujuan = st.text_input("NIP Pejabat Tujuan", "19XXXXXXXXXXXXXX")

    st.subheader("🖋️ TANDA TANGAN ASAL")
    ttd_label_spt = st.selectbox("Label Jabatan SPT", ["BUPATI NGADA", "WAKIL BUPATI NGADA", "An. BUPATI NGADA"])
    pjb = st.text_input("Nama Pejabat Asal", "BERNADINUS DHEY NGEBU, SP")
    gol_pjb = st.text_input("Pangkat/Gol Asal", "Pembina Utama Madya")
    nip_ttd = st.text_input("NIP Pejabat Asal", "19650101 198603 1 045")

    if st.button("🖨️ CETAK SEKARANG"):
        st.components.v1.html("<script>setTimeout(function(){ window.parent.print(); }, 1200);</script>", height=0)

# --- TEMPLATE RENDER ---
def get_ttd_statis(nama, gol, nip, label, space=70):
    return f'''<div style="text-align:center; line-height:1.2; font-size:10.5pt;"><b>{label}</b><br><div style="height:{space}px;"></div><b><u>{nama}</u></b><br>{gol}<br>NIP. {nip}</div>'''

html_out = '<div class="main-container">'

# 1. SPT (KOP GARUDA)
if "SPT" in opsi_cetak:
    kop_spt = f'<div class="kop-garuda"><img src="data:image/png;base64,{logo.GARUDA}"><h2>BUPATI NGADA</h2></div>'
    p_rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{i+1}.</td><td width='20%'>Nama</td><td width='5%'>:</td><td><b>{p['nama']}</b></td></tr><tr><td></td><td></td><td></td><td>Pangkat/Gol</td><td>:</td><td>{p['gol']}</td></tr><tr><td></td><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr><tr><td></td><td></td><td></td><td>Jabatan</td><td>:</td><td>{p['jab']}</td></tr>" for i, p in enumerate(daftar)])
    html_out += f'''<div class="kertas">{kop_spt}
        <div class="judul-rapat"><h3>SURAT PERINTAH TUGAS</h3><p>NOMOR : {no_spt}</p></div>
        <div class="isi-surat-spt">
            <table class="visum-table"><tr><td width="12%">Dasar</td><td width="5%">:</td><td>{anggaran}</td></tr></table>
            <p class="text-center text-bold" style="margin:10px 0; letter-spacing:4px;">M E M E R I N T A H K A N</p>
            <table class="visum-table">{p_rows}</table>
            <table class="visum-table" style="margin-top:10px;"><tr><td width="12%">Untuk</td><td width="5%">:</td><td>{maksud} ke {tujuan}</td></tr></table>
        </div>
        <div style="margin-left:55%; margin-top:20px;">
            <table class="visum-table">
                <tr><td width="40%">Ditetapkan di</td><td width="5%">:</td><td>Bajawa</td></tr>
                <tr><td>Pada Tanggal</td><td>:</td><td>{datetime.now().strftime('%d %B %Y')}</td></tr>
            </table>
            {get_ttd_statis(pjb, gol_pjb, nip_ttd, ttd_label_spt, 80)}
        </div></div>'''

# 2. SPD DEPAN (KOP PEMDA)
kop_pemda = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p class="text-bold">BAJAWA</p></td><td width="15%"></td></tr></table>'''
for p in daftar:
    if "SPD Depan" in opsi_cetak:
        html_out += f'''<div class="kertas">{kop_pemda}<div style="margin-left:60%; line-height:1.0;"><table class="visum-table"><tr><td width="40%">Lembar ke</td><td width="5%">:</td><td>{p["lembar"]}</td></tr><tr><td>Kode No</td><td>:</td><td>{kode_spd}</td></tr><tr><td>Nomor</td><td>:</td><td>{p["spd"]}</td></tr></table></div><div class="judul-rapat" style="margin-top:5px;"><h3>SURAT PERJALANAN DINAS</h3><h3>(SPD)</h3></div><table class="tabel-border" style="margin-top:10px;">
            <tr><td class="col-no">1.</td><td width="42%">Pejabat pemberi perintah</td><td colspan="3"><b>BUPATI NGADA</b></td></tr>
            <tr><td class="col-no">2.</td><td>Nama Pegawai diperintah</td><td colspan="3"><b>{p['nama']}</b></td></tr>
            <tr><td class="col-no" rowspan="3">3.</td><td>a. Pangkat/Golongan</td><td colspan="3">{p['gol']}</td></tr>
            <tr><td>b. Jabatan</td><td colspan="3">{p['jab']}</td></tr>
            <tr><td>c. Tingkat Menurut Peraturan</td><td colspan="3">-</td></tr>
            <tr><td class="col-no">4.</td><td>Maksud Perjalanan Dinas</td><td colspan="3">{maksud}</td></tr>
            <tr><td class="col-no">5.</td><td>Alat angkut</td><td colspan="3">{alat}</td></tr>
            <tr><td class="col-no" rowspan="2">6.</td><td>a. Tempat Berangkat</td><td colspan="3">Bajawa</td></tr>
            <tr><td>b. Tempat Tujuan</td><td colspan="3">{tujuan}</td></tr>
            <tr><td class="col-no" rowspan="3">7.</td><td>Lamanya Perjalanan Dinas</td><td colspan="3">{lama}</td></tr>
            <tr><td>a. Tanggal Berangkat</td><td colspan="3">{tgl_bkt}</td></tr>
            <tr><td>b. Tanggal Harus Kembali</td><td colspan="3">{tgl_kbl}</td></tr>
            <tr><td class="col-no">10.</td><td>Keterangan lain-lain</td><td colspan="3">-</td></tr>
        </table><div style="margin-left:55%; margin-top:10px;">{get_ttd_statis(pjb, gol_pjb, nip_ttd, "An. BUPATI NGADA", 65)}</div></div>'''

# 3. SPD BELAKANG (POIN II KIRI BERSIH)
if "SPD Belakang" in opsi_cetak:
    ttd_asal = get_ttd_statis(pjb, gol_pjb, nip_ttd, "An. BUPATI NGADA", 60)
    ttd_tujuan = f'''<div style="text-align:center; line-height:1.2; font-size:10pt;"><br><b>Mengesahkan</b><br>{instansi_tujuan}<div style="height:65px;"></div><b><u>{pjb_tujuan}</u></b><br>{gol_tujuan}<br>NIP. {nip_tujuan}</div>'''

    def rv(num, label, val, d_v, is_n=True):
        n_c = f'<td width="10%">{num}</td>' if is_n else ""
        return f'''<table class="visum-table"><tr>{n_c}<td width="35%">{label}</td><td width="5%">:</td><td>{val}</td></tr><tr>{"<td></td>" if is_n else ""}<td>Pada Tanggal</td><td>:</td><td>{d_v}</td></tr></table>'''

    html_out += f'''<div class="kertas"><table class="tabel-border" style="height:88%;">
        <tr style="height: 220px;"><td width="50%"></td><td style="padding:10px;">{rv("I.", "Berangkat dari", "Bajawa", tgl_bkt)}<table class="visum-table"><tr><td width="10%"></td><td width="35%">Ke</td><td width="5%">:</td><td>{tujuan}</td></tr></table>{ttd_asal}</td></tr>
        <tr style="height: 190px;"><td>{rv("II.", "Tiba di", tujuan, tgl_bkt)}</td><td style="padding:10px;">{rv("", "Berangkat dari", tujuan, tgl_kbl, False)}<table class="visum-table"><tr><td width="35%">Ke</td><td width="5%">:</td><td>Bajawa</td></tr></table>{ttd_tujuan}</td></tr>
        <tr style="height: 190px;"><td>{rv("III.", "Tiba di", "", "")}</td><td style="padding:10px;">{rv("", "Berangkat dari", "", "", False)}</td></tr>
        <tr style="height: 190px;"><td>{rv("IV.", "Tiba di", "", "")}</td><td style="padding:10px;">{rv("", "Berangkat dari", "", "", False)}</td></tr>
        <tr style="height: 220px;"><td>{rv("V.", "Tiba Kembali", "Bajawa", tgl_kbl)}</td><td style="padding:10px;"><p style="font-style:italic; font-size:9.2pt; line-height:1.2; margin-top:5px;">Telah diperiksa, dengan keterangan bahwa perjalanan tersebut atas perintahnya dan semata-mata untuk kepentingan jabatan</p>{ttd_asal}</td></tr>
    </table>
    <div style="border:1pt solid black; border-top:none; padding:8px; font-size:10.5pt;"><b>VI. Catatan Lain-lain</b></div>
    <div style="border:1pt solid black; border-top:none; padding:8px; font-size:8.6pt; text-align:justify; color:black; line-height:1.2;">
        <b>VII. Perhatian :</b><br>
        Pejabat yang menerbitkan SPD, pegawai yang melakukan perjalanan dinas, para pejabat yang mengesahkan tanggal berangkat/tiba, serta Bendahara Pengeluaran bertanggung jawab berdasarkan peraturan-peraturan Keuangan Negara apabila negara menderita rugi akibat kesalahan, kelalaian dan kealpaannya.
    </div></div>'''

html_out += '</div>'
st.markdown(html_out, unsafe_allow_html=True)
