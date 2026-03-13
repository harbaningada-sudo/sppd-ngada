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

# --- BAGIAN LOGO (TEMPEL KODE BASE64 MU DI ANTARA KUTIP TIGA) ---
logo_data_url = """PASTE_KODE_BASE64_MILIKMU_DI_SINI""" 

if len(logo_data_url) > 100:
    logo_html = f'<img src="{logo_data_url}" style="width: 75px; height: auto; margin-right: 20px;">'
else:
    logo_html = '<div style="width: 75px; color:red;">Logo Kosong</div>'

# 2. PANEL INPUT SIDEBAR
with st.sidebar:
    st.header("📋 INPUT DATA")
    
    with st.expander("📄 DATA SURAT", expanded=True):
        no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
        no_spd = st.text_input("Nomor SPD", "530 /02/2026")
        kode_no = st.text_input("Kode No", "094/Prokopim")
        maksud = st.text_area("Maksud Perjalanan", "Monitoring dan Pendataan Pemilik Tambang Pasir...")
        tujuan = st.text_input("Tempat Tujuan", "Kecamatan Golewa")

    with st.expander("👤 DATA PEGAWAI (MULTI)", expanded=True):
        if 'jumlah_pegawai' not in st.session_state:
            st.session_state.jumlah_pegawai = 1
        
        col_btn1, col_btn2 = st.columns(2)
        if col_btn1.button("➕ Tambah"):
            st.session_state.jumlah_pegawai += 1
        if col_btn2.button("➖ Kurang") and st.session_state.jumlah_pegawai > 1:
            st.session_state.jumlah_pegawai -= 1

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
        ttd_nama = st.text_input("Nama Penandatangan", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
        ttd_nip = st.text_input("NIP Penandatangan", "19710328 199203 1 011")
        ttd_gol = st.text_input("Gol Penandatangan", "Pembina Utama Muda - IV/c")

    st.markdown("---")
    if st.button("🖨️ CETAK SEMUA"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

    # --- FITUR DOWNLOAD EXCEL (ENGINE OPENPYXL) ---
    df = pd.DataFrame(daftar_pegawai)
    df.insert(0, 'No', range(1, len(df) + 1))
    df['Nomor SPT'] = no_spt
    df['Tujuan'] = tujuan
    df['Tanggal Berangkat'] = tgl_p.strftime('%d-%m-%Y')
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Register_SPD')
    processed_data = output.getvalue()

    st.download_button(
        label="📥 UNDUH REGISTER (EXCEL)",
        data=processed_data,
        file_name=f'Register_SPD_{tgl_p.strftime("%d%m%Y")}.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# FORMAT TANGGAL
bulan_list = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
def tgl_str(d): return f"{d.day} {bulan_list[d.month-1]} {d.year}"

# --- CSS & TEMPLATE ---
style_html = f"""
<style>
    .wrap {{ background-color: #525659; padding: 20px; display: flex; flex-direction: column; align-items: center; gap: 25px; }}
    .kertas {{ background-color: white; width: 210mm; min-height: 297mm; padding: 15mm 20mm 20mm 25mm; color: black; font-family: Arial, sans-serif; font-size: 10pt; box-shadow: 0 0 15px rgba(0,0,0,0.5); box-sizing: border-box; page-break-after: always; position: relative; }}
    .kop-container {{ display: flex; align-items: center; border-bottom: 3px solid black; padding-bottom: 5px; margin-bottom: 15px; }}
    .kop-text {{ flex: 1; text-align: center; line-height: 1.2; }}
    .tabel-polos {{ width: 100%; border-collapse: collapse; margin-bottom: 10px; }}
    .tabel-polos td {{ border: none; padding: 2px; vertical-align: top; }}
    .tabel-border {{ width: 100%; border-collapse: collapse; border: 1.2px solid black; }}
    .tabel-border td, .tabel-border th {{ border: 1.2px solid black; padding: 8px 10px; vertical-align: top; }}
    .text-center {{ text-align: center; }}
    .text-bold {{ font-weight: bold; }}
    .text-underline {{ text-decoration: underline; }}
</style>
"""

content_html = f'<div class="wrap">{style_html}'

# --- HALAMAN 1: SPT ---
pegawai_spt = ""
for i, p in enumerate(daftar_pegawai):
    pegawai_spt += f"""
    <tr><td></td><td>{i+1}.</td><td>Nama</td><td>:</td><td class="text-bold">{p['nama']}</td></tr>
    <tr><td></td><td></td><td>Pangkat/Gol</td><td>:</td><td>{p['gol']}</td></tr>
    <tr><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr>
    <tr><td></td><td></td><td>Jabatan</td><td>:</td><td>{p['jabatan']}</td></tr>
    <tr><td colspan="5" height="5px"></td></tr>
    """

content_html += f"""
<div class="kertas">
    <div class="kop-container">{logo_html}<div class="kop-text">
        <h3 style="margin:0;">PEMERINTAH KABUPATEN NGADA</h3><h2 style="margin:0;">SEKRETARIAT DAERAH</h2>
        <p style="margin:0; font-size: 9pt;">Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834 BAJAWA</p>
    </div></div>
    <h3 class="text-center text-bold text-underline">SURAT PERINTAH TUGAS</h3>
    <p class="text-center" style="margin-top:-10px;">NOMOR : {no_spt}</p>
    <table class="tabel-polos"><tr><td width="15%">Dasar</td><td width="2%">:</td><td>DPA Bagian Perekonomian dan SDA Setda Ngada TA 2026</td></tr></table>
    <p class="text-center text-bold" style="margin: 15px 0;">M E M E R I N T A H K A N</p>
    <table class="tabel-polos"><tr valign="top"><td width="15%">Kepada</td><td colspan="4"></td></tr>{pegawai_spt}</table>
    <table class="tabel-polos"><tr><td width="15%">Untuk</td><td width="2%">:</td><td style="text-align:justify;">{maksud}</td></tr></table>
    <div style="margin-left:55%; margin-top:30px;">
        <p style="margin:0;">Ditetapkan di : Bajawa</p><p style="margin:0;">Pada Tanggal : {tgl_str(tgl_cetak)}</p>
        <br><p class="text-bold" style="margin:0;">An. BUPATI NGADA</p><p style="margin:0;">Pj. Sekretaris Daerah,</p>
        <br><br><br><p class="text-bold text-underline" style="margin:0;">{ttd_nama}</p><p style="margin:0;">{ttd_gol}</p><p style="margin:0;">NIP. {ttd_nip}</p>
    </div>
</div>
"""

# --- HALAMAN 2: SPD DEPAN ---
for p in daftar_pegawai:
    content_html += f"""
    <div class="kertas">
        <div class="kop-container">{logo_html}<div class="kop-text">
            <h3 style="margin:0;">PEMERINTAH KABUPATEN NGADA</h3><h2 style="margin:0;">SEKRETARIAT DAERAH</h2>
            <p style="margin:0; font-size: 9pt;">Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834 BAJAWA</p>
        </div></div>
        <div style="margin-left: 60%; font-size: 9pt;">
            <table><tr><td>Kode No</td><td>:</td><td>{kode_no}</td></tr><tr><td>Nomor</td><td>:</td><td>{no_spd}</td></tr></table>
        </div>
        <h3 class="text-center text-bold text-underline" style="margin-bottom:0;">SURAT PERINTAH DINAS (SPD)</h3>
        <table class="tabel-border">
            <tr><td width="5%">1.</td><td width="40%">Pejabat yang memberi perintah</td><td>BUPATI NGADA</td></tr>
            <tr><td>2.</td><td>Nama Pegawai yang diperintahkan</td><td class="text-bold">{p['nama']}</td></tr>
            <tr><td>3.</td><td>a. Pangkat/Golongan<br>b. Jabatan<br>c. Tingkat Menurut Peraturan</td><td>{p['gol']}<br>{p['jabatan']}<br>Tingkat C</td></tr>
            <tr><td>4.</td><td>Maksud Perjalanan Dinas</td><td>{maksud}</td></tr>
            <tr><td>5.</td><td>Alat angkut yang digunakan</td><td>Kendaraan Dinas</td></tr>
            <tr><td>6.</td><td>a. Tempat Berangkat<br>b. Tempat Tujuan</td><td>Bajawa<br>{tujuan}</td></tr>
            <tr><td>7.</td><td>a. Lamanya Perjalanan Dinas<br>b. Tanggal Berangkat<br>c. Tanggal Harus Kembali</td><td>{lama} Hari<br>{tgl_str(tgl_p)}<br>{tgl_str(tgl_k)}</td></tr>
            <tr><td>8.</td><td>Pengikut: Nama</td><td>Tgl Lahir / Ket</td></tr>
            <tr><td height="20px"></td><td>1.</td><td></td></tr>
            <tr><td>9.</td><td>Pembebanan Anggaran</td><td>Bagian Perekonomian dan SDA</td></tr>
            <tr><td>10.</td><td>Keterangan lain-lain</td><td></td></tr>
        </table>
        <div style="margin-left:55%; margin-top:20px;">
            <p style="margin:0;">Dikeluarkan di : Bajawa</p><p style="margin:0;">Pada Tanggal : {tgl_str(tgl_cetak)}</p>
            <br><p class="text-bold" style="margin:0;">An. BUPATI NGADA</p><p style="margin:0;">Pj. Sekretaris Daerah,</p>
            <br><br><br><p class="text-bold text-underline" style="margin:0;">{ttd_nama}</p><p style="margin:0;">{ttd_gol}</p><p style="margin:0;">NIP. {ttd_nip}</p>
        </div>
    </div>
    """

# --- HALAMAN 3: SPD BELAKANG ---
content_html += f"""
<div class="kertas" style="padding-top: 30mm;">
    <table class="tabel-border">
        <tr style="height: 180px;"><td width="45%"></td><td>I. Berangkat dari : Bajawa<br>Ke : {tujuan}<br>Tgl : {tgl_str(tgl_p)}<br><br><div class="text-center">An. Bupati Ngada<br>Pj. Sekretaris Daerah<br><br><br><span class="text-bold text-underline">{ttd_nama}</span></div></td></tr>
        <tr style="height: 140px;"><td>II. Tiba di : {tujuan}</td><td>Berangkat dari : {tujuan}<br>Ke : Bajawa</td></tr>
        <tr style="height: 180px;"><td>V. Tiba Kembali : Bajawa<br>Tgl : {tgl_str(tgl_k)}</td><td><div class="text-center">An. Bupati Ngada<br>Pj. Sekretaris Daerah<br><br><br><span class="text-bold text-underline">{ttd_nama}</span></div></td></tr>
    </table>
</div>
"""

# --- HALAMAN 4: BUKU REGISTER ---
rows_reg = ""
for i, p in enumerate(daftar_pegawai):
    rows_reg += f"<tr><td class='text-center'>{i+1}</td><td>{p['nama']}<br><small>NIP: {p['nip']}</small></td><td class='text-center'>{no_spt}</td><td class='text-center'>{tgl_str(tgl_p)}</td><td>{tujuan}</td><td></td></tr>"

content_html += f"""
<div class="kertas">
    <div class="kop-container">{logo_html}<div class="kop-text">
        <h3 style="margin:0;">PEMERINTAH KABUPATEN NGADA</h3><h2 style="margin:0;">SEKRETARIAT DAERAH</h2>
        <p style="margin:0;">BAGIAN PEREKONOMIAN DAN SUMBER DAYA ALAM</p>
    </div></div>
    <h3 class="text-center text-bold" style="margin-bottom: 20px;">BUKU REGISTER PERJALANAN DINAS</h3>
    <table class="tabel-border">
        <thead><tr style="background-color: #f2f2f2;"><th>No</th><th>Nama / NIP</th><th>Nomor SPT/SPD</th><th>Tanggal</th><th>Tujuan</th><th>Tanda Terima</th></tr></thead>
        <tbody>{rows_reg}</tbody>
    </table>
</div>
"""

content_html += "</div>"
st.components.v1.html(content_html, height=1500, scrolling=True)
