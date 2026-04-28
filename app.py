import streamlit as st
import pandas as pd
from datetime import datetime
import logo  # Pastikan file logo.py ada di folder yang sama
from io import BytesIO

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Ngada Pro", layout="wide")

# --- KUNCI DATA AGAR TIDAK HILANG (SESSION STATE) ---
if 'jml' not in st.session_state: st.session_state.jml = 1
if 'arsip_register' not in st.session_state: st.session_state.arsip_register = []

# 2. CSS TERBAIK UNTUK KONSISTENSI LAYAR & CETAK
st.markdown("""
<style>
    /* UI Streamlit */
    header, footer, .stDeployButton { display: none !important; }
    .stApp { background-color: #525659 !important; }
    
    /* Container untuk memposisikan kertas di tengah layar */
    .main-container { 
        display: flex; flex-direction: column; align-items: center; 
        width: 100%; padding: 20px 0; 
    }

    /* KERTAS LEGAL (DIKUNCI 215.9 x 330 mm) */
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
    .tabel-border td { border: 1pt solid black !important; padding: 5px 8px; vertical-align: top; font-size: 9.5pt; color: black !important; }
    .visum-table { width: 100%; border-collapse: collapse; }
    .visum-table td { padding: 2px 0; vertical-align: top; font-size: 10pt; color: black !important; }

    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }

    /* Pengaturan saat Print */
    @media print {
        @page { size: legal portrait; margin: 0; }
        .stApp { background-color: white !important; }
        [data-testid="stSidebar"], .stButton, .no-print { display: none !important; }
        .main-container { padding: 0 !important; margin: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; border: none !important; }
    }
</style>
""", unsafe_allow_html=True)

# 3. NAVIGASI INPUT (SIDEBAR)
with st.sidebar:
    st.header("📋 NAVIGASI INPUT")
    tab_menu = st.radio("Pilih Menu", ["Input & Cetak", "Riwayat Register"])
    
    if tab_menu == "Input & Cetak":
        wilayah = st.selectbox("Wilayah", ["Dalam Daerah", "Luar Daerah"])
        opsi_cetak = st.multiselect("Dokumen", ["SPT", "SPD Depan", "SPD Belakang"], default=["SPT", "SPD Depan"])
        
        # --- INPUT NAMA YANG BERTUGAS ---
        st.subheader("👤 PEGAWAI BERTUGAS")
        c1, c2 = st.columns(2)
        if c1.button("➕ Tambah"): st.session_state.jml += 1
        if c2.button("➖ Hapus") and st.session_state.jml > 1: st.session_state.jml -= 1
        
        daftar = []
        for i in range(st.session_state.jml):
            with st.expander(f"Pegawai {i+1}", expanded=(i==0)):
                p = {
                    "nama": st.text_input("Nama", key=f"nm_{i}"),
                    "nip": st.text_input("NIP", key=f"np_{i}"),
                    "gol": st.text_input("Gol", "III/a", key=f"gl_{i}"),
                    "jab": st.text_input("Jabatan", key=f"jb_{i}"),
                    "spd": st.text_input("No SPD", f"530 /02/2026", key=f"sd_{i}"),
                    "lembar": st.text_input("Lembar ke", "I", key=f"lb_{i}")
                }
                daftar.append(p)

        # --- INPUT DATA UTAMA ---
        with st.expander("📄 DETAIL PERJALANAN"):
            no_spt = st.text_input("No SPT", "094/Prokopim/557/02/2026")
            maksud = st.text_area("Maksud", "Dampingi Bupati...")
            tujuan = st.text_input("Tujuan", "Riung")
            tgl_bkt = st.text_input("Tgl Berangkat", "17 Maret 2026")
            tgl_kbl = st.text_input("Tgl Kembali", "18 Maret 2026")
            lama = st.text_input("Lama", "2 (Dua) hari")
            anggaran = st.text_area("Dasar", "DPA Bagian Perekonomian 2026")

        # --- INPUT PENANDA TANGAN ---
        with st.expander("🖋️ PENANDA TANGAN"):
            ttd_label = st.selectbox("Label TTD", ["An. BUPATI NGADA", "WAKIL BUPATI NGADA", "BUPATI NGADA"])
            pjb = st.text_input("Nama Pejabat", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
            jab_ttd = st.text_input("Jabatan", "Pj. Sekretaris Daerah")
            ub = st.text_input("Ub. (Jika Ada)", "Asisten Perekonomian")
            nip_ttd = st.text_input("NIP Pejabat", "19710328 199203 1 011")

        if st.button("🖨️ PROSES CETAK"):
            # Simpan ke register sebelum print
            for p in daftar:
                st.session_state.arsip_register.append({"Nama": p['nama'], "Tujuan": tujuan, "Tgl": tgl_bkt})
            st.components.v1.html("<script>window.parent.print();</script>", height=0)

# --- FUNGSI RENDER TTD ---
def get_ttd_html(space=70):
    ub_html = f"Ub. {ub},<br>" if (ub and ttd_label == "An. BUPATI NGADA") else ""
    jab_html = f"{jab_ttd},<br>" if ttd_label == "An. BUPATI NGADA" else ""
    return f'''
    <div style="margin-left:55%; margin-top:20px; text-align:center; line-height:1.2;">
        <b>{ttd_label}</b><br>{jab_html}{ub_html}
        <div style="height:{space}px;"></div>
        <b><u>{pjb}</u></b><br>NIP. {nip_ttd}
    </div>'''

# 4. TAMPILAN KERTAS (OUTPUT)
html_content = '<div class="main-container">'

if tab_menu == "Input & Cetak":
    # --- HALAMAN SPT ---
    if "SPT" in opsi_cetak:
        kop_f = f'<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>BAJAWA</p></td><td width="15%"></td></tr></table>'
        
        pegawai_rows = ""
        for i, p in enumerate(daftar):
            pegawai_rows += f'''
            <tr><td width="12%">Kepada</td><td width="5%">:</td><td width="5%">{i+1}.</td><td width="20%">Nama</td><td>: <b>{p['nama']}</b></td></tr>
            <tr><td colspan="3"></td><td>NIP</td><td>: {p['nip']}</td></tr>
            <tr><td colspan="3"></td><td>Jabatan</td><td>: {p['jab']}</td></tr>'''

        html_content += f'''
        <div class="kertas">
            {kop_f}
            <div class="judul-rapat"><h3 class="underline">SURAT PERINTAH TUGAS</h3><p>Nomor: {no_spt}</p></div>
            <table class="visum-table"><tr><td width="12%">Dasar</td><td width="5%">:</td><td>{anggaran}</td></tr></table>
            <p class="text-center text-bold" style="margin:10px 0;">MEMERINTAHKAN:</p>
            <table class="visum-table">{pegawai_rows}</table>
            <table class="visum-table" style="margin-top:20px;"><tr><td width="12%">Untuk</td><td width="5%">:</td><td>{maksud} ke {tujuan} selama {lama}.</td></tr></table>
            {get_ttd_html()}
        </div>'''

    # --- HALAMAN SPD ---
    if "SPD Depan" in opsi_cetak:
        for p in daftar:
            html_content += f'''
            <div class="kertas">
                <div style="margin-left:60%; line-height:1.2;">No SPD: {p['spd']}<br>Lembar ke: {p['lembar']}</div>
                <div class="judul-rapat"><h3 class="underline">SURAT PERJALANAN DINAS</h3></div>
                <table class="tabel-border">
                    <tr><td width="5%" class="text-center">1</td><td width="40%">Nama Pegawai</td><td><b>{p['nama']}</b></td></tr>
                    <tr><td class="text-center">2</td><td>NIP / Gol</td><td>{p['nip']} / {p['gol']}</td></tr>
                    <tr><td class="text-center">3</td><td>Maksud Perjalanan</td><td>{maksud}</td></tr>
                    <tr><td class="text-center">4</td><td>Tempat Tujuan</td><td>{tujuan}</td></tr>
                    <tr><td class="text-center">5</td><td>Lama Perjalanan</td><td>{lama} ({tgl_bkt} s/d {tgl_kbl})</td></tr>
                </table>
                {get_ttd_html(55)}
            </div>'''

html_content += '</div>'
st.markdown(html_content, unsafe_allow_html=True)
