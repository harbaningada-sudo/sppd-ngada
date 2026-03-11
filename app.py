import streamlit as st
from datetime import datetime

# 1. KONFIGURASI HALAMAN WIDE (Agar Layar Penuh)
st.set_page_config(page_title="Otomasi SPT & SPPD Ngada", layout="wide")

# 2. CSS UNTUK PRESISI A4 & LAYOUT BERDAMPINGAN
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
        table-layout: fixed;
    }
    .tabel-sppd td { border: 1.5px solid black; padding: 10px; vertical-align: top; }
    .text-center { text-align: center; }
</style>
""", unsafe_allow_html=True)

# 3. FUNGSI TANGGAL INDO
def format_indo(tgl):
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    return f"{tgl.day} {bulan[tgl.month-1]} {tgl.year}"

# 4. PEMBAGIAN KOLOM (Kiri Input, Kanan Preview)
col_input, col_preview = st.columns([1, 2])

with col_input:
    st.header("📋 Input Data")
    no_spt = st.text_input("Nomor SPT", "094/Perekonomian/2026")
    nama = st.text_input("Nama Pegawai", "RAYMUNDUS BENA, S.S., M.Hum")
    nip = st.text_input("NIP Pegawai", "19XXXXXXXXXXXXXX")
    jabatan = st.text_input("Jabatan", "Kepala Bagian Perekonomian & SDA")
    maksud = st.text_area("Maksud Tugas", "Perjalanan Dinas dalam rangka...")
    tujuan = st.text_input("Tujuan", "Kupang")
    tgl_pergi = st.date_input("Tanggal Berangkat", datetime(2026, 2, 9))
    tgl_kembali = st.date_input("Tanggal Kembali", datetime(2026, 2, 11))
    
    st.markdown("---")
    if st.button("🖨️ Cetak Semua Dokumen"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

with col_preview:
    st.header("🔍 Pratinjau Dokumen")
    
    # --- HALAMAN DEPAN (SPT) ---
    st.markdown(f"""
    <div class="kertas-a4">
        <h3 class="text-center" style="text-decoration:underline;">SURAT PERINTAH TUGAS</h3>
        <p class="text-center">Nomor: {no_spt}</p>
        <br><br>
        <p><b>MEMERINTAHKAN:</b></p>
        <table style="width:100%; border:none;">
            <tr><td style="width:25%">Nama</td><td>: <b>{nama}</b></td></tr>
            <tr><td>NIP</td><td>: {nip}</td></tr>
            <tr><td>Jabatan</td><td>: {jabatan}</td></tr>
        </table>
        <br>
        <p>Untuk: {maksud} ke {tujuan} pada tanggal {format_indo(tgl_pergi)} s/d {format_indo(tgl_kembali)}.</p>
        <br><br><br>
        <div style="margin-left:50%; text-align:center;">
            <p>Dikeluarkan di: Bajawa</p>
            <p>Pada Tanggal: {format_indo(datetime.now())}</p>
            <br><b>BUPATI NGADA</b><br><br><br><br>
            <u><b>{nama}</b></u>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- HALAMAN BELAKANG (SPPD) ---
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
                        <u><b>{nama}</b></u>
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
                    <div style="font-style:italic; font-size:8.5pt;">Telah diperiksa, dengan keterangan bahwa perjalanan tersebut atas perintahnya dan semata-mata untuk kepentingan jabatan.</div>
                    <div class="text-center" style="margin-top:15px;"><b>BUPATI NGADA</b><br><br><br><b>..........................................</b></div>
                </td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
