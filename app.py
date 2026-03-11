import streamlit as st
from datetime import datetime

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Cetak Dokumen Sesuai Template Excel", layout="wide")

st.markdown("""
<style>
    /* Reset Tampilan */
    header, footer, #MainMenu {visibility: hidden;}
    
    /* CSS KERTAS A4 PRESISI */
    .kertas-a4 {
        background-color: white;
        width: 210mm;
        min-height: 297mm;
        padding: 12mm 15mm;
        margin: 10px auto;
        color: black;
        font-family: "Arial", sans-serif;
        font-size: 10pt;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
        box-sizing: border-box;
    }

    /* STYLE TABEL IDENTIK EXCEL */
    .tabel-template {
        width: 100%;
        border-collapse: collapse;
        table-layout: fixed;
    }
    .tabel-template td {
        border: 1px solid black;
        padding: 5px 8px;
        vertical-align: top;
        line-height: 1.3;
    }
    .no-border td { border: none !important; }
    
    /* KHUSUS SPD BELAKANG (GARIS GESER KE KANAN) */
    .col-belakang-kiri { width: 44%; }
    .col-belakang-kanan { width: 56%; }

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

# 2. PANEL INPUT SIDEBAR
with st.sidebar:
    st.header("📋 Data Template")
    no_spt = st.text_input("Nomor Surat", "094/PROKOPIM/388/02/2026")
    maksud = st.text_area("Maksud Perjalanan", "Koordinasi dan Konsultasi...")
    tujuan = st.text_input("Tempat Tujuan", "Kupang")
    tgl_p = st.date_input("Tanggal Berangkat", datetime(2026, 2, 9))
    tgl_k = st.date_input("Tanggal Kembali", datetime(2026, 2, 11))
    
    st.markdown("---")
    st.write("👥 **Data Pegawai**")
    input_pegawai = st.text_area("Format: Nama | NIP | Jabatan | Gol", 
                                 "RAYMUNDUS BENA, S.S., M.Hum | 19XXXXXXXXXXXXXX | Wakil Bupati Ngada | Pembina Utama Muda (IV/c)")
    
    daftar = []
    for line in input_pegawai.split('\n'):
        if '|' in line:
            p = line.split('|')
            daftar.append({"nama": p[0].strip(), "nip": p[1].strip(), "jabatan": p[2].strip(), "gol": p[3].strip()})

    if st.button("🖨️ CETAK SESUAI TEMPLATE"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

# 3. RENDER BERDASARKAN TEMPLATE EXCEL
if daftar:
    # --- TEMPLATE 1: SPT (Sesuai CSV SPT) ---
    st.subheader("Template SPT")
    rows_spt = "".join([f"<tr><td align='center'>{i+1}</td><td>{p['nama']}</td><td>{p['nip']}</td><td>{p['gol']}</td><td>{p['jabatan']}</td></tr>" for i, p in enumerate(daftar)])
    st.markdown(f"""
    <div class="kertas-a4">
        <h3 align="center" style="text-decoration:underline;">SURAT PERINTAH TUGAS</h3>
        <p align="center">Nomor: {no_spt}</p>
        <br>
        <p><b>MEMERINTAHKAN:</b></p>
        <table class="tabel-template">
            <tr style="background:#eee;"><td width="8%">No</td><td>Nama</td><td>NIP</td><td>Pangkat/Gol</td><td>Jabatan</td></tr>
            {rows_spt}
        </table>
        <p style="margin-top:15px;">Untuk: {maksud} ke {tujuan} pada {format_indo(tgl_p)} s/d {format_indo(tgl_k)}.</p>
        <div style="margin-left:55%; margin-top:40px; text-align:center;">
            <b>BUPATI NGADA</b><br><br><br><br>
            <u><b>ANDREAS PARU</b></u>
        </div>
    </div>
    """, unsafe_allow_html=True)

    for p in daftar:
        # --- TEMPLATE 2: SPD DEPAN (Sesuai CSV SPD Depan 1) ---
        st.subheader(f"Template SPD Depan - {p['nama']}")
        st.markdown(f"""
        <div class="kertas-a4">
            <h3 align="center">SURAT PERJALANAN DINAS (SPD)</h3>
            <table class="tabel-template">
                <tr><td width="5%">1</td><td width="45%">Pejabat Pemberi Perintah</td><td>Bupati Ngada</td></tr>
                <tr><td>2</td><td>Nama Pegawai diperintah</td><td><b>{p['nama']}</b></td></tr>
                <tr><td>3</td><td>a. Pangkat / Golongan<br>b. Jabatan<br>c. Tingkat Biaya</td><td>{p['gol']}<br>{p['jabatan']}<br>Tingkat A</td></tr>
                <tr><td>4</td><td>Maksud Perjalanan Dinas</td><td>{maksud}</td></tr>
                <tr><td>5</td><td>Alat Angkut dipergunakan</td><td>Pesawat Udara / Kendaraan Dinas</td></tr>
                <tr><td>6</td><td>a. Tempat Berangkat<br>b. Tempat Tujuan</td><td>Bajawa<br>{tujuan}</td></tr>
                <tr><td>7</td><td>a. Lama Perjalanan<br>b. Tgl Berangkat<br>c. Tgl Kembali</td><td>3 Hari<br>{format_indo(tgl_p)}<br>{format_indo(tgl_k)}</td></tr>
                <tr><td>8</td><td>Pengikut: Nama</td><td>NIP</td></tr>
                <tr><td>9</td><td>Beban Anggaran</td><td>DPA Sekretariat Daerah Kab. Ngada</td></tr>
            </table>
            <div style="margin-left:55%; margin-top:30px; text-align:center;">
                <b>BUPATI NGADA</b><br><br><br><br>
                <u><b>ANDREAS PARU</b></u>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # --- TEMPLATE 3: SPD BELAKANG (Sesuai CSV SPD BELAKANG) ---
        st.subheader(f"Template SPD Belakang - {p['nama']}")
        st.markdown(f"""
        <div class="kertas-a4">
            <table class="tabel-template">
                <tr style="height:5.5cm;">
                    <td class="col-belakang-kiri"></td>
                    <td class="col-belakang-kanan">
                        I. Berangkat dari : Bajawa <br> Ke : {tujuan} <br> Tanggal : {format_indo(tgl_p)}
                        <div align="center"><br><b>BUPATI NGADA</b><br><br><br><br><u><b>ANDREAS PARU</b></u></div>
                    </td>
                </tr>
                <tr style="height:4.5cm;">
                    <td>II. Tiba : {tujuan}<br>Tgl: {format_indo(tgl_p)}</td>
                    <td>Berangkat dari : {tujuan}<br>Ke: Bajawa<br>Tgl: {format_indo(tgl_k)}</td>
                </tr>
                <tr style="height:4.5cm;"><td>III. Tiba di :</td><td>Berangkat dari :</td></tr>
                <tr style="height:5.5cm;">
                    <td>V. Tiba Kembali : Bajawa<br>Tgl: {format_indo(tgl_k)}</td>
                    <td>
                        <div style="font-style:italic; font-size:9pt;">Telah diperiksa...</div>
                        <div align="center"><br><b>BUPATI NGADA</b><br><br><br><br><b>....................</b></div>
                    </td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
