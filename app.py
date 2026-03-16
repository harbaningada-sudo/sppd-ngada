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
        .kertas { box-shadow: none !important; margin: 0 !important; border: none !important; padding: 10mm 15mm !important; }
    }
</style>
""", unsafe_allow_html=True)

# --- BAGIAN LOGO (PASTE KODE BASE64 DI SINI) ---
LOGO_PEMDA = """PASTE_KODE_BASE64_PEMDA_DI_SINI"""
LOGO_GARUDA = """PASTE_KODE_BASE64_GARUDA_DI_SINI"""

# 2. PANEL INPUT SIDEBAR
with st.sidebar:
    st.header("📋 INPUT DATA")
    jenis = st.radio("📍 Jenis Perjalanan", ["Dalam Daerah", "Luar Daerah"])
    
    with st.expander("📄 DATA SURAT", expanded=True):
        no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
        kode_no = st.text_input("Kode No", "094/Prokopim")
        maksud = st.text_area("Maksud Perjalanan", "Monitoring dan Pendataan Pemilik Tambang Pasir...")
        tujuan = st.text_input("Tempat Tujuan", "Kecamatan Golewa")
        alat_angkut = st.text_input("Alat Angkutan", "Mobil")
        mata_anggaran = st.text_input("Mata Anggaran (9b)", "")

    with st.expander("👤 DATA PEGAWAI", expanded=True):
        if 'jml' not in st.session_state: st.session_state.jml = 1
        c1, c2 = st.columns(2)
        if c1.button("➕ Tambah"): st.session_state.jml += 1
        if c2.button("➖ Kurang") and st.session_state.jml > 1: st.session_state.jml -= 1
        
        daftar_pegawai = []
        for i in range(st.session_state.jml):
            st.markdown(f"**Pegawai {i+1}**")
            p_no_spd = st.text_input(f"Nomor SPD P-{i+1}", f"531 /02/2026", key=f"spd{i}")
            p_lembar = st.text_input(f"Lembar Ke P-{i+1}", "I / II / III", key=f"lembar{i}")
            p_nama = st.text_input(f"Nama P-{i+1}", f"Nama Pegawai {i+1}", key=f"n{i}")
            p_nip = st.text_input(f"NIP P-{i+1}", "19XXXXXXXXXXXXXX", key=f"nip{i}")
            p_gol = st.text_input(f"Gol P-{i+1}", "Penata Muda - III/a", key=f"g{i}")
            p_jabatan = st.text_input(f"Jabatan P-{i+1}", "Perencana Ahli Pertama", key=f"j{i}")
            daftar_pegawai.append({"no_spd": p_no_spd, "lembar": p_lembar, "nama": p_nama, "nip": p_nip, "gol": p_gol, "jabatan": p_jabatan})

    with st.expander("🕒 TTD", expanded=False):
        tgl_p = st.date_input("Berangkat", datetime.now())
        tgl_k = st.date_input("Kembali", datetime.now())
        lama = st.text_input("Lama Hari", "1 (Satu) hari")
        tgl_ctk = st.date_input("Tanggal Cetak", datetime.now())
        st.markdown("---")
        ttd_an = st.text_input("a.n.", "BUPATI NGADA")
        ttd_jab_tengah = st.text_input("Jabatan 1", "Sekretaris Daerah")
        ttd_ub = st.text_input("Jabatan 2 (u.b.)", "Asisten Perekonomian dan Pembangunan")
        ttd_nama = st.text_input("Nama Pejabat", "Dr. Nicolaus Noywuli, S.Pt, M.Si")
        ttd_gol = st.text_input("Pangkat/Gol", "Pembina Utama Muda- IV/c")
        ttd_nip = st.text_input("NIP", "19720921 200012 1 004")

    if st.button("🖨️ CETAK SEMUA"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

# HELPER TANGGAL
def tgl_str(d):
    bln = ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"]
    return f"{d.day} {bln[d.month-1]} {d.year}"

# --- CSS ---
style_html = """
<style>
    .wrap { display: flex; flex-direction: column; align-items: center; gap: 30px; background: #525659; padding: 20px; }
    .kertas { background: white; width: 210mm; min-height: 297mm; padding: 10mm 15mm; color: black; font-family: Arial, sans-serif; box-sizing: border-box; page-break-after: always; position: relative; }
    .kop-daerah { display: flex; align-items: center; border-bottom: 3.5px solid black; padding-bottom: 5px; margin-bottom: 10px; }
    .tabel-border { width: 100%; border-collapse: collapse; border: 1.2px solid black; font-size: 9.5pt; table-layout: fixed; }
    .tabel-border td { border: 1.2px solid black; padding: 8px; vertical-align: top; }
    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }
    .inner-visum { width: 100%; border-collapse: collapse; margin-bottom: 5px; }
    .inner-visum td { border: none !important; padding: 0 0 2px 0 !important; font-size: 9.5pt; }
</style>
"""

content_html = f'<div class="wrap">{style_html}'

# HELPERS
header_kop_sekda = f"""<div class="kop-daerah"><img src="{LOGO_PEMDA}" style="width:65px; margin-right:15px;"><div style="flex:1; text-align:center;"><h3 style="margin:0; font-size:13pt;">PEMERINTAH KABUPATEN NGADA</h3><h2 style="margin:0; font-size:15pt;">SEKRETARIAT DAERAH</h2><p style="margin:0; font-size:8.5pt;">Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834</p><p style="margin:0; font-size:10pt; font-weight:bold; letter-spacing:1px;">BAJAWA</p></div></div>"""

def get_ttd_block():
    return f"""<div style="margin-left:50%; margin-top:20px; line-height: 1.2; font-size: 10.5pt;"><p style="margin:0;">Ditetapkan di : Bajawa</p><p style="margin:0;">Pada Tanggal : {tgl_str(tgl_ctk)}</p><br><p class="text-bold" style="margin:0;">a.n. {ttd_an}</p><p class="text-bold" style="margin:0;">{ttd_jab_tengah}</p><p class="text-bold" style="margin:0;">u.b. {ttd_ub},</p><br><br><br><br><p class="text-bold underline" style="margin:0;">{ttd_nama}</p><p style="margin:0;">{ttd_gol}</p><p style="margin:0;">NIP. {ttd_nip}</p></div>"""

# --- 1. SPT ---
content_html += f'<div class="kertas">{"<div style=\'text-align:center;\'><img src=\'"+LOGO_GARUDA+"\' style=\'width:75px;\'><br><h3 style=\'margin:5px 0;\'>BUPATI NGADA</h3></div>" if jenis == "Luar Daerah" else header_kop_sekda}<h3 class="text-center text-bold underline" style="margin-top:10px;">SURAT PERINTAH TUGAS</h3><p class="text-center" style="margin-top:-10px;">NOMOR : {no_spt}</p><table width="100%" style="border-collapse:collapse; font-size:10.5pt;"><tr><td width="15%">Dasar</td><td>: {dasar_surat if jenis == "Luar Daerah" else "DPA Bagian Perekonomian dan SDA Setda Ngada Tahun Anggaran 2026"}</td></tr></table><p class="text-center text-bold" style="margin: 10px 0;">M E M E R I N T A H K A N</p><table width="100%" style="border-collapse:collapse; font-size:10.5pt;"><tr><td width="15%">Kepada</td><td colspan="3"></td></tr>{"".join([f"<tr><td width='5%'></td><td width='5%'>{i+1}.</td><td width='15%'>Nama</td><td>: <b>{p['nama']}</b></td></tr><tr><td></td><td></td><td>Pangkat/Gol</td><td>: {p['gol']}</td></tr><tr><td></td><td></td><td>NIP</td><td>: {p['nip']}</td></tr><tr><td></td><td></td><td>Jabatan</td><td>: {p['jabatan']}</td></tr><tr><td colspan=\'4\' height=\'6px\'></td></tr>" for i, p in enumerate(daftar_pegawai)])}</table><table width="100%" style="border-collapse:collapse; font-size:10.5pt;"><tr><td width="15%">Untuk</td><td>: {maksud} ke {tujuan}</td></tr></table>{get_ttd_block()}</div>'

# --- 2. SPD DEPAN ---
for p in daftar_pegawai:
    content_html += f"""<div class="kertas">{header_kop_sekda}<div style="margin-left:60%; font-size:9pt;"><table><tr><td>Lembar Ke</td><td>: {p['lembar']}</td></tr><tr><td>Kode No</td><td>: {kode_no}</td></tr><tr><td>Nomor</td><td>: {p['no_spd']}</td></tr></table></div><h3 class="text-center text-bold underline" style="margin-bottom:5px; margin-top:5px;">SURAT PERINTAH DINAS (SPD)</h3><table class="tabel-border"><tr><td width="5%">1.</td><td width="42%">Pejabat yang memberi perintah</td><td colspan="3"><b>BUPATI NGADA</b></td></tr><tr><td>2.</td><td>Nama Pegawai yang diperintahkan</td><td colspan="3"><b>{p['nama']}</b></td></tr><tr><td rowspan="3">3.</td><td>a. Pangkat/Golongan</td><td colspan="3">{p['gol']}</td></tr><tr><td>b. Jabatan</td><td colspan="3">{p['jabatan']}</td></tr><tr><td>c. Tingkat Menurut Peraturan</td><td colspan="3"></td></tr><tr><td>4.</td><td>Maksud Perjalanan Dinas</td><td colspan="3">{maksud}</td></tr><tr><td>5.</td><td>Alat angkut yang digunakan</td><td colspan="3">{alat_angkut}</td></tr><tr><td rowspan="2">6.</td><td>a. Tempat Berangkat</td><td colspan="3">Bajawa</td></tr><tr><td>b. Tempat Tujuan</td><td colspan="3">{tujuan}</td></tr><tr><td rowspan="3">7.</td><td>Lamanya Perjalanan Dinas</td><td colspan="3">{lama}</td></tr><tr><td>a. Tanggal Berangkat</td><td colspan="3">{tgl_str(tgl_p)}</td></tr><tr><td>b. Tanggal Harus Kembali</td><td colspan="3">{tgl_str(tgl_k)}</td></tr><tr><td>8.</td><td>Pengikut&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Nama</td><td width="20%" class="text-center">Tanggal Lahir</td><td colspan="2" class="text-center">Keterangan</td></tr><tr><td></td><td>1.</td><td></td><td colspan="2"></td></tr><tr><td></td><td>2.</td><td></td><td colspan="2"></td></tr><tr><td rowspan="3">9.</td><td>Pembebanan Anggaran</td><td colspan="3"></td></tr><tr><td>a. Instansi</td><td colspan="3">a. Bagian Perekonomian dan SDA</td></tr><tr><td>b. Mata Anggaran</td><td colspan="3">b. {mata_anggaran}</td></tr><tr><td>10.</td><td>Keterangan lain-lain</td><td colspan="3"></td></tr></table>{get_ttd_block()}</div>"""

# --- 3. SPD BELAKANG (VISUM FINAL) ---
    visum_ttd_clean = f"""<div style="text-align:center; margin-top:10px; line-height:1.2; font-size:9.5pt;"><p class="text-bold" style="margin:0;">a.n. {ttd_an}</p><p class="text-bold" style="margin:0;">{ttd_jab_tengah}</p><br><br><br><br><p class="text-bold underline" style="margin:0;">{ttd_nama}</p><p style="margin:0;">{ttd_gol}</p><p style="margin:0;">NIP. {ttd_nip}</p></div>"""

    content_html += f"""
    <div class="kertas">
        <table class="tabel-border">
            <tr style="height: 170px;">
                <td width="48%"></td>
                <td>
                    <table class="inner-visum">
                        <tr><td width="40%">I. Berangkat dari</td><td>: Bajawa</td></tr>
                        <tr><td>&nbsp;&nbsp;&nbsp;Ke</td><td>: {tujuan}</td></tr>
                        <tr><td>&nbsp;&nbsp;&nbsp;Pada Tanggal</td><td>: {tgl_str(tgl_p)}</td></tr>
                    </table>
                    {visum_ttd_clean}
                </td>
            </tr>
            <tr style="height: 160px;">
                <td>
                    <table class="inner-visum">
                        <tr><td width="40%">II. Tiba di</td><td>: {tujuan}</td></tr>
                        <tr><td>&nbsp;&nbsp;&nbsp;Pada Tanggal</td><td>: {tgl_str(tgl_p)}</td></tr>
                    </table>
                </td>
                <td>
                    <table class="inner-visum">
                        <tr><td width="40%">Berangkat dari</td><td>: {tujuan}</td></tr>
                        <tr><td>Ke</td><td>: Bajawa</td></tr>
                        <tr><td>Pada Tanggal</td><td>: {tgl_str(tgl_k)}</td></tr>
                    </table>
                </td>
            </tr>
            <tr style="height: 100px;">
                <td><table class="inner-visum"><tr><td width="40%">III. Tiba di</td><td>:</td></tr><tr><td>Pada Tanggal</td><td>:</td></tr></table></td>
                <td><table class="inner-visum"><tr><td width="40%">Berangkat dari</td><td>:</td></tr><tr><td>Ke</td><td>:</td></tr><tr><td>Pada Tanggal</td><td>:</td></tr></table></td>
            </tr>
            <tr style="height: 100px;">
                <td><table class="inner-visum"><tr><td width="40%">IV. Tiba di</td><td>:</td></tr><tr><td>Pada Tanggal</td><td>:</td></tr></table></td>
                <td><table class="inner-visum"><tr><td width="40%">Berangkat dari</td><td>:</td></tr><tr><td>Ke</td><td>:</td></tr><tr><td>Pada Tanggal</td><td>:</td></tr></table></td>
            </tr>
            <tr style="height: 220px;">
                <td>
                    <table class="inner-visum">
                        <tr><td width="40%">V. Tiba Kembali</td><td>: Bajawa</td></tr>
                        <tr><td>&nbsp;&nbsp;&nbsp;Pada Tanggal</td><td>: {tgl_str(tgl_k)}</td></tr>
                    </table>
                </td>
                <td>
                    <p style="margin:0 0 10px 0; font-style:italic; font-size:8.5pt;">Telah diperiksa, dengan keterangan bahwa perjalanan tersebut atas perintahnya dan semata-mata untuk kepentingan jabatan</p>
                    {visum_ttd_clean}
                </td>
            </tr>
        </table>
        <table class="tabel-border" style="border-top:none;">
            <tr><td width="48%">VI. Catatan Lain-lain</td><td></td></tr>
            <tr><td colspan="2">VII. Perhatian :</td></tr>
            <tr><td colspan="2" style="font-size:8pt; text-align:justify; padding:5px 10px; line-height:1.3;">Pejabat yang menerbitkan SPD, pegawai yang melakukan perjalanan dinas, para pejabat yang mengesahkan tanggal berangkat/tiba, serta Bendahara Pengeluaran bertanggung jawab berdasarkan peraturan-peraturan Keuangan Negara apabila negara menderita rugi akibat kesalahan, kelalaian dan kealpaannya.</td></tr>
        </table>
    </div>"""

# --- 4. REGISTER ---
reg_rows = "".join([f"<tr><td class='text-center'>{i+1}</td><td>{p['nama']}</td><td>{no_spt}</td><td>{p['no_spd']}</td><td>{maksud} ke {tujuan}</td><td>{tgl_str(tgl_p)}</td><td>{tgl_str(tgl_k)}</td><td></td></tr>" for i, p in enumerate(daftar_pegawai)])
content_html += f"""<div class="kertas" style="width:297mm; min-height:210mm;"><h3 class="text-center">BUKU REGISTER PERJALANAN DINAS</h3><table class="tabel-border"><thead><tr style="background:#eee;"><th width="30">No</th><th>Nama</th><th>No SPT</th><th>No SPD</th><th>Maksud Tujuan</th><th width="80">Pergi</th><th width="80">Pulang</th><th>Ket</th></tr></thead><tbody>{reg_rows}</tbody></table></div></div>"""

st.components.v1.html(content_html, height=2500, scrolling=True)
