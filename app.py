import streamlit as st
from datetime import datetime
import pandas as pd
import io

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Prokopim Ngada", layout="wide")

st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    .main { background-color: #525659; }
    @media print {
        .no-print { display: none !important; }
        .wrap { background-color: white !important; padding: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; border: none !important; }
    }
</style>
""", unsafe_allow_html=True)

# --- LOGO DALAM DAERAH (TEMPEL BASE64 PEMDA DI SINI) ---
logo_pemda_base64 = """PASTE_KODE_BASE64_PEMDA_DI_SINI""" 

# --- LOGO GARUDA (UNTUK LUAR DAERAH - SAYA BERIKAN BASE64 STANDAR GARUDA EMAS) ---
logo_garuda = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/National_emblem_of_Indonesia_Garuda_Pancasila.svg/1200px-National_emblem_of_Indonesia_Garuda_Pancasila.svg.png"

# 2. PANEL INPUT SIDEBAR
with st.sidebar:
    st.header("📋 INPUT DATA")
    
    # --- TAMBAHAN OPSI JENIS PERJALANAN ---
    jenis_perjalanan = st.radio("📍 Jenis Perjalanan", ["Dalam Daerah", "Luar Daerah"], index=0)
    
    with st.expander("📄 DATA SURAT", expanded=True):
        no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
        no_spd = st.text_input("Nomor SPD", "530 /02/2026")
        kode_no = st.text_input("Kode No", "094/Prokopim")
        dasar_surat = st.text_area("Dasar (Hanya Luar Daerah)", "Surat Balai Besar Konservasi Sumber Daya Alam...")
        maksud = st.text_area("Maksud Perjalanan", "Monitoring dan Pendataan Pemilik Tambang Pasir...")
        tujuan = st.text_input("Tempat Tujuan", "Kecamatan Golewa")

    with st.expander("👤 DATA PEGAWAI (MULTI)", expanded=True):
        if 'jumlah_pegawai' not in st.session_state: st.session_state.jumlah_pegawai = 1
        c1, c2 = st.columns(2)
        if c1.button("➕ Tambah"): st.session_state.jumlah_pegawai += 1
        if c2.button("➖ Kurang") and st.session_state.jumlah_pegawai > 1: st.session_state.jumlah_pegawai -= 1
        
        daftar_pegawai = []
        for i in range(st.session_state.jumlah_pegawai):
            st.markdown(f"**Pegawai {i+1}**")
            p_nama = st.text_input(f"Nama P-{i+1}", f"Nama Pegawai {i+1}", key=f"n{i}")
            p_nip = st.text_input(f"NIP P-{i+1}", "19XXXXXXXXXXXXXX", key=f"nip{i}")
            p_gol = st.text_input(f"Gol P-{i+1}", "Penata Muda - III/a", key=f"g{i}")
            p_jabatan = st.text_input(f"Jabatan P-{i+1}", "Pelaksana", key=f"j{i}")
            daftar_pegawai.append({"nama": p_nama, "nip": p_nip, "gol": p_gol, "jabatan": p_jabatan})

    with st.expander("🕒 WAKTU & TTD", expanded=False):
        tgl_p = st.date_input("Tanggal Berangkat", datetime(2026, 2, 25))
        tgl_k = st.date_input("Tanggal Kembali", datetime(2026, 2, 26))
        lama = st.text_input("Lama Hari", "2 (Dua)")
        tgl_cetak = st.date_input("Tanggal Cetak", datetime(2026, 2, 25))
        jabatan_ttd = st.text_input("Jabatan Penandatangan", "WAKIL BUPATI NGADA" if jenis_perjalanan == "Luar Daerah" else "Pj. Sekretaris Daerah")
        ttd_nama = st.text_input("Nama Penandatangan", "BERNADINUS DHEY NGEBU, SP" if jenis_perjalanan == "Luar Daerah" else "Yohanes C. Watu Ngebu, S.Sos., M.Si")
        ttd_nip = st.text_input("NIP Penandatangan", "19650101 198603 1 045")
        ttd_gol = st.text_input("Gol Penandatangan", "Pembina Utama Madya")

    st.button("🖨️ CETAK SEMUA", on_click=lambda: st.components.v1.html("<script>window.parent.print();</script>", height=0))

# FORMAT TANGGAL
bulan_list = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
def tgl_str(d): return f"{d.day} {bulan_list[d.month-1]} {d.year}"

# --- LOGIKA KOP SPT ---
if jenis_perjalanan == "Luar Daerah":
    kop_spt_html = f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <img src="{logo_garuda}" style="width: 80px; height: auto; margin-bottom: 10px;">
        <h3 style="margin:0; letter-spacing: 2px;">BUPATI NGADA</h3>
    </div>
    """
    dasar_html = f"<tr><td width='15%'>Dasar</td><td width='2%'>:</td><td>{dasar_surat}</td></tr>"
else:
    logo_pemda_html = f'<img src="{logo_pemda_base64}" style="width: 75px; height: auto; margin-right: 20px;">' if len(logo_pemda_base64) > 100 else ""
    kop_spt_html = f"""
    <div class="kop-container">{logo_pemda_html}<div class="kop-text">
        <h3 style="margin:0;">PEMERINTAH KABUPATEN NGADA</h3><h2 style="margin:0;">SEKRETARIAT DAERAH</h2>
        <p style="margin:0; font-size: 9pt;">Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834 BAJAWA</p>
    </div></div>
    """
    dasar_html = f"<tr><td width='15%'>Dasar</td><td width='2%'>:</td><td>DPA Bagian Perekonomian dan SDA Setda Ngada TA 2026</td></tr>"

# --- TEMPLATE CSS ---
style_html = """<style>
    .wrap { background-color: #525659; padding: 20px; display: flex; flex-direction: column; align-items: center; gap: 25px; }
    .kertas { background-color: white; width: 210mm; min-height: 297mm; padding: 15mm 20mm 20mm 25mm; color: black; font-family: Arial, sans-serif; font-size: 10pt; box-shadow: 0 0 15px rgba(0,0,0,0.5); box-sizing: border-box; page-break-after: always; position: relative; }
    .kop-container { display: flex; align-items: center; border-bottom: 3px solid black; padding-bottom: 5px; margin-bottom: 15px; }
    .kop-text { flex: 1; text-align: center; line-height: 1.2; }
    .tabel-polos { width: 100%; border-collapse: collapse; margin-bottom: 10px; }
    .tabel-polos td { border: none; padding: 2px; vertical-align: top; }
    .tabel-border { width: 100%; border-collapse: collapse; border: 1.2px solid black; }
    .tabel-border td { border: 1.2px solid black; padding: 8px 10px; vertical-align: top; }
    .text-center { text-align: center; } .text-bold { font-weight: bold; } .text-underline { text-decoration: underline; }
</style>"""

content_html = f'<div class="wrap">{style_html}'

# --- HALAMAN 1: SPT ---
pegawai_spt = ""
for i, p in enumerate(daftar_pegawai):
    pegawai_spt += f"<tr><td></td><td>{i+1}.</td><td>Nama</td><td>:</td><td class='text-bold'>{p['nama']}</td></tr>" \
                   f"<tr><td></td><td></td><td>Pangkat/Gol</td><td>:</td><td>{p['gol']}</td></tr>" \
                   f"<tr><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr>" \
                   f"<tr><td></td><td></td><td>Jabatan</td><td>:</td><td>{p['jabatan']}</td></tr>" \
                   f"<tr><td colspan='5' height='5px'></td></tr>"

content_html += f"""
<div class="kertas">
    {kop_spt_html}
    <h3 class="text-center text-bold text-underline">SURAT PERINTAH TUGAS</h3>
    <p class="text-center" style="margin-top:-10px;">NOMOR : {no_spt}</p>
    <table class="tabel-polos">{dasar_html}</table>
    <p class="text-center text-bold" style="margin: 15px 0;">M E M E R I N T A H K A N</p>
    <table class="tabel-polos"><tr valign="top"><td width="15%">Kepada</td><td colspan="4"></td></tr>{pegawai_spt}</table>
    <table class="tabel-polos"><tr><td width="15%">Untuk</td><td width="2%">:</td><td style="text-align:justify;">{maksud}</td></tr></table>
    <div style="margin-left:55%; margin-top:30px;">
        <p style="margin:0;">Ditetapkan di : Bajawa</p><p style="margin:0;">Pada Tanggal : {tgl_str(tgl_cetak)}</p>
        <br><p class="text-bold" style="margin:0;">An. BUPATI NGADA</p><p style="margin:0;">{jabatan_ttd},</p>
        <br><br><br><p class="text-bold text-underline" style="margin:0;">{ttd_nama}</p><p style="margin:0;">{ttd_gol}</p><p style="margin:0;">NIP. {ttd_nip}</p>
    </div>
</div>
"""

# --- HALAMAN 2 & 3: SPD DEPAN & BELAKANG (Format Tetap Sama) ---
# ... (Sama dengan kode sebelumnya) ...

# (Hanya Cuplikan di bawah untuk menghemat tempat, pastikan di file asli kamu lengkap)
for p in daftar_pegawai:
    # SPD Depan tetap pakai logo Pemda di Kop
    logo_pemda_html = f'<img src="{logo_pemda_base64}" style="width: 75px; height: auto; margin-right: 20px;">' if len(logo_pemda_base64) > 100 else ""
    content_html += f"""
    <div class="kertas">
        <div class="kop-container">{logo_pemda_html}<div class="kop-text">
            <h3 style="margin:0;">PEMERINTAH KABUPATEN NGADA</h3><h2 style="margin:0;">SEKRETARIAT DAERAH</h2>
            <p style="margin:0; font-size: 9pt;">Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834 BAJAWA</p>
        </div></div>
        <div style="margin-left: 60%; font-size: 9pt;"><table><tr><td>Kode No</td><td>:</td><td>{kode_no}</td></tr><tr><td>Nomor</td><td>:</td><td>{no_spd}</td></tr></table></div>
        <h3 class="text-center text-bold text-underline" style="margin-bottom:0;">SURAT PERINTAH DINAS (SPD)</h3>
        <table class="tabel-border">
            <tr><td width="5%">1.</td><td width="40%">Pejabat yang memberi perintah</td><td>BUPATI NGADA</td></tr>
            <tr><td>2.</td><td>Nama Pegawai yang diperintahkan</td><td class="text-bold">{p['nama']}</td></tr>
            <tr><td>3.</td><td>a. Pangkat/Golongan<br>b. Jabatan<br>c. Tingkat Menurut Peraturan</td><td>{p['gol']}<br>{p['jabatan']}<br>Tingkat C</td></tr>
            <tr><td>4.</td><td>Maksud Perjalanan Dinas</td><td>{maksud}</td></tr>
            <tr><td>5.</td><td>Alat angkut yang digunakan</td><td>Kendaraan Dinas</td></tr>
            <tr><td>6.</td><td>a. Tempat Berangkat<br>b. Tempat Tujuan</td><td>Bajawa<br>{tujuan}</td></tr>
            <tr><td>7.</td><td>a. Lamanya Perjalanan Dinas<br>b. Tanggal Berangkat<br>c. Tanggal Harus Kembali</td><td>{lama} Hari<br>{tgl_str(tgl_p)}<br>{tgl_str(tgl_k)}</td></tr>
            <tr><td>8.</td><td>Pengikut: Nama</td><td>Tgl Lahir / Ket</td></tr><tr><td height="20px"></td><td>1.</td><td></td></tr>
            <tr><td>9.</td><td>Pembebanan Anggaran</td><td>Bagian Perekonomian dan SDA</td></tr>
            <tr><td>10.</td><td>Keterangan lain-lain</td><td></td></tr>
        </table>
        <div style="margin-left:55%; margin-top:20px;">
            <p style="margin:0;">Dikeluarkan di : Bajawa</p><p style="margin:0;">Pada Tanggal : {tgl_str(tgl_cetak)}</p>
            <br><p class="text-bold" style="margin:0;">An. BUPATI NGADA</p><p style="margin:0;">{jabatan_ttd},</p>
            <br><br><br><p class="text-bold text-underline" style="margin:0;">{ttd_nama}</p><p style="margin:0;">{ttd_gol}</p><p style="margin:0;">NIP. {ttd_nip}</p>
        </div>
    </div>
    """

# --- SPD BELAKANG ---
content_html += f"""
<div class="kertas" style="padding-top: 30mm;">
    <table class="tabel-border">
        <tr style="height: 180px;"><td width="45%"></td><td>I. Berangkat dari : Bajawa<br>Ke : {tujuan}<br>Tgl : {tgl_str(tgl_p)}<br><br><div class="text-center">An. Bupati Ngada<br>{jabatan_ttd}<br><br><br><span class="text-bold text-underline">{ttd_nama}</span></div></td></tr>
        <tr style="height: 140px;"><td>II. Tiba di : {tujuan}</td><td>Berangkat dari : {tujuan}<br>Ke : Bajawa</td></tr>
        <tr style="height: 180px;"><td>V. Tiba Kembali : Bajawa<br>Tgl : {tgl_str(tgl_k)}</td><td><div class="text-center">An. Bupati Ngada<br>{jabatan_ttd}<br><br><br><span class="text-bold text-underline">{ttd_nama}</span></div></td></tr>
    </table>
</div>
"""

content_html += "</div>"
st.components.v1.html(content_html, height=2000, scrolling=True)
