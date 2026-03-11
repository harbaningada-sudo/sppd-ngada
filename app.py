import streamlit as st
from datetime import datetime

# 1. KONFIGURASI HALAMAN WIDE
st.set_page_config(page_title="Otomasi SPT Multi-Pegawai", layout="wide")

# 2. CSS PRESISI A4
st.markdown("""
<style>
    @media print {
        header, footer, .stSidebar, .stButton, .no-print { display: none !important; }
        @page { size: A4; margin: 0; }
        .kertas-a4 {
            width: 210mm !important;
            height: 297mm !important;
            margin: 0 !important;
            padding: 10mm 15mm !important;
            border: none !important;
            box-sizing: border-box;
            page-break-after: always;
        }
    }
    .kertas-a4 {
        background-color: white;
        padding: 15mm;
        margin: 10px auto;
        width: 210mm;
        min-height: 297mm;
        color: black;
        font-family: Arial, sans-serif;
        font-size: 10pt;
        border: 1px solid #ddd;
        box-sizing: border-box;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    .tabel-sppd {
        width: 100%;
        height: 250mm;
        border: 1.5px solid black;
        border-collapse: collapse;
    }
    .tabel-sppd td { border: 1.5px solid black; padding: 10px; vertical-align: top; }
    .text-center { text-align: center; }
</style>
""", unsafe_allow_html=True)

def format_indo(tgl):
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    return f"{tgl.day} {bulan[tgl.month-1]} {tgl.year}"

# 3. SIDEBAR INPUT
with st.sidebar:
    st.header("📋 Data Surat")
    no_spt = st.text_input("Nomor SPT", "094/Perekonomian/2026")
    maksud = st.text_area("Maksud Tugas", "Perjalanan Dinas dalam rangka...")
    tujuan = st.text_input("Tujuan", "Kupang")
    tgl_pergi = st.date_input("Tanggal Berangkat", datetime(2026, 2, 9))
    tgl_kembali = st.date_input("Tanggal Kembali", datetime(2026, 2, 11))
    
    st.markdown("---")
    st.header("👥 Data Pegawai")
    # Fitur Multi-Pegawai menggunakan text_area (satu baris satu nama)
    input_pegawai = st.text_area("Masukkan Nama & NIP (Format: Nama | NIP)", 
                                 "RAYMUNDUS BENA, S.S., M.Hum | 19XXXXXXXXXXXXXX\nPEGAWAI KEDUA, S.T | 19YYYYYYYYYYYYYY")
    
    # Memproses input menjadi list
    daftar_pegawai = []
    for line in input_pegawai.split('\n'):
        if '|' in line:
            n, ni = line.split('|')
            daftar_pegawai.append({"nama": n.strip(), "nip": ni.strip()})

    st.markdown("---")
    if st.button("🖨️ Cetak Semua"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

# 4. PREVIEW DI SEBELAH KANAN
# Kita gunakan perulangan agar setiap pegawai punya halaman SPPD sendiri
if daftar_pegawai:
    # --- HALAMAN 1: SPT (Daftar Semua Nama) ---
    st.subheader("Halaman Depan: SPT")
    rows_pegawai = "".join([f"<tr><td>{i+1}.</td><td>{p['nama']}</td><td>{p['nip']}</td></tr>" for i, p in enumerate(daftar_pegawai)])
    
    st.markdown(f"""
    <div class="kertas-a4">
        <h3 class="text-center" style="text-decoration:underline;">SURAT PERINTAH TUGAS</h3>
        <p class="text-center">Nomor: {no_spt}</p>
        <br>
        <p><b>MEMERINTAHKAN:</b></p>
        <table style="width:100%; border-collapse: collapse;" border="1">
            <tr style="background-color: #f2f2f2;"><th>No</th><th>Nama</th><th>NIP</th></tr>
            {rows_pegawai}
        </table>
        <br>
        <p>Untuk: {maksud} ke {tujuan} pada tanggal {format_indo(tgl_pergi)} s/d {format_indo(tgl_kembali)}.</p>
        <div style="margin-left:50%; text-align:center; margin-top:50px;">
            <p>Dikeluarkan di: Bajawa</p>
            <br><b>BUPATI NGADA</b><br><br><br><br>
            <u><b>RAYMUNDUS BENA, S.S., M.Hum</b></u>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- HALAMAN BERIKUTNYA: SPPD BELAKANG UNTUK TIAP PEGAWAI ---
    for p in daftar_pegawai:
        st.subheader(f"Halaman Belakang: SPPD - {p['nama']}")
        st.markdown(f"""
        <div class="kertas-a4">
            <table class="tabel-sppd">
                <tr style="height: 20%;">
                    <td style="width: 42%;"></td>
                    <td style="width: 58%;">
                        I. &nbsp; Berangkat dari : Bajawa <br>
                        &nbsp;&nbsp;&nbsp;&nbsp; Ke : {tujuan} <br>
                        &nbsp;&nbsp;&nbsp;&nbsp; Pada Tanggal : {format_indo(tgl_pergi)} <br>
                        <div class="text-center" style="margin-top:15px;">
                            <b>BUPATI NGADA</b><br><br><br><br>
                            <u><b>{p['nama']}</b></u>
                        </div>
                    </td>
                </tr>
                <tr style="height: 18%;">
                    <td>II. Tiba di : {tujuan} <br> &nbsp;&nbsp;&nbsp;&nbsp; Pada Tanggal : {format_indo(tgl_pergi)}</td>
                    <td>Berangkat dari : {tujuan} <br> Ke : Bajawa <br> Pada Tanggal : {format_indo(tgl_kembali)}</td>
                </tr>
                <tr style="height: 18%;"><td>III. Tiba di :</td><td>Berangkat dari :</td></tr>
                <tr style="height: 18%;"><td>IV. Tiba di :</td><td>Berangkat dari :</td></tr>
                <tr style="height: 22%;">
                    <td>V. Tiba Kembali di : Bajawa <br> &nbsp;&nbsp;&nbsp;&nbsp; Pada Tanggal : {format_indo(tgl_kembali)}</td>
                    <td>
                        <div style="font-style:italic; font-size:8pt;">Telah diperiksa...</div>
                        <div class="text-center" style="margin-top:15px;"><b>BUPATI NGADA</b><br><br><br><b>...................</b></div>
                    </td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
else:
    st.error("Silakan masukkan data pegawai di sidebar (Nama | NIP)")
