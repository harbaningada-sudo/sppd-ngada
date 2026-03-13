import streamlit as st
from datetime import datetime
import base64
from pathlib import Path

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Prokopim Ngada", layout="wide")

st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton {display:none; }
    .main { background-color: #525659; }
</style>
""", unsafe_allow_html=True)

# FUNGSI UNTUK MENGUBAH GAMBAR LOKAL MENJADI BASE64
def get_image_as_base64(path):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        return None

# TENTUKAN PATH KE LOGO ANDA
# Pastikan file logo_ngada.jpg ada di folder yang sama dengan app.py
logo_path = Path("logo_ngada.jpg")

# CEK APAKAH LOGO ADA, JIKA ADA UBAH KE BASE64
logo_base64 = get_image_as_base64(logo_path)

if logo_base64:
    # Membuat tag IMG HTML dengan data Base64
    logo_html = f'<img src="data:image/jpeg;base64,{logo_base64}" class="logo-img">'
else:
    # Jika logo tidak ditemukan, berikan pesan kesalahan di Streamlit
    st.error(f"File gambar '{logo_path.name}' tidak ditemukan di folder yang sama dengan app.py.")
    logo_html = "" # Teks kosong jika logo tidak ada

# 2. PANEL INPUT SIDEBAR
with st.sidebar:
    st.header("📋 INPUT DATA")
    
    with st.expander("📄 DATA SURAT", expanded=True):
        no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
        no_spd = st.text_input("Nomor SPD", "530 /02/2026")
        kode_no = st.text_input("Kode No", "094/Prokopim")
        maksud = st.text_area("Maksud Perjalanan", "Monitoring dan Pendataan Pemilik Tambang Pasir...")
        tujuan = st.text_input("Tempat Tujuan", "Kecamatan Golewa")

    with st.expander("👤 PEGAWAI", expanded=True):
        nama = st.text_input("Nama Pegawai", "Silfinus Febri Yanto Rugat, S.E.")
        nip = st.text_input("NIP", "19XXXXXXXXXXXXXX")
        gol = st.text_input("Pangkat/Gol", "Penata Muda - III/a")
        jabatan = st.text_area("Jabatan", "Perencana Ahli Pertama Pada Bagian")

    with st.expander("🕒 WAKTU", expanded=False):
        tgl_p = st.date_input("Tanggal Berangkat", datetime(2026, 2, 25))
        tgl_k = st.date_input("Tanggal Kembali", datetime(2026, 2, 26))
        lama = st.text_input("Lama Hari", "2 (Dua)")

    with st.expander("🖋️ PENANDATANGAN", expanded=False):
        tgl_cetak = st.date_input("Tanggal Cetak", datetime(2026, 2, 25))
        ttd_nama = st.text_input("Nama Pejabat", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
        ttd_nip = st.text_input("NIP Pejabat", "19710328 199203 1 011")
        ttd_gol = st.text_input("Gol Pejabat", "Pembina Utama Muda - IV/c")

    if st.button("🖨️ CETAK SEMUA HALAMAN"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

# FORMAT TANGGAL
bulan_list = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
def tgl_str(d): return f"{d.day} {bulan_list[d.month-1]} {d.year}"

# 3. TEMPLATE HTML
surat_html = f"""
<style>
    .wrap {{ background-color: #525659; padding: 20px; display: flex; flex-direction: column; align-items: center; gap: 25px; }}
    .kertas {{ background-color: white; width: 210mm; min-height: 297mm; padding: 15mm 20mm 20mm 25mm; color: black; font-family: Arial, sans-serif; font-size: 10pt; box-shadow: 0 0 15px rgba(0,0,0,0.5); box-sizing: border-box; page-break-after: always; }}
    
    /* GAYA UNTUK KOP SURAT DENGAN LOGO (UNTUK SPT & SPPD DEPAN) */
    .kop-container {{
        display: flex;
        align-items: center; /* Sejajarkan logo dan teks secara vertikal di tengah */
        border-bottom: 3px solid black;
        padding-bottom: 5px;
        margin-bottom: 15px;
    }}
    .logo-img {{
        width: 80px; /* Atur lebar logo sesuai kebutuhan */
        height: auto; /* Jaga proporsi tinggi logo */
        margin-right: 20px; /* Beri jarak antara logo dan teks kop */
    }}
    .kop-text {{
        flex: 1; /* Biarkan teks mengambil sisa ruang yang tersedia */
        text-align: center;
        line-height: 1.2;
    }}
    
    /* GAYA UNTUK KOP SURAT TANPA LOGO (UNTUK SPPD BELAKANG) */
    .kop-tanpa-logo {{
        text-align: center;
        border-bottom: 3px solid black;
        padding-bottom: 5px;
        margin-bottom: 15px;
        line-height: 1.2;
    }}
    
    .tabel-polos {{ width: 100%; border-collapse: collapse; }}
    .tabel-polos td {{ border: none; padding: 2px; vertical-align: top; }}
    .tabel-border {{ width: 100%; border-collapse: collapse; border: 1.2px solid black; }}
    .tabel-border td {{ border: 1.2px solid black; padding: 12px 10px; vertical-align: top; }}
    .text-center {{ text-align: center; }}
    .text-bold {{ font-weight: bold; }}
    .text-underline {{ text-decoration: underline; }}
</style>

<div class="wrap">
    <div class="kertas">
        <div class="kop-container">
            {logo_html} <div class="kop-text">
                <h3 style="margin:0; font-size: 14pt;">PEMERINTAH KABUPATEN NGADA</h3>
                <h2 style="margin:0; font-size: 14pt;">SEKRETARIAT DAERAH</h2>
                <p style="margin:0; font-size: 10pt;">Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834</p>
                <h3 style="margin:0; font-size: 14pt;">BAJAWA</h3>
            </div>
        </div>
        <h3 class="text-center text-bold text-underline">SURAT PERINTAH TUGAS</h3>
        <p class="text-center" style="margin-top:-10px;">NOMOR : {no_spt}</p>
        <table class="tabel-polos">
            <tr><td width="15%">Dasar</td><td width="2%">:</td><td>DPA Bagian Perekonomian dan SDA Setda Ngada Tahun Anggaran 2026</td></tr>
        </table>
        <p class="text-center text-bold" style="letter-spacing: 2px; margin: 20px 0;">M E M E R I N T A H K A N</p>
        <table class="tabel-polos">
            <tr><td width="15%">Kepada</td><td width="5%">: 1.</td><td width="15%">Nama</td><td width="2%">:</td><td class="text-bold">{nama}</td></tr>
            <tr><td></td><td></td><td>Pangkat/Gol</td><td>:</td><td>{gol}</td></tr>
            <tr><td></td><td></td><td>NIP</td><td>:</td><td>{nip}</td></tr>
            <tr><td></td><td></td><td>Jabatan</td><td>:</td><td>{jabatan}</td></tr>
        </table>
        <br>
        <table class="tabel-polos">
            <tr><td width="15%">Untuk</td><td width="2%">:</td><td style="text-align:justify;">{maksud}</td></tr>
        </table>
        <div style="margin-left:55%; margin-top:40px;">
            <p style="margin:0;">Ditetapkan di : Bajawa</p>
            <p style="margin:0;">Pada Tanggal : {tgl_str(tgl_cetak)}</p>
            <br><p class="text-bold" style="margin:0;">An. BUPATI NGADA</p>
            <p style="margin:0;">Pj. Sekretaris Daerah,</p>
            <br><br><br><br>
            <p class="text-bold text-underline" style="margin:0;">{ttd_nama}</p>
            <p style="margin:0;">{ttd_gol}</p>
            <p style="margin:0;">NIP. {ttd_nip}</p>
        </div>
    </div>

    <div class="kertas">
        <div class="kop-container">
            {logo_html} <div class="kop-text">
                <h3 style="margin:0; font-size: 14pt;">PEMERINTAH KABUPATEN NGADA</h3>
                <h2 style="margin:0; font-size: 14pt;">SEKRETARIAT DAERAH</h2>
                <p style="margin:0; font-size: 10pt;">Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834</p>
                <h3 style="margin:0; font-size: 14pt;">BAJAWA</h3>
            </div>
        </div>
        <div style="margin-left: 60%;">
            <table class="tabel-polos" style="font-size: 9pt;">
                <tr><td>Lembar ke</td><td>:</td><td></td></tr>
                <tr><td>Kode No</td><td>:</td><td>{kode_no}</td></tr>
                <tr><td>Nomor</td><td>:</td><td>{no_spd}</td></tr>
            </table>
        </div>
        <h3 class="text-center text-bold text-underline" style="margin-top:10px; margin-bottom:0;">SURAT PERINTAH DINAS</h3>
        <p class="text-center" style="margin-top:0;">(SPD)</p>
        <table class="tabel-border">
            <tr><td width="5%">1.</td><td width="40%">Pejabat yang memberi perintah</td><td>BUPATI NGADA</td></tr>
            <tr><td>2.</td><td>Nama Pegawai yang diperintahkan</td><td class="text-bold">{nama}</td></tr>
            <tr><td>3.</td><td>a. Pangkat/Golongan<br>b. Jabatan<br>c. Tingkat Menurut Peraturan</td><td>{gol}<br>{jabatan}<br>Tingkat C</td></tr>
            <tr><td>4.</td><td>Maksud Perjalanan Dinas</td><td>{maksud}</td></tr>
            <tr><td>5.</td><td>Alat angkut yang digunakan</td><td>Pesawat Udara / Kendaraan Dinas</td></tr>
            <tr><td>6.</td><td>a. Tempat Berangkat<br>b. Tempat Tujuan</td><td>Bajawa<br>{tujuan}</td></tr>
            <tr><td>7.</td><td>a. Lamanya Perjalanan Dinas<br>b. Tanggal Berangkat<br>c. Tanggal Harus Kembali</td><td>{lama} Hari<br>{tgl_str(tgl_p)}<br>{tgl_str(tgl_k)}</td></tr>
            <tr><td>8.</td><td>Pengikut: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Nama</td><td class="text-center">Tanggal Lahir / Keterangan</td></tr>
            <tr><td height="25px"></td><td>1.</td><td></td></tr>
            <tr><td>9.</td><td>Pembebanan Anggaran<br>a. Instansi<br>b. Mata Anggaran</td><td><br>a. Bagian Perekonomian dan SDA<br>b. </td></tr>
            <tr><td>10.</td><td>Keterangan lain-lain</td><td></td></tr>
        </table>
        <div style="margin-left:55%; margin-top:20px;">
            <p style="margin:0;">Dikeluarkan di : Bajawa</p>
            <p style="margin:0;">Pada Tanggal : {tgl_str(tgl_cetak)}</p>
            <br><p class="text-bold" style="margin:0;">An. BUPATI NGADA</p>
            <p style="margin:0;">Pj. Sekretaris Daerah,</p>
            <br><br><br><br>
            <p class="text-bold text-underline" style="margin:0;">{ttd_nama}</p>
            <p style="margin:0;">{ttd_gol}</p>
            <p style="margin:0;">NIP. {ttd_nip}</p>
        </div>
    </div>

    <div class="kertas">
        <div class="kop-tanpa-logo">
            <h3 style="margin:0; font-size: 14pt;">PEMERINTAH KABUPATEN NGADA</h3>
            <h2 style="margin:0; font-size: 14pt;">SEKRETARIAT DAERAH</h2>
            <p style="margin:0; font-size: 10pt;">Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834</p>
            <h3 style="margin:0; font-size: 14pt;">BAJAWA</h3>
        </div>
        
        <table class="tabel-border">
            <tr style="height: 200px;">
                <td width="45%"></td>
                <td>I. Berangkat dari : Bajawa<br>Ke : {tujuan}<br>Pada Tanggal : {tgl_str(tgl_p)}<br><br>
                <div class="text-center">An. Bupati Ngada<br>Pj. Sekretaris Daerah<br><br><br><br><br>
                <span class="text-bold text-underline">{ttd_nama}</span><br>{ttd_gol}<br>NIP. {ttd_nip}</div></td>
            </tr>
            <tr style="height: 160px;">
                <td>II. Tiba di : {tujuan}<br>Pada Tanggal : {tgl_str(tgl_p)}</td>
                <td>Berangkat dari : {tujuan}<br>Ke : Bajawa<br>Pada Tanggal : {tgl_str(tgl_k)}</td>
            </tr>
            <tr style="height: 160px;">
                <td>III. Tiba di :<br>Pada Tanggal :</td>
                <td>Berangkat dari :<br>Ke :<br>Pada Tanggal :</td>
            </tr>
            <tr style="height: 160px;">
                <td>IV. Tiba di :<br>Pada Tanggal :</td>
                <td>Berangkat dari :<br>Ke :<br>Pada Tanggal :</td>
            </tr>
            <tr style="height: 200px;">
                <td>V. Tiba Kembali : Bajawa<br>Pada Tanggal : {tgl_str(tgl_k)}</td>
                <td><div style="font-style: italic; text-align: center; font-size: 8.5pt; margin-bottom: 15px;">Telah diperiksa, dengan keterangan bahwa perjalanan tersebut atas perintahnya dan semata-mata untuk kepentingan jabatan</div>
                <div class="text-center">An. Bupati Ngada<br>Pj. Sekretaris Daerah<br><br><br><br><br>
                <span class="text-bold text-underline">{ttd_nama}</span><br>{ttd_gol}<br>NIP. {ttd_nip}</div></td>
            </tr>
            <tr><td colspan="2">VI. Catatan Lain-lain</td></tr>
            <tr><td colspan="2">VII. Perhatian :</td></tr>
            <tr><td colspan="2" style="text-align: justify; font-style: italic; padding: 10px; font-size: 8.5pt;">Pejabat yang menerbitkan SPD, pegawai yang melakukan perjalanan dinas, para pejabat yang mengesahkan tanggal berangkat/tiba, serta Bendahara Pengeluaran bertanggung jawab berdasarkan peraturan-peraturan Keuangan Negara apabila negara menderita rugi akibat kesalahan, kelalaian dan kealpaannya.</td></tr>
        </table>
    </div>
</div>
"""

st.components.v1.html(surat_html, height=4500, scrolling=True)
