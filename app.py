import streamlit as st
from datetime import datetime

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Prokopim Ngada", layout="wide")

st.markdown("""
<style>
    /* Sembunyikan elemen Streamlit */
    header, footer, #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    .main { background-color: #525659; }

    /* KERTAS A4 (SANGAT PRESISI) */
    .kertas-a4 {
        background-color: white;
        width: 210mm;
        min-height: 297mm;
        padding: 15mm 20mm;
        margin: 15px auto;
        color: black;
        font-family: "Arial", sans-serif;
        font-size: 10.5pt;
        box-shadow: 0 0 15px rgba(0,0,0,0.4);
        box-sizing: border-box;
    }

    /* TABEL EXCEL STYLE */
    .tabel-excel {
        width: 100%;
        border-collapse: collapse;
        table-layout: fixed;
    }
    .tabel-excel td {
        border: 1px solid black;
        padding: 5px 10px;
        vertical-align: top;
        line-height: 1.3;
    }
    
    .no-border td { border: none !important; padding: 2px !important; }
    .text-center { text-align: center; }
    .text-bold { font-weight: bold; }
    .text-underline { text-decoration: underline; }

    /* KHUSUS SPD BELAKANG (GARIS GESER) */
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

# 2. OPSI INPUTAN SIDEBAR (PERSIS SEPERTI DI PYTHON)
with st.sidebar:
    st.header("⚙️ OPSI INPUT DATA")
    
    with st.expander("📄 DATA SURAT (SPT/SPD)", expanded=True):
        no_spt = st.text_input("Nomor SPT", "094/PROKOPIM/388/02/2026")
        no_spd = st.text_input("Nomor SPD", "094/PROKOPIM/388/02/2026")
        maksud = st.text_area("Maksud Tugas", "Koordinasi dan Konsultasi...")
        tujuan = st.text_input("Tempat Tujuan", "Kupang")
        alat = st.text_input("Alat Angkut", "Pesawat Udara / Kendaraan Dinas")
        tingkat = st.text_input("Tingkat Biaya", "Tingkat A")

    with st.expander("🕒 WAKTU & ANGGARAN", expanded=False):
        tgl_p = st.date_input("Tanggal Berangkat", datetime(2026, 2, 9))
        tgl_k = st.date_input("Tanggal Kembali", datetime(2026, 2, 11))
        lama = st.text_input("Lama Perjalanan", "3 (Tiga)")
        dpa = st.text_input("Instansi", "DPA Sekretariat Daerah Kab. Ngada")
        mata_anggaran = st.text_input("Mata Anggaran", "5.1.02.04.01.0001")

    with st.expander("👥 PEJABAT & PEGAWAI", expanded=True):
        pemberi = st.text_input("Pemberi Perintah", "Bupati Ngada")
        nama_ttd = st.text_input("Nama Penandatangan", "ANDREAS PARU")
        st.info("Nama | NIP | Jabatan | Gol")
        peg_txt = st.text_area("Daftar Pegawai", "RAYMUNDUS BENA, S.S., M.Hum | 19XXXXXXXXXXXXXX | Wakil Bupati Ngada | Pembina Utama Muda (IV/c)")

    daftar = []
    for line in peg_txt.split('\n'):
        if '|' in line:
            p = line.split('|')
            daftar.append({"nama": p[0].strip(), "nip": p[1].strip(), "jab": p[2].strip(), "gol": p[3].strip()})

    st.markdown("---")
    if st.button("🖨️ CETAK SESUAI TEMPLATE PDF"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

# 3. RENDER DOKUMEN (SANGAT PRESISI)
if daftar:
    # --- 1. HALAMAN SPT ---
    st.markdown(f"""<div class="kertas-a4">
        <h3 align="center" class="text-underline">SURAT PERINTAH TUGAS</h3>
        <p align="center" style="margin-top:-10px;">Nomor: {no_spt}</p><br>
        <table class="tabel-excel no-border">
            <tr><td width="15%">Menimbang</td><td width="2%">:</td><td>Bahwa untuk kepentingan dinas...</td></tr>
            <tr><td>Dasar</td><td>:</td><td>Program Kerja Sekretariat Daerah Kabupaten Ngada.</td></tr>
        </table>
        <p align="center" class="text-bold" style="margin:20px 0;">MEMERINTAHKAN:</p>
        <table class="tabel-excel">
            <tr align="center" style="background:#eee; font-weight:bold;">
                <td width="8%">No</td><td>Nama / NIP</td><td>Pangkat / Gol</td><td>Jabatan</td>
            </tr>
            {"".join([f"<tr><td align='center'>{i+1}</td><td>{p['nama']}<br>NIP. {p['nip']}</td><td align='center'>{p['gol']}</td><td>{p['jab']}</td></tr>" for i, p in enumerate(daftar)])}
        </table>
        <p style="margin-top:20px;">Untuk: {maksud} ke {tujuan} pada tanggal {format_indo(tgl_p)} s/d {format_indo(tgl_k)}.</p>
        <div style="margin-left:55%; margin-top:50px; text-align:center;">
            <p>Dikeluarkan di: Bajawa</p>
            <p>Pada Tanggal: {format_indo(datetime.now())}</p>
            <b>{pemberi.upper()}</b><br><br><br><br><b>{nama_ttd}</b>
        </div>
    </div>""", unsafe_allow_html=True)

    for p in daftar:
        # --- 2. SPD DEPAN ---
        st.markdown(f"""<div class="kertas-a4">
            <h3 align="center" style="margin-bottom:20px;">SURAT PERJALANAN DINAS (SPD)</h3>
            <table class="tabel-excel">
                <tr><td width="5%">1.</td><td width="45%">Pejabat Pemberi Perintah</td><td>{pemberi}</td></tr>
                <tr><td>2.</td><td>Nama Pegawai diperintah</td><td><b>{p['nama']}</b></td></tr>
                <tr><td>3.</td><td>a. Pangkat dan Golongan<br>b. Jabatan<br>c. Tingkat Biaya Perjalanan</td><td>{p['gol']}<br>{p['jab']}<br>{tingkat}</td></tr>
                <tr><td>4.</td><td>Maksud Perjalanan Dinas</td><td>{maksud}</td></tr>
                <tr><td>5.</td><td>Alat Angkut dipergunakan</td><td>{alat}</td></tr>
                <tr><td>6.</td><td>a. Tempat Berangkat<br>b. Tempat Tujuan</td><td>Bajawa<br>{tujuan}</td></tr>
                <tr><td>7.</td><td>a. Lama Perjalanan<br>b. Tanggal Berangkat<br>c. Tanggal Kembali</td><td>{lama} Hari<br>{format_indo(tgl_p)}<br>{format_indo(tgl_k)}</td></tr>
                <tr><td>8.</td><td>Pengikut : Nama</td><td>NIP</td></tr>
                <tr><td>9.</td><td>Pembebanan Anggaran<br>a. Instansi<br>b. Mata Anggaran</td><td><br>{dpa}<br>{mata_anggaran}</td></tr>
            </table>
            <div style="margin-left:55%; margin-top:40px; text-align:center;">
                <p>Dikeluarkan di: Bajawa</p>
                <b>{pemberi.upper()}</b><br><br><br><br><b>{nama_ttd}</b>
            </div>
        </div>""", unsafe_allow_html=True)

        # --- 3. SPD BELAKANG ---
        st.markdown(f"""<div class="kertas-a4">
            <table class="tabel-excel">
                <tr style="height:6cm;"><td class="col-kiri"></td><td class="col-kanan">I. Berangkat: Bajawa<br>Ke: {tujuan}<br>Tgl: {format_indo(tgl_p)}<div align="center"><br><b>{pemberi.upper()}</b><br><br><br><br><b>{nama_ttd}</b></div></td></tr>
                <tr style="height:5.5cm;"><td>II. Tiba: {tujuan}<br>Tgl: {format_indo(tgl_p)}</td><td>Berangkat dari: {tujuan}<br>Ke: Bajawa<br>Tgl: {format_indo(tgl_k)}</td></tr>
                <tr style="height:5cm;"><td>III. Tiba di:</td><td>Berangkat dari:</td></tr>
                <tr style="height:6cm;"><td>V. Tiba Kembali: Bajawa<br>Tgl: {format_indo(tgl_k)}</td><td><div align="center" style="font-style:italic; font-size:9pt;">Telah diperiksa...</div><div align="center" style="margin-top:20px;"><b>{pemberi.upper()}</b><br><br><br><br><b>....................</b></div></td></tr>
            </table>
        </div>""", unsafe_allow_html=True)
else:
    st.info("👈 Masukkan data di sebelah kiri untuk melihat pratinjau.")
