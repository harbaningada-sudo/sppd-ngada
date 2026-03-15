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

# --- BAGIAN LOGO (TEMPEL KODE BASE64 DI SINI) ---
LOGO_PEMDA = """PASTE_KODE_BASE64_PEMDA_DI_SINI"""
LOGO_GARUDA = """PASTE_KODE_BASE64_GARUDA_DI_SINI"""

# 2. SIDEBAR INPUT
with st.sidebar:
    st.header("📋 INPUT DATA")
    jenis = st.radio("📍 Jenis Perjalanan", ["Dalam Daerah", "Luar Daerah"])
    
    with st.expander("📄 DATA SURAT", expanded=True):
        no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
        no_spd = st.text_input("Nomor SPD", "530 /02/2026")
        kode_no = st.text_input("Kode No", "094/Prokopim")
        maksud = st.text_area("Maksud Perjalanan", "Monitoring dan Pendataan...")
        tujuan = st.text_input("Tempat Tujuan", "Kecamatan Golewa")
        dasar_surat = st.text_area("Dasar (Khusus Luar Daerah)", "Surat Balai Besar...")

    with st.expander("👤 DATA PEGAWAI", expanded=True):
        if 'jml' not in st.session_state: st.session_state.jml = 1
        c1, c2 = st.columns(2)
        if c1.button("➕ Tambah"): st.session_state.jml += 1
        if c2.button("➖ Kurang") and st.session_state.jml > 1: st.session_state.jml -= 1
        
        daftar_pegawai = []
        for i in range(st.session_state.jml):
            st.markdown(f"**Pegawai {i+1}**")
            n = st.text_input(f"Nama P-{i+1}", f"Nama {i+1}", key=f"n{i}")
            nip = st.text_input(f"NIP P-{i+1}", "19XXXXXXXXXXXXXX", key=f"nip{i}")
            gol = st.text_input(f"Gol P-{i+1}", "III/a", key=f"g{i}")
            jab = st.text_input(f"Jabatan P-{i+1}", "Pelaksana", key=f"j{i}")
            daftar_pegawai.append({"nama": n, "nip": nip, "gol": gol, "jabatan": jab})

    with st.expander("🕒 TTD", expanded=False):
        tgl_p = st.date_input("Berangkat", datetime.now())
        tgl_k = st.date_input("Kembali", datetime.now())
        tgl_ctk = st.date_input("Tgl Cetak", datetime.now())
        jab_ttd = st.text_input("Jabatan TTD", "WAKIL BUPATI NGADA" if jenis == "Luar Daerah" else "Pj. Sekretaris Daerah")
        nama_ttd = st.text_input("Nama TTD", "BERNADINUS DHEY NGEBU, SP" if jenis == "Luar Daerah" else "Yohanes C. Watu Ngebu, S.Sos., M.Si")
        nip_ttd = st.text_input("NIP TTD", "19650101 198603 1 045" if jenis == "Luar Daerah" else "19710328 199203 1 011")

    if st.button("🖨️ CETAK SEMUA"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

# HELPER TANGGAL
def fmt(d):
    bln = ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"]
    return f"{d.day} {bln[d.month-1]} {d.year}"

# --- 3. GENERATE HTML ---
style = """<style>
    .wrap { display: flex; flex-direction: column; align-items: center; gap: 30px; background: #525659; padding: 20px; }
    .kertas { background: white; width: 210mm; min-height: 297mm; padding: 20mm; color: black; font-family: 'Times New Roman'; box-sizing: border-box; page-break-after: always; box-shadow: 0 0 10px rgba(0,0,0,0.5); }
    .kop-daerah { display: flex; align-items: center; border-bottom: 3px solid black; padding-bottom: 5px; margin-bottom: 15px; }
    .tabel-polos, .tabel-border { width: 100%; border-collapse: collapse; font-size: 11pt; }
    .tabel-border td, .tabel-border th { border: 1px solid black; padding: 8px; vertical-align: top; }
    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }
</style>"""

html_content = f'<div class="wrap">{style}'

# LOGIKA HEADER
header_spt = f'<div class="text-center"><img src="{LOGO_GARUDA}" width="75"><br><h3 style="margin:5px 0;">BUPATI NGADA</h3></div>' if jenis == "Luar Daerah" else \
             f'<div class="kop-daerah"><img src="{LOGO_PEMDA}" width="70"><div style="flex:1; text-align:center;"><h3 style="margin:0;">PEMERINTAH KABUPATEN NGADA</h3><h2 style="margin:0;">SEKRETARIAT DAERAH</h2><small>Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834 BAJAWA</small></div></div>'

header_spd = f'<div class="kop-daerah"><img src="{LOGO_PEMDA}" width="70"><div style="flex:1; text-align:center;"><h3 style="margin:0;">PEMERINTAH KABUPATEN NGADA</h3><h2 style="margin:0;">SEKRETARIAT DAERAH</h2><small>Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834 BAJAWA</small></div></div>'

dasar = dasar_surat if jenis == "Luar Daerah" else "DPA Bagian Perekonomian dan SDA Setda Ngada TA 2026"

# HALAMAN 1: SPT
rows = "".join([f"<tr><td width='5%'></td><td width='5%'>{i+1}.</td><td width='20%'>Nama/NIP</td><td width='2%'>:</td><td><b>{p['nama']}</b> / {p['nip']}</td></tr>" for i, p in enumerate(daftar_pegawai)])
html_content += f"""<div class="kertas">{header_spt}<h3 class="text-center underline">SURAT PERINTAH TUGAS</h3><p class="text-center" style="margin-top:-10px;">Nomor: {no_spt}</p>
<table class="tabel-polos"><tr><td width="15%">Dasar</td><td>: {dasar}</td></tr></table><p class="text-center text-bold" style="margin:15px 0;">MEMERINTAHKAN:</p>
<table class="tabel-polos"><tr><td width="15%">Kepada</td><td colspan="4"></td></tr>{rows}</table><br>
<table class="tabel-polos"><tr><td width="15%">Untuk</td><td>: {maksud} ke {tujuan}</td></tr></table>
<div style="margin-left:55%; margin-top:30px;">Ditetapkan di: Bajawa<br>Pada Tanggal: {fmt(tgl_ctk)}<br><b>An. BUPATI NGADA</b><br>{jab_ttd},<br><br><br><br><b>{nama_ttd}</b><br>NIP. {nip_ttd}</div></div>"""

# HALAMAN 2: SPD DEPAN (LOOPING)
for p in daftar_pegawai:
    html_content += f"""<div class="kertas">{header_spd}<div style="margin-left:60%; font-size:10pt;">Kode No: {kode_no}<br>Nomor: {no_spd}</div><h3 class="text-center underline">SURAT PERJALANAN DINAS (SPD)</h3>
    <table class="tabel-border">
    <tr><td>1</td><td>Pejabat Memberi Perintah</td><td>BUPATI NGADA</td></tr>
    <tr><td>2</td><td>Nama Pegawai diperintah</td><td><b>{p['nama']}</b></td></tr>
    <tr><td>3</td><td>Pangkat / Jabatan</td><td>{p['gol']} / {p['jabatan']}</td></tr>
    <tr><td>4</td><td>Maksud Perjalanan</td><td>{maksud}</td></tr>
    <tr><td>5</td><td>Alat Angkut</td><td>Kendaraan Dinas</td></tr>
    <tr><td>6</td><td>Tempat Berangkat / Tujuan</td><td>Bajawa / {tujuan}</td></tr>
    <tr><td>7</td><td>Tgl Berangkat / Kembali</td><td>{fmt(tgl_p)} / {fmt(tgl_k)}</td></tr>
    </table><div style="margin-left:55%; margin-top:20px;"><b>An. BUPATI NGADA</b><br>{jab_ttd},<br><br><br><b>{nama_ttd}</b></div></div>"""

# HALAMAN 3: SPD BELAKANG
html_content += f"""<div class="kertas" style="padding-top:30mm;"><table class="tabel-border" style="height:80%;">
<tr><td width="50%"></td><td>I. Berangkat dari: Bajawa<br>Ke: {tujuan}<br>Tgl: {fmt(tgl_p)}<br><br><b>{nama_ttd}</b></td></tr>
<tr><td>II. Tiba di: {tujuan}</td><td>Berangkat dari: {tujuan}<br>Ke: Bajawa</td></tr>
<tr><td>Tiba Kembali: Bajawa<br>Tgl: {fmt(tgl_k)}</td><td><br><b>{nama_ttd}</b></td></tr>
</table></div>"""

# HALAMAN 4: REGISTER
reg_rows = "".join([f"<tr><td>{i+1}</td><td>{p['nama']}</td><td>{no_spt}</td><td>{no_spd}</td><td>{fmt(tgl_p)}</td><td>{tujuan}</td><td></td></tr>" for i, p in enumerate(daftar_pegawai)])
html_content += f"""<div class="kertas" style="width:297mm; min-height:210mm;"><h3 class="text-center">REGISTER PERJALANAN DINAS</h3>
<table class="tabel-border"><thead><tr style="background:#eee;"><th>No</th><th>Nama</th><th>No SPT</th><th>No SPD</th><th>Tgl</th><th>Tujuan</th><th>Ket</th></tr></thead>
<tbody>{reg_rows}</tbody></table></div></div>"""

st.components.v1.html(html_content, height=1500, scrolling=True)
