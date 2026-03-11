import streamlit as st
from datetime import datetime

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem Cetak Dokumen Prokopim", layout="wide")

st.markdown("""
<style>
    header, footer, #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* CSS UNTUK TAMPILAN KERTAS A4 */
    .kertas-a4 {
        background-color: white;
        width: 210mm;
        min-height: 297mm;
        padding: 15mm 20mm;
        margin: 10px auto;
        color: black;
        font-family: "Arial", sans-serif;
        font-size: 10pt;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
        box-sizing: border-box;
    }

    /* TABEL STANDAR */
    .tabel-full { width: 100%; border-collapse: collapse; margin-top: 10px; }
    .tabel-full td, .tabel-full th { border: 1px solid black; padding: 5px; }

    /* TABEL SPD BELAKANG (PRESISI EXCEL) */
    .tabel-belakang { width: 100%; border: 1.5px solid black; border-collapse: collapse; table-layout: fixed; }
    .tabel-belakang td { border: 1.5px solid black; padding: 8px; vertical-align: top; }
    .col-kiri { width: 44%; }
    .col-kanan { width: 56%; }

    @media print {
        .stSidebar, .stButton, .no-print { display: none !important; }
        @page { size: A4; margin: 0; }
        .kertas-a4 { margin: 0 !important; box-shadow: none !important; border: none !important; page-break-after: always; }
    }
</style>
""", unsafe_allow_html=True)

def format_indo(tgl):
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    return f"{tgl.day} {bulan[tgl.month-1]} {tgl.year}"

# 2. INPUT DATA (SIDEBAR)
with st.sidebar:
    st.header("📋 Data Utama")
    no_spt = st.text_input("Nomor SPT", "094/PROKOPIM/388/02/2026")
    maksud = st.text_area("Maksud Tugas", "Melakukan Perjalanan Dinas dalam rangka...")
    tujuan = st.text_input("Tujuan", "Kupang")
    alat_angkut = st.text_input("Alat Angkut", "Pesawat Udara / Kendaraan Dinas")
    tgl_p = st.date_input("Berangkat", datetime(2026, 2, 9))
    tgl_k = st.date_input("Kembali", datetime(2026, 2, 11))
    
    st.markdown("---")
    st.header("👥 Data Pegawai")
    input_pegawai = st.text_area("Format: Nama | NIP | Jabatan", 
                                 "RAYMUNDUS BENA, S.S., M.Hum | 19XXXXXXXXXXXXXX | Wakil Bupati Ngada")
    
    daftar = []
    for line in input_pegawai.split('\n'):
        if '|' in line:
            parts = line.split('|')
            daftar.append({"nama": parts[0].strip(), "nip": parts[1].strip(), "jabatan": parts[2].strip()})

    if st.button("🖨️ CETAK SEMUA DOKUMEN"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

# 3. RENDER DOKUMEN (PREVIEW)
if daftar:
    # --- HALAMAN 1: SPT ---
    st.subheader("1. Halaman SPT")
    rows_spt = "".join([f"<tr><td align='center'>{i+1}</td><td>{p['nama']}</td><td>{p['nip']}</td><td>{p['jabatan']}</td></tr>" for i, p in enumerate(daftar)])
    st.markdown(f"""
    <div class="kertas-a4">
        <h3 align="center" style="text-decoration:underline; margin-bottom:0;">SURAT PERINTAH TUGAS</h3>
        <p align="center">Nomor: {no_spt}</p>
        <br>
        <p><b>DASAR:</b> Program Kerja Sekretariat Daerah Kabupaten Ngada.</p>
        <p><b>MEMERINTAHKAN:</b></p>
        <table class="tabel-full">
            <tr><th>No</th><th>Nama</th><th>NIP</th><th>Jabatan</th></tr>
            {rows_spt}
        </table>
        <br>
        <p><b>UNTUK:</b> {maksud} ke {tujuan} pada {format_indo(tgl_p)} s/d {format_indo(tgl_k)}.</p>
        <div style="margin-left:55%; margin-top:40px; text-align:center;">
            <b>BUPATI NGADA</b><br><br><br><br>
            <u><b>ANDREAS PARU</b></u>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- HALAMAN 2: SPD DEPAN ---
    st.subheader("2. Halaman SPD Depan")
    for p in daftar:
        st.markdown(f"""
        <div class="kertas-a4">
            <h3 align="center">SURAT PERJALANAN DINAS (SPD)</h3>
            <table class="tabel-full">
                <tr><td width="5%">1.</td><td width="45%">Pejabat Pemberi Perintah</td><td>Sekretaris Daerah</td></tr>
                <tr><td>2.</td><td>Nama Pegawai yang diperintah</td><td><b>{p['nama']}</b></td></tr>
                <tr><td>3.</td><td>a. NIP<br>b. Jabatan</td><td>{p['nip']}<br>{p['jabatan']}</td></tr>
                <tr><td>4.</td><td>Maksud Perjalanan Dinas</td><td>{maksud}</td></tr>
                <tr><td>5.</td><td>Alat Angkut yang dipergunakan</td><td>{alat_angkut}</td></tr>
                <tr><td>6.</td><td>a. Tempat Berangkat<br>b. Tempat Tujuan</td><td>Bajawa<br>{tujuan}</td></tr>
                <tr><td>7.</td><td>Lama Perjalanan Dinas</td><td>3 (Tiga) Hari</td></tr>
            </table>
            <div style="margin-left:55%; margin-top:40px; text-align:center;">
                <p>Ditetapkan di: Bajawa</p>
                <b>Sekretaris Daerah</b><br><br><br><br>
                <b>( NAMA SEKDA )</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- HALAMAN 3: SPD BELAKANG ---
    st.subheader("3. Halaman SPD Belakang")
    for p in daftar:
        st.markdown(f"""
        <div class="kertas-a4">
            <table class="tabel-belakang">
                <tr style="height:5.5cm;">
                    <td class="col-kiri"></td>
                    <td class="col-kanan">
                        I. Berangkat dari : Bajawa <br> Ke : {tujuan} <br> Tanggal : {format_indo(tgl_p)}
                        <div align="center"><br><b>BUPATI NGADA</b><br><br><br><br><u><b>{p['nama']}</b></u></div>
                    </td>
                </tr>
                <tr style="height:4.5cm;">
                    <td>II. Tiba di : {tujuan}<br>Tanggal : {format_indo(tgl_p)}</td>
                    <td>Berangkat dari : {tujuan}<br>Ke : Bajawa<br>Tanggal : {format_indo(tgl_k)}</td>
                </tr>
                <tr style="height:4.5cm;"><td>III. Tiba di :</td><td>Berangkat dari :</td></tr>
                <tr style="height:5.5cm;">
                    <td>V. Tiba Kembali : Bajawa<br>Tanggal : {format_indo(tgl_k)}</td>
                    <td style="font-style:italic; font-size:9pt;">Telah diperiksa...
                        <div align="center" style="font-style:normal;"><br><b>BUPATI NGADA</b><br><br><br><br><b>....................</b></div>
                    </td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
