import streamlit as st
from datetime import datetime

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="SPD Ngada Fix", layout="wide")

st.markdown("""
<style>
    /* Dasar Aplikasi di Layar */
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

    /* Tabel SPD */
    .tabel-border { 
        width: 100%; 
        border-collapse: collapse !important; 
        border: 1.5pt solid black !important; 
    }
    .tabel-border td { 
        border: 1.5pt solid black !important; 
        padding: 6px 10px !important; 
        vertical-align: top; 
        color: black !important;
        font-size: 10.5pt;
    }

    .kop { display: flex; align-items: center; border-bottom: 3.5pt solid black; padding-bottom: 5px; margin-bottom: 15px; }
    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }

    /* LOGIKA CETAK: Paksa Muncul */
    @media print {
        [data-testid="stSidebar"], .stButton, .no-print { display: none !important; }
        .stApp, .main-container { background-color: white !important; padding: 0 !important; margin: 0 !important; }
        .kertas { 
            box-shadow: none !important; 
            margin: 0 !important; 
            width: 210mm !important; 
            display: block !important; /* KUNCI: Paksa tampil */
            visibility: visible !important;
            page-break-after: always !important;
        }
        table, td { border: 1.5pt solid black !important; -webkit-print-color-adjust: exact !important; }
        @page { size: A4; margin: 0; }
    }
</style>
""", unsafe_allow_html=True)

# --- LOGO (PASTE DISINI) ---
LOGO_PEMDA = "PASTE_KODE_BASE64_PEMDA_DI_SINI"
LOGO_GARUDA = "PASTE_KODE_BASE64_GARUDA_DI_SINI"

with st.sidebar:
    st.header("📋 INPUT DATA")
    jenis = st.radio("Jenis Perjalanan", ["Dalam Daerah", "Luar Daerah"])
    
    with st.expander("📄 DATA SURAT", expanded=True):
        no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
        kode_no = st.text_input("Kode No", "094/Prokopim")
        maksud = st.text_area("Maksud", "Monitoring dan Pendataan...")
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
            p_n = st.text_input(f"Nama P-{i+1}", f"Nama {i+1}", key=f"n{i}")
            p_nip = st.text_input(f"NIP P-{i+1}", "19XXXXXXXXXXXXXX", key=f"nip{i}")
            p_spd = st.text_input(f"No SPD P-{i+1}", f"531 /02/2026", key=f"spd{i}")
            daftar.append({"nama": p_n, "nip": p_nip, "spd": p_spd})

    pjb = st.text_input("Pejabat TTD", "Dr. Nicolaus Noywuli, S.Pt, M.Si")
    
    if st.button("🖨️ CETAK SEKARANG"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

# --- RENDER PROSES ---
def tgl(): return f"{datetime.now().day} Maret 2026"

html_out = '<div class="main-container">'
kop_s = f'<div class="kop"><img src="data:image/png;base64,{LOGO_PEMDA}" style="width:70px; margin-right:20px;"><div style="flex:1; text-align:center; color:black;"><h3 style="margin:0;">PEMERINTAH KABUPATEN NGADA</h3><h2 style="margin:0;">SEKRETARIAT DAERAH</h2><p style="margin:0; font-size:9pt;">BAJAWA</p></div></div>'
ttd_box = f'<div style="margin-left:55%; margin-top:30px; line-height:1.2; color:black;">Ditetapkan di : Bajawa<br>Tanggal : {tgl()}<br><br><b>Sekretaris Daerah</b><br><br><br><br><b><u>{pjb}</u></b></div>'

# 1. SPT
html_out += f'<div class="kertas">{kop_s}<h3 class="text-center underline" style="color:black;">SURAT PERINTAH TUGAS</h3>'
html_out += '<table width="100%" style="font-size:11pt; color:black;">' + "".join([f"<tr><td width='20%'>Kepada {i+1}</td><td>: <b>{p['nama']}</b> (NIP. {p['nip']})</td></tr>" for i,p in enumerate(daftar)]) + f'</table><p style="color:black;">Untuk: Monitoring ke {tujuan}</p>{ttd_box}</div>'

# 2. SPD
for p in daftar:
    html_out += f"""<div class="kertas">{kop_s}
    <div style="margin-left:65%; font-size:9pt; color:black;"><table><tr><td>Nomor SPD</td><td>: {p['spd']}</td></tr></table></div>
    <h3 class="text-center underline" style="color:black;">SURAT PERINTAH DINAS (SPD)</h3>
    <table class="tabel-border">
        <tr><td width="40%">1. Pejabat Pemberi Perintah</td><td>BUPATI NGADA</td></tr>
        <tr><td>2. Nama Pegawai</td><td><b>{p['nama']}</b></td></tr>
        <tr><td>3. Maksud Perjalanan</td><td>{maksud}</td></tr>
        <tr><td>4. Tujuan</td><td>{tujuan}</td></tr>
        <tr><td>5. Alat Angkut</td><td>{alat}</td></tr>
        <tr><td>6. Lama Perjalanan</td><td>{lama}</td></tr>
        <tr><td>7. Anggaran</td><td>{anggaran}</td></tr>
    </table>{ttd_box}</div>"""

html_out += '</div>'

# Gunakan st.markdown untuk menampilkan hasil akhir
st.markdown(html_out, unsafe_allow_html=True)
