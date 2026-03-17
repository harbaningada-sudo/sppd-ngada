import streamlit as st
from datetime import datetime

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="SPD Ngada Pro", layout="wide")

# --- BAGIAN LOGO (ISI DULU DI SINI) ---
LOGO_PEMDA = "PASTE_KODE_BASE64_PEMDA_DI_SINI"
LOGO_GARUDA = "PASTE_KODE_BASE64_GARUDA_DI_SINI"

# 2. PANEL INPUT SIDEBAR (Tempat kamu isi data)
with st.sidebar:
    st.header("📋 DATA INPUT")
    jenis_perjalanan = st.radio("📍 Jenis Perjalanan", ["Dalam Daerah", "Luar Daerah"])
    
    with st.expander("📄 DATA SURAT", expanded=True):
        no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
        kode_no = st.text_input("Kode No", "094/Prokopim")
        maksud_tugas = st.text_area("Maksud Perjalanan", "Monitoring dan Pendataan Pemilik Tambang Pasir...")
        tempat_tujuan = st.text_input("Tujuan", "Kecamatan Golewa")
        alat_angkut = st.text_input("Alat Angkut", "Mobil Dinas")
        lama_hari = st.text_input("Lama Hari", "1 (Satu) hari")
        mata_anggaran = st.text_input("Mata Anggaran (9b)", "Bagian Perekonomian dan SDA")

    with st.expander("👤 PEGAWAI"):
        if 'jml' not in st.session_state: st.session_state.jml = 1
        c1, c2 = st.columns(2)
        if c1.button("➕"): st.session_state.jml += 1
        if c2.button("➖") and st.session_state.jml > 1: st.session_state.jml -= 1
        
        daftar_pegawai = []
        for i in range(st.session_state.jml):
            st.markdown(f"**Pegawai {i+1}**")
            p_nama = st.text_input(f"Nama P-{i+1}", f"Nama {i+1}", key=f"n{i}")
            p_nip = st.text_input(f"NIP P-{i+1}", "19XXXXXXXXXXXXXX", key=f"nip{i}")
            p_gol = st.text_input(f"Gol P-{i+1}", "III/a", key=f"g{i}")
            p_jab = st.text_input(f"Jabatan P-{i+1}", "Perencana", key=f"j{i}")
            p_spd = st.text_input(f"No SPD P-{i+1}", f"531 /02/2026", key=f"spd{i}")
            p_lembar = st.text_input(f"Lembar P-{i+1}", "I", key=f"lbr{i}")
            daftar_pegawai.append({"nama": p_nama, "nip": p_nip, "gol": p_gol, "jab": p_jab, "spd": p_spd, "lembar": p_lembar})

    with st.expander("🕒 TANDA TANGAN"):
        tgl_cetak = st.date_input("Tanggal Cetak", datetime.now())
        nama_pejabat = st.text_input("Pejabat TTD", "Dr. Nicolaus Noywuli, S.Pt, M.Si")
        nip_pejabat = st.text_input("NIP TTD", "19720921 200012 1 004")

    if st.button("🖨️ CETAK SEKARANG"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

# Fungsi format tanggal
def tgl_indo(d):
    bln = ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"]
    return f"{d.day} {bln[d.month-1]} {d.year}"

# --- 3. PROSES PEMBUATAN HTML (ISOLASI TOTAL) ---
html_content = f"""
<html>
<head>
<style>
    body {{ background-color: #525659; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; }}
    
    .kertas {{ 
        background-color: white !important; 
        width: 210mm; 
        min-height: 297mm; 
        padding: 15mm 20mm; 
        margin-bottom: 30px;
        color: black !important; 
        font-family: Arial, sans-serif; 
        box-sizing: border-box; 
        box-shadow: 0 0 15px rgba(0,0,0,0.5);
    }}

    .kop-sekda {{ display: flex; align-items: center; border-bottom: 3.5pt solid black; padding-bottom: 5px; margin-bottom: 15px; }}
    .kop-teks {{ flex: 1; text-align: center; }}
    .logo-garuda {{ text-align: center; margin-bottom: 10px; }}

    .tabel-spd {{ width: 100%; border-collapse: collapse; border: 1.5pt solid black; table-layout: fixed; }}
    .tabel-spd td {{ border: 1.5pt solid black; padding: 6px 10px; vertical-align: top; font-size: 10.5pt; color: black; }}

    .text-center {{ text-align: center; }} .text-bold {{ font-weight: bold; }} .underline {{ text-decoration: underline; }}
    
    @media print {{
        body {{ background-color: white; padding: 0; }}
        .kertas {{ box-shadow: none; margin: 0; page-break-after: always; }}
        table {{ -webkit-print-color-adjust: exact; }}
    }}
</style>
</head>
<body>
"""

# Template Kop & TTD
kop_html = f'<div class="kop-sekda"><img src="data:image/png;base64,{LOGO_PEMDA}" style="width:75px; margin-right:20px;"><div class="kop-teks"><h3 style="margin:0;">PEMERINTAH KABUPATEN NGADA</h3><h2 style="margin:0;">SEKRETARIAT DAERAH</h2><p style="margin:0; font-size:9pt;">Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834</p><p style="margin:0; font-size:10pt; font-weight:bold;">BAJAWA</p></div></div>'
kop_garuda_html = f'<div class="logo-garuda"><img src="data:image/png;base64,{LOGO_GARUDA}" style="width:85px;"><h2 style="margin:5px 0; color:black;">BUPATI NGADA</h2></div>'
ttd_html = f'<div style="margin-left:55%; margin-top:30px; line-height:1.3; color:black;">Ditetapkan di : Bajawa<br>Pada Tanggal : {tgl_indo(tgl_cetak)}<br><br><b>a.n. BUPATI NGADA</b><br><b>Sekretaris Daerah</b><br><b>u.b. Asisten Perekonomian dan Pembangunan,</b><br><br><br><br><b><u>{nama_pejabat}</u></b><br>NIP. {nip_pejabat}</div>'

# 1. HALAMAN SPT
spt_kop = kop_garuda_html if jenis_perjalanan == "Luar Daerah" else kop_html
pegawai_rows = "".join([f"<tr><td width='15%'>{'Kepada' if i==0 else ''}</td><td width='5%'>{i+1}.</td><td width='15%'>Nama</td><td width='2%'>:</td><td><b>{p['nama']}</b></td></tr><tr><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr>" for i,p in enumerate(daftar_pegawai)])

html_content += f'<div class="kertas">{spt_kop}<h3 class="text-center text-bold underline" style="margin-top:10px;">SURAT PERINTAH TUGAS</h3><p class="text-center" style="margin-top:-10px;">NOMOR : {no_spt}</p><table width="100%" style="font-size:11pt;"><tr><td width="15%">Dasar</td><td width="2%">:</td><td>DPA Bagian Perekonomian dan SDA TA 2026</td></tr></table><p class="text-center text-bold" style="margin:15px 0;">M E M E R I N T A H K A N</p><table width="100%" style="font-size:11pt;">{pegawai_rows}</table><table width="100%" style="font-size:11pt; margin-top:10px;"><tr><td width="15%">Untuk</td><td width="2%">:</td><td>{maksud_tugas} ke {tempat_tujuan}</td></tr></table>{ttd_html}</div>'

# 2. HALAMAN SPD
for p in daftar_pegawai:
    html_content += f"""<div class="kertas">{kop_html}
    <div style="margin-left:65%; font-size:9.5pt;">
        <table>
            <tr><td>Lembar Ke</td><td>: {p['lembar']}</td></tr>
            <tr><td>Kode No</td><td>: {kode_no}</td></tr>
            <tr><td>Nomor</td><td>: {p['spd']}</td></tr>
        </table>
    </div>
    <h3 class="text-center text-bold underline" style="margin:10px 0;">SURAT PERINTAH DINAS (SPD)</h3>
    <table class="tabel-spd">
        <tr><td width="5%">1.</td><td width="42%">Pejabat pemberi perintah</td><td colspan="3">BUPATI NGADA</td></tr>
        <tr><td>2.</td><td>Nama Pegawai diperintah</td><td colspan="3"><b>{p['nama']}</b></td></tr>
        <tr><td rowspan="3">3.</td><td>a. Pangkat/Golongan</td><td colspan="3">{p['gol']}</td></tr>
        <tr><td>b. Jabatan</td><td colspan="3">{p['jab']}</td></tr>
        <tr><td>c. Tingkat Peraturan</td><td colspan="3"></td></tr>
        <tr><td>4.</td><td>Maksud Perjalanan Dinas</td><td colspan="3">{maksud_tugas}</td></tr>
        <tr><td>5.</td><td>Alat angkut</td><td colspan="3">{alat_angkut}</td></tr>
        <tr><td rowspan="2">6.</td><td>a. Tempat Berangkat</td><td colspan="3">Bajawa</td></tr>
        <tr><td>b. Tempat Tujuan</td><td colspan="3">{tempat_tujuan}</td></tr>
        <tr><td rowspan="3">7.</td><td>Lamanya Perjalanan Dinas</td><td colspan="3">{lama_hari}</td></tr>
        <tr><td>a. Tanggal Berangkat</td><td colspan="3">{tgl_indo(datetime.now())}</td></tr>
        <tr><td>b. Tanggal Harus Kembali</td><td colspan="3">{tgl_indo(datetime.now())}</td></tr>
        <tr><td>8.</td><td>Pengikut: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Nama</td><td width="20%" class="text-center">Tgl Lahir</td><td colspan="2" class="text-center">Ket</td></tr>
        <tr><td></td><td>1.</td><td></td><td colspan="2"></td></tr>
        <tr><td rowspan="3">9.</td><td>Pembebanan Anggaran</td><td colspan="3"></td></tr>
        <tr><td>a. Instansi</td><td colspan="3">Bagian Perekonomian dan SDA</td></tr>
        <tr><td>b. Mata Anggaran</td><td colspan="3">{mata_anggaran}</td></tr>
        <tr><td>10.</td><td>Keterangan lain-lain</td><td colspan="3"></td></tr>
    </table>{ttd_html}</div>"""

html_content += "</body></html>"

# TAMPILKAN HASIL ISOLASI
st.components.v1.html(html_content, height=1200, scrolling=True)
