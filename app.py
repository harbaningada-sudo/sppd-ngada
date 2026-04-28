import streamlit as st
import pandas as pd
from datetime import datetime
import logo  # Memastikan file logo.py ada untuk gambar Kop & Garuda
from io import BytesIO

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Ngada Pro", layout="wide")

# --- INISIALISASI SESSION STATE ---
if 'jml' not in st.session_state: st.session_state.jml = 1
if 'arsip_register' not in st.session_state: st.session_state.arsip_register = []

# 2. CSS CUSTOM (STYLING KERTAS & UI)
st.markdown("""
<style>
    /* Menghilangkan elemen default Streamlit saat cetak */
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    .stApp { background-color: #525659 !important; }
    
    /* Container Utama */
    .main-container { display: flex; flex-direction: column; align-items: center; width: 100%; padding: 10px 0; }

    /* KERTAS LEGAL (215.9mm x 330mm) */
    .kertas { 
        background-color: white !important; 
        width: 215.9mm; height: 330mm; 
        padding: 10mm 15mm; margin-bottom: 20px; 
        color: black !important; font-family: Arial, sans-serif; 
        box-sizing: border-box; box-shadow: 0 0 20px rgba(0,0,0,0.8);
        font-size: 10.5pt; page-break-after: always; position: relative;
    }

    /* KOP & TABEL */
    .kop-table { width: 100%; border-bottom: 3.5pt solid black !important; margin-bottom: 5px; border-collapse: collapse; }
    .kop-teks { text-align: center; line-height: 1.1; }
    .tabel-border { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; }
    .tabel-border td { border: 1pt solid black !important; padding: 4px 8px; vertical-align: top; font-size: 9.5pt; color: black; }
    .visum-table { width: 100%; border-collapse: collapse; border: none !important; }
    .visum-table td { border: none !important; padding: 1px 0; font-size: 10pt; color: black; vertical-align: top; }
    
    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }

    @media print {
        [data-testid="stSidebar"], .stButton, .no-print { display: none !important; }
        .stApp, .main-container { background-color: white !important; padding: 0 !important; margin: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; width: 215.9mm !important; height: 330mm !important; }
        @page { size: legal portrait; margin: 0; }
    }
</style>
""", unsafe_allow_html=True)

# 3. NAVIGASI INPUT (SIDEBAR)
with st.sidebar:
    st.header("📋 NAVIGASI INPUT")
    wilayah = st.selectbox("Jenis Wilayah", ["Dalam Daerah", "Luar Daerah"])
    tab = st.radio("Menu", ["Input & Cetak", "Kelola Register"])

    if tab == "Input & Cetak":
        opsi = st.multiselect("Dokumen", ["SPT", "SPD Depan"], default=["SPT", "SPD Depan"])
        
        # --- INPUT DATA PEGAWAI ---
        with st.expander("👤 DATA PEGAWAI", expanded=True):
            c1, c2 = st.columns(2)
            if c1.button("➕ Tambah"): st.session_state.jml += 1
            if c2.button("➖ Hapus") and st.session_state.jml > 1: st.session_state.jml -= 1
            
            daftar = []
            for i in range(st.session_state.jml):
                st.markdown(f"**Pegawai {i+1}**")
                daftar.append({
                    "nama": st.text_input("Nama", key=f"nm_{i}"),
                    "nip": st.text_input("NIP", key=f"np_{i}"),
                    "gol": st.text_input("Gol", "III/a", key=f"gl_{i}"),
                    "jab": st.text_input("Jabatan", key=f"jb_{i}"),
                    "spd": st.text_input("No SPD", f"530 /02/2026", key=f"sd_{i}"),
                    "lembar": st.text_input("Lembar", "I", key=f"lb_{i}")
                })

        # --- INPUT DATA UTAMA ---
        with st.expander("📄 DATA SURAT"):
            no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
            maksud = st.text_area("Maksud", "Mendampingi Bupati...")
            tujuan = st.text_input("Tujuan", "Kecamatan Riung")
            tgl_bkt = st.text_input("Tgl Berangkat", "17 Maret 2026")
            lama = st.text_input("Lama Hari", "1 (Satu) hari")
            anggaran = st.text_area("Dasar Anggaran", "DPA Bagian Perekonomian 2026")

        # --- INPUT PENANDA TANGAN ---
        with st.expander("🖋️ PENANDA TANGAN"):
            ttd_label = st.selectbox("Status", ["An. BUPATI NGADA", "WAKIL BUPATI NGADA", "BUPATI NGADA"])
            pjb_nama = st.text_input("Nama Pejabat", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
            jab_ttd = st.text_input("Jabatan Utama", "Pj. Sekretaris Daerah")
            ub = st.text_input("Ub. (Jika Ada)", "Asisten Perekonomian")
            nip_ttd = st.text_input("NIP Pejabat", "19710328 199203 1 011")

        if st.button("🖨️ PROSES CETAK"):
            st.components.v1.html("<script>window.parent.print();</script>", height=0)

# --- FUNGSI RENDER TTD ---
def get_ttd(space=75):
    jab_h = f"{jab_ttd},<br>" if ttd_label == "An. BUPATI NGADA" else ""
    ub_h = f"Ub. {ub},<br>" if (ub and ttd_label == "An. BUPATI NGADA") else ""
    return f'''
    <div style="margin-left:55%; margin-top:20px; text-align:center; line-height:1.2;">
        <b>{ttd_label}</b><br>{jab_h}{ub_h}
        <div style="height:{space}px;"></div>
        <b><u>{pjb_nama}</u></b><br>NIP. {nip_ttd}
    </div>'''

# 4. AREA TAMPILAN (MAIN)
if tab == "Input & Cetak":
    html_final = '<div class="main-container">'
    
    # Kop Pemda
    kop_pemda = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>BAJAWA</p></td><td width="15%"></td></tr></table>'''

    # RENDER SPT
    if "SPT" in opsi:
        kop_spt = f'<div class="text-center"><img src="data:image/png;base64,{logo.GARUDA}" width="70"><br><h2>BUPATI NGADA</h2></div>' if wilayah == "Luar Daerah" else kop_pemda
        p_rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{i+1}.</td><td width='20%'>Nama</td><td>: <b>{p['nama']}</b></td></tr><tr><td colspan='3'></td><td>NIP</td><td>: {p['nip']}</td></tr>" for i, p in enumerate(daftar)])
        html_final += f'<div class="kertas">{kop_spt}<div class="judul-rapat"><h3 class="underline text-center">SURAT PERINTAH TUGAS</h3><p class="text-center">Nomor: {no_spt}</p></div><table class="visum-table"><tr><td width="12%">Dasar</td><td width="5%">:</td><td>{anggaran}</td></tr></table><p class="text-center text-bold" style="margin:10px 0;">MEMERINTAHKAN:</p><table class="visum-table">{p_rows}</table><table class="visum-table" style="margin-top:20px;"><tr><td width="12%">Untuk</td><td width="5%">:</td><td>{maksud} ke {tujuan} selama {lama}.</td></tr></table>{get_ttd(80)}</div>'

    # RENDER SPD
    if "SPD Depan" in opsi:
        for p in daftar:
            html_final += f'''<div class="kertas">{kop_pemda}<div style="margin-left:60%; line-height:1.2;">No SPD: {p['spd']}<br>Lembar: {p['lembar']}</div><div class="judul-rapat"><h3 class="underline text-center">SURAT PERJALANAN DINAS</h3></div><table class="tabel-border" style="margin-top:10px;"><tr><td width="5%">1</td><td width="40%">Pejabat Pemberi Perintah</td><td>BUPATI NGADA</td></tr><tr><td>2</td><td>Nama Pegawai</td><td><b>{p['nama']}</b></td></tr><tr><td>3</td><td>Maksud</td><td>{maksud}</td></tr><tr><td>4</td><td>Tujuan</td><td>{tujuan}</td></tr><tr><td>5</td><td>Tanggal</td><td>{tgl_bkt}</td></tr></table>{get_ttd(60)}</div>'''

    html_final += '</div>'
    st.markdown(html_final, unsafe_allow_html=True)
