import streamlit as st
from datetime import datetime
import logo  # Memanggil file logo.py di repository GitHub kamu

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Ngada Pro", layout="wide")

st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    .stApp { background-color: #525659 !important; }

    .main-container {
        display: flex; flex-direction: column; align-items: center; width: 100%; padding: 10px 0;
    }

    /* KERTAS LEGAL */
    .kertas { 
        background-color: white !important; 
        width: 215.9mm; min-height: 330mm; 
        padding: 10mm 15mm; margin-bottom: 30px; 
        color: black !important; font-family: "Arial", sans-serif; 
        box-sizing: border-box; box-shadow: 0 0 20px rgba(0,0,0,0.8); 
    }

    /* KOP SURAT (Line Spacing 1.0) */
    .kop-table { width: 100%; border: none !important; border-bottom: 3.5pt solid black !important; margin-bottom: 10px; }
    .kop-table td { border: none !important; padding: 0 !important; vertical-align: middle; }
    .kop-teks { text-align: center; line-height: 1.0 !important; } 
    .kop-teks h3 { margin: 0; font-size: 13pt; font-weight: bold; line-height: 1.0; }
    .kop-teks h2 { margin: 0; font-size: 15pt; font-weight: bold; line-height: 1.0; padding: 1px 0; }
    .kop-teks p { margin: 0; font-size: 9pt; line-height: 1.0; }

    /* TABEL SPD BERGARIS */
    .tabel-border { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; table-layout: fixed; }
    .tabel-border td { border: 1pt solid black !important; padding: 2px 4px !important; vertical-align: top; color: black !important; font-size: 9.2pt; overflow: hidden; }
    
    /* TABEL KHUSUS VISUM UNTUK SEJAJARKAN TITIK DUA */
    .visum-table { width: 100%; border: none !important; border-collapse: collapse; margin: 0 !important; }
    .visum-table td { border: none !important; padding: 0 !important; font-size: 9.2pt; line-height: 1.2; color: black !important; }

    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }

    @media print {
        [data-testid="stSidebar"], .stButton { display: none !important; }
        .stApp, .main-container { background-color: white !important; padding: 0 !important; margin: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; width: 215.9mm !important; }
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
            n = st.text_input(f"Nama P-{i+1}", f"Dr. Nicolaus Noywuli, S.Pt., M.Si", key=f"n{i}")
            ni = st.text_input(f"NIP P-{i+1}", "19720921 200012 1 004", key=f"nip{i}")
            g = st.text_input(f"Gol P-{i+1}", "Pembina Utama Muda - IV/c", key=f"g{i}")
            j = st.text_input(f"Jabatan P-{i+1}", "Asisten Perekonomian dan Pembangunan", key=f"j{i}")
            s = st.text_input(f"No SPD P-{i+1}", f"530 /02/2026", key=f"spd{i}")
            l = st.text_input(f"Lembar P-{i+1}", "I", key=f"lbr{i}")
            daftar.append({"nama": n, "nip": ni, "gol": g, "jab": j, "spd": s, "lembar": l})

    st.subheader("🖋️ PENANDATANGAN")
    pjb = st.text_input("Nama Pejabat", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
    gol_pjb = st.text_input("Pangkat/Gol", "Pembina Utama Muda - IV/c")
    jab_ttd = st.text_input("Jabatan", "Pj. Sekretaris Daerah")
    nip_ttd = st.text_input("NIP", "19710328 199203 1 011")

    if st.button("🖨️ PROSES CETAK"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

def tgl_str(d):
    bln = ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"]
    return f"{d.day} {bln[d.month-1]} {d.year}"

# --- RENDER LOGIC ---
html_out = '<div class="main-container">'

# 1. HALAMAN SPT & 2. HALAMAN SPD DEPAN (KODE DIABSTRAKSI AGAR SINGKAT)
kop_pemda = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="70"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834</p><p class="text-bold">BAJAWA</p></td><td width="15%"></td></tr></table>'''
kop_garuda = f'''<div class="text-center" style="margin-bottom:10px;"><img src="data:image/png;base64,{logo.GARUDA}" width="80"><br><h2 style="margin:0; color:black; font-size:14pt; font-weight:bold;">BUPATI NGADA</h2></div>'''
ttd_global = f'''<div style="margin-left:55%; margin-top:15px; line-height:1.2; color:black; font-size:10pt;"><table class="visum-table"><tr><td width="40%">Ditetapkan di</td><td width="5%">:</td><td>Bajawa</td></tr><tr><td>Pada Tanggal</td><td>:</td><td>{tgl_str(datetime.now())}</td></tr></table><br><b>An. BUPATI NGADA</b><br>{jab_ttd},<br><br><br><br><b><u>{pjb}</u></b><br>{gol_pjb}<br>NIP. {nip_ttd}</div>'''

# SPT Render
s_kop = kop_garuda if jenis == "Luar Daerah" else kop_pemda
peg_rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='3%'>:</td><td width='4%'>{i+1}.</td><td width='20%'>Nama</td><td width='2%'>:</td><td><b>{p['nama']}</b></td></tr><tr><td></td><td></td><td></td><td>Pangkat/Gol</td><td>:</td><td>{p['gol']}</td></tr><tr><td></td><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr><tr><td></td><td></td><td></td><td>Jabatan</td><td>:</td><td>{p['jab']}</td></tr>" for i, p in enumerate(daftar)])
html_out += f'<div class="kertas">{s_kop}<div class="text-center" style="margin-top:5px;"><h3 class="text-bold underline">SURAT PERINTAH TUGAS</h3><p>NOMOR : {no_spt}</p></div><table class="visum-table" style="margin-top:15px;"><tr><td width="12%">Dasar</td><td width="3%">:</td><td>{anggaran}</td></tr></table><p class="text-center text-bold" style="margin:15px 0;">M E M E R I N T A H K A N</p><table class="visum-table">{peg_rows}</table><table class="visum-table" style="margin-top:15px;"><tr><td width="12%">Untuk</td><td width="3%">:</td><td>{maksud} ke {tujuan}</td></tr></table>{ttd_global}</div>'

# SPD Depan
for p in daftar:
    html_out += f'''<div class="kertas">{kop_pemda}<div style="margin-left:60%; font-size:9.5pt; line-height:1.1;"><table class="visum-table"><tr><td width="40%">Lembar ke</td><td width="5%">:</td><td>{p["lembar"]}</td></tr><tr><td>Kode No</td><td>:</td><td>{kode_no_spd}</td></tr><tr><td>Nomor</td><td>:</td><td>{p["spd"]}</td></tr></table></div><h3 class="text-center text-bold underline" style="margin:5px 0 0 0;">SURAT PERJALANAN DINAS</h3><h3 class="text-center text-bold" style="margin-bottom:10px;">(SPD)</h3><table class="tabel-border"><tr><td width="4%">1.</td><td width="42%">Pejabat yang memberi perintah</td><td colspan="3"><b>BUPATI NGADA</b></td></tr><tr><td>2.</td><td>Nama Pegawai yang diperintahkan</td><td colspan="3"><b>{p['nama']}</b></td></tr><tr><td rowspan="3">3.</td><td>a. Pangkat/Golongan</td><td colspan="3">{p['gol']}</td></tr><tr><td>b. Jabatan</td><td colspan="3">{p['jab']}</td></tr><tr><td>c. Tingkat Menurut Peraturan</td><td colspan="3"></td></tr><tr><td>4.</td><td>Maksud Perjalanan Dinas</td><td colspan="3">{maksud}</td></tr><tr><td>5.</td><td>Alat angkut yang digunakan</td><td colspan="3">{alat}</td></tr><tr><td rowspan="2">6.</td><td>a. Tempat Berangkat</td><td colspan="3">Bajawa</td></tr><tr><td>b. Tempat Tujuan</td><td colspan="3">{tujuan}</td></tr><tr><td rowspan="3">7.</td><td>Lamanya Perjalanan Dinas</td><td colspan="3">{lama}</td></tr><tr><td>a. Tanggal Berangkat</td><td colspan="3">{tgl_str(datetime.now())}</td></tr><tr><td>b. Tanggal Harus Kembali</td><td colspan="3">{tgl_str(datetime.now())}</td></tr><tr><td>8.</td><td>Pengikut &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Nama</td><td class="text-center" width="20%">Tanggal Lahir</td><td colspan="2" class="text-center">Keterangan</td></tr><tr style="height:22px;"><td></td><td>1.</td><td></td><td colspan="2"></td></tr><tr style="height:22px;"><td></td><td>2.</td><td></td><td colspan="2"></td></tr><tr><td rowspan="3">9.</td><td>Pembebanan Anggaran</td><td colspan="3"></td></tr><tr><td>a. Instansi</td><td colspan="3">a. Bagian Perekonomian dan SDA</td></tr><tr><td>b. Mata Anggaran</td><td colspan="3"></td></tr><tr><td>10.</td><td>Keterangan lain-lain</td><td colspan="3"></td></tr></table>{ttd_global}</div>'''

    # 3. VISUM BELAKANG (PERBAIKAN II, III, IV NAIK BARIS & VII LENGKAP)
    ttd_v = f'<div style="text-align:center; line-height:1.1; font-size:9pt;"><br><b>An. BUPATI NGADA</b><br>{jab_ttd},<br><br><br><br><b><u>{pjb}</u></b><br>{gol_pjb}<br>NIP. {nip_ttd}</div>'
    
    def row_vis(num, label, val, date_v, show_num=True):
        n = f'<td width="10%">{num}</td>' if show_num else ""
        return f'''<table class="visum-table">
            <tr>{n}<td width="40%">{label}</td><td width="5%">:</td><td>{val}</td></tr>
            <tr>{"<td></td>" if show_num else ""}<td>Pada Tanggal</td><td>:</td><td>{date_v}</td></tr>
        </table>'''

    html_out += f'''<div class="kertas"><table class="tabel-border">
        <tr style="height: 175px;"><td width="50%"></td><td style="padding:5px;">{row_vis("I.", "Berangkat dari", "Bajawa", tgl_str(datetime.now()))}
            <table class="visum-table"><tr><td width="10%"></td><td width="40%">Ke</td><td width="5%">:</td><td>{tujuan}</td></tr></table>{ttd_v}</td></tr>
        <tr style="height: 155px;"><td>{row_vis("II.", "Tiba di", tujuan, tgl_str(datetime.now()))}</td>
            <td style="padding:5px;">{row_vis("", "Berangkat dari", tujuan, tgl_str(datetime.now()), False)}
            <table class="visum-table"><tr><td width="40%">Ke</td><td width="5%">:</td><td>Bajawa</td></tr></table></td></tr>
        <tr style="height: 150px;"><td>{row_vis("III.", "Tiba di", "", "")}</td>
            <td style="padding:5px;">{row_vis("", "Berangkat dari", "", "", False)}</td></tr>
        <tr style="height: 150px;"><td>{row_vis("IV.", "Tiba di", "", "")}</td>
            <td style="padding:5px;">{row_vis("", "Berangkat dari", "", "", False)}</td></tr>
        <tr style="height: 175px;"><td>{row_vis("V.", "Tiba Kembali", "Bajawa", tgl_str(datetime.now()))}</td>
            <td style="padding:5px;"><p style="font-style:italic; font-size:8.8pt; line-height:1.2; margin-top:2px;">Telah diperiksa, dengan keterangan bahwa perjalanan tersebut atas perintahnya dan semata-mata untuk kepentingan jabatan</p>{ttd_v}</td></tr>
    </table><div style="border:1pt solid black; border-top:none; padding:8px; font-size:10pt;"><b>VI. Catatan Lain-lain</b></div>
    <div style="border:1pt solid black; border-top:none; padding:8px; font-size:8.3pt; text-align:justify; color:black; line-height:1.2;">
        <b>VII. Perhatian :</b><br>Pejabat yang menerbitkan SPD, pegawai yang melakukan perjalanan dinas, para pejabat yang mengesahkan tanggal berangkat/tiba, serta Bendahara Pengeluaran bertanggung jawab berdasarkan peraturan-peraturan Keuangan Negara apabila negara menderita rugi akibat kesalahan, kelalaian dan kealpaannya.
    </div></div>'''

html_out += '</div>'
st.markdown(html_out, unsafe_allow_html=True)
