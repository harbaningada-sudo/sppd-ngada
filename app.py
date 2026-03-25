import streamlit as st
import pandas as pd
from datetime import datetime
import logo 

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Ngada Pro", layout="wide")

# INISIALISASI DATABASE REGISTER (HARUS DI ATAS)
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

    /* KOP KHUSUS GARUDA (UNTUK SPT LUAR DAERAH) */
    .kop-garuda { text-align: center; margin-bottom: 15px; line-height: 1.0; width: 100%; }
    .kop-garuda img { width: 70px; margin-bottom: 8px; }
    .kop-garuda h2 { margin: 0; font-size: 16pt; font-weight: bold; letter-spacing: 2px; }

    .kop-table { width: 100%; border: none !important; border-bottom: 3.5pt solid black !important; margin-bottom: 5px; }
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

# 2. PANEL KONTROL SIDEBAR
with st.sidebar:
    st.header("📋 PANEL KONTROL")
    # Variabel tab_menu didefinisikan di sini
    tab_menu = st.radio("Menu Utama", ["Input & Cetak", "Kelola Register"])
    
    if tab_menu == "Input & Cetak":
        jenis_perjalanan = st.selectbox("Jenis SPT/SPD", ["Dalam Daerah", "Luar Daerah"])
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
                    "jab": st.text_input(f"Jab P-{i+1}", "Pelaksana", key=f"j{i}"),
                    "spd": st.text_input(f"No SPD P-{i+1}", f"530 /02/2026", key=f"spd{i}"),
                    "lembar": "I"
                })

        with st.expander("📄 DATA UTAMA"):
            no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
            maksud = st.text_area("Maksud", "Dalam rangka mendampingi...")
            tujuan = st.text_input("Tujuan", "Kecamatan Riung")
            tgl_bkt = st.text_input("Tgl Berangkat", "17 Maret 2026")
            tgl_kbl = st.text_input("Tgl Pulang", "17 Maret 2026")

    st.subheader("🖋️ TANDA TANGAN")
    pjb = st.text_input("Nama Pejabat", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
    gol_pjb = st.text_input("Pangkat/Gol", "Pembina Utama Muda - IV/c")
    jab_ttd = st.text_input("Jabatan", "Pj. Sekretaris Daerah")
    ub = st.text_input("Ub.", "Asisten Perekonomian dan Pembangunan")
    nip_ttd = st.text_input("NIP", "19710328 199203 1 011")

    if st.button("🖨️ PROSES CETAK"):
        for p in daftar:
            st.session_state.arsip_register.append({"Nama": p['nama'], "Tujuan": tujuan, "Bkt": tgl_bkt})
        st.components.v1.html("<script>setTimeout(function(){ window.parent.print(); }, 1200);</script>", height=0)

# --- TEMPLATE KOMPONEN ---
def get_ttd_statis(space):
    return f'''<div style="text-align:center; line-height:1.2; font-size:10.5pt;"><b>An. BUPATI NGADA</b><br>{jab_ttd},<br>{f"Ub. {ub}," if ub else ""}<div style="height:{space}px;"></div><b><u>{pjb}</u></b><br>{gol_pjb}<br>NIP. {nip_ttd}</div>'''

html_out = '<div class="main-container">'

if tab_menu == "Input & Cetak":
    # 1. SPT
    if "SPT" in opsi_cetak:
        kop = f'<div class="kop-garuda"><img src="data:image/png;base64,{logo.GARUDA}"><h2>BUPATI NGADA</h2></div>' if jenis_perjalanan == "Luar Daerah" else f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>BAJAWA</p></td><td width="15%"></td></tr></table>'''
        p_rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{i+1}.</td><td width='20%'>Nama</td><td width='5%'>:</td><td><b>{p['nama']}</b></td></tr><tr><td></td><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr>" for i, p in enumerate(daftar)])
        html_out += f'<div class="kertas">{kop}<div class="judul-rapat"><h3>SURAT PERINTAH TUGAS</h3><p>NOMOR : {no_spt}</p></div><div class="isi-surat-spt"><table class="visum-table"><tr><td width="12%">Dasar</td><td width="3%">:</td><td>DPA 2026</td></tr></table><p class="text-center text-bold" style="margin:10px 0;">M E M E R I N T A H K A N</p><table class="visum-table">{p_rows}</table><table class="visum-table" style="margin-top:10px;"><tr><td width="12%">Untuk</td><td width="5%">:</td><td>{maksud} ke {tujuan}</td></tr></table></div><div style="margin-left:55%;">{get_ttd_statis(80)}</div></div>'

    # 2. SPD DEPAN
    for p in daftar:
        if "SPD Depan" in opsi_cetak:
            kop_p = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>BAJAWA</p></td><td width="15%"></td></tr></table>'''
            html_out += f'''<div class="kertas">{kop_p}<div style="margin-left:60%; line-height:1.0;">Lembar ke: I<br>Nomor: {p['spd']}</div><div class="judul-rapat"><h3>SURAT PERJALANAN DINAS</h3><h3>(SPD)</h3></div><table class="tabel-border" style="margin-top:10px;">
                <tr><td class="col-no">1.</td><td width="42%">Pejabat pemberi perintah</td><td>BUPATI NGADA</td></tr>
                <tr><td class="col-no">2.</td><td>Nama Pegawai</td><td><b>{p['nama']}</b></td></tr>
                <tr><td class="col-no">4.</td><td>Maksud Perjalanan</td><td>{maksud}</td></tr>
                <tr><td class="col-no">6.</td><td>Tempat Tujuan</td><td>{tujuan}</td></tr>
                <tr><td class="col-no">7.</td><td>Tgl Berangkat</td><td>{tgl_bkt}</td></tr>
            </table><div style="margin-left:55%; margin-top:10px;">{get_ttd_statis(65)}</div></div>'''

    # 3. SPD BELAKANG (Bersih Poin II Kiri)
    if "SPD Belakang" in opsi_cetak:
        ttd_bk = get_ttd_statis(65)
        def rv(num, label, val, d_v): return f'''<table class="visum-table"><tr><td width="10%">{num}</td><td width="35%">{label}</td><td width="5%">:</td><td>{val}</td></tr><tr><td></td><td>Pada Tanggal</td><td>:</td><td>{d_v}</td></tr></table>'''
        html_out += f'''<div class="kertas"><table class="tabel-border" style="height:88%;">
            <tr style="height: 220px;"><td width="50%"></td><td style="padding:10px;">{rv("I.", "Berangkat dari", "Bajawa", tgl_bkt)}<br>{ttd_bk}</td></tr>
            <tr style="height: 190px;"><td>{rv("II.", "Tiba di", tujuan, tgl_bkt)}<br></td><td style="padding:10px;">{rv("", "Berangkat dari", tujuan, tgl_kbl)}</td></tr>
            <tr style="height: 220px;"><td>{rv("V.", "Tiba Kembali", "Bajawa", tgl_kbl)}</td><td style="padding:10px;"><p style="font-style:italic; font-size:9.2pt; line-height:1.2;">Telah diperiksa...</p>{ttd_bk}</td></tr>
        </table><div style="border:1pt solid black; border-top:none; padding:8px; font-size:10.5pt;"><b>VI. Catatan Lain-lain</b></div><div style="border:1pt solid black; border-top:none; padding:8px; font-size:8.6pt; text-align:justify;"><b>VII. Perhatian :</b> Pejabat yang menerbitkan SPD...</div></div>'''

html_out += '</div>'
st.markdown(html_out, unsafe_allow_html=True)
