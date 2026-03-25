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

    /* KOP GARUDA (KHUSUS SPT LUAR DAERAH) */
    .kop-garuda { text-align: center; margin-bottom: 15px; line-height: 1.0; width: 100%; }
    .kop-garuda img { width: 70px; margin-bottom: 8px; }
    .kop-garuda h2 { margin: 0; font-size: 16pt; font-weight: bold; letter-spacing: 2px; text-transform: uppercase; }

    /* KOP PEMDA (UNTUK SPT DALAM DAERAH & SPD DEPAN) */
    .kop-table { width: 100%; border: none !important; border-bottom: 3.5pt solid black !important; margin-bottom: 5px; border-collapse: collapse; }
    .kop-table td { border: none !important; padding: 0 !important; vertical-align: middle; }
    .kop-teks { text-align: center; line-height: 1.0 !important; } 
    .kop-teks h3, .kop-teks h2 { margin: 0; line-height: 1.0 !important; padding: 1px 0; }
    
    .judul-rapat { text-align: center; line-height: 1.0 !important; margin-top: 5px; }
    .judul-rapat h3 { margin: 0; font-weight: bold; text-decoration: underline; }
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
    tab_menu = st.radio("Fokus Wilayah", ["Luar Daerah", "Dalam Daerah"])
    opsi_cetak = st.multiselect("Dokumen", ["SPT", "SPD Depan", "SPD Belakang"], default=["SPT", "SPD Depan", "SPD Belakang"])
    
    with st.expander("👤 PEGAWAI", expanded=True):
        if 'jml' not in st.session_state: st.session_state.jml = 1
        c1, c2 = st.columns(2)
        if c1.button("➕"): st.session_state.jml += 1
        if c2.button("➖") and st.session_state.jml > 1: st.session_state.jml -= 1
        
        daftar = []
        for i in range(st.session_state.jml):
            daftar.append({
                "nama": st.text_input(f"Nama {i+1}", f"Pegawai {i+1}", key=f"n{i}"),
                "nip": st.text_input(f"NIP {i+1}", "19XXXXXXXXXXXXXX", key=f"nip{i}"),
                "gol": st.text_input(f"Gol {i+1}", "III/a", key=f"g{i}"),
                "jab": st.text_input(f"Jabatan {i+1}", "Pelaksana", key=f"j{i}"),
                "spd": st.text_input(f"No SPD {i+1}", f"530 /.../2026", key=f"spd{i}")
            })

    with st.expander("📄 DATA TUGAS"):
        no_spt = st.text_input("No SPT", "094/Prokopim/...")
        tujuan = st.text_input("Tujuan", "Labuan Bajo")
        maksud = st.text_area("Maksud", "Kegiatan...")
        tgl_bkt = st.text_input("Tgl Berangkat", "17 Maret 2026")
        tgl_kbl = st.text_input("Tgl Kembali", "20 Maret 2026")

    st.subheader("🖋️ PENANDA TANGAN")
    pjb = st.text_input("Nama Pejabat", "BERNADINUS DHEY NGEBU, SP")
    gol_pjb = st.text_input("Pangkat", "Pembina Utama Madya")
    nip_ttd = st.text_input("NIP", "19650101 198603 1 045")

    if st.button("🖨️ CETAK SEKARANG"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

# --- FUNGSI TANDA TANGAN ---
def render_ttd(label="An. BUPATI NGADA", space=75):
    return f'''<div style="text-align:center; line-height:1.2; font-size:10.5pt; width:280px; margin-left:auto;"><b>{label}</b><br><div style="height:{space}px;"></div><b><u>{pjb}</u></b><br>{gol_pjb}<br>NIP. {nip_ttd}</div>'''

html_out = '<div class="main-container">'

# 1. SPT (LOGIKA CABANG)
if "SPT" in opsi_cetak:
    if tab_menu == "Luar Daerah":
        kop = f'<div class="kop-garuda"><img src="data:image/png;base64,{logo.GARUDA}"><h2>BUPATI NGADA</h2></div>'
    else:
        kop = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>BAJAWA</p></td><td width="15%"></td></tr></table>'''
    
    p_rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{i+1}.</td><td width='18%'>Nama</td><td width='3%'>:</td><td><b>{p['nama']}</b></td></tr><tr><td></td><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr>" for i, p in enumerate(daftar)])
    html_out += f'''<div class="kertas">{kop}<div class="judul-rapat"><h3>SURAT PERINTAH TUGAS</h3><p>NOMOR : {no_spt}</p></div><div class="isi-surat-spt"><table class="visum-table"><tr><td width="12%">Dasar</td><td width="5%">:</td><td>DPA 2026</td></tr></table><p class="text-center text-bold" style="margin:10px 0; letter-spacing:4px;">M E M E R I N T A H K A N</p><table class="visum-table">{p_rows}</table><table class="visum-table" style="margin-top:10px;"><tr><td width="12%">Untuk</td><td width="5%">:</td><td>{maksud} ke {tujuan}</td></tr></table></div><div style="margin-top:30px;">{render_ttd("WAKIL BUPATI NGADA" if tab_menu=="Luar Daerah" else "An. BUPATI NGADA", 85)}</div></div>'''

# 2. SPD DEPAN
for p in daftar:
    if "SPD Depan" in opsi_cetak:
        kop_p = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>BAJAWA</p></td><td width="15%"></td></tr></table>'''
        html_out += f'''<div class="kertas">{kop_p}<div style="margin-left:60%; line-height:1.0;">Lembar ke: I<br>Nomor: {p['spd']}</div><div class="judul-rapat"><h3>SURAT PERJALANAN DINAS</h3><h3>(SPD)</h3></div><table class="tabel-border" style="margin-top:10px;">
            <tr><td class="col-no">1.</td><td width="42%">Pejabat pemberi perintah</td><td colspan="3"><b>BUPATI NGADA</b></td></tr>
            <tr><td class="col-no">2.</td><td>Nama Pegawai</td><td colspan="3"><b>{p['nama']}</b></td></tr>
            <tr><td class="col-no">6.</td><td>Tempat Tujuan</td><td colspan="3">{tujuan}</td></tr>
            <tr><td class="col-no">7.</td><td>Tgl Berangkat</td><td colspan="3">{tgl_bkt}</td></tr>
        </table><div style="margin-top:15px;">{render_ttd("An. BUPATI NGADA", 65)}</div></div>'''

# 3. SPD BELAKANG (POIN II KIRI BERSIH)
if "SPD Belakang" in opsi_cetak:
    ttd_asal = render_ttd("An. BUPATI NGADA", 65)
    def rv(num, label, val, d_v): return f'''<table class="visum-table"><tr><td width="10%">{num}</td><td width="35%">{label}</td><td width="5%">:</td><td>{val}</td></tr><tr><td></td><td>Pada Tanggal</td><td>:</td><td>{d_v}</td></tr></table>'''
    
    html_out += f'''<div class="kertas"><table class="tabel-border" style="height:88%;">
        <tr style="height: 220px;"><td width="50%"></td><td style="padding:10px;">{rv("I.", "Berangkat dari", "Bajawa", tgl_bkt)}<br>{ttd_asal}</td></tr>
        <tr style="height: 190px;"><td>{rv("II.", "Tiba di", tujuan, tgl_bkt)}<br></td><td style="padding:10px;">{rv("", "Berangkat dari", tujuan, tgl_kbl)}</td></tr>
        <tr style="height: 220px;"><td>{rv("V.", "Tiba Kembali", "Bajawa", tgl_kbl)}</td><td style="padding:10px;"><p style="font-style:italic; font-size:9.2pt; line-height:1.2;">Telah diperiksa, dengan keterangan bahwa perjalanan tersebut atas perintahnya...</p>{ttd_asal}</td></tr>
    </table><div style="border:1pt solid black; border-top:none; padding:8px; font-size:10.5pt;"><b>VI. Catatan Lain-lain</b></div><div style="border:1pt solid black; border-top:none; padding:8px; font-size:8.5pt; text-align:justify;"><b>VII. Perhatian :</b> Pejabat yang menerbitkan SPD... bertanggung jawab...</div></div>'''

html_out += '</div>'
st.markdown(html_out, unsafe_allow_html=True)
