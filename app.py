import streamlit as st
import pandas as pd
from datetime import datetime
import logo  # Memastikan file logo.py ada di repository
from io import BytesIO

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Ngada Pro", layout="wide")

# INISIALISASI DATABASE REGISTER
if 'arsip_register' not in st.session_state:
    st.session_state.arsip_register = []

# 2. CSS UNTUK STABILITAS TAMPILAN & PRESISI CETAK
st.markdown("""
<style>
    /* Sembunyikan elemen bawaan Streamlit */
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    
    /* Background abu-abu seperti PDF Viewer */
    .stApp { 
        background-color: #525659 !important; 
    }

    /* Container utama agar kertas di tengah */
    .main-container { 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        width: 100%; 
        padding: 20px 0; 
    }

    /* KERTAS UMUM (PORTRAIT LEGAL) - Dikunci ukurannya */
    .kertas { 
        background-color: white !important; 
        width: 215.9mm; 
        height: 330mm; 
        padding: 15mm 20mm; 
        margin-bottom: 30px; 
        color: black !important; 
        font-family: Arial, sans-serif; 
        box-sizing: border-box; 
        box-shadow: 0 0 20px rgba(0,0,0,0.5);
        font-size: 10.5pt; 
        page-break-after: always; 
        position: relative;
        flex-shrink: 0; /* Mencegah kertas gepeng di layar kecil */
    }

    /* KOP SURAT */
    .kop-table { width: 100%; border: none !important; border-bottom: 3.5pt solid black !important; margin-bottom: 10px; }
    .kop-table td { border: none !important; padding: 0 !important; vertical-align: middle; }
    .kop-teks { text-align: center; line-height: 1.1 !important; } 
    .kop-teks h3, .kop-teks h2, .kop-teks p { margin: 0; padding: 1px 0; }

    /* KHUSUS KOP GARUDA */
    .kop-garuda { text-align: center; margin-bottom: 15px; width: 100%; }
    .kop-garuda img { width: 80px; margin-bottom: 5px; }
    .kop-garuda h2 { margin: 0; font-size: 16pt; font-weight: bold; letter-spacing: 2px; }

    .judul-rapat { text-align: center; line-height: 1.2; margin-top: 10px; margin-bottom: 15px; }
    .judul-rapat h3, .judul-rapat p { margin: 0; }

    /* TABEL SPD */
    .tabel-border { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; table-layout: fixed; }
    .tabel-border td { border: 1pt solid black !important; padding: 5px 8px !important; vertical-align: top; color: black !important; font-size: 9.5pt; line-height: 1.2; }
    
    .col-no { width: 35px !important; text-align: center !important; }

    .visum-table { width: 100%; border: none !important; border-collapse: collapse; margin: 0 !important; }
    .visum-table td { border: none !important; padding: 1px 0 !important; font-size: 10pt; line-height: 1.3; color: black !important; }

    .text-center { text-align: center; } 
    .text-bold { font-weight: bold; } 
    .underline { text-decoration: underline; }

    /* Pengaturan Cetak */
    @media print {
        @page { size: legal portrait; margin: 0; }
        body { margin: 0; }
        .stApp { background-color: white !important; }
        [data-testid="stSidebar"], .stButton, .no-print { display: none !important; }
        .main-container { padding: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; width: 215.9mm; height: 330mm; }
    }
</style>
""", unsafe_allow_html=True)

# 3. SIDEBAR PANEL KONTROL
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
                st.markdown(f"---")
                daftar.append({
                    "nama": st.text_input(f"Nama Pegawai {i+1}", f"Nama {i+1}", key=f"n{i}"),
                    "nip": st.text_input(f"NIP {i+1}", "19XXXXXXXXXXXXXX", key=f"nip{i}"),
                    "gol": st.text_input(f"Gol {i+1}", "III/a", key=f"g{i}"),
                    "jab": st.text_input(f"Jabatan {i+1}", "Pelaksana", key=f"j{i}"),
                    "spd": st.text_input(f"No SPD {i+1}", f"530 /02/2026", key=f"spd{i}"),
                    "lembar": st.text_input(f"Lembar ke {i+1}", "I", key=f"lbr{i}")
                })

        with st.expander("📄 DATA PERJALANAN"):
            no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
            kode_spd = st.text_input("Kode No SPD", "094/Prokopim")
            maksud = st.text_area("Maksud Perjalanan", "Dalam rangka mendampingi...")
            tujuan = st.text_input("Tujuan", "Kecamatan Riung")
            alat = st.text_input("Alat Angkut", "Mobil Dinas")
            lama = st.text_input("Lama Hari", "1 (Satu) hari")
            tgl_bkt = st.text_input("Tanggal Berangkat", "17 Maret 2026")
            tgl_kbl = st.text_input("Tanggal Pulang", "17 Maret 2026")
            default_dasar = "DPA Bagian Perekonomian dan SDA Setda Ngada 2026" if wilayah == "Dalam Daerah" else ""
            anggaran = st.text_area("Dasar Anggaran", value=default_dasar)

        st.subheader("🖋️ PENANDATANGAN")
        ttd_label = st.selectbox("Label TTD", ["An. BUPATI NGADA", "WAKIL BUPATI NGADA", "BUPATI NGADA"])
        pjb = st.text_input("Nama Pejabat", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
        gol_pjb = st.text_input("Pangkat/Gol Pejabat", "Pembina Utama Muda - IV/c")
        jab_ttd = st.text_input("Jabatan Utama", "Pj. Sekretaris Daerah")
        ub = st.text_input("Atas Nama (Ub.)", "Asisten Perekonomian dan Pembangunan")
        nip_ttd = st.text_input("NIP Pejabat", "19710328 199203 1 011")

        if st.button("🖨️ PROSES & CETAK"):
            for p in daftar:
                st.session_state.arsip_register.append({
                    "Nama": p['nama'], "No SPT": no_spt, "No SPD": p['spd'],
                    "Tujuan": tujuan, "Berangkat": tgl_bkt, "Pulang": tgl_kbl, "Lama": lama, "Ket": wilayah
                })
            st.components.v1.html("<script>setTimeout(function(){ window.parent.print(); }, 1000);</script>", height=0)

    elif tab_menu == "Kelola Register":
        st.subheader("📂 RIWAYAT REGISTER")
        if st.session_state.arsip_register:
            df_reg = pd.DataFrame(st.session_state.arsip_register)
            st.dataframe(df_reg, use_container_width=True)
            if st.button("🧹 Kosongkan Data"):
                st.session_state.arsip_register = []
                st.rerun()

# 4. LOGIKA EXCEL
if st.session_state.arsip_register:
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        pd.DataFrame(st.session_state.arsip_register).to_excel(writer, index=False, sheet_name='Register_SPD')
    st.sidebar.download_button(label="📥 DOWNLOAD EXCEL", data=output.getvalue(), file_name=f"SPD_{datetime.now().strftime('%Y%m%d')}.xlsx")

# 5. FUNGSI RENDER KOMPONEN HTML
def render_ttd(space): 
    label_final = f"<b>{ttd_label}</b>"
    jab_final = f"<br>{jab_ttd}," if ttd_label == "An. BUPATI NGADA" else ""
    ub_final = f"<br>Ub. {ub}," if (ub and ttd_label == "An. BUPATI NGADA") else ""
    return f'''
    <div style="width: 100%; margin-top: 15px;">
        <div style="width: 50%; margin-left: 50%; text-align: center; line-height: 1.2;">
            {label_final}{jab_final}{ub_final}
            <div style="height:{space}px;"></div>
            <b><u>{pjb}</u></b><br>{gol_pjb}<br>NIP. {nip_ttd}
        </div>
    </div>
    '''

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

# 6. GENERATE TAMPILAN KERTAS
html_out = '<div class="main-container">'

if tab_menu == "Input & Cetak":
    # HALAMAN SPT
    if "SPT" in opsi_cetak:
        kop_f = f'<div class="kop-garuda"><img src="data:image/png;base64,{logo.GARUDA}"><h2>BUPATI NGADA</h2></div>' if wilayah == "Luar Daerah" else kop_pemda
        p_rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{i+1}.</td><td width='20%'>Nama</td><td width='5%'>:</td><td><b>{p['nama']}</b></td></tr><tr><td></td><td></td><td></td><td>Pangkat/Gol</td><td>:</td><td>{p['gol']}</td></tr><tr><td></td><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr><tr><td></td><td></td><td></td><td>Jabatan</td><td>:</td><td>{p['jab']}</td></tr>" for i, p in enumerate(daftar)])
        html_out += f'''<div class="kertas">{kop_f}
            <div class="judul-rapat"><h3 class="text-bold underline">SURAT PERINTAH TUGAS</h3><p>NOMOR : {no_spt}</p></div>
            <table class="visum-table"><tr><td width="12%">Dasar</td><td width="5%">:</td><td>{anggaran}</td></tr></table>
            <p class="text-center text-bold" style="margin:15px 0;">M E M E R I N T A H K A N</p>
            <table class="visum-table">{p_rows}</table>
            <table class="visum-table" style="margin-top:20px;"><tr><td width="12%">Untuk</td><td width="5%">:</td><td>{maksud} ke {tujuan} selama {lama} terhitung tanggal {tgl_bkt}.</td></tr></table>
            {render_ttd(80)}</div>'''

    # HALAMAN SPD PER PEGAWAI
    for p in daftar:
        if "SPD Depan" in opsi_cetak:
            html_out += f'''<div class="kertas">{kop_pemda}
                <div style="margin-left:60%; line-height:1.1;"><table class="visum-table"><tr><td width="40%">Lembar ke</td><td width="5%">:</td><td>{p["lembar"]}</td></tr><tr><td>Kode No</td><td>:</td><td>{kode_spd}</td></tr><tr><td>Nomor</td><td>:</td><td>{p["spd"]}</td></tr></table></div>
                <div class="judul-rapat"><h3 class="text-bold underline">SURAT PERJALANAN DINAS</h3><h3 class="text-bold">(SPD)</h3></div>
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
                    <tr style="height:25px;"><td></td><td>1.</td><td></td><td colspan="2"></td></tr>
                    <tr><td class="col-no" rowspan="3">9.</td><td>Pembebanan Anggaran</td><td colspan="3"></td></tr>
                    <tr><td>a. Instansi</td><td colspan="3">a. Bagian Perekonomian dan SDA</td></tr>
                    <tr><td>b. Mata Anggaran</td><td colspan="3"></td></tr>
                    <tr><td class="col-no">10.</td><td>Keterangan lain-lain</td><td colspan="3">-</td></tr>
                </table>{render_ttd(60)}</div>'''

        if "SPD Belakang" in opsi_cetak:
            html_out += f'''<div class="kertas">
                <table class="tabel-border" style="height:85%;">
                    <tr style="height:18%;"><td width="50%"></td><td><table class="visum-table"><tr><td width="10%">I.</td><td width="35%">Berangkat dari</td><td>: Bajawa</td></tr><tr><td></td><td>Ke</td><td>: {tujuan}</td></tr><tr><td></td><td>Pada Tanggal</td><td>: {tgl_bkt}</td></tr></table>{render_ttd(40)}</td></tr>
                    <tr style="height:18%;"><td><table class="visum-table"><tr><td width="10%">II.</td><td width="35%">Tiba di</td><td>: {tujuan}</td></tr><tr><td></td><td>Pada Tanggal</td><td>: {tgl_bkt}</td></tr></table></td><td><table class="visum-table"><tr><td width="10%"></td><td width="35%">Berangkat dari</td><td>: {tujuan}</td></tr><tr><td></td><td>Ke</td><td>: Bajawa</td></tr><tr><td></td><td>Pada Tanggal</td><td>: {tgl_kbl}</td></tr></table></td></tr>
                    <tr style="height:18%;"><td><table class="visum-table"><tr><td width="10%">III.</td><td width="35%">Tiba di</td><td>: </td></tr><tr><td></td><td>Pada Tanggal</td><td>: </td></tr></table></td><td><table class="visum-table"><tr><td width="10%"></td><td width="35%">Berangkat dari</td><td>: </td></tr><tr><td></td><td>Ke</td><td>: </td></tr><tr><td></td><td>Pada Tanggal</td><td>: </td></tr></table></td></tr>
                    <tr style="height:18%;"><td><table class="visum-table"><tr><td width="10%">IV.</td><td width="35%">Tiba di</td><td>: </td></tr><tr><td></td><td>Pada Tanggal</td><td>: </td></tr></table></td><td><table class="visum-table"><tr><td width="10%"></td><td width="35%">Berangkat dari</td><td>: </td></tr><tr><td></td><td>Ke</td><td>: </td></tr><tr><td></td><td>Pada Tanggal</td><td>: </td></tr></table></td></tr>
                    <tr style="height:20%;"><td><table class="visum-table"><tr><td width="10%">V.</td><td width="35%">Tiba di</td><td>: Bajawa</td></tr><tr><td></td><td>Pada Tanggal</td><td>: {tgl_kbl}</td></tr></table></td><td><p style="font-style:italic; font-size:9pt;">Telah diperiksa dengan keterangan bahwa perjalanan tersebut atas perintahnya dan semata-mata untuk kepentingan jabatan</p>{render_ttd(40)}</td></tr>
                </table>
                <div style="border:1pt solid black; border-top:none; padding:10px; font-size:9.5pt;"><b>VI. Catatan Lain-lain</b></div>
                <div style="border:1pt solid black; border-top:none; padding:10px; font-size:8.5pt; text-align:justify;"><b>VII. Perhatian:</b> Pejabat yang menerbitkan SPD, pegawai yang melakukan perjalanan dinas, para pejabat yang mengesahkan tanggal berangkat/tiba, serta Bendahara Pengeluaran bertanggung jawab berdasarkan peraturan-peraturan Keuangan Negara apabila negara menderita rugi akibat kesalahan, kelalaian dan kealpaannya.</div>
            </div>'''

html_out += '</div>'
st.markdown(html_out, unsafe_allow_html=True)
