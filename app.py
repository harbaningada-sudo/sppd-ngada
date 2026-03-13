import streamlit as st
from datetime import datetime

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Prokopim Ngada", layout="wide")

st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    .main { background-color: #525659; }
</style>
""", unsafe_allow_html=True)

# 2. PANEL INPUT SIDEBAR
with st.sidebar:
    st.header("📋 INPUT DATA UTAMA")
    
    with st.expander("📄 NOMOR & MAKSUD", expanded=True):
        no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
        no_spd = st.text_input("Nomor SPD", "530 /02/2026")
        maksud = st.text_area("Maksud Perjalanan", "Monitoring dan Pendataan Pemilik Tambang Pasir...")
        tujuan = st.text_input("Tempat Tujuan", "Kecamatan Golewa")

    with st.expander("👤 DATA PEGAWAI", expanded=True):
        nama = st.text_input("Nama Pegawai", "Silfinus Febri Yanto Rugat, S.E.")
        nip = st.text_input("NIP", "19XXXXXXXXXXXXXX")
        gol = st.text_input("Pangkat/Gol", "Penata Muda - III/a")
        jabatan = st.text_area("Jabatan", "Perencana Ahli Pertama Pada Bagian")

    with st.expander("🕒 TANGGAL & WAKTU", expanded=False):
        tgl_p = st.date_input("Tanggal Berangkat", datetime(2026, 2, 25))
        tgl_k = st.date_input("Tanggal Kembali", datetime(2026, 2, 26))
        tgl_cetak = st.date_input("Tanggal Cetak SPT/SPD", datetime(2026, 2, 25))
        lama = st.text_input("Lama Hari", "2 (Dua)")

    with st.expander("🖋️ PENANDATANGAN (PEJABAT)", expanded=False):
        ttd_nama = st.text_input("Nama Pejabat", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
        ttd_nip = st.text_input("NIP Pejabat", "19710328 199203 1 011")
        ttd_gol = st.text_input("Gol Pejabat", "Pembina Utama Muda - IV/c")

    if st.button("🖨️ CETAK SEMUA HALAMAN"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

# FORMAT TANGGAL
bulan_list = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
def tgl_str(d): return f"{d.day} {bulan_list[d.month-1]} {d.year}"

# 3. RENDER SEMUA HALAMAN
surat_html = f"""
<style>
    .wrap {{ background-color: #525659; padding: 20px; display: flex; flex-direction: column; align-items: center; gap: 25px; }}
    .kertas {{ background-color: white; width: 210mm; min-height: 297mm; padding: 15mm 20mm 20mm 25mm; color: black; font-family: Arial, sans-serif; font-size: 10pt; box-shadow: 0 0 15px rgba(0,0,0,0.5); box-sizing: border-box; page-break-after: always; position: relative; }}
    .kop {{ text-align: center; border-bottom: 3px solid black; padding-bottom: 2px; margin-bottom: 15px; line-height: 1.2; }}
    .tabel-polos {{ width: 100%; border-collapse: collapse; }}
    .tabel-polos td {{ border: none; padding: 2px; vertical-align: top; }}
    .tabel-border {{ width: 100%; border-collapse: collapse; border: 1px solid black; }}
    .tabel-border td {{ border: 1px solid black; padding: 5px 8px; vertical-align: top; }}
    .text-center {{ text-align: center; }}
    .text-bold {{ font-weight: bold; }}
    .text-underline {{ text-decoration: underline; }}
    .small-text {{ font-size: 8.5pt; line-height: 1.3; }}
</style>

<div class="wrap">
    <div class="kertas">
        <div class="kop">
            <h3 style="margin:0;">PEMERINTAH KABUPATEN NGADA</h3>
            <h2 style="margin:0;">SEKRETARIAT DAERAH</h2>
            <p style="margin:0;">Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834</p>
            <h3 style="margin:0;">BAJAWA</h3>
        </div>
        <h3 class="text-center text-bold text-underline">SURAT PERINTAH TUGAS</h3>
        <p class="text-center" style="margin-top:-10px;">NOMOR : {no_spt}</p>
        <table class="tabel-polos">
            <tr><td width="15%">Dasar</td><td width="2%">:</td><td>DPA Bagian Perekonomian dan SDA Setda Ngada Tahun Anggaran 2026</td></tr>
        </table>
        <p class="text-center text-bold" style="letter-spacing: 2px; margin: 20px 0;">M E M E R I N T A H K A N</p>
        <table class="tabel-polos">
            <tr><td width="15%">Kepada</td><td width="5%">: 1.</td><td width="15%">Nama</td><td width="2%">:</td><td class="text-bold">{nama}</td></tr>
            <tr><td></td><td></td><td>Pangkat/Gol</td><td>:</td><td>{gol}</td></tr>
            <tr><td></td><td></td><td>NIP</td><td>:</td><td>{nip}</td></tr>
            <tr><td></td><td></td><td>Jabatan</td><td>:</td><td>{jabatan}</td></tr>
        </table>
        <br>
        <table class="tabel-polos">
            <tr><td width="15%">Untuk</td><td width="2%">:</td><td style="text-align:justify;">{maksud}</td></tr>
        </table>
        <div style="margin-left:55%; margin-top:40px;">
            <p style="margin:0;">Ditetapkan di : Bajawa</p>
            <p style="margin:0;">Pada Tanggal : {tgl_str(tgl_cetak)}</p>
            <br><p class="text-bold" style="margin:0;">An. BUPATI NGADA</p>
            <p style="margin:0;">Pj. Sekretaris Daerah,</p>
            <br><br><br><br>
            <p class="text-bold text-underline" style="margin:0;">{ttd_nama}</p>
            <p style="margin:0;">{ttd_gol}</p>
            <p style="margin:0;">NIP. {ttd_nip}</p>
        </div>
    </div>

    <div class="kertas">
        <table class="tabel-border">
            <tr style="height: 120px;">
                <td width="45%"></td>
                <td>
                    I. Berangkat dari : Bajawa<br>
                    Ke : {tujuan}<br>
                    Pada Tanggal : {tgl_str(tgl_p)}<br><br>
                    <div class="text-center">
                        An. Bupati Ngada<br>Pj. Sekretaris Daerah<br><br><br><br>
                        <span class="text-bold text-underline">{ttd_nama}</span><br>
                        {ttd_gol}<br>
                        NIP. {ttd_nip}
                    </div>
                </td>
            </tr>
            <tr style="height: 110px;">
                <td>
                    II. Tiba di : {tujuan}<br>
                    Pada Tanggal : {tgl_str(tgl_p)}
                </td>
                <td>
                    Berangkat dari : {tujuan}<br>
                    Ke : Bajawa<br>
                    Pada Tanggal : {tgl_str(tgl_k)}
                </td>
            </tr>
            <tr style="height: 110px;">
                <td>III. Tiba di :<br>Pada Tanggal :</td>
                <td>Berangkat dari :<br>Ke :<br>Pada Tanggal :</td>
            </tr>
            <tr style="height: 110px;">
                <td>IV. Tiba di :<br>Pada Tanggal :</td>
                <td>Berangkat dari :<br>Ke :<br>Pada Tanggal :</td>
            </tr>
            <tr style="height: 120px;">
                <td>
                    V. Tiba Kembali : Bajawa<br>
                    Pada Tanggal : {tgl_str(tgl_k)}
                </td>
                <td>
                    <div class="small-text" style="font-style: italic; text-align: center; margin-bottom: 10px;">
                        Telah diperiksa, dengan keterangan bahwa perjalanan tersebut atas perintahnya dan semata-mata untuk kepentingan jabatan
                    </div>
                    <div class="text-center">
                        An. Bupati Ngada<br>Pj. Sekretaris Daerah<br><br><br><br>
                        <span class="text-bold text-underline">{ttd_nama}</span><br>
                        {ttd_gol}<br>
                        NIP. {ttd_nip}
                    </div>
                </td>
            </tr>
            <tr><td colspan="2">VI. Catatan Lain-lain</td></tr>
            <tr><td colspan="2">VII. Perhatian :</td></tr>
            <tr>
                <td colspan="2" class="small-text" style="text-align: justify; font-style: italic; padding: 10px;">
                    Pejabat yang menerbitkan SPD, pegawai yang melakukan perjalanan dinas, para pejabat yang mengesahkan tanggal berangkat/tiba, serta Bendahara Pengeluaran bertanggung jawab berdasarkan peraturan-peraturan Keuangan Negara apabila negara menderita rugi akibat kesalahan, kelalaian dan kealpaannya.
                </td>
            </tr>
        </table>
    </div>
</div>
"""

st.components.v1.html(surat_html, height=2500, scrolling=True)
