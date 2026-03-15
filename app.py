import streamlit as st
from datetime import datetime

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Prokopim Ngada", layout="wide")

st.markdown("""
<style>
    /* Sembunyikan elemen bawaan Streamlit */
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    
    /* Latar belakang aplikasi abu-abu agar kertas putih terlihat kontras */
    .stApp { background-color: #525659 !important; }

    /* Container utama untuk memposisikan kertas di tengah */
    .main-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        padding: 20px 0;
    }

    /* FORMAT KERTAS A4 */
    .kertas { 
        background-color: white !important; 
        width: 210mm; 
        min-height: 297mm; 
        padding: 20mm; 
        margin-bottom: 30px;
        color: black !important; 
        font-family: Arial, Helvetica, sans-serif; 
        box-sizing: border-box; 
        box-shadow: 0 0 20px rgba(0,0,0,0.5);
        position: relative;
    }

    /* Teks Kop dan Tabel */
    .kop-daerah { display: flex; align-items: center; border-bottom: 3.5px solid black; padding-bottom: 5px; margin-bottom: 15px; }
    .kop-daerah img { width: 70px; height: auto; margin-right: 20px; }
    .kop-teks { flex: 1; text-align: center; color: black; }
    
    .tabel-border { 
        width: 100%; 
        border-collapse: collapse !important; 
        border: 1.5pt solid black !important; 
        table-layout: fixed; 
    }
    .tabel-border td { 
        border: 1.5pt solid black !important; 
        padding: 6px 10px !important; 
        vertical-align: top; 
        color: black !important;
        font-size: 10.5pt;
    }

    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }

    /* LOGIKA CETAK */
    @media print {
        [data-testid="stSidebar"], .stButton { display: none !important; }
        .stApp { background-color: white !important; }
        .main-container { padding: 0 !important; }
        .kertas { 
            box-shadow: none !important; 
            margin: 0 !important; 
            width: 100% !important; 
            page-break-after: always; 
        }
        @page { size: A4; margin: 0; }
    }
</style>
""", unsafe_allow_html=True)

# --- BAGIAN LOGO (Paste kode Base64 di sini) ---
LOGO_PEMDA = "PASTE_KODE_BASE64_PEMDA_DI_SINI"

# 2. PANEL INPUT SIDEBAR
with st.sidebar:
    st.header("📋 INPUT DATA")
    
    with st.expander("📄 DATA SURAT", expanded=True):
        no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
        kode_no = st.text_input("Kode No", "094/Prokopim")
        maksud = st.text_area("Maksud", "Dalam Rangka Monitoring dan Pendataan Pemilik Tambang Pasir...")
        tujuan = st.text_input("Tempat Tujuan", "Kecamatan Golewa")
        alat = st.text_input("Alat Angkut", "Mobil")
        lama = st.text_input("Lama Hari", "1 (Satu) hari")
        mata_anggaran = st.text_input("Mata Anggaran (9b)", "Bagian Perekonomian dan SDA")

    with st.expander("👤 DATA PEGAWAI", expanded=True):
        if 'jml' not in st.session_state: st.session_state.jml = 1
        c1, c2 = st.columns(2)
        if c1.button("➕ Tambah"): st.session_state.jml += 1
        if c2.button("➖ Kurang") and st.session_state.jml > 1: st.session_state.jml -= 1
        
        daftar = []
        for i in range(st.session_state.jml):
            st.markdown(f"**Pegawai {i+1}**")
            p_n = st.text_input(f"Nama P-{i+1}", f"Nama Pegawai {i+1}", key=f"n{i}")
            p_nip = st.text_input(f"NIP P-{i+1}", "19XXXXXXXXXXXXXX", key=f"nip{i}")
            p_gol = st.text_input(f"Gol P-{i+1}", "Penata Muda - III/a", key=f"g{i}")
            p_jab = st.text_input(f"Jabatan P-{i+1}", "Perencana Ahli Pertama", key=f"j{i}")
            p_spd = st.text_input(f"No SPD P-{i+1}", f"531 /02/2026", key=f"spd{i}")
            p_lbr = st.text_input(f"Lembar P-{i+1}", "I", key=f"lbr{i}")
            daftar.append({"nama": p_n, "nip": p_nip, "gol": p_gol, "jab": p_jab, "spd": p_spd, "lembar": p_lbr})

    with st.expander("🕒 TANDA TANGAN", expanded=False):
        tgl_ctk = st.date_input("Tanggal Cetak", datetime.now())
        ttd_nama = st.text_input("Nama Pejabat", "Dr. Nicolaus Noywuli, S.Pt, M.Si")
        ttd_nip = st.text_input("NIP Pejabat", "19720921 200012 1 004")

    if st.button("🖨️ CETAK SEKARANG"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

def tgl_str(d):
    bln = ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"]
    return f"{d.day} {bln[d.month-1]} {d.year}"

# --- RENDER KONTEN ---
html_output = '<div class="main-container">'

kop = f"""<div class="kop-daerah">
    <img src="data:image/png;base64,{LOGO_PEMDA}">
    <div class="kop-teks">
        <h3 style="margin:0; font-size:14pt;">PEMERINTAH KABUPATEN NGADA</h3>
        <h2 style="margin:0; font-size:16pt;">SEKRETARIAT DAERAH</h2>
        <p style="margin:0; font-size:9pt;">Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834</p>
        <p style="margin:0; font-size:11pt; font-weight:bold;">BAJAWA</p>
    </div></div>"""

ttd_box = f"""<div style="margin-left:55%; margin-top:30px; line-height:1.2; color:black;">Ditetapkan di : Bajawa<br>Pada Tanggal : {tgl_str(tgl_ctk)}<br><br><b>a.n. BUPATI NGADA</b><br><b>Sekretaris Daerah</b><br><b>u.b. Asisten Perekonomian dan Pembangunan,</b><br><br><br><br><b><u>{ttd_nama}</u></b><br>NIP. {ttd_nip}</div>"""

# SPD DEPAN LOOP
for p in daftar:
    html_output += f"""<div class="kertas">{kop}
    <div style="margin-left:65%; font-size:9pt; color:black;">
        <table>
            <tr><td>Lembar Ke</td><td>: {p['lembar']}</td></tr>
            <tr><td>Kode No</td><td>: {kode_no}</td></tr>
            <tr><td>Nomor</td><td>: {p['spd']}</td></tr>
        </table>
    </div>
    <h3 class="text-center text-bold underline" style="margin:10px 0; color:black;">SURAT PERINTAH DINAS (SPD)</h3>
    <table class="tabel-border">
        <tr><td width="5%">1.</td><td width="42%">Pejabat pemberi perintah</td><td colspan="3"><b>BUPATI NGADA</b></td></tr>
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
        <tr><td>8.</td><td>Pengikut: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Nama</td><td width="20%" class="text-center">Tgl Lahir</td><td colspan="2" class="text-center">Keterangan</td></tr>
        <tr><td></td><td>1.</td><td></td><td colspan="2"></td></tr>
        <tr><td></td><td>2.</td><td></td><td colspan="2"></td></tr>
        <tr><td rowspan="3">9.</td><td>Pembebanan Anggaran</td><td colspan="3"></td></tr>
        <tr><td>a. Instansi</td><td colspan="3">Bagian Perekonomian dan SDA</td></tr>
        <tr><td>b. Mata Anggaran</td><td colspan="3">{mata_anggaran}</td></tr>
        <tr><td>10.</td><td>Keterangan lain-lain</td><td colspan="3"></td></tr>
    </table>{ttd_box}</div>"""

html_output += '</div>'
st.components.v1.html(html_output, height=1200, scrolling=True)
