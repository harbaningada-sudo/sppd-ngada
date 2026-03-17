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

    /* KHUSUS HALAMAN BELAKANG TURUN LAGI AGAR TIDAK TERPOTONG PRINTER CANON */
    .kertas-belakang { margin-top: 75mm !important; }

    /* KOP SURAT (Line Spacing 1.0 Rapat) */
    .kop-table { width: 100%; border: none !important; border-bottom: 3.5pt solid black !important; margin-bottom: 10px; }
    .kop-table td { border: none !important; padding: 0 !important; vertical-align: middle; }
    .kop-teks { text-align: center; line-height: 1.0 !important; } 
    .kop-teks h3 { margin: 0; font-size: 13pt; font-weight: bold; line-height: 1.0; }
    .kop-teks h2 { margin: 0; font-size: 15pt; font-weight: bold; line-height: 1.0; padding: 2px 0; }
    .kop-teks p { margin: 0; font-size: 9pt; line-height: 1.0; }

    /* ISI SURAT (Line Spacing 1.5) */
    .isi-surat { line-height: 1.5 !important; }
    .isi-surat td, .isi-surat p { line-height: 1.5 !important; }

    /* TABEL SPD BERGARIS */
    .tabel-border { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; table-layout: fixed; }
    .tabel-border td { border: 1pt solid black !important; padding: 4px 6px !important; vertical-align: top; color: black !important; font-size: 9pt; }
    
    /* TABEL KHUSUS VISUM UNTUK SEJAJARKAN TITIK DUA */
    .inner-table { width: 100%; border: none !important; border-collapse: collapse; margin: 0 !important; }
    .inner-table td { border: none !important; padding: 0 !important; font-size: 9pt; color: black !important; vertical-align: top; }

    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }

    @media print {
        [data-testid="stSidebar"], .stButton { display: none !important; }
        .stApp, .main-container { background-color: white !important; padding: 0 !important; margin: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; width: 215.9mm !important; page-break-after: always; }
        .kertas-belakang { margin-top: 70mm !important; }
        @page { size: legal; margin: 0; }
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 PANEL KONTROL")
    opsi_cetak = st.multiselect("Pilih Dokumen", ["SPT", "SPD Depan", "SPD Belakang", "Register"], default=["SPT", "SPD Depan", "SPD Belakang"])
    
    with st.expander("📄 DATA UTAMA", expanded=True):
        no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
        kode_no_spd = st.text_input("Kode No SPD", "094/Prokopim")
        maksud = st.text_area("Maksud Perjalanan", "Mendampingi Kunjungan Kementerian...")
        tujuan = st.text_input("Tujuan", "Kecamatan Jerebuu")
        alat = st.text_input("Alat Angkut", "Mobil Dinas")
        lama = st.text_input("Lama Hari", "1 (Satu) hari")
        tgl_berangkat = st.text_input("Tanggal Berangkat", "17 Maret 2026")
        tgl_kembali = st.text_input("Tanggal Kembali", "17 Maret 2026")
        anggaran = st.text_input("Dasar Anggaran", "DPA Bagian Perekonomian dan SDA Setda Ngada 2026")

    with st.expander("👤 DATA PEGAWAI", expanded=True):
        if 'jml_p' not in st.session_state: st.session_state.jml_p = 1
        c1, c2 = st.columns(2)
        with c1:
            if st.button("➕ Pegawai"): st.session_state.jml_p += 1
        with c2:
            if st.button("➖ Hapus") and st.session_state.jml_p > 1: st.session_state.jml_p -= 1
        
        daftar = []
        for i in range(st.session_state.jml_p):
            st.markdown(f"**Pegawai {i+1}**")
            n = st.text_input(f"Nama", f"Nama {i+1}", key=f"n{i}")
            ni = st.text_input(f"NIP", "19XXXXXXXXXXXXXX", key=f"nip{i}")
            g = st.text_input(f"Gol", "III/a", key=f"g{i}")
            j = st.text_input(f"Jabatan", "Pelaksana", key=f"j{i}")
            s = st.text_input(f"No SPD", f"530 /02/2026", key=f"spd{i}")
            l = st.text_input(f"Lembar ke", "I", key=f"lbr{i}")
            daftar.append({"nama": n, "nip": ni, "gol": g, "jab": j, "spd": s, "lembar": l})

    st.subheader("🖋️ TANDA TANGAN")
    pjb = st.text_input("Nama Pejabat", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
    gol_pjb = st.text_input("Pangkat/Gol", "Pembina Utama Muda - IV/c")
    jab_ttd = st.text_input("Jabatan Utama", "Pj. Sekretaris Daerah")
    ub_ttd = st.text_input("Ub. (Atas Nama)", "Asisten Perekonomian dan Pembangunan")
    nip_ttd = st.text_input("NIP", "19710328 199203 1 011")

    # TOMBOL CETAK DENGAN REFRESH & DELAY JAVASCRIPT
    if st.button("🖨️ CETAK SEKARANG"):
        st.components.v1.html("""
            <script>
                setTimeout(function(){ window.parent.print(); }, 2000);
            </script>
        """, height=0)

# --- KOMPONEN ---
kop_pemda = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="70"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834</p><p class="text-bold">BAJAWA</p></td><td width="15%"></td></tr></table>'''
ttd_global = f'''<div style="margin-left:55%; margin-top:15px; line-height:1.2; color:black; font-size:10pt;"><table class="inner-table"><tr><td width="40%">Ditetapkan di</td><td width="5%">:</td><td>Bajawa</td></tr><tr><td>Pada Tanggal</td><td>:</td><td>{tgl_berangkat}</td></tr></table><br><b>An. BUPATI NGADA</b><br>{jab_ttd},<br>{f"Ub. {ub_ttd}," if ub_ttd else ""}<br><br><br><br><b><u>{pjb}</u></b><br>{gol_pjb}<br>NIP. {nip_ttd}</div>'''

html_out = '<div class="main-container">'

# 1. CETAK SPT (Line Spacing 1.5)
if "SPT" in opsi_cetak:
    peg_rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='3%'>:</td><td width='4%'>{i+1}.</td><td width='25%'>Nama</td><td width='3%'>:</td><td><b>{p['nama']}</b></td></tr><tr><td></td><td></td><td></td><td>Pangkat/Gol</td><td>:</td><td>{p['gol']}</td></tr><tr><td></td><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr><tr><td></td><td></td><td></td><td>Jabatan</td><td>:</td><td>{p['jab']}</td></tr>" for i, p in enumerate(daftar)])
    html_out += f'<div class="kertas">{kop_pemda}<div class="text-center" style="margin-top:5px;"><h3 class="text-bold underline">SURAT PERINTAH TUGAS</h3><p>NOMOR : {no_spt}</p></div><div class="isi-surat"><table class="inner-table" style="margin-top:15px;"><tr><td width="12%">Dasar</td><td width="3%">:</td><td>{anggaran}</td></tr></table><p class="text-center text-bold" style="margin:15px 0;">M E M E R I N T A H K A N</p><table class="inner-table">{peg_rows}</table><table class="inner-table" style="margin-top:15px;"><tr><td width="12%">Untuk</td><td width="3%">:</td><td>{maksud} ke {tujuan}</td></tr></table></div>{ttd_global}</div>'

# 2. CETAK SPD DEPAN & BELAKANG
for p in daftar:
    if "SPD Depan" in opsi_cetak:
        html_out += f'''<div class="kertas">{kop_pemda}<div style="margin-left:60%; font-size:9.5pt; line-height:1.1;"><table class="inner-table"><tr><td width="40%">Lembar ke</td><td width="5%">:</td><td>{p["lembar"]}</td></tr><tr><td>Kode No</td><td>:</td><td>{kode_no_spd}</td></tr><tr><td>Nomor</td><td>:</td><td>{p["spd"]}</td></tr></table></div><h3 class="text-center text-bold underline" style="margin:5px 0 0 0;">SURAT PERJALANAN DINAS</h3><h3 class="text-center text-bold" style="margin-bottom:10px;">(SPD)</h3><div class="isi-surat"><table class="tabel-border"><tr><td width="4%">1.</td><td width="42%">Pejabat yang memberi perintah</td><td colspan="3"><b>BUPATI NGADA</b></td></tr><tr><td>2.</td><td>Nama Pegawai yang diperintahkan</td><td colspan="3"><b>{p['nama']}</b></td></tr><tr><td rowspan="3">3.</td><td>a. Pangkat/Golongan</td><td colspan="3">{p['gol']}</td></tr><tr><td>b. Jabatan</td><td colspan="3">{p['jab']}</td></tr><tr><td>c. Tingkat Menurut Peraturan</td><td colspan="3"></td></tr><tr><td>4.</td><td>Maksud Perjalanan Dinas</td><td colspan="3">{maksud}</td></tr><tr><td>5.</td><td>Alat angkut yang digunakan</td><td colspan="3">{alat}</td></tr><tr><td rowspan="2">6.</td><td>a. Tempat Berangkat</td><td colspan="3">Bajawa</td></tr><tr><td>b. Tempat Tujuan</td><td colspan="3">{tujuan}</td></tr><tr><td rowspan="3">7.</td><td>Lamanya Perjalanan Dinas</td><td colspan="3">{lama}</td></tr><tr><td>a. Tanggal Berangkat</td><td colspan="3">{tgl_berangkat}</td></tr><tr><td>b. Tanggal Harus Kembali</td><td colspan="3">{tgl_kembali}</td></tr><tr><td>8.</td><td>Pengikut &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Nama</td><td class="text-center" width="20%">Tanggal Lahir</td><td colspan="2" class="text-center">Keterangan</td></tr><tr style="height:22px;"><td></td><td>1.</td><td></td><td colspan="2"></td></tr><tr><td rowspan="3">9.</td><td>Pembebanan Anggaran</td><td colspan="3"></td></tr><tr><td>a. Instansi</td><td colspan="3">a. Bagian Perekonomian dan SDA</td></tr><tr><td>b. Mata Anggaran</td><td colspan="3"></td></tr><tr><td>10.</td><td>Keterangan lain-lain</td><td colspan="3"></td></tr></table></div>{ttd_global}</div>'''

    if "SPD Belakang" in opsi_cetak:
        ttd_v = f'<div style="text-align:center; line-height:1.1; font-size:9pt;"><br><b>An. BUPATI NGADA</b><br>{jab_ttd},<br>{f"Ub. {ub_ttd}," if ub_ttd else ""}<br><br><br><br><b><u>{pjb}</u></b><br>{gol_pjb}<br>NIP. {nip_ttd}</div>'
        def rv(num, label, val, date_v, is_num=True):
            n_col = f'<td width="10%">{num}</td>' if is_num else ""
            return f'''<table class="inner-table"><tr>{n_col}<td width="35%">{label}</td><td width="3%">:</td><td>{val}</td></tr><tr>{"<td></td>" if is_num else ""}<td>Pada Tanggal</td><td>:</td><td>{date_v}</td></tr></table>'''

        html_out += f'''<div class="kertas kertas-belakang"><table class="tabel-border">
            <tr style="height: 180px;"><td width="50%"></td><td style="padding:5px;">{rv("I.", "Berangkat dari", "Bajawa", tgl_berangkat)}<table class="inner-table"><tr><td width="10%"></td><td width="35%">Ke</td><td width="3%">:</td><td>{tujuan}</td></tr></table>{ttd_v}</td></tr>
            <tr style="height: 155px;"><td>{rv("II.", "Tiba di", tujuan, tgl_berangkat)}</td><td style="padding:5px;">{rv("", "Berangkat dari", tujuan, tgl_kembali, False)}<table class="inner-table"><tr><td width="35%">Ke</td><td width="3%">:</td><td>Bajawa</td></tr></table></td></tr>
            <tr style="height: 150px;"><td>{rv("III.", "Tiba di", "", "")}</td><td style="padding:5px;">{rv("", "Berangkat dari", "", "", False)}</td></tr>
            <tr style="height: 150px;"><td>{rv("IV.", "Tiba di", "", "")}</td><td style="padding:5px;">{rv("", "Berangkat dari", "", "", False)}</td></tr>
            <tr style="height: 180px;"><td>{rv("V.", "Tiba Kembali", "Bajawa", tgl_kembali)}</td><td style="padding:5px;"><p style="font-style:italic; font-size:8.8pt; line-height:1.2; margin-top:2px;">Telah diperiksa, dengan keterangan bahwa perjalanan tersebut atas perintahnya dan semata-mata untuk kepentingan jabatan</p>{ttd_v}</td></tr>
        </table><div style="border:1pt solid black; border-top:none; padding:5px; font-size:10pt;"><b>VI. Catatan Lain-lain</b></div>
        <div style="border:1pt solid black; border-top:none; padding:8px; font-size:8pt; text-align:justify; color:black; line-height:1.2;"><b>VII. Perhatian :</b><br>Pejabat yang menerbitkan SPD, pegawai yang melakukan perjalanan dinas, para pejabat yang mengesahkan tanggal berangkat/tiba, serta Bendahara Pengeluaran bertanggung jawab berdasarkan peraturan-peraturan Keuangan Negara apabila negara menderita rugi akibat kesalahan, kelalaian dan kealpaannya.</div></div>'''

# 3. REGISTER
if "Register" in opsi_cetak:
    r_rows = "".join([f"<tr><td class='text-center'>{i+1}</td><td>{p['nama']}</td><td>{no_spt}</td><td>{p['spd']}</td><td>{tgl_berangkat}</td><td>{tujuan}</td></tr>" for i, p in enumerate(daftar)])
    html_out += f'''<div class="kertas"><h3 class="text-center text-bold">REGISTER SURAT PERJALANAN DINAS</h3><br><table class="tabel-border"><thead><tr style="background:#eee;"><th>No</th><th>Nama</th><th>No SPT</th><th>No SPD</th><th>Tgl Bkt</th><th>Tujuan</th></tr></thead><tbody>{r_rows}</tbody></table></div>'''

html_out += '</div>'
st.markdown(html_out, unsafe_allow_html=True)
