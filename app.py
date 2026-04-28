import streamlit as st
import pandas as pd
from datetime import datetime
import logo  # Pastikan file logo.py ada di folder yang sama
from io import BytesIO

# 1. KONFIGURASI HALAMAN (Wajib di baris paling atas)
st.set_page_config(
    page_title="Sistem SPD Ngada Pro", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- INISIALISASI DATA ---
if 'arsip_register' not in st.session_state:
    st.session_state.arsip_register = []
if 'jml' not in st.session_state:
    st.session_state.jml = 1

# 2. CSS UNTUK TAMPILAN KERTAS & SIDEBAR
st.markdown("""
<style>
    /* Menghilangkan header default agar bersih */
    header, footer, .stDeployButton { visibility: hidden; display: none !important; }
    
    /* Warna area kerja (Abu-abu seperti viewer PDF) */
    [data-testid="stMainViewContainer"] {
        background-color: #525659 !important;
    }

    /* Wadah Kertas di Tengah */
    .main-container { 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        width: 100%; 
        padding: 20px 0; 
    }

    /* KERTAS UKURAN LEGAL */
    .kertas { 
        background-color: white !important; 
        width: 215.9mm; 
        height: 330mm; 
        padding: 10mm 15mm; 
        margin-bottom: 25px; 
        color: black !important; 
        font-family: Arial, sans-serif; 
        box-sizing: border-box; 
        box-shadow: 0 0 20px rgba(0,0,0,0.5);
        font-size: 10.5pt; 
        position: relative;
        overflow: hidden;
    }

    /* STYLE KOP & TABEL */
    .kop-table { width: 100%; border-bottom: 3.5pt solid black !important; margin-bottom: 10px; border-collapse: collapse; }
    .kop-teks { text-align: center; line-height: 1.1 !important; }
    .kop-teks h3, .kop-teks h2 { margin: 2px 0; }
    
    .tabel-border { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; }
    .tabel-border td { border: 1pt solid black !important; padding: 4px 8px !important; color: black !important; font-size: 9.5pt; }
    
    .visum-table { width: 100%; border-collapse: collapse; }
    .visum-table td { border: none !important; padding: 2px 0; font-size: 10pt; color: black !important; vertical-align: top; }

    .text-center { text-align: center; } 
    .text-bold { font-weight: bold; } 
    .underline { text-decoration: underline; }

    /* PENGATURAN SAAT PRINT */
    @media print {
        [data-testid="stSidebar"], .stButton, .no-print { display: none !important; }
        [data-testid="stMainViewContainer"] { background-color: white !important; }
        .main-container { padding: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; }
        @page { size: legal portrait; margin: 0; }
    }
</style>
""", unsafe_allow_html=True)

# 3. PANEL NAVIGASI (SIDEBAR KIRI)
with st.sidebar:
    st.header("📋 NAVIGASI INPUT")
    wilayah = st.selectbox("Pilih Wilayah", ["Dalam Daerah", "Luar Daerah"])
    menu = st.radio("Pindah Menu", ["Input & Cetak", "Kelola Register"])
    
    if menu == "Input & Cetak":
        opsi_cetak = st.multiselect("Dokumen yang Dicetak", ["SPT", "SPD Depan"], default=["SPT", "SPD Depan"])
        
        # INPUT DATA PEGAWAI
        with st.expander("👤 DATA PEGAWAI", expanded=True):
            col1, col2 = st.columns(2)
            if col1.button("➕ Tambah"): st.session_state.jml += 1
            if col2.button("➖ Hapus") and st.session_state.jml > 1: st.session_state.jml -= 1
            
            list_pegawai = []
            for i in range(st.session_state.jml):
                st.markdown(f"**Pegawai {i+1}**")
                list_pegawai.append({
                    "nama": st.text_input("Nama Lengkap", f"Nama {i+1}", key=f"n_{i}"),
                    "nip": st.text_input("NIP", "19XXXXXXXXXXXXXX", key=f"nip_{i}"),
                    "gol": st.text_input("Golongan", "III/a", key=f"g_{i}"),
                    "jab": st.text_input("Jabatan", "Pelaksana", key=f"j_{i}"),
                    "spd": st.text_input("Nomor SPD", f"530/02/2026", key=f"s_{i}"),
                    "lbr": st.text_input("Lembar Ke", "I", key=f"l_{i}")
                })

        # DATA PERJALANAN
        with st.expander("📄 DATA PERJALANAN"):
            no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
            maksud = st.text_area("Maksud Tugas", "Melakukan koordinasi...")
            tujuan = st.text_input("Tujuan", "Kecamatan Riung")
            lama = st.text_input("Lama Hari", "1 (Satu) hari")
            tgl_bkt = st.text_input("Tanggal Berangkat", "17 Maret 2026")
            anggaran = st.text_area("Dasar Anggaran", "DPA Bagian Perekonomian 2026")

        # PENANDA TANGAN
        with st.expander("🖋️ PEJABAT TTD"):
            ttd_status = st.selectbox("Status", ["An. BUPATI NGADA", "BUPATI NGADA"])
            pjb_nama = st.text_input("Nama Pejabat TTD", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
            pjb_jab = st.text_input("Jabatan Utama", "Pj. Sekretaris Daerah")
            pjb_ub = st.text_input("Ub. (Jika Ada)", "Asisten Perekonomian")
            pjb_nip = st.text_input("NIP Pejabat TTD", "19710328 199203 1 011")

        if st.button("🖨️ CETAK SEKARANG"):
            st.components.v1.html("<script>window.parent.print();</script>", height=0)

# --- FUNGSI TANDA TANGAN ---
def render_ttd(gap):
    status_h = f"<b>{ttd_status}</b><br>"
    jab_h = f"{pjb_jab},<br>" if ttd_status == "An. BUPATI NGADA" else ""
    ub_h = f"Ub. {pjb_ub},<br>" if (pjb_ub and ttd_status == "An. BUPATI NGADA") else ""
    return f'''
    <div style="margin-left:55%; margin-top:20px; text-align:center; line-height:1.2;">
        {status_h}{jab_h}{ub_h}
        <div style="height:{gap}px;"></div>
        <b><u>{pjb_nama}</u></b><br>NIP. {pjb_nip}
    </div>'''

# 4. TAMPILAN HALAMAN UTAMA (PREVIEW)
if menu == "Input & Cetak":
    # Persiapan Kop
    kop_surat = f'''
    <table class="kop-table">
        <tr>
            <td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td>
            <td class="kop-teks">
                <h3>PEMERINTAH KABUPATEN NGADA</h3>
                <h2>SEKRETARIAT DAERAH</h2>
                <p>Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834</p>
                <p class="text-bold">BAJAWA</p>
            </td>
            <td width="15%"></td>
        </tr>
    </table>'''

    container_html = '<div class="main-container">'

    # BAGIAN SPT
    if "SPT" in opsi_cetak:
        kop_f = f'<div class="text-center"><img src="data:image/png;base64,{logo.GARUDA}" width="75"><br><h2>BUPATI NGADA</h2></div>' if wilayah == "Luar Daerah" else kop_surat
        rows_peg = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{idx+1}.</td><td width='20%'>Nama</td><td>: <b>{p['nama']}</b></td></tr><tr><td colspan='3'></td><td>NIP</td><td>: {p['nip']}</td></tr>" for idx, p in enumerate(list_pegawai)])
        
        container_html += f'''
        <div class="kertas">
            {kop_f}
            <div class="text-center" style="margin-top:10px;"><h3 class="underline">SURAT PERINTAH TUGAS</h3><p>Nomor: {no_spt}</p></div>
            <table class="visum-table"><tr><td width="12%">Dasar</td><td width="5%">:</td><td>{anggaran}</td></tr></table>
            <p class="text-center text-bold" style="margin:10px 0;">MEMERINTAHKAN:</p>
            <table class="visum-table">{rows_peg}</table>
            <table class="visum-table" style="margin-top:20px;"><tr><td width="12%">Untuk</td><td width="5%">:</td><td>{maksud} ke {tujuan} selama {lama}.</td></tr></table>
            {render_ttd(80)}
        </div>'''

    # BAGIAN SPD
    if "SPD Depan" in opsi_cetak:
        for p in list_pegawai:
            container_html += f'''
            <div class="kertas">
                {kop_surat}
                <div style="margin-left:60%; line-height:1.1; font-size:9pt;">
                    Nomor SPD: {p['spd']}<br>Lembar ke: {p['lbr']}
                </div>
                <div class="text-center"><h3 class="underline">SURAT PERJALANAN DINAS (SPD)</h3></div>
                <table class="tabel-border" style="margin-top:10px;">
                    <tr><td width="5%">1</td><td width="42%">Pejabat Pemberi Perintah</td><td><b>BUPATI NGADA</b></td></tr>
                    <tr><td>2</td><td>Nama Pegawai diperintah</td><td><b>{p['nama']}</b></td></tr>
                    <tr><td rowspan="2">3</td><td>a. Pangkat / Golongan</td><td>{p['gol']}</td></tr>
                    <tr><td>b. Jabatan</td><td>{p['jab']}</td></tr>
                    <tr><td>4</td><td>Maksud Perjalanan</td><td>{maksud}</td></tr>
                    <tr><td>5</td><td>Tempat Tujuan</td><td>{tujuan}</td></tr>
                    <tr><td>6</td><td>Lamanya Perjalanan</td><td>{lama}</td></tr>
                    <tr><td>7</td><td>Tanggal Berangkat</td><td>{tgl_bkt}</td></tr>
                </table>
                {render_ttd(60)}
            </div>'''

    container_html += '</div>'
    
    # PERINTAH RENDER (Wajib pakai unsafe_allow_html=True)
    st.markdown(container_html, unsafe_allow_html=True)

elif menu == "Kelola Register":
    st.title("📂 Register SPD")
    st.info("Fitur register data sedang dalam pengembangan.")
