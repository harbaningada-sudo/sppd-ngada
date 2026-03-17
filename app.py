import streamlit as st
from datetime import datetime

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Prokopim Ngada", layout="wide")

st.markdown("""
<style>
    /* Dasar Aplikasi */
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    .stApp { background-color: #525659 !important; }

    .main-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        padding: 20px 0;
    }

    /* KERTAS A4 */
    .kertas { 
        background-color: white !important; 
        width: 210mm; 
        min-height: 297mm; 
        padding: 15mm 20mm; 
        margin-bottom: 30px;
        color: black !important; 
        font-family: Arial, sans-serif; 
        box-sizing: border-box; 
        box-shadow: 0 0 20px rgba(0,0,0,0.8);
        display: block;
    }

    /* TABEL SPD: Garis Hitam Tegas */
    .tabel-border { 
        width: 100%; 
        border-collapse: collapse !important; 
        border: 1.5pt solid black !important; 
        table-layout: fixed;
    }
    .tabel-border td { 
        border: 1.5pt solid black !important; 
        padding: 5px 8px !important; 
        vertical-align: top; 
        color: black !important;
        font-size: 10pt;
    }

    .kop { display: flex; align-items: center; border-bottom: 3.5pt solid black; padding-bottom: 5px; margin-bottom: 15px; }
    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }

    /* LOGIKA CETAK */
    @media print {
        [data-testid="stSidebar"], .stButton { display: none !important; }
        .stApp, .main-container { background-color: white !important; padding: 0 !important; margin: 0 !important; }
        .kertas { 
            box-shadow: none !important; 
            margin: 0 !important; 
            width: 210mm !important; 
            display: block !important;
            page-break-after: always !important;
        }
        table, td { border: 1.5pt solid black !important; -webkit-print-color-adjust: exact !important; }
        @page { size: A4; margin: 0; }
    }
</style>
""", unsafe_allow_html=True)

# --- BAGIAN LOGO ---
LOGO_PEMDA = "import streamlit as st
from datetime import datetime

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Prokopim Ngada", layout="wide")

st.markdown("""
<style>
    /* Dasar Aplikasi */
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    .stApp { background-color: #525659 !important; }

    .main-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        padding: 20px 0;
    }

    /* KERTAS A4 */
    .kertas { 
        background-color: white !important; 
        width: 210mm; 
        min-height: 297mm; 
        padding: 15mm 20mm; 
        margin-bottom: 30px;
        color: black !important; 
        font-family: Arial, sans-serif; 
        box-sizing: border-box; 
        box-shadow: 0 0 20px rgba(0,0,0,0.8);
        display: block;
    }

    /* TABEL SPD: Garis Hitam Tegas */
    .tabel-border { 
        width: 100%; 
        border-collapse: collapse !important; 
        border: 1.5pt solid black !important; 
        table-layout: fixed;
    }
    .tabel-border td { 
        border: 1.5pt solid black !important; 
        padding: 5px 8px !important; 
        vertical-align: top; 
        color: black !important;
        font-size: 10pt;
    }

    .kop { display: flex; align-items: center; border-bottom: 3.5pt solid black; padding-bottom: 5px; margin-bottom: 15px; }
    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }

    /* LOGIKA CETAK */
    @media print {
        [data-testid="stSidebar"], .stButton { display: none !important; }
        .stApp, .main-container { background-color: white !important; padding: 0 !important; margin: 0 !important; }
        .kertas { 
            box-shadow: none !important; 
            margin: 0 !important; 
            width: 210mm !important; 
            display: block !important;
            page-break-after: always !important;
        }
        table, td { border: 1.5pt solid black !important; -webkit-print-color-adjust: exact !important; }
        @page { size: A4; margin: 0; }
    }
</style>
""", unsafe_allow_html=True)

# --- BAGIAN LOGO ---
LOGO_PEMDA = "PASTE_KODE_BASE64_PEMDA_DI_SINI"
LOGO_GARUDA = "PASTE_KODE_BASE64_GARUDA_DI_SINI"

with st.sidebar:
    st.header("📋 INPUT DATA")
    jenis = st.radio("Jenis Perjalanan", ["Dalam Daerah", "Luar Daerah"])
    
    with st.expander("📄 DATA SURAT", expanded=True):
        no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
        kode_no = st.text_input("Kode No", "094/Prokopim")
        maksud = st.text_area("Maksud", "Monitoring dan Pendataan Pemilik Tambang Pasir...")
        tujuan = st.text_input("Tujuan", "Kecamatan Golewa")
        alat = st.text_input("Alat Angkut", "Mobil Dinas")
        lama = st.text_input("Lama Hari", "1 (Satu) hari")
        anggaran = st.text_input("Mata Anggaran", "Bagian Perekonomian dan SDA")

    with st.expander("👤 PEGAWAI"):
        if 'jml' not in st.session_state: st.session_state.jml = 1
        c1, c2 = st.columns(2)
        if c1.button("➕"): st.session_state.jml += 1
        if c2.button("➖") and st.session_state.jml > 1: st.session_state.jml -= 1
        daftar = []
        for i in range(st.session_state.jml):
            st.markdown(f"**Pegawai {i+1}**")
            n = st.text_input(f"Nama P-{i+1}", f"Nama {i+1}", key=f"n{i}")
            ni = st.text_input(f"NIP P-{i+1}", "19XXXXXXXXXXXXXX", key=f"nip{i}")
            g = st.text_input(f"Gol P-{i+1}", "III/a", key=f"g{i}")
            j = st.text_input(f"Jabatan P-{i+1}", "Perencana", key=f"j{i}")
            s = st.text_input(f"No SPD P-{i+1}", f"531 /02/2026", key=f"spd{i}")
            l = st.text_input(f"Lembar P-{i+1}", "I", key=f"lbr{i}")
            daftar.append({"nama": n, "nip": ni, "gol": g, "jab": j, "spd": s, "lembar": l})

    with st.expander("🕒 TTD"):
        tgl_c = st.date_input("Tanggal Cetak", datetime.now())
        pjb = st.text_input("Pejabat", "Dr. Nicolaus Noywuli, S.Pt, M.Si")
        nip_p = st.text_input("NIP", "19720921 200012 1 004")

    if st.button("🖨️ CETAK SEKARANG"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

def tgl_str(d):
    bln = ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"]
    return f"{d.day} {bln[d.month-1]} {d.year}"

# --- RENDER ---
html_out = '<div class="main-container">'

kop_s = f'<div class="kop"><img src="data:image/png;base64,{LOGO_PEMDA}" style="width:70px; margin-right:20px;"><div style="flex:1; text-align:center; color:black;"><h3 style="margin:0;">PEMERINTAH KABUPATEN NGADA</h3><h2 style="margin:0;">SEKRETARIAT DAERAH</h2><p style="margin:0; font-size:9pt;">Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834</p><p style="margin:0; font-size:10pt; font-weight:bold;">BAJAWA</p></div></div>'
kop_b = f'<div style="text-align:center; margin-bottom:10px;"><img src="data:image/png;base64,{LOGO_GARUDA}" style="width:85px;"><h2 style="margin:5px 0; color:black;">BUPATI NGADA</h2></div>'
ttd_box = f'<div style="margin-left:55%; margin-top:30px; line-height:1.2; color:black;">Ditetapkan di : Bajawa<br>Pada Tanggal : {tgl_str(tgl_c)}<br><br><b>a.n. BUPATI NGADA</b><br><b>Sekretaris Daerah</b><br><b>u.b. Asisten Perekonomian dan Pembangunan,</b><br><br><br><br><b><u>{pjb}</u></b><br>NIP. {nip_p}</div>'

# 1. SPT
s_kop = kop_b if jenis == "Luar Daerah" else kop_s
rows_spt = "".join([f"<tr><td width='15%'>{'Kepada' if i==0 else ''}</td><td width='5%'>{i+1}.</td><td width='15%'>Nama</td><td width='2%'>:</td><td><b>{p['nama']}</b></td></tr><tr><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr>" for i,p in enumerate(daftar)])
html_out += f'<div class="kertas">{s_kop}<h3 class="text-center text-bold underline" style="color:black; margin-top:10px;">SURAT PERINTAH TUGAS</h3><p class="text-center" style="margin-top:-10px; color:black;">NOMOR : {no_spt}</p><table width="100%" style="font-size:11pt; color:black;"><tr><td width="15%">Dasar</td><td width="2%">:</td><td>DPA Bagian Perekonomian dan SDA TA 2026</td></tr></table><p class="text-center text-bold" style="margin:15px 0; color:black;">M E M E R I N T A H K A N</p><table width="100%" style="font-size:11pt; color:black;">{rows_spt}</table><table width="100%" style="font-size:11pt; margin-top:10px; color:black;"><tr><td width="15%">Untuk</td><td width="2%">:</td><td>{maksud} ke {tujuan}</td></tr></table>{ttd_box}</div>'

# 2. SPD DEPAN & BELAKANG
for p in daftar:
    # --- SPD DEPAN ---
    html_out += f"""<div class="kertas">{kop_s}
    <div style="margin-left:65%; font-size:9.5pt; color:black;"><table><tr><td>Lembar Ke</td><td>: {p['lembar']}</td></tr><tr><td>Kode No</td><td>: {kode_no}</td></tr><tr><td>Nomor</td><td>: {p['spd']}</td></tr></table></div>
    <h3 class="text-center text-bold underline" style="margin:10px 0; color:black;">SURAT PERINTAH DINAS (SPD)</h3>
    <table class="tabel-border">
        <tr><td width="5%">1.</td><td width="42%">Pejabat pemberi perintah</td><td colspan="3">BUPATI NGADA</td></tr>
        <tr><td>2.</td><td>Nama Pegawai diperintah</td><td colspan="3"><b>{p['nama']}</b></td></tr>
        <tr><td rowspan="3">3.</td><td>a. Pangkat/Golongan</td><td colspan="3">{p['gol']}</td></tr>
        <tr><td>b. Jabatan</td><td colspan="3">{p['jab']}</td></tr>
        <tr><td>c. Tingkat Peraturan</td><td colspan="3"></td></tr>
        <tr><td>4.</td><td>Maksud Perjalanan Dinas</td><td colspan="3">{maksud}</td></tr>
        <tr><td>5.</td><td>Alat angkut</td><td colspan="3">{alat}</td></tr>
        <tr><td rowspan="2">6.</td><td>a. Tempat Berangkat</td><td colspan="3">Bajawa</td></tr>
        <tr><td>b. Tempat Tujuan</td><td colspan="3">{tujuan}</td></tr>
        <tr><td rowspan="3">7.</td><td>Lamanya Perjalanan Dinas</td><td colspan="3">{lama}</td></tr>
        <tr><td>a. Tanggal Berangkat</td><td colspan="3">{tgl_str(datetime.now())}</td></tr>
        <tr><td>b. Tanggal Harus Kembali</td><td colspan="3">{tgl_str(datetime.now())}</td></tr>
        <tr><td>8.</td><td>Pengikut: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Nama</td><td width="20%" class="text-center text-bold">Tgl Lahir</td><td colspan="2" class="text-center text-bold">Ket</td></tr>
        <tr><td></td><td>1.</td><td></td><td colspan="2"></td></tr>
        <tr><td rowspan="3">9.</td><td>Pembebanan Anggaran</td><td colspan="3"></td></tr>
        <tr><td>a. Instansi</td><td colspan="3">Bagian Perekonomian dan SDA</td></tr>
        <tr><td>b. Mata Anggaran</td><td colspan="3">{anggaran}</td></tr>
        <tr><td>10.</td><td>Keterangan lain-lain</td><td colspan="3"></td></tr>
    </table>{ttd_box}</div>"""

    # --- SPD BELAKANG (VISUM) ---
    ttd_v = f"""<div style="text-align:center; line-height:1.2; font-size:9pt; color:black;"><br><b>a.n. BUPATI NGADA</b><br><b>Sekretaris Daerah</b><br><br><br><br><b><u>{pjb}</u></b><br>NIP. {nip_p}</div>"""
    html_out += f"""<div class="kertas">
    <table class="tabel-border">
        <tr style="height: 180px;"><td width="50%"></td><td>I. Berangkat dari : Bajawa<br>Ke : {tujuan}<br>Tgl : {tgl_str(datetime.now())}<br>{ttd_v}</td></tr>
        <tr style="height: 160px;"><td>II. Tiba di : {tujuan}<br>Tgl : {tgl_str(datetime.now())}</td><td>Berangkat dari : {tujuan}<br>Ke : Bajawa<br>Tgl : {tgl_str(datetime.now())}</td></tr>
        <tr style="height: 200px;"><td>V. Tiba Kembali : Bajawa<br>Tgl : {tgl_str(datetime.now())}</td><td><p style="font-style:italic; font-size:8pt;">Telah diperiksa dengan keterangan bahwa perjalanan tersebut di atas benar dilakukan atas perintahnya...</p>{ttd_v}</td></tr>
    </table>
    <div style="border:1.5pt solid black; border-top:none; padding:10px; font-size:8.5pt; color:black; text-align:justify;">
        <b>VI. Catatan Lain-lain</b><br><b>VII. Perhatian:</b> Pejabat yang menerbitkan SPD dan pegawai yang melakukan perjalanan dinas bertanggung jawab atas kerugian negara akibat kesalahan atau kelalaiannya.
    </div></div>"""

html_out += '</div>'
st.markdown(html_out, unsafe_allow_html=True)"
LOGO_GARUDA = "PASTE_KODE_BASE64_GARUDA_DI_SINI"

with st.sidebar:
    st.header("📋 INPUT DATA")
    jenis = st.radio("Jenis Perjalanan", ["Dalam Daerah", "Luar Daerah"])
    
    with st.expander("📄 DATA SURAT", expanded=True):
        no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
        kode_no = st.text_input("Kode No", "094/Prokopim")
        maksud = st.text_area("Maksud", "Monitoring dan Pendataan Pemilik Tambang Pasir...")
        tujuan = st.text_input("Tujuan", "Kecamatan Golewa")
        alat = st.text_input("Alat Angkut", "Mobil Dinas")
        lama = st.text_input("Lama Hari", "1 (Satu) hari")
        anggaran = st.text_input("Mata Anggaran", "Bagian Perekonomian dan SDA")

    with st.expander("👤 PEGAWAI"):
        if 'jml' not in st.session_state: st.session_state.jml = 1
        c1, c2 = st.columns(2)
        if c1.button("➕"): st.session_state.jml += 1
        if c2.button("➖") and st.session_state.jml > 1: st.session_state.jml -= 1
        daftar = []
        for i in range(st.session_state.jml):
            st.markdown(f"**Pegawai {i+1}**")
            n = st.text_input(f"Nama P-{i+1}", f"Nama {i+1}", key=f"n{i}")
            ni = st.text_input(f"NIP P-{i+1}", "19XXXXXXXXXXXXXX", key=f"nip{i}")
            g = st.text_input(f"Gol P-{i+1}", "III/a", key=f"g{i}")
            j = st.text_input(f"Jabatan P-{i+1}", "Perencana", key=f"j{i}")
            s = st.text_input(f"No SPD P-{i+1}", f"531 /02/2026", key=f"spd{i}")
            l = st.text_input(f"Lembar P-{i+1}", "I", key=f"lbr{i}")
            daftar.append({"nama": n, "nip": ni, "gol": g, "jab": j, "spd": s, "lembar": l})

    with st.expander("🕒 TTD"):
        tgl_c = st.date_input("Tanggal Cetak", datetime.now())
        pjb = st.text_input("Pejabat", "Dr. Nicolaus Noywuli, S.Pt, M.Si")
        nip_p = st.text_input("NIP", "19720921 200012 1 004")

    if st.button("🖨️ CETAK SEKARANG"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

def tgl_str(d):
    bln = ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"]
    return f"{d.day} {bln[d.month-1]} {d.year}"

# --- RENDER ---
html_out = '<div class="main-container">'

kop_s = f'<div class="kop"><img src="data:image/png;base64,{LOGO_PEMDA}" style="width:70px; margin-right:20px;"><div style="flex:1; text-align:center; color:black;"><h3 style="margin:0;">PEMERINTAH KABUPATEN NGADA</h3><h2 style="margin:0;">SEKRETARIAT DAERAH</h2><p style="margin:0; font-size:9pt;">Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834</p><p style="margin:0; font-size:10pt; font-weight:bold;">BAJAWA</p></div></div>'
kop_b = f'<div style="text-align:center; margin-bottom:10px;"><img src="data:image/png;base64,{LOGO_GARUDA}" style="width:85px;"><h2 style="margin:5px 0; color:black;">BUPATI NGADA</h2></div>'
ttd_box = f'<div style="margin-left:55%; margin-top:30px; line-height:1.2; color:black;">Ditetapkan di : Bajawa<br>Pada Tanggal : {tgl_str(tgl_c)}<br><br><b>a.n. BUPATI NGADA</b><br><b>Sekretaris Daerah</b><br><b>u.b. Asisten Perekonomian dan Pembangunan,</b><br><br><br><br><b><u>{pjb}</u></b><br>NIP. {nip_p}</div>'

# 1. SPT
s_kop = kop_b if jenis == "Luar Daerah" else kop_s
rows_spt = "".join([f"<tr><td width='15%'>{'Kepada' if i==0 else ''}</td><td width='5%'>{i+1}.</td><td width='15%'>Nama</td><td width='2%'>:</td><td><b>{p['nama']}</b></td></tr><tr><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr>" for i,p in enumerate(daftar)])
html_out += f'<div class="kertas">{s_kop}<h3 class="text-center text-bold underline" style="color:black; margin-top:10px;">SURAT PERINTAH TUGAS</h3><p class="text-center" style="margin-top:-10px; color:black;">NOMOR : {no_spt}</p><table width="100%" style="font-size:11pt; color:black;"><tr><td width="15%">Dasar</td><td width="2%">:</td><td>DPA Bagian Perekonomian dan SDA TA 2026</td></tr></table><p class="text-center text-bold" style="margin:15px 0; color:black;">M E M E R I N T A H K A N</p><table width="100%" style="font-size:11pt; color:black;">{rows_spt}</table><table width="100%" style="font-size:11pt; margin-top:10px; color:black;"><tr><td width="15%">Untuk</td><td width="2%">:</td><td>{maksud} ke {tujuan}</td></tr></table>{ttd_box}</div>'

# 2. SPD DEPAN & BELAKANG
for p in daftar:
    # --- SPD DEPAN ---
    html_out += f"""<div class="kertas">{kop_s}
    <div style="margin-left:65%; font-size:9.5pt; color:black;"><table><tr><td>Lembar Ke</td><td>: {p['lembar']}</td></tr><tr><td>Kode No</td><td>: {kode_no}</td></tr><tr><td>Nomor</td><td>: {p['spd']}</td></tr></table></div>
    <h3 class="text-center text-bold underline" style="margin:10px 0; color:black;">SURAT PERINTAH DINAS (SPD)</h3>
    <table class="tabel-border">
        <tr><td width="5%">1.</td><td width="42%">Pejabat pemberi perintah</td><td colspan="3">BUPATI NGADA</td></tr>
        <tr><td>2.</td><td>Nama Pegawai diperintah</td><td colspan="3"><b>{p['nama']}</b></td></tr>
        <tr><td rowspan="3">3.</td><td>a. Pangkat/Golongan</td><td colspan="3">{p['gol']}</td></tr>
        <tr><td>b. Jabatan</td><td colspan="3">{p['jab']}</td></tr>
        <tr><td>c. Tingkat Peraturan</td><td colspan="3"></td></tr>
        <tr><td>4.</td><td>Maksud Perjalanan Dinas</td><td colspan="3">{maksud}</td></tr>
        <tr><td>5.</td><td>Alat angkut</td><td colspan="3">{alat}</td></tr>
        <tr><td rowspan="2">6.</td><td>a. Tempat Berangkat</td><td colspan="3">Bajawa</td></tr>
        <tr><td>b. Tempat Tujuan</td><td colspan="3">{tujuan}</td></tr>
        <tr><td rowspan="3">7.</td><td>Lamanya Perjalanan Dinas</td><td colspan="3">{lama}</td></tr>
        <tr><td>a. Tanggal Berangkat</td><td colspan="3">{tgl_str(datetime.now())}</td></tr>
        <tr><td>b. Tanggal Harus Kembali</td><td colspan="3">{tgl_str(datetime.now())}</td></tr>
        <tr><td>8.</td><td>Pengikut: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Nama</td><td width="20%" class="text-center text-bold">Tgl Lahir</td><td colspan="2" class="text-center text-bold">Ket</td></tr>
        <tr><td></td><td>1.</td><td></td><td colspan="2"></td></tr>
        <tr><td rowspan="3">9.</td><td>Pembebanan Anggaran</td><td colspan="3"></td></tr>
        <tr><td>a. Instansi</td><td colspan="3">Bagian Perekonomian dan SDA</td></tr>
        <tr><td>b. Mata Anggaran</td><td colspan="3">{anggaran}</td></tr>
        <tr><td>10.</td><td>Keterangan lain-lain</td><td colspan="3"></td></tr>
    </table>{ttd_box}</div>"""

    # --- SPD BELAKANG (VISUM) ---
    ttd_v = f"""<div style="text-align:center; line-height:1.2; font-size:9pt; color:black;"><br><b>a.n. BUPATI NGADA</b><br><b>Sekretaris Daerah</b><br><br><br><br><b><u>{pjb}</u></b><br>NIP. {nip_p}</div>"""
    html_out += f"""<div class="kertas">
    <table class="tabel-border">
        <tr style="height: 180px;"><td width="50%"></td><td>I. Berangkat dari : Bajawa<br>Ke : {tujuan}<br>Tgl : {tgl_str(datetime.now())}<br>{ttd_v}</td></tr>
        <tr style="height: 160px;"><td>II. Tiba di : {tujuan}<br>Tgl : {tgl_str(datetime.now())}</td><td>Berangkat dari : {tujuan}<br>Ke : Bajawa<br>Tgl : {tgl_str(datetime.now())}</td></tr>
        <tr style="height: 200px;"><td>V. Tiba Kembali : Bajawa<br>Tgl : {tgl_str(datetime.now())}</td><td><p style="font-style:italic; font-size:8pt;">Telah diperiksa dengan keterangan bahwa perjalanan tersebut di atas benar dilakukan atas perintahnya...</p>{ttd_v}</td></tr>
    </table>
    <div style="border:1.5pt solid black; border-top:none; padding:10px; font-size:8.5pt; color:black; text-align:justify;">
        <b>VI. Catatan Lain-lain</b><br><b>VII. Perhatian:</b> Pejabat yang menerbitkan SPD dan pegawai yang melakukan perjalanan dinas bertanggung jawab atas kerugian negara akibat kesalahan atau kelalaiannya.
    </div></div>"""

html_out += '</div>'
st.markdown(html_out, unsafe_allow_html=True)
