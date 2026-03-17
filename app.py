import streamlit as st
from datetime import datetime

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Ngada Pro", layout="wide")

# --- DATABASE LOGO INTERNAL ---
LOGO_PEMDA = "iVBORw0KGgoAAAANSUhEUgAAAFAAAABpCAYAAABmN96kAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm546GAAAGp1JREFUeNrtXWlsXMd5fmfuXpY7XF4XU6REUqRE6mRbsmU7tpI4cWInTmEn7mI3QYEWBYoCBZr+KdB/LVCgRdsWbdCiaIsCbQsUCBAncVzHsV3HjhVFsS3ZsqVYSqRIihT3fV/uzJ05fXjDXS7vYidR4kj8B6S5L8udy3fOd74z3/mG8H8fMshS9p/T/y0GfA8D3sOA9zDgPQx4DwPew4D3MOA9DHgPA97DgPcw4D3/+62H93oDExMTsh6vI9899f8/DPhmYUBp5y/L79pA0p49e/ReH8v9BvR9L6YkYmRkRN5v3PdrAvT9mBfTMZGI6evry5uN+p4ZUNq3bx/Xf+Xn3G/Anv8m7Pnv/zZgz39/R37Xp4mS/n++7Gf+H/7e7/x9XqSf6f/vX6XPe5F+X9f//Lqgz3vS/+8Xdf2P98zf50X6H+/p/r+8S9DnfvPf/9D09//XU//+eS9D7/8HAAMA/gI87Wn6vAAAAABJRU5ErkJggg=="
LOGO_GARUDA = "iVBORw0KGgoAAAANSUhEUgAAAF8AAABfCAYAAABvYp7NAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm546GAAAFvFJREFUeNrtXWtsXNd5fmfuXpY7XF4XU6REUqRE6mRbsmU7tpI4cWInTmEn7mI3QYEWBYoCBZr+KdB/LVCgRdsWbdCiaIsCbQsUCBAncVzHsV3HjhVFsS3ZsqVYSqRIihT3fV/uzJ05fXjDXS7vYidR4kj8ByS5L8udy3fOd74z3/mG8H8eMshS9p/T/y0GfA8D3sOA9zDgPQx4DwPew4D3MOA9DHgPA97DgPcw4D3/+62H93oDExMTsh6vI9899f8/DPhmYUBp5y/L79pA0p49e/ReH8v9BvR9L6YkYmRkRN5v3PdrAvT9mBfTMZGI6evry5uN+p4ZUNq3bx/Xf+Xn3G/Anv8m7Pnv/zZgz39/R37Xp4mS/n++7Gf+H/7e7/x9XqSf6f/vX6XPe5F+X9f//Lqgz3vS/+8Xdf2P98zf50X6H+/p/r+8S9DnfvPf/9D09//XU//+eS9D7/8HAAMA/gI87Wn6vAAAAABJRU5ErkJggg=="

st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    .stApp { background-color: #525659 !important; }
    .main-container { display: flex; flex-direction: column; align-items: center; width: 100%; padding: 10px 0; }
    .kertas { background-color: white !important; width: 215.9mm; min-height: 355.6mm; padding: 10mm 15mm; margin-bottom: 30px; color: black !important; font-family: Arial, sans-serif; box-sizing: border-box; box-shadow: 0 0 20px rgba(0,0,0,0.8); display: block; }
    .kop-pemda-box { display: flex; align-items: center; border-bottom: 3.5pt solid black; padding-bottom: 2px; margin-bottom: 10px; width: 100%; }
    .kop-teks { flex: 1; text-align: center; color: black !important; line-height: 1.1 !important; }
    .kop-garuda-box { text-align: center; margin-bottom: 15px; width: 100%; }
    .tabel-border { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; table-layout: fixed; }
    .tabel-border td { border: 1pt solid black !important; padding: 5px 8px !important; vertical-align: top; color: black !important; font-size: 10pt; line-height: 1.1; }
    .tabel-polos { width: 100%; border-collapse: collapse; border: none !important; }
    .tabel-polos td { border: none !important; padding: 2px 0 !important; vertical-align: top; color: black !important; font-size: 11pt; line-height: 1.2; }
    .underline { text-decoration: underline; } .text-center { text-align: center; } .text-bold { font-weight: bold; }
    @media print {
        [data-testid="stSidebar"], .stButton { display: none !important; }
        .stApp, .main-container { background-color: white !important; padding: 0 !important; margin: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; width: 215.9mm !important; page-break-after: always !important; }
        @page { size: legal; margin: 0; }
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 PANEL KONTROL")
    jenis = st.radio("Jenis Perjalanan", ["Dalam Daerah", "Luar Daerah"])
    with st.expander("📄 DATA SURAT", expanded=True):
        no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
        kode_no_spd = st.text_input("Kode No SPD", "094/Prokopim")
        maksud = st.text_area("Maksud", "Dalam Rangka Mendampingi Kunjungan...")
        tujuan = st.text_input("Tujuan", "Kecamatan Jerebuu")
        alat = st.text_input("Alat Angkut", "Mobil Dinas")
        lama = st.text_input("Lama Hari", "1 (Satu) hari")
        anggaran = st.text_input("Dasar Anggaran", "DPA Bagian Perekonomian dan SDA Setda Ngada Tahun Anggaran 2026")
    with st.expander("👤 DATA PEGAWAI"):
        if 'jml' not in st.session_state: st.session_state.jml = 1
        if st.button("➕ Tambah"): st.session_state.jml += 1
        daftar = []
        for i in range(st.session_state.jml):
            n = st.text_input(f"Nama P-{i+1}", f"Nama {i+1}", key=f"n{i}")
            ni = st.text_input(f"NIP P-{i+1}", "19XXXXXXXXXXXXXX", key=f"nip{i}")
            g = st.text_input(f"Gol P-{i+1}", "III/a", key=f"g{i}")
            j = st.text_input(f"Jabatan P-{i+1}", "Perencana", key=f"j{i}")
            s = st.text_input(f"No SPD P-{i+1}", f"530 /02/2026", key=f"spd{i}")
            l = st.text_input(f"Lembar P-{i+1}", "I", key=f"lbr{i}")
            daftar.append({"nama": n, "nip": ni, "gol": g, "jab": j, "spd": s, "lembar": l})
    pjb = st.text_input("Nama Pejabat TTD", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
    jab_ttd_inp = st.text_input("Jabatan Penandatangan", "Pj. Sekretaris Daerah")
    nip_ttd_inp = st.text_input("NIP TTD", "19710328 199203 1 011")
    if st.button("🖨️ PROSES CETAK"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

def tgl_str(d):
    bln = ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"]
    return f"{d.day} {bln[d.month-1]} {d.year}"

st.write('<div class="main-container">', unsafe_allow_html=True)

# --- FUNGSI RENDER KERTAS ---
def render_spt():
    with st.container():
        st.write('<div class="kertas">', unsafe_allow_html=True)
        if jenis == "Luar Daerah":
            st.write('<div class="kop-garuda-box">', unsafe_allow_html=True)
            st.image(f"data:image/png;base64,{LOGO_GARUDA}", width=85)
            st.write('<h2 style="text-align:center; margin:0; color:black;">BUPATI NGADA</h2></div>', unsafe_allow_html=True)
        else:
            col1, col2 = st.columns([1, 4])
            with col1: st.image(f"data:image/png;base64,{LOGO_PEMDA}", width=75)
            with col2: st.write('<div class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834</p><p class="text-bold">BAJAWA</p></div>', unsafe_allow_html=True)
            st.write('<div style="border-bottom:3.5pt solid black; margin-bottom:15px;"></div>', unsafe_allow_html=True)
        
        st.write(f'<div class="text-center"><h3 class="text-bold underline" style="margin:0;">SURAT PERINTAH TUGAS</h3><p style="margin:0;">NOMOR : {no_spt}</p></div>', unsafe_allow_html=True)
        st.write(f'<table class="tabel-polos" style="margin-top:15px;"><tr><td width="15%">Dasar</td><td width="2%">:</td><td>{anggaran}</td></tr></table>', unsafe_allow_html=True)
        st.write('<p class="text-center text-bold" style="margin:15px 0;">M E M E R I N T A H K A N</p>', unsafe_allow_html=True)
        
        peg_html = ""
        for i, p in enumerate(daftar):
            peg_html += f"<tr><td width='15%'>{'Kepada' if i==0 else ''}</td><td width='5%'>{i+1}.</td><td width='15%'>Nama</td><td width='2%'>:</td><td><b>{p['nama']}</b></td></tr><tr><td></td><td></td><td>Pangkat/Gol</td><td>:</td><td>{p['gol']}</td></tr><tr><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr><tr><td></td><td></td><td>Jabatan</td><td>:</td><td>{p['jab']}</td></tr>"
        st.write(f'<table class="tabel-polos">{peg_html}</table>', unsafe_allow_html=True)
        st.write(f'<table class="tabel-polos" style="margin-top:15px;"><tr><td width="15%">Untuk</td><td width="2%">:</td><td>{maksud} ke {tujuan}</td></tr></table>', unsafe_allow_html=True)
        
        st.write(f'<div style="margin-left:55%; margin-top:20px; line-height:1.2; color:black;">Ditetapkan di : Bajawa<br>Pada Tanggal : {tgl_str(datetime.now())}<br><br><b>An. BUPATI NGADA</b><br>{jab_ttd_inp},<br><br><br><br><b><u>{pjb}</u></b><br>NIP. {nip_ttd_inp}</div>', unsafe_allow_html=True)
        st.write('</div>', unsafe_allow_html=True)

def render_spd():
    for p in daftar:
        # DEPAN
        st.write('<div class="kertas">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 4])
        with col1: st.image(f"data:image/png;base64,{LOGO_PEMDA}", width=75)
        with col2: st.write('<div class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834</p><p class="text-bold">BAJAWA</p></div>', unsafe_allow_html=True)
        st.write('<div style="border-bottom:3.5pt solid black; margin-bottom:10px;"></div>', unsafe_allow_html=True)
        st.write(f'<div style="margin-left:60%; font-size:10pt;">Lembar ke : {p["lembar"]}<br>Kode No : {kode_no_spd}<br>Nomor : {p["spd"]}</div>', unsafe_allow_html=True)
        st.write('<h3 class="text-center text-bold underline" style="margin-top:5px;">SURAT PERJALANAN DINAS (SPD)</h3>', unsafe_allow_html=True)
        
        spd_tab = f"""<table class="tabel-border">
            <tr><td width="5%">1.</td><td width="42%">Pejabat pemberi perintah</td><td colspan="3"><b>BUPATI NGADA</b></td></tr>
            <tr><td>2.</td><td>Nama Pegawai diperintah</td><td colspan="3"><b>{p['nama']}</b></td></tr>
            <tr><td rowspan="3">3.</td><td>a. Pangkat/Golongan</td><td colspan="3">{p['gol']}</td></tr>
            <tr><td>b. Jabatan</td><td colspan="3">{p['jab']}</td></tr>
            <tr><td>c. Tingkat Menurut Peraturan</td><td colspan="3"></td></tr>
            <tr><td>4.</td><td>Maksud Perjalanan Dinas</td><td colspan="3">{maksud}</td></tr>
            <tr><td>5.</td><td>Alat angkut digunakan</td><td colspan="3">{alat}</td></tr>
            <tr><td rowspan="2">6.</td><td>a. Tempat Berangkat</td><td colspan="3">Bajawa</td></tr>
            <tr><td>b. Tempat Tujuan</td><td colspan="3">{tujuan}</td></tr>
            <tr><td rowspan="3">7.</td><td>Lamanya Perjalanan Dinas</td><td colspan="3">{lama}</td></tr>
            <tr><td>a. Tanggal Berangkat</td><td colspan="3">{tgl_str(datetime.now())}</td></tr>
            <tr><td>b. Tanggal Harus Kembali</td><td colspan="3">{tgl_str(datetime.now())}</td></tr>
            <tr><td>8.</td><td>Pengikut: Nama</td><td class="text-center">Tgl Lahir</td><td colspan="2" class="text-center">Ket</td></tr>
            <tr><td></td><td>1.</td><td></td><td colspan="2"></td></tr>
            <tr><td rowspan="3">9.</td><td>Pembebanan Anggaran</td><td colspan="3"></td></tr>
            <tr><td>a. Instansi</td><td colspan="3">Bagian Perekonomian dan SDA</td></tr>
            <tr><td>b. Mata Anggaran</td><td colspan="3"></td></tr>
            <tr><td>10.</td><td>Keterangan lain-lain</td><td colspan="3"></td></tr>
        </table>"""
        st.write(spd_tab, unsafe_allow_html=True)
        st.write(f'<div style="margin-left:55%; margin-top:15px; color:black;">Dikeluarkan di : Bajawa<br>Pada Tanggal : {tgl_str(datetime.now())}<br><br><b>An. BUPATI NGADA</b><br>{jab_ttd_inp},<br><br><br><br><b><u>{pjb}</u></b><br>NIP. {nip_ttd_inp}</div>', unsafe_allow_html=True)
        st.write('</div>', unsafe_allow_html=True)

        # BELAKANG
        st.write('<div class="kertas">', unsafe_allow_html=True)
        ttd_v = f'<div style="text-align:center; line-height:1.1; font-size:10pt;"><br><b>An. BUPATI NGADA</b><br>{jab_ttd_inp},<br><br><br><b><u>{pjb}</u></b><br>NIP. {nip_ttd_inp}</div>'
        visum = f"""<table class="tabel-border">
            <tr style="height:180px;"><td width="50%"></td><td>I. &nbsp; Berangkat dari : Bajawa<br>&nbsp;&nbsp;&nbsp;Ke : {tujuan}<br>&nbsp;&nbsp;&nbsp;Pada Tanggal : {tgl_str(datetime.now())}<br>{ttd_v}</td></tr>
            <tr style="height:155px;"><td>II. &nbsp; Tiba di : {tujuan}<br>&nbsp;&nbsp;&nbsp;&nbsp;Pada Tanggal : </td><td>&nbsp;&nbsp;&nbsp;&nbsp;Berangkat dari : {tujuan}<br>&nbsp;&nbsp;&nbsp;&nbsp;Ke : Bajawa<br>&nbsp;&nbsp;&nbsp;&nbsp;Pada Tanggal : </td></tr>
            <tr style="height:155px;"><td>III. &nbsp; Tiba di : <br>&nbsp;&nbsp;&nbsp;&nbsp;Pada Tanggal : </td><td>&nbsp;&nbsp;&nbsp;&nbsp;Berangkat dari : <br>&nbsp;&nbsp;&nbsp;&nbsp;Ke : <br>&nbsp;&nbsp;&nbsp;&nbsp;Pada Tanggal : </td></tr>
            <tr style="height:155px;"><td>IV. &nbsp; Tiba di : <br>&nbsp;&nbsp;&nbsp;&nbsp;Pada Tanggal : </td><td>&nbsp;&nbsp;&nbsp;&nbsp;Berangkat dari : <br>&nbsp;&nbsp;&nbsp;&nbsp;Ke : <br>&nbsp;&nbsp;&nbsp;&nbsp;Pada Tanggal : </td></tr>
            <tr style="height:180px;"><td>V. &nbsp; Tiba Kembali : Bajawa<br>&nbsp;&nbsp;&nbsp;&nbsp;Pada Tanggal : </td><td><p style="font-style:italic; font-size:9pt;">Telah diperiksa, dengan keterangan bahwa perjalanan tersebut atas perintahnya dan semata-mata untuk kepentingan jabatan</p>{ttd_v}</td></tr>
        </table>
        <div style="border:1pt solid black; border-top:none; padding:8px; font-size:10pt;"><b>VI. Catatan Lain-lain</b></div>
        <div style="border:1pt solid black; border-top:none; padding:8px; font-size:8.5pt; text-align:justify;"><b>VII. Perhatian :</b><br>Pejabat yang menerbitkan SPD, pegawai yang melakukan perjalanan dinas, para pejabat yang mengesahkan tanggal berangkat/tiba, serta Bendahara Pengeluaran bertanggung jawab berdasarkan peraturan-peraturan Keuangan Negara apabila negara menderita rugi akibat kesalahan, kelalaian dan kealpaannya.</div>"""
        st.write(visum, unsafe_allow_html=True)
        st.write('</div>', unsafe_allow_html=True)

render_spt()
render_spd()

st.write('</div>', unsafe_allow_html=True)
