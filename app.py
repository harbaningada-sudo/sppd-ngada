import streamlit as st
from datetime import datetime
import logo  # Memanggil file logo.py di repository kamu

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Ngada Pro", layout="wide")

# CSS UNTUK PRESISI CETAK FULL LEGAL & LANDSCAPE REGISTER
st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    .stApp { background-color: #525659 !important; }

    .main-container {
        display: flex; flex-direction: column; align-items: center; width: 100%; padding: 10px 0;
    }

    /* KERTAS UMUM (PORTRAIT LEGAL) */
    .kertas { 
        background-color: white !important; 
        width: 215.9mm; 
        height: 330mm; /* Dikunci tinggi legal agar penuh */
        padding: 10mm 15mm; 
        margin-bottom: 20px; 
        color: black !important; 
        font-family: Arial, sans-serif; 
        box-sizing: border-box; 
        box-shadow: 0 0 20px rgba(0,0,0,0.8);
        font-size: 10.5pt;
        page-break-after: always;
        overflow: hidden;
        position: relative;
    }

    /* KHUSUS REGISTER (LANDSCAPE) */
    .kertas-landscape {
        width: 355.6mm !important;
        height: 215.9mm !important;
        padding: 15mm !important;
    }

    /* KOP & JUDUL (Line Spacing 1.0 Rapat) */
    .kop-table { width: 100%; border: none !important; border-bottom: 3.5pt solid black !important; margin-bottom: 5px; }
    .kop-table td { border: none !important; padding: 0 !important; vertical-align: middle; }
    .kop-teks { text-align: center; line-height: 1.0 !important; } 
    .kop-teks h3, .kop-teks h2, .kop-teks p { margin: 0; line-height: 1.0 !important; padding: 1px 0; }
    
    .judul-rapat { text-align: center; line-height: 1.0 !important; margin-top: 5px; }
    .judul-rapat h3, .judul-rapat p { margin: 0; line-height: 1.0 !important; }

    /* ISI NARASI SPT (Line Spacing 1.5) */
    .isi-surat-spt { line-height: 1.5 !important; margin-top: 10px; }

    /* TABEL SPD DEPAN (Line Spacing 1.0) */
    .tabel-border { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; table-layout: fixed; }
    .tabel-border td { border: 1pt solid black !important; padding: 5px 8px !important; vertical-align: top; color: black !important; font-size: 10pt; line-height: 1.1 !important; }
    
    /* FIX NOMOR 1. sd 10. SEJAJAR */
    .col-no { width: 35px !important; text-align: left !important; }

    /* TABEL VISUM (FULL LEGAL SPACE) */
    .visum-table { width: 100%; border: none !important; border-collapse: collapse; margin: 0 !important; }
    .visum-table td { border: none !important; padding: 0 !important; font-size: 10pt; line-height: 1.2; color: black !important; vertical-align: top; }

    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }

    @media print {
        [data-testid="stSidebar"], .stButton { display: none !important; }
        .stApp, .main-container { background-color: white !important; padding: 0 !important; margin: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; width: 215.9mm !important; height: 330mm !important; }
        
        .kertas-landscape { 
            width: 355.6mm !important; 
            height: 215.9mm !important;
        }
        
        @page { size: legal portrait; margin: 0; }
        .register-page { @page { size: legal landscape; } }
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 PANEL KONTROL")
    opsi_cetak = st.multiselect("Pilih Dokumen", ["SPT", "SPD Depan", "SPD Belakang", "Register"], default=["SPT", "SPD Depan", "SPD Belakang"])
    
    with st.expander("👤 DATA PEGAWAI", expanded=True):
        if 'jml' not in st.session_state: st.session_state.jml = 1
        c1, c2 = st.columns(2)
        if c1.button("➕ Tambah"): st.session_state.jml += 1
        if c2.button("➖ Hapus") and st.session_state.jml > 1: st.session_state.jml -= 1
        
        daftar = []
        for i in range(st.session_state.jml):
            st.markdown(f"**Pegawai {i+1}**")
            n = st.text_input(f"Nama", f"Nama {i+1}", key=f"n{i}")
            ni = st.text_input(f"NIP", "19XXXXXXXXXXXXXX", key=f"nip{i}")
            g = st.text_input(f"Gol", "III/a", key=f"g{i}")
            j = st.text_input(f"Jabatan", "Pelaksana", key=f"j{i}")
            s = st.text_input(f"No SPD", f"530 /02/2026", key=f"spd{i}")
            l = st.text_input(f"Lembar ke", "I", key=f"lbr{i}")
            daftar.append({"nama": n, "nip": ni, "gol": g, "jab": j, "spd": s, "lembar": l})

    with st.expander("📄 DATA UTAMA"):
        no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
        kode_spd = st.text_input("Kode No SPD", "094/Prokopim")
        maksud = st.text_area("Maksud Perjalanan", "Mendampingi kunjungan...")
        tujuan = st.text_input("Tujuan", "Kecamatan Jerebuu")
        alat = st.text_input("Alat Angkut", "Mobil Dinas")
        lama = st.text_input("Lama Hari", "1 (Satu) hari")
        tgl_bkt = st.text_input("Tanggal Berangkat", "17 Maret 2026")
        tgl_kbl = st.text_input("Tanggal Kembali", "17 Maret 2026")
        ket_reg = st.text_input("Keterangan Register", "-")
        anggaran = st.text_input("Dasar Anggaran", "DPA Bagian Perekonomian dan SDA Setda Ngada 2026")

    st.subheader("🖋️ TANDA TANGAN")
    pjb = st.text_input("Nama Pejabat", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
    gol_pjb = st.text_input("Pangkat/Gol", "Pembina Utama Muda - IV/c")
    jab_ttd = st.text_input("Jabatan Utama", "Pj. Sekretaris Daerah")
    ub = st.text_input("Ub.", "Asisten Perekonomian dan Pembangunan")
    nip_ttd = st.text_input("NIP", "19710328 199203 1 011")

    if st.button("🖨️ PROSES CETAK"):
        st.components.v1.html("<script>setTimeout(function(){ window.parent.print(); }, 1200);</script>", height=0)

# --- TEMPLATE KOMPONEN ---
kop_pemda = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834</p><p class="text-bold">BAJAWA</p></td><td width="15%"></td></tr></table>'''

# Fungsi Ruang TTD
def box_ttd(h): return f'<div style="height:{h}px;"></div>'

html_out = '<div class="main-container">'

# 1. SPT
if "SPT" in opsi_cetak:
    p_rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{i+1}.</td><td width='20%'>Nama</td><td width='5%'>:</td><td><b>{p['nama']}</b></td></tr><tr><td></td><td></td><td></td><td>Pangkat/Gol</td><td>:</td><td>{p['gol']}</td></tr><tr><td></td><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr><tr><td></td><td></td><td></td><td>Jabatan</td><td>:</td><td>{p['jab']}</td></tr>" for i, p in enumerate(daftar)])
    html_out += f'<div class="kertas">{kop_pemda}<div class="judul-rapat"><h3 class="text-bold underline">SURAT PERINTAH TUGAS</h3><p>NOMOR : {no_spt}</p></div><div class="isi-surat-spt"><table class="visum-table"><tr><td width="12%">Dasar</td><td width="5%">:</td><td>{anggaran}</td></tr></table><p class="text-center text-bold" style="margin:15px 0;">M E M E R I N T A H K A N</p><table class="visum-table">{p_rows}</table><table class="visum-table" style="margin-top:10px;"><tr><td width="12%">Untuk</td><td width="5%">:</td><td>{maksud} ke {tujuan}</td></tr></table></div><div style="margin-left:55%; margin-top:20px; line-height:1.2;"><b>An. BUPATI NGADA</b><br>{jab_ttd},<br>{f"Ub. {ub}," if ub else ""}{box_ttd(90)}<b><u>{pjb}</u></b><br>{gol_pjb}<br>NIP. {nip_ttd}</div></div>'

# 2. SPD DEPAN & BELAKANG
for p in daftar:
    if "SPD Depan" in opsi_cetak:
        html_out += f'''<div class="kertas">{kop_pemda}<div style="margin-left:60%; line-height:1.0;"><table class="visum-table"><tr><td width="40%">Lembar ke</td><td width="5%">:</td><td>{p["lembar"]}</td></tr><tr><td>Kode No</td><td>:</td><td>{kode_spd}</td></tr><tr><td>Nomor</td><td>:</td><td>{p["spd"]}</td></tr></table></div><div class="judul-rapat" style="margin-top:5px;"><h3 class="text-bold underline">SURAT PERJALANAN DINAS</h3><h3 class="text-bold">(SPD)</h3></div><table class="tabel-border">
            <tr><td class="col-no">1.</td><td width="42%">Pejabat yang memberi perintah</td><td colspan="3"><b>BUPATI NGADA</b></td></tr>
            <tr><td class="col-no">2.</td><td>Nama Pegawai yang diperintahkan</td><td colspan="3"><b>{p['nama']}</b></td></tr>
            <tr><td class="col-no" rowspan="3">3.</td><td>a. Pangkat/Golongan</td><td colspan="3">{p['gol']}</td></tr>
            <tr><td>b. Jabatan</td><td colspan="3">{p['jab']}</td></tr>
            <tr><td>c. Tingkat Menurut Peraturan</td><td colspan="3"></td></tr>
            <tr><td class="col-no">4.</td><td>Maksud Perjalanan Dinas</td><td colspan="3">{maksud}</td></tr>
            <tr><td class="col-no">5.</td><td>Alat angkut yang digunakan</td><td colspan="3">{alat}</td></tr>
            <tr><td class="col-no" rowspan="2">6.</td><td>a. Tempat Berangkat</td><td colspan="3">Bajawa</td></tr>
            <tr><td>b. Tempat Tujuan</td><td colspan="3">{tujuan}</td></tr>
            <tr><td class="col-no" rowspan="3">7.</td><td>Lamanya Perjalanan Dinas</td><td colspan="3">{lama}</td></tr>
            <tr><td>a. Tanggal Berangkat</td><td colspan="3">{tgl_bkt}</td></tr>
            <tr><td>b. Tanggal Harus Kembali</td><td colspan="3">{tgl_kbl}</td></tr>
            <tr><td class="col-no">8.</td><td>Pengikut &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Nama</td><td class="text-center" width="20%">Tanggal Lahir</td><td colspan="2" class="text-center">Keterangan</td></tr>
            <tr style="height:22px;"><td></td><td>1.</td><td></td><td colspan="2"></td></tr>
            <tr><td class="col-no" rowspan="3">9.</td><td>Pembebanan Anggaran</td><td colspan="3"></td></tr>
            <tr><td>a. Instansi</td><td colspan="3">a. Bagian Perekonomian dan SDA</td></tr>
            <tr><td>b. Mata Anggaran</td><td colspan="3"></td></tr>
            <tr><td class="col-no">10.</td><td>Keterangan lain-lain</td><td colspan="3"></td></tr>
        </table><div style="margin-left:55%; margin-top:10px; line-height:1.2;"><b>An. BUPATI NGADA</b><br>{jab_ttd},<br>{f"Ub. {ub}," if ub else ""}{box_ttd(80)}<b><u>{pjb}</u></b><br>{gol_pjb}<br>NIP. {nip_ttd}</div></div>'''

    if "SPD Belakang" in opsi_cetak:
        ttd_v = f'<div style="text-align:center; line-height:1.2; font-size:10pt;"><br><b>An. BUPATI NGADA</b><br>{jab_ttd},<br>{f"Ub. {ub}," if ub else ""}{box_ttd(90)}<b><u>{pjb}</u></b><br>{gol_pjb}<br>NIP. {nip_ttd}</div>'
        def rv(num, label, val, d_v, is_n=True):
            n_c = f'<td width="10%">{num}</td>' if is_n else ""
            return f'''<table class="visum-table"><tr>{n_c}<td width="35%">{label}</td><td width="5%">:</td><td>{val}</td></tr><tr>{"<td></td>" if is_n else ""}<td>Pada Tanggal</td><td>:</td><td>{d_v}</td></tr></table>'''

        html_out += f'''<div class="kertas"><table class="tabel-border" style="height:90%;">
            <tr style="height: 230px;"><td width="50%"></td><td style="padding:10px;">{rv("I.", "Berangkat dari", "Bajawa", tgl_bkt)}<table class="visum-table"><tr><td width="10%"></td><td width="35%">Ke</td><td width="5%">:</td><td>{tujuan}</td></tr></table>{ttd_v}</td></tr>
            <tr style="height: 200px;"><td>{rv("II.", "Tiba di", tujuan, tgl_bkt)}</td><td style="padding:10px;">{rv("", "Berangkat dari", tujuan, tgl_kbl, False)}<table class="visum-table"><tr><td width="35%">Ke</td><td width="5%">:</td><td>Bajawa</td></tr></table></td></tr>
            <tr style="height: 200px;"><td>{rv("III.", "Tiba di", "", "")}</td><td style="padding:10px;">{rv("", "Berangkat dari", "", "", False)}</td></tr>
            <tr style="height: 200px;"><td>{rv("IV.", "Tiba di", "", "")}</td><td style="padding:10px;">{rv("", "Berangkat dari", "", "", False)}</td></tr>
            <tr style="height: 230px;"><td>{rv("V.", "Tiba Kembali", "Bajawa", tgl_kbl)}</td><td style="padding:10px;"><p style="font-style:italic; font-size:9.2pt; line-height:1.2; margin-top:5px;">Telah diperiksa, dengan keterangan bahwa perjalanan tersebut atas perintahnya dan semata-mata untuk kepentingan jabatan</p>{ttd_v}</td></tr>
        </table><div style="border:1pt solid black; border-top:none; padding:8px; font-size:10.5pt;"><b>VI. Catatan Lain-lain</b></div><div style="border:1pt solid black; border-top:none; padding:8px; font-size:8.8pt; text-align:justify; color:black; line-height:1.3;"><b>VII. Perhatian :</b> Pejabat yang menerbitkan SPD, pegawai yang melakukan perjalanan dinas, para pejabat yang mengesahkan tanggal berangkat/tiba, serta Bendahara Pengeluaran bertanggung jawab berdasarkan peraturan-peraturan Keuangan Negara apabila negara menderita rugi akibat kesalahan, kelalaian dan kealpaannya.</div></div>'''

# 3. REGISTER (LANDSCAPE)
if "Register" in opsi_cetak:
    r_rows = "".join([f"<tr><td class='text-center'>{i+1}</td><td>{p['nama']}</td><td>{no_spt}</td><td>{p['spd']}</td><td>{tgl_bkt}</td><td>{tgl_kbl}</td><td>{lama}</td><td>{ket_reg}</td></tr>" for i, p in enumerate(daftar)])
    html_out += f'''<div class="kertas kertas-landscape register-page"><h3 class="text-center text-bold">REGISTER SURAT PERJALANAN DINAS</h3><br><table class="tabel-border" style="font-size:9.5pt; width:100%;"><thead><tr style="background:#eee;"><th>No</th><th>Nama Pegawai</th><th>Nomor SPT</th><th>Nomor SPD</th><th>Tanggal Berangkat</th><th>Tanggal Pulang</th><th>Lamanya</th><th>Keterangan</th></tr></thead><tbody>{r_rows}</tbody></table></div>'''

html_out += '</div>'
st.markdown(html_out, unsafe_allow_html=True)
