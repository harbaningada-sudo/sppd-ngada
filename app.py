import streamlit as st
from datetime import datetime

# 1. SETTING HALAMAN
st.set_page_config(page_title="Sistem Cetak Prokopim Ngada", layout="wide")

st.markdown("""
<style>
    header, footer, #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    .main { background-color: #525659; }

    /* KERTAS A4 IDENTIK EXCEL */
    .kertas-a4 {
        background-color: white;
        width: 210mm;
        min-height: 297mm;
        padding: 10mm 15mm;
        margin: 20px auto;
        color: black;
        font-family: "Arial", sans-serif;
        font-size: 10pt;
        box-shadow: 0 0 15px rgba(0,0,0,0.5);
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
        padding: 4px 8px;
        vertical-align: top;
        height: 35px; /* Menyesuaikan tinggi baris excel */
    }
    
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

# 2. INPUT DATA SIDEBAR
with st.sidebar:
    st.header("⚙️ Data Input")
    no_surat = st.text_input("Nomor Surat", "094/PROKOPIM/388/02/2026")
    maksud = st.text_area("Maksud Tugas", "Melakukan koordinasi dan konsultasi...")
    tujuan = st.text_input("Tujuan", "Kupang")
    tgl_p = st.date_input("Berangkat", datetime(2026, 2, 9))
    tgl_k = st.date_input("Kembali", datetime(2026, 2, 11))
    
    st.markdown("---")
    st.subheader("👥 Pegawai")
    input_txt = st.text_area("Nama | NIP | Jabatan | Gol", "RAYMUNDUS BENA, S.S., M.Hum | 19XXXXXXXXXXXXXX | Wakil Bupati Ngada | Pembina Utama Muda (IV/c)")
    
    daftar = []
    for line in input_txt.split('\n'):
        if '|' in line:
            parts = line.split('|')
            daftar.append({"nama": parts[0].strip(), "nip": parts[1].strip(), "jabatan": parts[2].strip(), "gol": parts[3].strip()})

    if st.button("🖨️ CETAK SEMUA"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

# 3. AREA PREVIEW
if daftar:
    # --- HALAMAN SPT ---
    st.markdown(f"""
    <div class="kertas-a4">
        <h3 align="center" style="text-decoration:underline;">SURAT PERINTAH TUGAS</h3>
        <p align="center">Nomor: {no_surat}</p>
        <br>
        <p><b>MEMERINTAHKAN:</b></p>
        <table class="tabel-excel">
            <tr style="text-align:center; font-weight:bold; background:#eee;">
                <td width="8%">No</td><td>Nama / NIP</td><td>Pangkat / Gol</td><td>Jabatan</td>
            </tr>
            {"".join([f"<tr><td align='center'>{i+1}</td><td>{p['nama']}<br>NIP. {p['nip']}</td><td align='center'>{p['gol']}</td><td>{p['jabatan']}</td></tr>" for i, p in enumerate(daftar)])}
        </table>
        <p style="margin-top:15px;">Untuk: {maksud} ke {tujuan} pada tanggal {format_indo(tgl_p)} s/d {format_indo(tgl_k)}.</p>
        <div style="margin-left:55%; margin-top:50px; text-align:center;">
            <b>BUPATI NGADA</b><br><br><br><br><b>ANDREAS PARU</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    for p in daftar:
        # --- SPD DEPAN (SESUAI POIN 1-9 EXCEL) ---
        st.markdown(f"""
        <div class="kertas-a4">
            <h3 align="center">SURAT PERJALANAN DINAS (SPD)</h3>
            <table class="tabel-excel">
                <tr><td width="5%">1.</td><td width="45%">Pejabat Pemberi Perintah</td><td>Bupati Ngada</td></tr>
                <tr><td>2.</td><td>Nama Pegawai diperintah</td><td><b>{p['nama']}</b></td></tr>
                <tr><td>3.</td><td>a. Pangkat dan Golongan<br>b. Jabatan<br>c. Tingkat Biaya Perjalanan</td><td>{p['gol']}<br>{p['jabatan']}<br>Tingkat A</td></tr>
                <tr><td>4.</td><td>Maksud Perjalanan Dinas</td><td>{maksud}</td></tr>
                <tr><td>5.</td><td>Alat Angkut dipergunakan</td><td>Pesawat Udara / Kendaraan Dinas</td></tr>
                <tr><td>6.</td><td>a. Tempat Berangkat<br>b. Tempat Tujuan</td><td>Bajawa<br>{tujuan}</td></tr>
                <tr><td>7.</td><td>a. Lamanya Perjalanan<br>b. Tanggal Berangkat<br>c. Tanggal Kembali</td><td>3 Hari<br>{format_indo(tgl_p)}<br>{format_indo(tgl_k)}</td></tr>
                <tr><td>8.</td><td>Pengikut : Nama</td><td>NIP</td></tr>
                <tr><td>9.</td><td>Pembebanan Anggaran<br>a. Instansi<br>b. Mata Anggaran</td><td><br>DPA Sekretariat Daerah Kab. Ngada<br>5.1.02.04.01.0001</td></tr>
            </table>
            <div style="margin-left:55%; margin-top:30px; text-align:center;">
                <b>BUPATI NGADA</b><br><br><br><br><b>ANDREAS PARU</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # --- SPD BELAKANG (SESUAI TEMPLATE BELAKANG) ---
        st.markdown(f"""
        <div class="kertas-a4">
            <table class="tabel-excel">
                <tr style="height:6cm;">
                    <td class="col-kiri"></td>
                    <td class="col-kanan">I. Berangkat: Bajawa<br>Ke: {tujuan}<br>Tgl: {format_indo(tgl_p)}<br><div align="center"><br><b>BUPATI NGADA</b><br><br><br><br><b>ANDREAS PARU</b></div></td>
                </tr>
                <tr style="height:5cm;">
                    <td>II. Tiba: {tujuan}<br>Tgl: {format_indo(tgl_p)}</td>
                    <td>Berangkat dari: {tujuan}<br>Ke: Bajawa<br>Tgl: {format_indo(tgl_k)}</td>
                </tr>
                <tr style="height:5cm;"><td>III. Tiba di:</td><td>Berangkat dari:</td></tr>
                <tr style="height:6cm;">
                    <td>V. Tiba Kembali: Bajawa<br>Tgl: {format_indo(tgl_k)}</td>
                    <td><div style="font-style:italic; font-size:9pt;">Telah diperiksa...</div><div align="center"><br><b>BUPATI NGADA</b><br><br><br><br><b>....................</b></div></td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
