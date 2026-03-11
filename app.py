import streamlit as st
from datetime import datetime

# 1. SETTING HALAMAN AGAR BERSIH & LEBAR
st.set_page_config(page_title="Aplikasi Cetak Prokopim Ngada", layout="wide")

st.markdown("""
<style>
    /* Menghilangkan UI Streamlit agar fokus ke kertas */
    header, footer, #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* BACKGROUND SEPERTI APLIKASI DESKTOP */
    .main { background-color: #525659; }

    /* KERTAS A4 (SANGAT PRESISI) */
    .kertas-a4 {
        background-color: white;
        width: 210mm;
        min-height: 297mm;
        padding: 15mm 20mm;
        margin: 20px auto;
        color: black;
        font-family: "Arial", sans-serif;
        font-size: 10.5pt;
        box-shadow: 0 0 15px rgba(0,0,0,0.5);
        box-sizing: border-box;
    }

    /* STYLE TABEL IDENTIK EXCEL */
    .tabel-excel {
        width: 100%;
        border-collapse: collapse;
        table-layout: fixed;
        margin-top: 10px;
    }
    .tabel-excel td {
        border: 1px solid black;
        padding: 6px 10px;
        vertical-align: top;
        word-wrap: break-word;
    }
    .no-border td { border: none !important; }
    
    /* CSS KHUSUS PRINT */
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

# 2. PANEL INPUT (DI SIDEBAR)
with st.sidebar:
    st.header("⚙️ Pengaturan Dokumen")
    no_surat = st.text_input("Nomor SPT/SPD", "094/PROKOPIM/388/02/2026")
    maksud_tugas = st.text_area("Maksud Perjalanan", "Melakukan koordinasi dan konsultasi terkait protokol...")
    tujuan = st.text_input("Tempat Tujuan", "Kupang")
    tgl_berangkat = st.date_input("Tanggal Berangkat", datetime(2026, 2, 9))
    tgl_kembali = st.date_input("Tanggal Kembali", datetime(2026, 2, 11))
    
    st.markdown("---")
    st.subheader("👥 Daftar Pegawai")
    st.caption("Format: Nama | NIP | Jabatan | Golongan")
    input_txt = st.text_area("Input Data", "RAYMUNDUS BENA, S.S., M.Hum | 19XXXXXXXXXXXXXX | Wakil Bupati Ngada | Pembina Utama Muda (IV/c)")
    
    pegawai_list = []
    for line in input_txt.split('\n'):
        if '|' in line:
            parts = line.split('|')
            pegawai_list.append({
                "nama": parts[0].strip(),
                "nip": parts[1].strip(),
                "jabatan": parts[2].strip(),
                "gol": parts[3].strip()
            })

    if st.button("🖨️ CETAK SEMUA"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

# 3. AREA PRATINJAU (SESUAI TEMPLATE EXCEL)
if pegawai_list:
    # --- HALAMAN 1: SPT (SURAT PERINTAH TUGAS) ---
    st.markdown(f"""
    <div class="kertas-a4">
        <h3 align="center" style="text-decoration:underline;">SURAT PERINTAH TUGAS</h3>
        <p align="center">Nomor: {no_surat}</p>
        <br>
        <p><b>MEMERINTAHKAN:</b></p>
        <table class="tabel-excel">
            <tr style="background:#f2f2f2; font-weight:bold; text-align:center;">
                <td width="8%">No</td><td>Nama / NIP</td><td>Pangkat / Gol</td><td>Jabatan</td>
            </tr>
            {"".join([f"<tr><td align='center'>{i+1}</td><td>{p['nama']}<br><small>NIP. {p['nip']}</small></td><td>{p['gol']}</td><td>{p['jabatan']}</td></tr>" for i, p in enumerate(pegawai_list)])}
        </table>
        <br>
        <p><b>UNTUK:</b> {maksud_tugas} ke {tujuan} selama 3 (tiga) hari kerja terhitung mulai tanggal {format_indo(tgl_berangkat)} s/d {format_indo(tgl_kembali)}.</p>
        <div style="margin-left:55%; margin-top:60px; text-align:center;">
            <b>BUPATI NGADA</b><br><br><br><br><br>
            <u><b>ANDREAS PARU</b></u>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- HALAMAN 2 & 3: SPD DEPAN & BELAKANG (PER PEGAWAI) ---
    for p in pegawai_list:
        # SPD DEPAN
        st.markdown(f"""
        <div class="kertas-a4">
            <h3 align="center">SURAT PERJALANAN DINAS (SPD)</h3>
            <table class="tabel-excel">
                <tr><td width="5%">1</td><td width="45%">Pejabat Pemberi Perintah</td><td>Bupati Ngada</td></tr>
                <tr><td>2</td><td>Nama Pegawai diperintah</td><td><b>{p['nama']}</b></td></tr>
                <tr><td>3</td><td>a. Pangkat / Golongan<br>b. Jabatan<br>c. Tingkat Biaya Perjalanan</td><td>{p['gol']}<br>{p['jabatan']}<br>Tingkat A</td></tr>
                <tr><td>4</td><td>Maksud Perjalanan Dinas</td><td>{maksud_tugas}</td></tr>
                <tr><td>5</td><td>Alat Angkut dipergunakan</td><td>Pesawat Udara / Kendaraan Dinas</td></tr>
                <tr><td>6</td><td>a. Tempat Berangkat<br>b. Tempat Tujuan</td><td>Bajawa<br>{tujuan}</td></tr>
                <tr><td>7</td><td>a. Lamanya Perjalanan<br>b. Tanggal Berangkat<br>c. Tanggal Kembali</td><td>3 Hari<br>{format_indo(tgl_berangkat)}<br>{format_indo(tgl_kembali)}</td></tr>
                <tr><td>8</td><td>Pengikut: Nama</td><td>NIP</td></tr>
                <tr><td>9</td><td>Pembebanan Anggaran<br>a. Instansi<br>b. Mata Anggaran</td><td><br>DPA Sekretariat Daerah Kab. Ngada<br>5.1.02.04.01.0001</td></tr>
            </table>
            <div style="margin-left:55%; margin-top:40px; text-align:center;">
                <p>Dikeluarkan di: Bajawa</p>
                <b>BUPATI NGADA</b><br><br><br><br>
                <u><b>ANDREAS PARU</b></u>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # SPD BELAKANG
        st.markdown(f"""
        <div class="kertas-a4">
            <table class="tabel-excel" style="height: 260mm;">
                <tr style="height: 6cm;">
                    <td width="44%"></td>
                    <td width="56%">I. Berangkat: Bajawa<br>Ke: {tujuan}<br>Tgl: {format_indo(tgl_berangkat)}<br><div align="center"><br><b>BUPATI NGADA</b><br><br><br><br><u><b>ANDREAS PARU</b></u></div></td>
                </tr>
                <tr style="height: 5cm;">
                    <td>II. Tiba: {tujuan}<br>Tgl: {format_indo(tgl_berangkat)}</td>
                    <td>Berangkat dari: {tujuan}<br>Ke: Bajawa<br>Tgl: {format_indo(tgl_kembali)}</td>
                </tr>
                <tr style="height: 5cm;"><td>III. Tiba di:</td><td>Berangkat dari:</td></tr>
                <tr style="height: 6cm;">
                    <td>V. Tiba Kembali: Bajawa<br>Tgl: {format_indo(tgl_kembali)}</td>
                    <td style="font-style:italic; font-size:9pt;">Telah diperiksa...<br><div align="center" style="font-style:normal; margin-top:20px;"><b>BUPATI NGADA</b><br><br><br><br><b>....................</b></div></td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
else:
    st.warning("Masukkan data pegawai di sidebar sebelah kiri untuk melihat pratinjau.")
