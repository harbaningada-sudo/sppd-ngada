import streamlit as st
import pandas as pd
from datetime import datetime
import logo  # Memanggil file logo.py di repository kamu
from io import BytesIO

# 1. KONFIGURASI HALAMAN (Wajib Paling Atas)
st.set_page_config(
    page_title="Sistem SPD Ngada Pro", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- INISIALISASI DATABASE REGISTER ---
if 'arsip_register' not in st.session_state:
    st.session_state.arsip_register = []
if 'jml' not in st.session_state:
    st.session_state.jml = 1

# 2. CSS UNTUK PRESISI CETAK & FIX SIDEBAR
st.markdown("""
<style>
    /* Sembunyikan elemen dekoratif Streamlit */
    header, footer, .stDeployButton { visibility: hidden; display: none !important; }
    
    /* Area Utama (Background Abu-abu seperti PDF Viewer) */
    [data-testid="stMainViewContainer"] {
        background-color: #525659 !important;
    }

    /* Container Kertas */
    .main-container { 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        width: 100%; 
        padding: 20px 0; 
    }

    /* KERTAS LEGAL (215.9mm x 330mm) */
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

    /* KOP SURAT */
    .kop-table { width: 100%; border-bottom: 3.5pt solid black !important; margin-bottom: 5px; border-collapse: collapse; }
    .kop-teks { text-align: center; line-height: 1.0 !important; }
    .kop-teks h3, .kop-teks h2, .kop-teks p { margin: 2px 0; }

    /* TABEL SPD */
    .tabel-border { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; }
    .tabel-border td { border: 1pt solid black !important; padding: 4px 8px !important; vertical-align: top; color: black !important; font-size: 9.5pt; }
    
    .visum-table { width: 100%; border-collapse: collapse; margin: 0 !important; }
    .visum-table td { border: none !important; padding: 1px 0; font-size: 10pt; line-height: 1.2; color: black !important; }

    .text-center { text-align: center; } 
    .text-bold { font-weight: bold; } 
    .underline { text-decoration: underline; }

    /* ATURAN CETAK */
    @media print {
        [data-testid="stSidebar"], .stButton, .no-print { display: none !important; }
        [data-testid="stMainViewContainer"] { background-color: white !important; }
        .main-container { padding: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; }
        @page { size: legal portrait; margin: 0; }
    }
</style>
""", unsafe_allow_html=True)

# 3. NAVIGASI INPUT (SIDEBAR)
with st.sidebar:
    st.header("📋 PANEL KONTROL")
    wilayah = st.selectbox("Jenis Wilayah", ["Dalam Daerah", "Luar Daerah"])
    tab_menu = st.radio("Menu", ["Input & Cetak", "Kelola Register"])
    
    if tab_menu == "Input & Cetak":
        opsi_cetak = st.multiselect("Pilih Dokumen", ["SPT", "SPD Depan", "SPD Belakang"], default=["SPT", "SPD Depan"])
        
        # --- DATA PEGAWAI ---
        with st.expander("👤 DATA PEGAWAI", expanded=True):
            c1, c2 = st.columns(2)
            if c1.button("➕ Tambah"): st.session_state.jml += 1
            if c2.button("➖ Hapus") and st.session_state.jml > 1: st.session_state.jml -= 1
            
            daftar = []
            for i in range(st.session_state.jml):
                st.markdown(f"**Pegawai {i+1}**")
                daftar.append({
                    "nama": st.text_input("Nama", f"Nama {i+1}", key=f"n{i}"),
                    "nip": st.text_input("NIP", "19XXXXXXXXXXXXXX", key=f"nip{i}"),
                    "gol": st.text_input("Gol", "III/a", key=f"g{i}"),
                    "jab": st.text_input("Jabatan", "Pelaksana", key=f"j{i}"),
                    "spd": st.text_input("No SPD", f"530 /02/2026", key=f"spd{i}"),
                    "lembar": st.text_input("Lembar ke", "I", key=f"lbr{i}")
                })

        # --- DATA UTAMA ---
        with st.expander("📄 DATA SURAT"):
            no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
            kode_spd = st.text_input("Kode No SPD", "094/Prokopim")
            maksud = st.text_area("Maksud Perjalanan", "Mendampingi Bupati...")
            tujuan = st.text_input("Tujuan", "Kecamatan Riung")
            alat = st.text_input("Alat Angkut", "Mobil Dinas")
            lama = st.text_input("Lama Hari", "1 (Satu) hari")
            tgl_bkt = st.text_input("Tgl Berangkat", "17 Maret 2026")
            tgl_kbl = st.text_input("Tgl Kembali", "17 Maret 2026")
            anggaran = st.text_area("Dasar Anggaran", "DPA Bagian Perekonomian 2026")

        # --- TANDA TANGAN ---
        with st.expander("🖋️ PENANDA TANGAN"):
            ttd_label = st.selectbox("Status", ["An. BUPATI NGADA", "WAKIL BUPATI NGADA", "BUPATI NGADA"])
            pjb = st.text_input("Nama Pejabat", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
            gol_pjb = st.text_input("Pangkat/Gol Pejabat", "Pembina Utama Muda - IV/c")
            jab_ttd = st.text_input("Jabatan Utama", "Pj. Sekretaris Daerah")
            ub = st.text_input("Ub. (Opsional)", "Asisten Perekonomian")
            nip_ttd = st.text_input("NIP Pejabat", "19710328 199203 1 011")

        if st.button("🖨️ PROSES CETAK & SIMPAN"):
            for p in daftar:
                st.session_state.arsip_register.append({
                    "Nama": p['nama'], "No SPT": no_spt, "No SPD": p['spd'],
                    "Tujuan": tujuan, "Berangkat": tgl_bkt, "Ket": wilayah
                })
            st.components.v1.html("<script>setTimeout(function(){ window.parent.print(); }, 1000);</script>", height=0)

# --- LOGIC RENDER TANDA TANGAN ---
def get_ttd_html(space):
    label_f = f"<b>{ttd_label}</b>"
    jab_f = f"{jab_ttd},<br>" if ttd_label == "An. BUPATI NGADA" else ""
    ub_f = f"Ub. {ub},<br>" if (ub and ttd_label == "An. BUPATI NGADA") else ""
    return f'''
    <div style="margin-left:55%; margin-top:15px; text-align:center; line-height:1.2;">
        {label_f}<br>{jab_f}{ub_f}
        <div style="height:{space}px;"></div>
        <b><u>{pjb}</u></b><br>{gol_pjb}<br>NIP. {nip_ttd}
    </div>'''

# 4. TAMPILAN UTAMA (PREVIEW KERTAS)
if tab_menu == "Input & Cetak":
    html_final = '<div class="main-container">'
    
    # Kop Pemda
    kop_pemda = f'''
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

    # --- RENDER SPT ---
    if "SPT" in opsi_cetak:
        kop_spt = f'<div class="text-center"><img src="data:image/png;base64,{logo.GARUDA}" width="75"><br><h2>BUPATI NGADA</h2></div>' if wilayah == "Luar Daerah" else kop_pemda
        p_rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{i+1}.</td><td width='20%'>Nama</td><td>: <b>{p['nama']}</b></td></tr><tr><td colspan='3'></td><td>NIP</td><td>: {p['nip']}</td></tr>" for i, p in enumerate(daftar)])
        
        html_final += f'''
        <div class="kertas">
            {kop_spt}
            <div class="text-center" style="margin-top:10px;"><h3 class="underline">SURAT PERINTAH TUGAS</h3><p>Nomor: {no_spt}</p></div>
            <table class="visum-table"><tr><td width="12%">Dasar</td><td width="5%">:</td><td>{anggaran}</td></tr></table>
            <p class="text-center text-bold" style="margin:10px 0;">MEMERINTAHKAN:</p>
            <table class="visum-table">{p_rows}</table>
            <table class="visum-table" style="margin-top:20px;"><tr><td width="12%">Untuk</td><td width="5%">:</td><td>{maksud} ke {tujuan} selama {lama}.</td></tr></table>
            {get_ttd_html(80)}
        </div>'''

    # --- RENDER SPD DEPAN ---
    if "SPD Depan" in opsi_cetak:
        for p in daftar:
            html_final += f'''
            <div class="kertas">
                {kop_pemda}
                <div style="margin-left:60%; line-height:1.1; font-size:9pt;">
                    Nomor SPD: {p['spd']}<br>Lembar ke: {p['lembar']}<br>Kode No: {kode_spd}
                </div>
                <div class="text-center"><h3 class="underline">SURAT PERJALANAN DINAS (SPD)</h3></div>
                <table class="tabel-border" style="margin-top:10px;">
                    <tr><td width="5%">1</td><td width="40%">Pejabat Pemberi Perintah</td><td><b>BUPATI NGADA</b></td></tr>
                    <tr><td>2</td><td>Nama Pegawai diperintah</td><td><b>{p['nama']}</b></td></tr>
                    <tr><td rowspan="2">3</td><td>a. Pangkat / Golongan</td><td>{p['gol']}</td></tr>
                    <tr><td>b. Jabatan</td><td>{p['jab']}</td></tr>
                    <tr><td>4</td><td>Maksud Perjalanan</td><td>{maksud}</td></tr>
                    <tr><td>5</td><td>Alat Angkut</td><td>{alat}</td></tr>
                    <tr><td rowspan="2">6</td><td>a. Tempat Berangkat</td><td>Bajawa</td></tr>
                    <tr><td>b. Tempat Tujuan</td><td>{tujuan}</td></tr>
                    <tr><td rowspan="3">7</td><td>a. Lamanya Perjalanan</td><td>{lama}</td></tr>
                    <tr><td>b. Tanggal Berangkat</td><td>{tgl_bkt}</td></tr>
                    <tr><td>c. Tanggal Kembali</td><td>{tgl_kbl}</td></tr>
                </table>
                {get_ttd_html(60)}
            </div>'''

    html_final += '</div>'
    st.markdown(html_final, unsafe_allow_html=True)

# --- MENU REGISTER ---
elif tab_menu == "Kelola Register":
    st.subheader("📂 RIWAYAT REGISTER SPD")
    if st.session_state.arsip_register:
        df = pd.DataFrame(st.session_state.arsip_register)
        st.dataframe(df, use_container_width=True)
        if st.button("🗑️ Hapus Semua Data"):
            st.session_state.arsip_register = []
            st.rerun()
    else:
        st.info("Belum ada data yang tersimpan.")
