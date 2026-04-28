import streamlit as st
import pandas as pd
from datetime import datetime
import logo  # Pastikan file logo.py ada di folder yang sama
from io import BytesIO

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Ngada Pro", layout="wide")

# --- INISIALISASI STATE AGAR INPUT TIDAK HILANG ---
if 'jml_pegawai' not in st.session_state: st.session_state.jml_pegawai = 1
if 'arsip_register' not in st.session_state: st.session_state.arsip_register = []

# 2. CSS UNTUK TAMPILAN KERTAS (Penting: unsafe_allow_html harus True)
st.markdown("""
<style>
    header, footer, .stDeployButton { visibility: hidden; display: none !important; }
    .stApp { background-color: #525659 !important; }
    .main-container { display: flex; flex-direction: column; align-items: center; width: 100%; padding: 20px 0; }
    
    .kertas { 
        background-color: white !important; 
        width: 215.9mm; height: 330mm; 
        padding: 15mm 20mm; margin-bottom: 25px; 
        color: black !important; font-family: Arial, sans-serif; 
        box-sizing: border-box; box-shadow: 0 0 20px rgba(0,0,0,0.5);
        font-size: 10.5pt; position: relative; flex-shrink: 0;
    }

    .kop-table { width: 100%; border: none !important; border-bottom: 3.5pt solid black !important; margin-bottom: 10px; }
    .kop-teks { text-align: center; line-height: 1.1; }
    .tabel-border { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; }
    .tabel-border td { border: 1pt solid black !important; padding: 5px 8px; vertical-align: top; color: black !important; font-size: 9.5pt; }
    .visum-table { width: 100%; border-collapse: collapse; margin: 0; }
    .visum-table td { padding: 2px 0; vertical-align: top; font-size: 10pt; color: black !important; }
    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }

    @media print {
        @page { size: legal portrait; margin: 0; }
        .stApp { background-color: white !important; }
        [data-testid="stSidebar"], .stButton, .no-print { display: none !important; }
        .main-container { padding: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; }
    }
</style>
""", unsafe_allow_html=True)

# 3. NAVIGASI INPUT DI SIDEBAR
with st.sidebar:
    st.header("📋 NAVIGASI INPUT")
    
    # Input Penandatangan (Pindahkan ke atas agar mudah)
    with st.expander("🖋️ DATA PENANDATANGAN", expanded=True):
        ttd_label = st.selectbox("Status", ["An. BUPATI NGADA", "WAKIL BUPATI NGADA", "BUPATI NGADA"])
        jab_ttd = st.text_input("Jabatan", "Pj. Sekretaris Daerah")
        ub = st.text_input("Ub. (Kosongkan jika tidak ada)", "Asisten Perekonomian dan Pembangunan")
        pjb_nama = st.text_input("Nama Pejabat", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
        pjb_nip = st.text_input("NIP", "19710328 199203 1 011")
        pjb_gol = st.text_input("Pangkat/Gol", "Pembina Utama Muda, IV/c")

    # Input Pegawai
    st.subheader("👤 PEGAWAI YANG BERTUGAS")
    c1, c2 = st.columns(2)
    if c1.button("➕ Tambah"): st.session_state.jml_pegawai += 1
    if c2.button("➖ Hapus") and st.session_state.jml_pegawai > 1: st.session_state.jml_pegawai -= 1
    
    daftar_petugas = []
    for i in range(st.session_state.jml_pegawai):
        with st.expander(f"Pegawai {i+1}", expanded=(i==0)):
            p = {
                "nama": st.text_input("Nama", key=f"n_{i}"),
                "nip": st.text_input("NIP", key=f"nip_{i}"),
                "gol": st.text_input("Gol", "III/a", key=f"g_{i}"),
                "jab": st.text_input("Jabatan", key=f"j_{i}"),
                "spd": st.text_input("No SPD", f"530 /02/2026", key=f"s_{i}"),
                "lembar": st.text_input("Lembar", "I", key=f"l_{i}")
            }
            daftar_petugas.append(p)

    # Data Perjalanan
    with st.expander("📄 DATA PERJALANAN"):
        no_spt = st.text_input("No SPT", "094/Prokopim/557/02/2026")
        tujuan = st.text_input("Tujuan", "Riung")
        maksud = st.text_area("Maksud", "Mendampingi...")
        tgl_bkt = st.text_input("Tgl Berangkat", "17 Maret 2026")
        lama = st.text_input("Lama Hari", "1 (Satu) hari")

    if st.button("🖨️ CETAK SEKARANG"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

# --- FUNGSI TTD ---
def get_ttd(space=70):
    jab_f = f"{jab_ttd},<br>" if ttd_label == "An. BUPATI NGADA" else ""
    ub_f = f"Ub. {ub},<br>" if (ub and ttd_label == "An. BUPATI NGADA") else ""
    return f'''
    <div style="margin-left:55%; margin-top:20px; text-align:center; line-height:1.2;">
        <b>{ttd_label}</b><br>{jab_f}{ub_f}
        <div style="height:{space}px;"></div>
        <b><u>{pjb_nama}</u></b><br>{pjb_gol}<br>NIP. {pjb_nip}
    </div>'''

# 4. PROSES RENDER KE LAYAR (SOLUSI ERROR KAMU)
html_output = '<div class="main-container">'

# Kertas SPT
html_output += f'''
<div class="kertas">
    <table class="kop-table">
        <tr>
            <td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td>
            <td class="kop-teks">
                <h3>PEMERINTAH KABUPATEN NGADA</h3>
                <h2>SEKRETARIAT DAERAH</h2>
                <p>BAJAWA</p>
            </td>
            <td width="15%"></td>
        </tr>
    </table>
    <div class="judul-rapat"><h3 class="underline text-center">SURAT PERINTAH TUGAS</h3><p class="text-center">Nomor: {no_spt}</p></div>
    <p style="margin-top:20px;">Memerintahkan kepada:</p>
    <table class="visum-table">
'''
for i, p in enumerate(daftar_petugas):
    html_output += f'<tr><td width="5%">{i+1}.</td><td width="20%">Nama</td><td>: <b>{p["nama"]}</b></td></tr>'
    html_output += f'<tr><td></td><td>NIP</td><td>: {p["nip"]}</td></tr>'
    html_output += f'<tr><td></td><td>Jabatan</td><td>: {p["jab"]}</td></tr>'

html_output += f'''
    </table>
    <p style="margin-top:15px;">Untuk: {maksud} ke {tujuan} selama {lama}.</p>
    {get_ttd(80)}
</div>'''

html_output += '</div>'

# --- BAGIAN PALING PENTING (Agar tidak muncul teks kode) ---
st.markdown(html_output, unsafe_allow_html=True)
