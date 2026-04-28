import streamlit as st
import pandas as pd
from datetime import datetime
import logo  
from io import BytesIO

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Ngada Pro", layout="wide")

# --- INISIALISASI SESSION STATE (AGAR DATA TIDAK HILANG) ---
if 'arsip_register' not in st.session_state:
    st.session_state.arsip_register = []

# Inisialisasi default nilai input jika belum ada
if 'form_data' not in st.session_state:
    st.session_state.form_data = {
        "no_spt": "094/Prokopim/557/02/2026",
        "kode_spd": "094/Prokopim",
        "maksud": "Dalam rangka mendampingi...",
        "tujuan": "Kecamatan Riung",
        "alat": "Mobil Dinas",
        "lama": "1 (Satu) hari",
        "tgl_bkt": "17 Maret 2026",
        "tgl_kbl": "17 Maret 2026",
        "anggaran": "DPA Bagian Perekonomian dan SDA Setda Ngada 2026"
    }

# 2. CSS UNTUK PRESISI (MODIFIKASI AGAR STABIL)
st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    .stApp { background-color: #525659 !important; }
    .main-container { display: flex; flex-direction: column; align-items: center; width: 100%; padding: 20px 0; }
    .kertas { 
        background-color: white !important; width: 215.9mm; height: 330mm; 
        padding: 15mm 20mm; margin-bottom: 30px; color: black !important; 
        font-family: Arial, sans-serif; box-sizing: border-box; 
        box-shadow: 0 0 20px rgba(0,0,0,0.5); font-size: 10.5pt; 
        page-break-after: always; position: relative; flex-shrink: 0;
    }
    .kop-table { width: 100%; border: none !important; border-bottom: 3.5pt solid black !important; margin-bottom: 10px; }
    .kop-table td { border: none !important; padding: 0 !important; vertical-align: middle; }
    .kop-teks { text-align: center; line-height: 1.1 !important; }
    .tabel-border { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; table-layout: fixed; }
    .tabel-border td { border: 1pt solid black !important; padding: 5px 8px !important; vertical-align: top; color: black !important; font-size: 9.5pt; }
    .visum-table { width: 100%; border: none !important; border-collapse: collapse; margin: 0 !important; }
    .visum-table td { border: none !important; padding: 1px 0 !important; font-size: 10pt; color: black !important; }
    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }
    @media print {
        @page { size: legal portrait; margin: 0; }
        .stApp { background-color: white !important; }
        [data-testid="stSidebar"], .stButton, .no-print { display: none !important; }
        .main-container { padding: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; width: 215.9mm; height: 330mm; }
    }
</style>
""", unsafe_allow_html=True)

# 3. SIDEBAR
with st.sidebar:
    st.header("📋 PANEL KONTROL")
    wilayah = st.selectbox("Jenis Wilayah", ["Dalam Daerah", "Luar Daerah"])
    tab_menu = st.radio("Menu", ["Input & Cetak", "Kelola Register"])
    
    if tab_menu == "Input & Cetak":
        opsi_cetak = st.multiselect("Pilih Dokumen", ["SPT", "SPD Depan", "SPD Belakang"], default=["SPT", "SPD Depan", "SPD Belakang"])
        
        with st.expander("👤 DATA PEGAWAI", expanded=True):
            if 'jml' not in st.session_state: st.session_state.jml = 1
            c1, c2 = st.columns(2)
            if c1.button("➕ Tambah"): st.session_state.jml += 1
            if c2.button("➖ Hapus") and st.session_state.jml > 1: st.session_state.jml -= 1
            
            daftar = []
            for i in range(st.session_state.jml):
                st.markdown(f"**Pegawai {i+1}**")
                daftar.append({
                    "nama": st.text_input(f"Nama", value=f"Nama {i+1}", key=f"n{i}"),
                    "nip": st.text_input(f"NIP", value="19XXXXXXXXXXXXXX", key=f"nip{i}"),
                    "gol": st.text_input(f"Gol", value="III/a", key=f"g{i}"),
                    "jab": st.text_input(f"Jabatan", value="Pelaksana", key=f"j{i}"),
                    "spd": st.text_input(f"No SPD", value=f"530 /02/2026", key=f"spd{i}"),
                    "lembar": st.text_input(f"Lembar ke", value="I", key=f"lbr{i}")
                })

        with st.expander("📄 DATA UTAMA"):
            # Menggunakan session_state agar inputan dikunci
            no_spt = st.text_input("Nomor SPT", value=st.session_state.form_data["no_spt"])
            kode_spd = st.text_input("Kode No SPD", value=st.session_state.form_data["kode_spd"])
            maksud = st.text_area("Maksud Perjalanan", value=st.session_state.form_data["maksud"])
            tujuan = st.text_input("Tujuan", value=st.session_state.form_data["tujuan"])
            alat = st.text_input("Alat Angkut", value=st.session_state.form_data["alat"])
            lama = st.text_input("Lama Hari", value=st.session_state.form_data["lama"])
            tgl_bkt = st.text_input("Tanggal Berangkat", value=st.session_state.form_data["tgl_bkt"])
            tgl_kbl = st.text_input("Tanggal Pulang", value=st.session_state.form_data["tgl_kbl"])
            anggaran = st.text_area("Dasar Anggaran", value=st.session_state.form_data["anggaran"])

            # Simpan perubahan ke session_state tiap kali ada input
            st.session_state.form_data.update({
                "no_spt": no_spt, "kode_spd": kode_spd, "maksud": maksud, "tujuan": tujuan,
                "alat": alat, "lama": lama, "tgl_bkt": tgl_bkt, "tgl_kbl": tgl_kbl, "anggaran": anggaran
            })

        st.subheader("🖋️ TANDA TANGAN")
        ttd_label = st.selectbox("Penandatangan", ["An. BUPATI NGADA", "WAKIL BUPATI NGADA", "BUPATI NGADA"])
        pjb = st.text_input("Nama Pejabat", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
        gol_pjb = st.text_input("Pangkat/Gol", "Pembina Utama Muda - IV/c")
        jab_ttd = st.text_input("Jabatan Utama", "Pj. Sekretaris Daerah")
        ub = st.text_input("Ub.", "Asisten Perekonomian dan Pembangunan")
        nip_ttd = st.text_input("NIP", "19710328 199203 1 011")

        if st.button("🖨️ PROSES CETAK & SIMPAN"):
            for p in daftar:
                st.session_state.arsip_register.append({
                    "Nama": p['nama'], "No SPT": no_spt, "No SPD": p['spd'],
                    "Tujuan": tujuan, "Berangkat": tgl_bkt, "Pulang": tgl_kbl, "Lama": lama, "Ket": wilayah
                })
            # Script cetak otomatis
            st.components.v1.html("<script>setTimeout(function(){ window.parent.print(); }, 1200);</script>", height=0)

# --- FUNGSI RENDER (Sama Seperti Sebelumnya) ---
def get_ttd(space): 
    label_final = f"<b>{ttd_label}</b>"
    jab_final = f"{jab_ttd}," if ttd_label == "An. BUPATI NGADA" else ""
    ub_final = f"Ub. {ub}," if (ub and ttd_label == "An. BUPATI NGADA") else ""
    return f'''<div style="margin-left:55%; margin-top:10px; line-height:1.2; text-align:center;">{label_final}<br>{jab_final}<br>{ub_final}<div style="height:{space}px;"></div><b><u>{pjb}</u></b><br>{gol_pjb}<br>NIP. {nip_ttd}</div>'''

kop_pemda = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834</p><p class="text-bold">BAJAWA</p></td><td width="15%"></td></tr></table>'''

# OUTPUT RENDER KERTAS
html_out = '<div class="main-container">'
if tab_menu == "Input & Cetak":
    if "SPT" in opsi_cetak:
        kop_f = f'<div class="kop-garuda"><img src="data:image/png;base64,{logo.GARUDA}"><h2>BUPATI NGADA</h2></div>' if wilayah == "Luar Daerah" else kop_pemda
        p_rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{i+1}.</td><td width='20%'>Nama</td><td width='5%'>:</td><td><b>{p['nama']}</b></td></tr><tr><td></td><td></td><td></td><td>Pangkat/Gol</td><td>:</td><td>{p['gol']}</td></tr><tr><td></td><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr><tr><td></td><td></td><td></td><td>Jabatan</td><td>:</td><td>{p['jab']}</td></tr>" for i, p in enumerate(daftar)])
        html_out += f'<div class="kertas">{kop_f}<div class="judul-rapat"><h3 class="text-bold underline">SURAT PERINTAH TUGAS</h3><p>NOMOR : {no_spt}</p></div><table class="visum-table"><tr><td width="12%">Dasar</td><td width="5%">:</td><td>{anggaran}</td></tr></table><p class="text-center text-bold" style="margin:10px 0;">M E M E R I N T A H K A N</p><table class="visum-table">{p_rows}</table><table class="visum-table" style="margin-top:25px;"><tr><td width="12%">Untuk</td><td width="5%">:</td><td>{maksud} ke {tujuan}</td></tr></table>{get_ttd(90)}</div>'

    for p in daftar:
        if "SPD Depan" in opsi_cetak:
            html_out += f'''<div class="kertas">{kop_pemda}
                <div style="margin-left:60%; line-height:1.0;"><table class="visum-table"><tr><td width="40%">Lembar ke</td><td width="5%">:</td><td>{p["lembar"]}</td></tr><tr><td>Kode No</td><td>:</td><td>{kode_spd}</td></tr><tr><td>Nomor</td><td>:</td><td>{p["spd"]}</td></tr></table></div>
                <div class="judul-rapat" style="margin-top:5px;"><h3 class="text-bold underline">SURAT PERJALANAN DINAS</h3><h3 class="text-bold">(SPD)</h3></div>
                <table class="tabel-border">
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
                    <tr><td class="col-no">8.</td><td>Pengikut: Nama</td><td class="text-center">Tgl Lahir</td><td colspan="2" class="text-center">Keterangan</td></tr>
                    <tr style="height:20px;"><td></td><td>1.</td><td></td><td colspan="2"></td></tr>
                    <tr><td class="col-no" rowspan="3">9.</td><td>Pembebanan Anggaran</td><td colspan="3"></td></tr>
                    <tr><td>a. Instansi</td><td colspan="3">a. Bagian Perekonomian dan SDA</td></tr>
                    <tr><td>b. Mata Anggaran</td><td colspan="3"></td></tr>
                    <tr><td class="col-no">10.</td><td>Keterangan lain-lain</td><td colspan="3">-</td></tr>
                </table>{get_ttd(65)}</div>'''

html_out += '</div>'
st.markdown(html_out, unsafe_allow_html=True)

# Tambahan untuk Kelola Register di bawah (opsional)
if tab_menu == "Kelola Register":
    st.subheader("📂 RIWAYAT REGISTER")
    if st.session_state.arsip_register:
        st.dataframe(pd.DataFrame(st.session_state.arsip_register), use_container_width=True)
