import streamlit as st
import pandas as pd
from datetime import datetime
import logo  # Memanggil file logo.py
from io import BytesIO

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Ngada Pro", layout="wide")

# --- INITIALIZE SESSION STATE (Kunci agar data tidak hilang) ---
if 'arsip_register' not in st.session_state:
    st.session_state.arsip_register = []
if 'jml' not in st.session_state:
    st.session_state.jml = 1

# Fungsi untuk sinkronisasi input ke session state
def sync_input(key, default_val):
    if key not in st.session_state:
        st.session_state[key] = default_val
    return st.session_state[key]

# 2. CSS TERBAIK (Presisi & Konsisten antar Device)
st.markdown("""
<style>
    /* Sembunyikan elemen UI Streamlit saat cetak */
    header, footer, .stDeployButton, [data-testid="stSidebarNav"] { display: none !important; }
    
    /* Background aplikasi agar seperti viewer PDF */
    .stApp { background-color: #525659 !important; }
    
    /* Container Kertas */
    .main-container { 
        display: flex; flex-direction: column; align-items: center; 
        width: 100%; padding: 20px 0; overflow-x: auto;
    }

    /* KERTAS LEGAL (DIKUNCI) */
    .kertas { 
        background-color: white !important; 
        width: 215.9mm; height: 330mm; 
        padding: 15mm 20mm; margin-bottom: 25px; 
        color: black !important; font-family: Arial, sans-serif; 
        box-sizing: border-box; box-shadow: 0 0 15px rgba(0,0,0,0.5);
        font-size: 10.5pt; position: relative; flex-shrink: 0;
        overflow: hidden;
    }

    /* Tabel & Kop */
    .kop-table { width: 100%; border-bottom: 3.5pt solid black !important; margin-bottom: 10px; }
    .kop-teks { text-align: center; line-height: 1.1; }
    .tabel-border { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; }
    .tabel-border td { border: 1pt solid black !important; padding: 5px 8px; vertical-align: top; font-size: 9.5pt; }
    .visum-table { width: 100%; border-collapse: collapse; }
    .visum-table td { padding: 1px 0; vertical-align: top; font-size: 10pt; }

    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }

    @media print {
        @page { size: legal portrait; margin: 0; }
        .stApp { background-color: white !important; }
        .main-container { padding: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; page-break-after: always; }
        [data-testid="stSidebar"], .no-print, .stButton { display: none !important; }
    }
</style>
""", unsafe_allow_html=True)

# 3. SIDEBAR (LOGIKA INPUT)
with st.sidebar:
    st.header("📋 PANEL KONTROL")
    wilayah = st.selectbox("Jenis Wilayah", ["Dalam Daerah", "Luar Daerah"])
    tab_menu = st.radio("Menu", ["Input & Cetak", "Kelola Register"])
    
    if tab_menu == "Input & Cetak":
        opsi_cetak = st.multiselect("Pilih Dokumen", ["SPT", "SPD Depan", "SPD Belakang"], default=["SPT", "SPD Depan"])
        
        # Pengaturan Jumlah Pegawai
        st.subheader("👤 DATA PEGAWAI")
        col_add, col_rem = st.columns(2)
        if col_add.button("➕ Tambah"): st.session_state.jml += 1
        if col_rem.button("➖ Hapus") and st.session_state.jml > 1: st.session_state.jml -= 1
        
        daftar_pegawai = []
        for i in range(st.session_state.jml):
            with st.expander(f"Pegawai {i+1}", expanded=(i == 0)):
                p_data = {
                    "nama": st.text_input("Nama", key=f"nama_{i}"),
                    "nip": st.text_input("NIP", key=f"nip_{i}"),
                    "gol": st.text_input("Gol", "III/a", key=f"gol_{i}"),
                    "jab": st.text_input("Jabatan", key=f"jab_{i}"),
                    "spd": st.text_input("No SPD", f"530 /02/2026", key=f"spd_{i}"),
                    "lembar": st.text_input("Lembar ke", "I", key=f"lbr_{i}")
                }
                daftar_pegawai.append(p_data)

        with st.expander("📄 DATA UTAMA (SPT/SPD)"):
            no_spt = st.text_input("Nomor SPT", key="no_spt_val")
            kode_spd = st.text_input("Kode No SPD", key="kode_spd_val")
            maksud = st.text_area("Maksud Perjalanan", key="maksud_val")
            tujuan = st.text_input("Tujuan", key="tujuan_val")
            alat = st.text_input("Alat Angkut", "Mobil Dinas", key="alat_val")
            lama = st.text_input("Lama Hari", "1 (Satu) hari", key="lama_val")
            tgl_bkt = st.text_input("Tgl Berangkat", key="tgl_bkt_val")
            tgl_kbl = st.text_input("Tgl Kembali", key="tgl_kbl_val")
            anggaran = st.text_area("Dasar Anggaran", key="anggaran_val")

        with st.expander("🖋️ PENANDATANGAN"):
            ttd_label = st.selectbox("Label", ["An. BUPATI NGADA", "BUPATI NGADA"], key="label_ttd")
            pjb = st.text_input("Nama Pejabat", key="pjb_val")
            gol_pjb = st.text_input("Pangkat/Gol", key="gol_pjb_val")
            jab_ttd = st.text_input("Jabatan", key="jab_ttd_val")
            nip_ttd = st.text_input("NIP", key="nip_ttd_val")

        if st.button("🖨️ PROSES CETAK"):
            # Simpan ke register
            for p in daftar_pegawai:
                st.session_state.arsip_register.append({
                    "Nama": p['nama'], "No SPT": no_spt, "Tujuan": tujuan, "Tgl": tgl_bkt
                })
            # Trigger Print Browser
            st.components.v1.html("<script>window.parent.print();</script>", height=0)

# --- FUNGSI HELPER TTD ---
def render_ttd(space=70):
    return f'''
    <div style="margin-left:55%; margin-top:20px; text-align:center; line-height:1.2;">
        <b>{ttd_label}</b><br>{jab_ttd}<br>
        <div style="height:{space}px;"></div>
        <b><u>{pjb}</u></b><br>{gol_pjb}<br>NIP. {nip_ttd}
    </div>'''

# 4. RENDER TAMPILAN
html_out = '<div class="main-container">'

if tab_menu == "Input & Cetak":
    # 1. TEMPLATE SPT
    if "SPT" in opsi_cetak:
        kop = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>BAJAWA</p></td><td width="15%"></td></tr></table>'''
        
        p_list = ""
        for i, p in enumerate(daftar_pegawai):
            p_list += f'''
            <tr><td width="12%">Kepada</td><td width="5%">:</td><td width="5%">{i+1}.</td><td width="20%">Nama</td><td>: <b>{p['nama']}</b></td></tr>
            <tr><td colspan="3"></td><td>NIP/Gol</td><td>: {p['nip']} / {p['gol']}</td></tr>
            <tr><td colspan="3"></td><td>Jabatan</td><td>: {p['jab']}</td></tr>'''

        html_out += f'''
        <div class="kertas">
            {kop}
            <div class="judul-rapat"><h3 class="underline">SURAT PERINTAH TUGAS</h3><p>Nomor: {no_spt}</p></div>
            <table class="visum-table"><tr><td width="12%">Dasar</td><td width="5%">:</td><td>{anggaran}</td></tr></table>
            <p class="text-center text-bold" style="margin:15px 0;">MEMERINTAHKAN:</p>
            <table class="visum-table">{p_list}</table>
            <table class="visum-table" style="margin-top:20px;"><tr><td width="12%">Untuk</td><td width="5%">:</td><td>{maksud} ke {tujuan} selama {lama}.</td></tr></table>
            {render_ttd()}
        </div>'''

    # 2. TEMPLATE SPD DEPAN
    if "SPD Depan" in opsi_cetak:
        for p in daftar_pegawai:
            html_out += f'''
            <div class="kertas">
                <table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2></td><td width="15%"></td></tr></table>
                <div style="margin-left:60%; font-size:9pt;">
                    Nomor SPD: {p['spd']}<br>Lembar: {p['lembar']}
                </div>
                <div class="judul-rapat"><h3 class="underline">SURAT PERJALANAN DINAS (SPD)</h3></div>
                <table class="tabel-border">
                    <tr><td class="text-center">1</td><td>Pejabat Pemberi Perintah</td><td>BUPATI NGADA</td></tr>
                    <tr><td class="text-center">2</td><td>Nama Pegawai</td><td><b>{p['nama']}</b></td></tr>
                    <tr><td class="text-center">3</td><td>Pangkat / Jabatan</td><td>{p['gol']} / {p['jab']}</td></tr>
                    <tr><td class="text-center">4</td><td>Maksud Perjalanan</td><td>{maksud}</td></tr>
                    <tr><td class="text-center">5</td><td>Alat Angkut</td><td>{alat}</td></tr>
                    <tr><td class="text-center">6</td><td>Tempat Berangkat / Tujuan</td><td>Bajawa / {tujuan}</td></tr>
                    <tr><td class="text-center">7</td><td>Lama / Tgl Berangkat</td><td>{lama} / {tgl_bkt}</td></tr>
                    <tr><td class="text-center">8</td><td>Pembebanan Anggaran</td><td>Bagian Perekonomian dan SDA</td></tr>
                </table>
                {render_ttd(50)}
            </div>'''

html_out += '</div>'
st.markdown(html_out, unsafe_allow_html=True)

# 5. KELOLA REGISTER
if tab_menu == "Kelola Register":
    st.subheader("📂 DATA REGISTER TERSIMPAN")
    if st.session_state.arsip_register:
        st.table(pd.DataFrame(st.session_state.arsip_register))
