import streamlit as st
from datetime import datetime

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem Cetak Dokumen Prokopim Ngada", layout="wide")

st.markdown("""
<style>
    /* Sembunyikan elemen UI Streamlit */
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

    /* TABEL UNTUK SPD DEPAN */
    .tabel-spd { width: 100%; border-collapse: collapse; margin-top: 10px; table-layout: fixed; }
    .tabel-spd td { border: 1px solid black; padding: 6px; vertical-align: top; }
    .no-border td { border: none !important; padding: 2px; }

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
    st.header("📋 Data Utama Surat")
    no_spt = st.text_input("Nomor SPT", "094/PROKOPIM/388/02/2026")
    maksud = st.text_area("Maksud Perjalanan Dinas", "Melakukan koordinasi dan konsultasi...")
    tujuan = st.text_input("Tempat Tujuan", "Kupang")
    alat_angkut = st.text_input("Alat Angkut", "Pesawat Udara / Kendaraan Dinas")
    tgl_p = st.date_input("Tanggal Berangkat", datetime(2026, 2, 9))
    tgl_k = st.date_input("Tanggal Kembali", datetime(2026, 2, 11))
    beban_anggaran = st.text_input("Beban Anggaran", "DPA Sekretariat Daerah Kab. Ngada")
    mata_anggaran = st.text_input("Mata Anggaran", "5.1.02.04.01.0001")
    
    st.markdown("---")
    st.header("👥 Data Pegawai")
    st.info("Format: Nama | NIP | Jabatan | Pangkat/Gol")
    input_pegawai = st.text_area("Input Pegawai", 
                                 "RAYMUNDUS BENA, S.S., M.Hum | 19XXXXXXXXXXXXXX | Wakil Bupati Ngada | Pembina Utama Muda (IV/c)")
    
    daftar = []
    for line in input_pegawai.split('\n'):
        if '|' in line:
            p = line.split('|')
            daftar.append({"nama": p[0].strip(), "nip": p[1].strip(), "jabatan": p[2].strip(), "gol": p[3].strip()})

    if st.button("🖨️ CETAK SEMUA DOKUMEN"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

# 3. RENDER DOKUMEN
if daftar:
    # --- HALAMAN 1: SPT ---
    st.subheader("1. Halaman SPT")
    rows_spt = "".join([f"<tr><td align='center'>{i+1}</td><td>{p['nama']}</td><td>{p['nip']}</td><td>{p['gol']}</td><td>{p['jabatan']}</td></tr>" for i, p in enumerate(daftar)])
    st.markdown(f"""
    <div class="kertas-a4">
        <h3 align="center" style="text-decoration:underline; margin-bottom:0;">SURAT PERINTAH TUGAS</h3>
        <p align="center">Nomor: {no_spt}</p>
        <br>
        <p><b>MEMERINTAHKAN:</b></p>
        <table class="tabel-spd" border="1" style="border-collapse:collapse; width:100%;">
            <tr style="background:#eee;"><th>No</th><th>Nama</th><th>NIP</th><th>Pangkat/Gol</th><th>Jabatan</th></tr>
            {rows_spt}
        </table>
        <br>
        <p><b>UNTUK:</b> {maksud} ke {tujuan} pada {format_indo(tgl_p)} s/d {format_indo(tgl_k)}.</p>
        <div style="margin-left:55%; margin-top:50px; text-align:center;">
            <p>Bajawa, {format_indo(datetime.now())}</p>
            <b>BUPATI NGADA</b><br><br><br><br>
            <u><b>ANDREAS PARU</b></u>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- HALAMAN 2: SPD DEPAN ---
    for p in daftar:
        st.subheader(f"2. SPD Depan - {p['nama']}")
        st.markdown(f"""
        <div class="kertas-a4">
            <h3 align="center" style="margin-bottom:20px;">SURAT PERJALANAN DINAS (SPD)</h3>
            <table class="tabel-spd">
                <tr><td width="5%">1.</td><td width="45%">Pejabat Pemberi Perintah</td><td>Bupati Ngada</td></tr>
                <tr><td>2.</td><td>Nama Pegawai yang diperintah</td><td><b>{p['nama']}</b></td></tr>
                <tr><td>3.</td><td>a. Pangkat dan Golongan<br>b. Jabatan<br>c. Tingkat Biaya Perjalanan</td><td>{p['gol']}<br>{p['jabatan']}<br>Tingkat A</td></tr>
                <tr><td>4.</td><td>Maksud Perjalanan Dinas</td><td>{maksud}</td></tr>
                <tr><td>5.</td><td>Alat Angkut yang dipergunakan</td><td>{alat_angkut}</td></tr>
                <tr><td>6.</td><td>a. Tempat Berangkat<br>b. Tempat Tujuan</td><td>Bajawa<br>{tujuan}</td></tr>
                <tr><td>7.</td><td>a. Lamanya Perjalanan Dinas<br>b. Tanggal Berangkat<br>c. Tanggal Kembali</td><td>3 Hari<br>{format_indo(tgl_p)}<br>{format_indo(tgl_k)}</td></tr>
                <tr><td>8.</td><td>Pengikut: Nama</td><td>NIP</td></tr>
                <tr><td>9.</td><td>Pembebanan Anggaran<br>a. Instansi<br>b. Mata Anggaran</td><td><br>{beban_anggaran}<br>{mata_anggaran}</td></tr>
            </table>
            <div style="margin-left:55%; margin-top:30px; text-align:center;">
                <p>Dikeluarkan di: Bajawa</p>
                <b>BUPATI NGADA</b><br><br><br><br>
                <u><b>ANDREAS PARU</b></u>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # --- HALAMAN 3: SPD BELAKANG ---
        st.subheader(f"3. SPD Belakang - {p['nama']}")
        st.markdown(f"""
        <div class="kertas-a4">
            <table class="tabel-belakang">
                <tr style="height:5.5cm;">
                    <td class="col-kiri"></td>
                    <td class="col-kanan">
                        I. Berangkat dari : Bajawa <br> Ke : {tujuan} <br> Tanggal : {format_indo(tgl_p)}
                        <div align="center"><br><b>BUPATI NGADA</b><br><br><br><br><u><b>ANDREAS PARU</b></u></div>
                    </td>
                </tr>
                <tr style="height:4.5cm;">
                    <td>II. Tiba di : {tujuan}<br>Tanggal : {format_indo(tgl_p)}</td>
                    <td>Berangkat dari : {tujuan}<br>Ke : Bajawa<br>Tanggal : {format_indo(tgl_k)}</td>
                </tr>
                <tr style="height:4.5cm;"><td>III. Tiba di :</td><td>Berangkat dari :</td></tr>
                <tr style="height:4.5cm;"><td>IV. Tiba di :</td><td>Berangkat dari :</td></tr>
                <tr style="height:5.5cm;">
                    <td>V. Tiba Kembali : Bajawa<br>Tanggal : {format_indo(tgl_k)}</td>
                    <td style="font-style:italic; font-size:9pt;">
                        Telah diperiksa, dengan keterangan bahwa perjalanan tersebut atas perintahnya dan semata-mata untuk kepentingan jabatan.
                        <div align="center" style="font-style:normal; font-size:10pt;"><br><b>BUPATI NGADA</b><br><br><br><br><b>...................................</b></div>
                    </td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
