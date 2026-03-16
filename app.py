import streamlit as st
from datetime import datetime

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Prokopim Ngada", layout="wide")

st.markdown("""
<style>
    /* Sembunyikan elemen bawaan Streamlit agar tidak ikut tercetak */
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    .stApp { background-color: #525659 !important; }

    /* Pengaturan Layar (Preview) */
    .main-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        padding: 20px 0;
    }

    /* KERTAS A4: Presisi Milimeter */
    .kertas { 
        background-color: white !important; 
        width: 210mm; 
        min-height: 297mm; 
        padding: 15mm 20mm; 
        margin-bottom: 30px;
        color: black !important; 
        font-family: Arial, Helvetica, sans-serif; 
        box-sizing: border-box; 
        box-shadow: 0 0 20px rgba(0,0,0,0.8);
        display: block;
        page-break-after: always;
    }

    /* KOP SURAT: Garis Tebal Sesuai Aturan */
    .kop-daerah { display: flex; align-items: center; border-bottom: 3.5pt solid black; padding-bottom: 5px; margin-bottom: 15px; }
    .kop-daerah img { width: 75px; height: auto; margin-right: 20px; }
    .kop-teks { flex: 1; text-align: center; color: black !important; line-height: 1.2; }
    
    /* TABEL: Kunci Lebar Kolom agar Garis Vertikal Lurus */
    .tabel-border { 
        width: 100%; 
        border-collapse: collapse !important; 
        border: 1.5pt solid black !important; 
        table-layout: fixed; /* MENGUNCI LEBAR KOLOM */
    }
    .tabel-border td { 
        border: 1.5pt solid black !important; 
        padding: 5px 8px !important; 
        vertical-align: top; 
        color: black !important;
        font-size: 10.5pt;
        line-height: 1.3;
    }

    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }

    /* --- LOGIKA CETAK (FORCING LAYOUT) --- */
    @media print {
        [data-testid="stSidebar"], .stButton, header, footer, .no-print { 
            display: none !important; 
        }
        .stApp, .main-container { 
            background-color: white !important; 
            padding: 0 !important; 
            margin: 0 !important; 
        }
        .kertas { 
            box-shadow: none !important; 
            margin: 0 !important; 
            width: 210mm !important; 
            padding: 10mm 15mm !important;
        }
        /* Memaksa garis tabel muncul pekat di kertas */
        table, td { 
            border: 1.5pt solid black !important; 
            -webkit-print-color-adjust: exact !important; 
            print-color-adjust: exact !important;
        }
        @page { size: A4; margin: 0; }
    }
</style>
""", unsafe_allow_html=True)

# --- BAGIAN LOGO (Paste Kode Base64) ---
LOGO_PEMDA = "PASTE_KODE_BASE64_PEMDA_DI_SINI"
LOGO_GARUDA = "PASTE_KODE_BASE64_GARUDA_DI_SINI"

with st.sidebar:
    st.header("📋 INPUT DATA")
    jenis = st.radio("📍 Jenis Perjalanan", ["Dalam Daerah", "Luar Daerah"])
    
    with st.expander("📄 DATA SURAT", expanded=True):
        no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
        kode_no = st.text_input("Kode No", "094/Prokopim")
        maksud = st.text_area("Maksud", "Monitoring dan Pendataan Pemilik Tambang Pasir...")
        tujuan = st.text_input("Tujuan", "Kecamatan Golewa")
        alat = st.text_input("Alat Angkut", "Mobil / Kendaraan Dinas")
        lama = st.text_input("Lama Hari", "1 (Satu) hari")
        anggaran = st.text_input("Mata Anggaran (9b)", "Bagian Perekonomian dan SDA")

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
            p_gol = st.text_input(f"Gol P-{i+1}", "III/a", key=f"g{i}")
            p_jab = st.text_input(f"Jabatan P-{i+1}", "Perencana", key=f"j{i}")
            p_spd = st.text_input(f"No SPD P-{i+1}", f"531 /02/2026", key=f"spd{i}")
            p_lbr = st.text_input(f"Lembar P-{i+1}", "I", key=f"lbr{i}")
            daftar.append({"nama": p_n, "nip": p_nip, "gol": p_gol, "jab": p_jab, "spd": p_spd, "lembar": p_lbr})

    with st.expander("🕒 TTD"):
        tgl_ctk = st.date_input("Tanggal Cetak", datetime.now())
        pejabat = st.text_input("Pejabat TTD", "Dr. Nicolaus Noywuli, S.Pt, M.Si")
        nip_pjb = st.text_input("NIP TTD", "19720921 200012 1 004")

    if st.button("🖨️ CETAK SEKARANG"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

def tgl_str(d):
    bln = ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"]
    return f"{d.day} {bln[d.month-1]} {d.year}"

# --- RENDER PROSES ---
html_output = '<div class="main-container">'

kop_sekda = f"""<div class="kop-daerah">
    <img src="data:image/png;base64,{LOGO_PEMDA}">
    <div class="kop-teks">
        <h3 style="margin:0; font-size:14pt;">PEMERINTAH KABUPATEN NGADA</h3>
        <h2 style="margin:0; font-size:16pt;">SEKRETARIAT DAERAH</h2>
        <p style="margin:0; font-size:9pt;">Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834</p>
        <p style="margin:0; font-size:11pt; font-weight:bold;">BAJAWA</p>
    </div></div>"""

kop_bupati = f"""<div style="text-align:center; margin-bottom:10px;">
    <img src="data:image/png;base64,{LOGO_GARUDA}" style="width:85px;">
    <h2 style="margin:5px 0; color:black;">BUPATI NGADA</h2>
</div>"""

ttd_box = f"""<div style="margin-left:55%; margin-top:30px; line-height:1.2; color:black;">
    Ditetapkan di : Bajawa<br>Pada Tanggal : {tgl_str(tgl_ctk)}<br><br>
    <b>a.n. BUPATI NGADA</b><br><b>Sekretaris Daerah</b><br><b>u.b. Asisten Perekonomian dan Pembangunan,</b><br><br><br><br>
    <b><u>{pejabat}</u></b><br>NIP. {nip_pjb}
</div>"""

# 1. HALAMAN SPT
s_kop = kop_bupati if jenis == "Luar Daerah" else kop_sekda
rows_spt = "".join([f"<tr><td width='15%'>{'Kepada' if i==0 else ''}</td><td width='5%'>{i+1}.</td><td width='15%'>Nama</td><td width='2%'>:</td><td><b>{p['nama']}</b></td></tr><tr><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr>" for i,p in enumerate(daftar)])

html_output += f"""<div class="kertas">{s_kop}
<h3 class="text-center text-bold underline" style="color:black; margin-top:10px;">SURAT PERINTAH TUGAS</h3>
<p class="text-center" style="margin-top:-10px; color:black;">NOMOR : {no_spt}</p>
<table width="100%" style="font-size:11pt; color:black; border-collapse:collapse;">
    <tr><td width="15%">Dasar</td><td width="2%">:</td><td>DPA Bagian Perekonomian dan SDA Setda Ngada Tahun Anggaran 2026</td></tr>
</table>
<p class="text-center text-bold" style="margin:15px 0; color:black;">M E M E R I N T A H K A N</p>
<table width="100%" style="font-size:11pt; color:black; border-collapse:collapse;">{rows_spt}</table>
<table width="100%" style="font-size:11pt; margin-top:10px; color:black; border-collapse:collapse;">
    <tr><td width="15%">Untuk</td><td width="2%">:</td><td>{maksud} ke {tujuan}</td></tr>
</table>{ttd_box}</div>"""

# 2. HALAMAN SPD
for p in daftar:
    html_output += f
