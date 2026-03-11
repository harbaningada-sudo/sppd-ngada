import streamlit as st
from datetime import datetime

# 1. KONFIGURASI HALAMAN (LAYOUT WIDE AGAR SEPERTI DI LAPTOP)
st.set_page_config(page_title="Sistem SPD Prokopim Ngada", layout="wide")

st.markdown("""
<style>
    /* Menghilangkan UI Streamlit agar bersih */
    header, footer, #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Layout Background Dashboard */
    .main { background-color: #f0f2f6; }

    /* KERTAS A4 (SANGAT PRESISI UNTUK CETAK) */
    .kertas-a4 {
        background-color: white;
        width: 210mm;
        min-height: 297mm;
        padding: 15mm 20mm;
        margin: 10px auto;
        color: black;
        font-family: "Arial", sans-serif;
        font-size: 10.5pt;
        box-shadow: 0 0 15px rgba(0,0,0,0.2);
        box-sizing: border-box;
    }

    /* TABEL IDENTIK TEMPLATE PDF/EXCEL */
    .tabel-excel {
        width: 100%;
        border-collapse: collapse;
        table-layout: fixed;
        margin-top: 10px;
    }
    .tabel-excel td {
        border: 1.5px solid black;
        padding: 6px 10px;
        vertical-align: top;
        line-height: 1.4;
    }
    
    /* PEMBAGIAN KOLOM SPD BELAKANG (Garis Geser Kanan) */
    .col-kiri { width: 44%; }
    .col-kanan { width: 56%; }

    .text-center { text-align: center; }
    .text-underline { text-decoration: underline; }

    @media print {
        .stSidebar, .stButton, .no-print { display: none !important; }
        @page { size: A4; margin: 0; }
        .kertas-a4 { 
            margin: 0 !important; 
            box-shadow: none !important; 
            border: none !important; 
            page-break-after: always; 
        }
    }
</style>
""", unsafe_allow_html=True)

def format_indo(tgl):
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    return f"{tgl.day} {bulan[tgl.month-1]} {tgl.year}"

# 2. OPSI INPUTAN DI SIDEBAR (PERSIS SEPERTI DI PYTHON LOKAL)
with st.sidebar:
    st.header("⚙️ PANEL INPUT DATA")
    
    with st.expander("📄 DATA SURAT (SPT/SPD)", expanded=True):
        no_spt = st.text_input("Nomor SPT", "094/PROKOPIM/388/02/2026")
        no_spd = st.text_input("Nomor SPD", "094/PROKOPIM/388/02/2026")
        maksud = st.text_area("Maksud Perjalanan", "Koordinasi dan Konsultasi...")
        tujuan = st.text_input("Tempat Tujuan", "Kupang")
        alat_angkut = st.text_input("Alat Angkut", "Pesawat Udara / Kendaraan Dinas")
        tingkat_biaya = st.selectbox("Tingkat Biaya", ["Tingkat A", "Tingkat B", "Tingkat C"])

    with st.expander("📅 WAKTU & ANGGARAN", expanded=False):
        tgl_p = st.date_input("Tanggal Berangkat", datetime(2026, 2, 9))
        tgl_k = st.date_input("Tanggal Kembali", datetime(2026, 2, 11))
        lama_hari = st.text_input("Lama Perjalanan", "3 (Tiga)")
        beban_anggaran = st.text_input("Beban Anggaran", "DPA Sekretariat Daerah Kab. Ngada")
        mata_anggaran = st.text_input("Mata Anggaran", "5.1.02.04.01.0001")

    with st.expander("👥 PEJABAT & PEGAWAI", expanded=True):
        pemberi_perintah = st.text_input("Pejabat Pemberi Perintah", "Bupati Ngada")
        nama_ttd = st.text_input("Nama Penandatangan (Bupati)", "ANDREAS PARU")
        st.info("Format: Nama | NIP | Jabatan | Golongan")
        input_pegawai = st.text_area("Daftar Pegawai", "RAYMUNDUS BENA, S.S., M.Hum | 19XXXXXXXXXXXXXX | Wakil Bupati Ngada | Pembina Utama Muda (IV/c)")

    daftar_pegawai = []
    for line in input_pegawai.split('\n'):
        if '|' in line:
            parts = line.split('|')
            daftar_pegawai.append({
                "nama": parts[0].strip(),
                "nip": parts[1].strip(),
                "jabatan": parts[2].strip(),
                "gol": parts[3].strip()
            })

    st.markdown("---")
    if st.button("🖨️ CETAK SEMUA DOKUMEN"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

# 3. LAYOUT PRATINJAU DOKUMEN (PERSIS TEMPLATE PDF)
if daftar_pegawai:
    # --- 1. SPT ---
    st.markdown(f"""<div class="kertas-a4">
        <h3 align="center" class="text-underline">SURAT PERINTAH TUGAS</h3>
        <p align="center" style="margin-top:-10px;">Nomor: {no_spt}</p><br>
        <p><b>MEMERINTAHKAN:</b></p>
        <table class="tabel-excel">
            <tr style="text-align:center; background:#eee; font-weight:bold;">
                <td width="8%">No</td><td>Nama / NIP</td><td>Pangkat / Gol</td><td>Jabatan</td>
            </tr>
            {"".join([f"<tr><td align='center'>{i+1}</td><td>{p['nama']}<br>NIP. {p['nip']}</td><td align='center'>{p['gol']}</td><td>{p['jabatan']}</td></tr>" for i, p in enumerate(daftar_pegawai)])}
        </table>
        <p style="margin-top:20px;">Untuk: {maksud} ke {tujuan} pada tanggal {format_indo(tgl_p)} s/d {format_indo(tgl_k)}.</p>
        <div style="margin-left:55%; margin-top:50px; text-align:center;">
            <p>Dikeluarkan di: Bajawa</p>
            <b>{pemberi_perintah.upper()}</b><br><br><br><br>
            <u><b>{nama_ttd}</b></u>
        </div>
    </div>""", unsafe_allow_html=True)

    for p in daftar_pegawai:
        # --- 2. SPD DEPAN ---
        st.markdown(f"""<div class="kertas-a4">
            <h3 align="center">SURAT PERJALANAN DINAS (SPD)</h3>
            <p align="center" style="margin-top:-15px;">Nomor: {no_spd}</p>
            <table class="tabel-excel">
                <tr><td width="5%">1.</td><td width="45%">Pejabat Pemberi Perintah</td><td>{pemberi_perintah}</td></tr>
                <tr><td>2.</td><td>Nama Pegawai diperintah</td><td><b>{p['nama']}</b></td></tr>
                <tr><td>3.</td><td>a. Pangkat / Golongan<br>b. Jabatan<br>c. Tingkat Biaya Perjalanan</td><td>{p['gol']}<br>{p['jabatan']}<br>{tingkat_biaya}</td></tr>
                <tr><td>4.</td><td>Maksud Perjalanan Dinas</td><td>{maksud}</td></tr>
                <tr><td>5.</td><td>Alat Angkut dipergunakan</td><td>{alat_angkut}</td></tr>
                <tr><td>6.</td><td>a. Tempat Berangkat<br>b. Tempat Tujuan</td><td>Bajawa<br>{tujuan}</td></tr>
                <tr><td>7.</td><td>a. Lama Perjalanan<br>b. Tanggal Berangkat<br>c. Tanggal Kembali</td><td>{lama_hari} Hari<br>{format_indo(tgl_p)}<br>{format_indo(tgl_k)}</td></tr>
                <tr><td>8.</td><td>Pengikut : Nama</td><td>NIP</td></tr>
                <tr><td>9.</td><td>Pembebanan Anggaran<br>a. Instansi<br>b. Mata Anggaran</td><td><br>{beban_anggaran}<br>{mata_anggaran}</td></tr>
            </table>
            <div style="margin-left:55%; margin-top:40px; text-align:center;">
                <p>Dikeluarkan di: Bajawa</p>
                <b>{pemberi_perintah.upper()}</b><br><br><br><br>
                <u><b>{nama_ttd}</b></u>
            </div>
        </div>""", unsafe_allow_html=True)

        # --- 3. SPD BELAKANG ---
        st.markdown(f"""<div class="kertas-a4">
            <table class="tabel-excel">
                <tr style="height:6.5cm;"><td class="col-kiri"></td><td class="col-kanan">I. Berangkat: Bajawa<br>Ke: {tujuan}<br>Tgl: {format_indo(tgl_p)}<div align="center"><br><b>{pemberi_perintah.upper()}</b><br><br><br><br><u><b>{nama_ttd}</b></u></div></td></tr>
                <tr style="height:5.5cm;"><td>II. Tiba: {tujuan}<br>Tgl: {format_indo(tgl_p)}</td><td>Berangkat dari: {tujuan}<br>Ke: Bajawa<br>Tgl: {format_indo(tgl_k)}</td></tr>
                <tr style="height:5.5cm;"><td>III. Tiba di:</td><td>Berangkat dari:</td></tr>
                <tr style="height:6.5cm;"><td>V. Tiba Kembali: Bajawa<br>Tgl: {format_indo(tgl_k)}</td><td><div align="center" style="font-style:italic; font-size:9pt;">Telah diperiksa...</div><div align="center" style="margin-top:20px;"><b>{pemberi_perintah.upper()}</b><br><br><br><br><b>....................</b></div></td></tr>
            </table>
        </div>""", unsafe_allow_html=True)
else:
    st.info("👈 Masukkan data pegawai di sidebar untuk memulai pratinjau.")
