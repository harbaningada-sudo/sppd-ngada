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
        .wrap { background-color: white !important; padding: 0 !important; margin: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; border: none !important; }
    }
</style>
""", unsafe_allow_html=True)

# --- BAGIAN LOGO (PASTE KODE BASE64 DI SINI) ---
LOGO_PEMDA = """PASTE_KODE_BASE64_PEMDA_DI_SINI"""
LOGO_GARUDA = """PASTE_KODE_BASE64_GARUDA_DI_SINI"""

# 2. PANEL INPUT SIDEBAR
with st.sidebar:
    st.header("📋 INPUT DATA")
    jenis = st.radio("📍 Jenis Perjalanan", ["Dalam Daerah", "Luar Daerah"])
    
    with st.expander("📄 DATA SURAT", expanded=True):
        no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
        kode_no = st.text_input("Kode No", "094/Prokopim")
        maksud = st.text_area("Maksud Perjalanan", "Monitoring dan Pendataan Pemilik Tambang Pasir...")
        tujuan = st.text_input("Tempat Tujuan", "Kecamatan Golewa")
        alat_angkut = st.text_input("Alat Angkutan", "Mobil")
        mata_anggaran = st.text_input("Mata Anggaran (9b)", "")
        dasar_surat = st.text_area("Dasar (Khusus Luar Daerah)", "Surat Balai Besar Konservasi Sumber Daya Alam...")

    with st.expander("👤 DATA PEGAWAI", expanded=True):
        if 'jml' not in st.session_state: st.session_state.jml = 1
        c1, c2 = st.columns(2)
        if c1.button("➕ Tambah"): st.session_state.jml += 1
        if c2.button("➖ Kurang") and st.session_state.jml > 1: st.session_state.jml -= 1
        
        daftar_pegawai = []
        for i in range(st.session_state.jml):
            st.markdown(f"**Pegawai {i+1}**")
            p_no_spd = st.text_input(f"Nomor SPD P-{i+1}", f"531 /02/2026", key=f"spd{i}")
            p_nama = st.text_input(f"Nama P-{i+1}", f"Nama Pegawai {i+1}", key=f"n{i}")
            p_nip = st.text_input(f"NIP P-{i+1}", "19XXXXXXXXXXXXXX", key=f"nip{i}")
            p_gol = st.text_input(f"Gol P-{i+1}", "Penata Muda - III/a", key=f"g{i}")
            p_jabatan = st.text_input(f"Jabatan P-{i+1}", "Perencana Ahli Pertama", key=f"j{i}")
            daftar_pegawai.append({"no_spd": p_no_spd, "nama": p_nama, "nip": p_nip, "gol": p_gol, "jabatan": p_jabatan})

    with st.expander("🕒 TTD", expanded=False):
        tgl_p = st.date_input("Berangkat", datetime.now())
        tgl_k = st.date_input("Kembali", datetime.now())
        lama = st.text_input("Lama Hari", "1 (Satu) hari")
        tgl_ctk = st.date_input("Tanggal Cetak", datetime.now())
        st.markdown("---")
        ttd_an = st.text_input("a.n.", "BUPATI NGADA")
        ttd_jab_tengah = st.text_input("Jabatan 1", "Sekretaris Daerah")
        ttd_ub = st.text_input("Jabatan 2 (u.b.)", "Asisten Perekonomian dan Pembangunan")
        ttd_nama = st.text_input("Nama Pejabat TTD", "Dr. Nicolaus Noywuli, S.Pt, M.Si")
        ttd_gol = st.text_input("Pangkat/Gol", "Pembina Utama Muda- IV/c")
        ttd_nip = st.text_input("NIP Pejabat", "19720921 200012 1 004")

    if st.button("🖨️ CETAK SEMUA"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

# HELPER TANGGAL
def tgl_str(d):
    bln = ["Januari","Februari","Maret","April","Mei","Juni"," Juli","Agustus","September","Oktober","November","Desember"]
    return f"{d.day} {bln[d.month-1]} {d.year}"

# --- CSS TEMPLATE (VERSI PENYEMPURNAAN FINAL) ---
style_html = """
<style>
    .wrap { display: flex; flex-direction: column; align-items: center; gap: 30px; background: #525659; padding: 20px; }
    .kertas { background: white; width: 210mm; min-height: 297mm; padding: 15mm 15mm 15mm 20mm; color: black; font-family: Arial, sans-serif; box-sizing: border-box; page-break-after: always; position: relative; }
    .kop-daerah { display: flex; align-items: center; border-bottom: 3.5px solid black; padding-bottom: 5px; margin-bottom: 10px; }
    .tabel-border { width: 100%; border-collapse: collapse; border: 1.3px solid black; font-size: 10.5pt; table-layout: fixed; }
    .tabel-border td { border: 1.3px solid black; padding: 4px 6px; vertical-align: top; word-wrap: break-word; }
    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }
    .no-b-bottom { border-bottom: none !important; }
    .no-b-top { border-top: none !important; }
    .p-0 { padding: 0 !important; }
</style>
"""

content_html = f'<div class="wrap">{style_html}'

# BLOK TTD
ttd_block = f"""
<div style="margin-left:50%; margin-top:25px; line-height: 1.2; font-size: 10.5pt;">
    <p style="margin:0;">Ditetapkan di : Bajawa</p>
    <p style="margin:0;">Pada Tanggal : {tgl_str(tgl_ctk)}</p><br>
    <p class="text-bold" style="margin:0;">a.n. {ttd_an}</p>
    <p class="text-bold" style="margin:0;">{ttd_jab_tengah}</p>
    <p class="text-bold" style="margin:0;">u.b. {ttd_ub},</p><br><br><br><br>
    <p class="text-bold underline" style="margin:0;">{ttd_nama}</p>
    <p style="margin:0;">{ttd_gol}</p>
    <p style="margin:0;">NIP. {ttd_nip}</p>
</div>"""

# --- 1. SPT ---
if jenis == "Luar Daerah":
    header_spt = f'<div class="text-center"><img src="{LOGO_GARUDA}" style="width:75px;"><br><h3 style="margin:5px 0;">BUPATI NGADA</h3></div>'
    dasar_isi = dasar_surat
else:
    header_spt = f'<div class="kop-daerah"><img src="{LOGO_PEMDA}" style="width:65px; margin-right:15px;"><div style="flex:1; text-align:center;"><h3 style="margin:0; font-size:13pt;">PEMERINTAH KABUPATEN NGADA</h3><h2 style="margin:0; font-size:15pt;">SEKRETARIAT DAERAH</h2><p style="margin:0; font-size:8.5pt;">Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834 BAJAWA</p></div></div>'
    dasar_isi = "DPA Bagian Perekonomian dan SDA Setda Ngada Tahun Anggaran 2026"

rows_peg = "".join([f"<tr><td width='5%'></td><td width='5%'>{i+1}.</td><td width='15%'>Nama</td><td>: <b>{p['nama']}</b></td></tr><tr><td></td><td></td><td>Pangkat/Gol</td><td>: {p['gol']}</td></tr><tr><td></td><td></td><td>NIP</td><td>: {p['nip']}</td></tr><tr><td></td><td></td><td>Jabatan</td><td>: {p['jabatan']}</td></tr><tr><td colspan='4' height='6px'></td></tr>" for i, p in enumerate(daftar_pegawai)])

content_html += f'<div class="kertas">{header_spt}<h3 class="text-center text-bold underline" style="margin-top:10px;">SURAT PERINTAH TUGAS</h3><p class="text-center" style="margin-top:-10px;">NOMOR : {no_spt}</p><table width="100%" style="border-collapse:collapse; font-size:10.5pt;"><tr><td width="15%">Dasar</td><td>: {dasar_isi}</td></tr></table><p class="text-center text-bold" style="margin: 10px 0;">M E M E R I N T A H K A N</p><table width="100%" style="border-collapse:collapse; font-size:10.5pt;"><tr><td width="15%">Kepada</td><td colspan="3"></td></tr>{rows_peg}</table><table width="100%" style="border-collapse:collapse; font-size:10.5pt;"><tr><td width="15%">Untuk</td><td>: {maksud} ke {tujuan}</td></tr></table>{ttd_block}</div>'

# --- 2. SPD DEPAN (MODIFIKASI FINAL) ---
header_spd = f'<div class="kop-daerah"><img src="{LOGO_PEMDA}" style="width:65px; margin-right:15px;"><div style="flex:1; text-align:center;"><h3 style="margin:0; font-size:13pt;">PEMERINTAH KABUPATEN NGADA</h3><h2 style="margin:0; font-size:15pt;">SEKRETARIAT DAERAH</h2><p style="margin:0; font-size:8.5pt;">Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834 BAJAWA</p></div></div>'

for p in daftar_pegawai:
    content_html += f"""
    <div class="kertas">{header_spd}
    <div style="margin-left:60%; font-size:9pt;">Kode No: {kode_no}<br>Nomor: {p['no_spd']}</div>
    <h3 class="text-center text-bold underline" style="margin-bottom:5px; margin-top:5px;">SURAT PERINTAH DINAS (SPD)</h3>
    <table class="tabel-border">
        <tr><td width="5%">1.</td><td width="42%">Pejabat yang memberi perintah</td><td colspan="3"><b>BUPATI NGADA</b></td></tr>
        <tr><td>2.</td><td>Nama Pegawai yang diperintahkan</td><td colspan="3"><b>{p['nama']}</b></td></tr>
        <tr><td class="no-b-bottom">3.</td><td>a. Pangkat/Golongan</td><td colspan="3">{p['gol']}</td></tr>
        <tr><td class="no-b-top no-b-bottom"></td><td>b. Jabatan</td><td colspan="3">{p['jabatan']}</td></tr>
        <tr><td class="no-b-top"></td><td>c. Tingkat Menurut Peraturan</td><td colspan="3"></td></tr>
        <tr><td>4.</td><td>Maksud Perjalanan Dinas</td><td colspan="3">{maksud}</td></tr>
        <tr><td>5.</td><td>Alat angkut yang digunakan</td><td colspan="3">{alat_angkut}</td></tr>
        <tr><td class="no-b-bottom">6.</td><td>a. Tempat Berangkat</td><td colspan="3">Bajawa</td></tr>
        <tr><td class="no-b-top"></td><td>b. Tempat Tujuan</td><td colspan="3">{tujuan}</td></tr>
        <tr><td class="no-b-bottom">7.</td><td>a. Lamanya Perjalanan Dinas</td><td colspan="3">{lama}</td></tr>
        <tr><td class="no-b-top no-b-bottom"></td><td>b. Tanggal Berangkat</td><td colspan="3">{tgl_str(tgl_p)}</td></tr>
        <tr><td class="no-b-top"></td><td>c. Tanggal Harus Kembali</td><td colspan="3">{tgl_str(tgl_k)}</td></tr>
        
        <tr><td class="no-b-bottom">8.</td><td>Pengikut</td><td width="20%" class="text-center">Nama</td><td width="15%" class="text-center">Tanggal Lahir</td><td width="18%" class="text-center">Keterangan</td></tr>
        <tr><td class="no-b-top no-b-bottom"></td><td>1.</td><td></td><td></td><td></td></tr>
        <tr><td class="no-b-top"></td><td>2.</td><td></td><td></td><td></td></tr>

        <tr><td class="no-b-bottom">9.</td><td>Pembebanan Anggaran</td><td colspan="3"></td></tr>
        <tr><td class="no-b-top no-b-bottom"></td><td>a. Instansi</td><td colspan="3">a. Bagian Perekonomian dan SDA</td></tr>
        <tr><td class="no-b-top"></td><td>b. Mata Anggaran</td><td colspan="3">b.</td></tr>
        
        <tr><td>10.</td><td>Keterangan lain-lain</td><td colspan="3"></td></tr>
    </table>{ttd_block}</div>"""

# --- 3. SPD BELAKANG & REGISTER (TETAP) ---
# ... (Kode SPD Belakang dan Register menyusul di bawah, identik dengan versi sebelumnya)
content_html += f"""<div class="kertas" style="padding-top:30mm;"><table class="tabel-border">
<tr style="height:180px;"><td width="45%"></td><td><div style="padding:8px;">I. Berangkat dari : Bajawa<br>Ke : {tujuan}<br>Tgl : {tgl_str(tgl_p)}<br><br><div class="text-center">a.n. {ttd_an}<br>{ttd_jab_tengah}<br>u.b. {ttd_ub},<br><br><br><span class="underline text-bold">{ttd_nama}</span></div></div></td></tr>
<tr style="height:150px;"><td><div style="padding:8px;">II. Tiba di : {tujuan}<br>Tgl : {tgl_str(tgl_p)}</div></td><td><div style="padding:8px;">Berangkat dari : {tujuan}<br>Ke : Bajawa<br>Tgl : {tgl_str(tgl_k)}</div></td></tr>
<tr style="height:180px;"><td><div style="padding:8px;">V. Tiba Kembali : Bajawa<br>Tgl : {tgl_str(tgl_k)}</div></td><td><div class="text-center" style="padding:8px;"><br>Telah diperiksa dengan keterangan bahwa perjalanan tersebut atas perintahnya.<br><br>a.n. {ttd_an}<br>{ttd_jab_tengah}<br>u.b. {ttd_ub},<br><br><br><span class="underline text-bold">{ttd_nama}</span></div></div></td></tr>
</table></div>"""

reg_rows = "".join([f"<tr><td class='text-center'>{i+1}</td><td>{p['nama']}</td><td>{no_spt}</td><td>{p['no_spd']}</td><td>{maksud} ke {tujuan}</td><td>{tgl_str(tgl_p)}</td><td>{tgl_str(tgl_k)}</td><td></td></tr>" for i, p in enumerate(daftar_pegawai)])
content_html += f"""<div class="kertas" style="width:297mm; min-height:210mm;"><h3 class="text-center">BUKU REGISTER PERJALANAN DINAS</h3><table class="tabel-border"><thead><tr style="background:#eee;"><th width="30">No</th><th>Nama</th><th>No SPT</th><th>No SPD</th><th>Maksud Tujuan</th><th width="80">Pergi</th><th width="80">Pulang</th><th>Ket</th></tr></thead><tbody>{reg_rows}</tbody></table></div></div>"""

st.components.v1.html(content_html, height=2500, scrolling=True)
