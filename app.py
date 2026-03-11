import streamlit as st
from datetime import datetime

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Prokopim Ngada", layout="wide")

st.markdown("""
<style>
    header, footer, #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    .main { background-color: #525659; }

    /* KERTAS A4 */
    .kertas-a4 {
        background-color: white;
        width: 210mm;
        min-height: 297mm;
        padding: 10mm 15mm;
        margin: 15px auto;
        color: black;
        font-family: "Arial", sans-serif;
        font-size: 10.5pt;
        box-shadow: 0 0 15px rgba(0,0,0,0.4);
        box-sizing: border-box;
    }

    /* AREA KOP SURAT (Kosong untuk Space Logo) */
    .kop-surat {
        height: 3.5cm;
        text-align: center;
        margin-bottom: 10px;
    }

    /* TABEL STYLE */
    .tabel-excel {
        width: 100%;
        border-collapse: collapse;
        table-layout: fixed;
    }
    .tabel-excel td {
        border: 1px solid black;
        padding: 6px 10px;
        vertical-align: top;
        line-height: 1.3;
    }
    
    .no-border td { border: none !important; padding: 2px !important; }
    .text-center { text-align: center; }
    .text-bold { font-weight: bold; }
    .text-underline { text-decoration: underline; }

    /* SPD BELAKANG */
    .col-kiri { width: 44%; }
    .col-kanan { width: 56%; }

    @media print {
        .stSidebar, .stButton, .no-print { display: none !important; }
        @page { size: A4; margin: 0; }
        .kertas-a4 { margin: 0 !important; box-shadow: none !important; border: none !important; page-break-after: always; }
    }
</style>
""", unsafe_allow_html=True)

def format_indo(tgl):
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    return f"{tgl.day} {bulan[tgl.month-1]} {tgl.year}"

# 2. OPSI INPUTAN SIDEBAR
with st.sidebar:
    st.header("⚙️ PANEL INPUT")
    
    with st.expander("📄 DATA SURAT", expanded=True):
        no_spt = st.text_input("Nomor SPT", "094/PROKOPIM/388/02/2026")
        no_spd = st.text_input("Nomor SPD", "094/PROKOPIM/388/02/2026")
        maksud = st.text_area("Maksud Tugas", "Melakukan koordinasi dan konsultasi...")
        tujuan = st.text_input("Tujuan", "Kupang")
        alat = st.text_input("Alat Angkut", "Pesawat Udara / Kendaraan Dinas")

    with st.expander("🕒 WAKTU & ANGGARAN", expanded=False):
        tgl_p = st.date_input("Berangkat", datetime(2026, 2, 9))
        tgl_k = st.date_input("Kembali", datetime(2026, 2, 11))
        lama = st.text_input("Lama Hari", "3 (Tiga)")
        dpa = st.text_input("Instansi", "Sekretariat Daerah Kabupaten Ngada")
        mata_anggaran = st.text_input("Mata Anggaran", "5.1.02.04.01.0001")

    with st.expander("👥 PEJABAT & PEGAWAI", expanded=True):
        pemberi = st.text_input("Pemberi Perintah", "Bupati Ngada")
        nama_ttd = st.text_input("Penandatangan", "ANDREAS PARU")
        st.info("Nama | NIP | Jabatan | Gol")
        peg_txt = st.text_area("Daftar Pegawai", "RAYMUNDUS BENA, S.S., M.Hum | 19XXXXXXXXXXXXXX | Wakil Bupati Ngada | IV/c")

    daftar = []
    for line in peg_txt.split('\n'):
        if '|' in line:
            p = line.split('|')
            daftar.append({"nama": p[0].strip(), "nip": p[1].strip(), "jab": p[2].strip(), "gol": p[3].strip()})

    st.markdown("---")
    if st.button("🖨️ CETAK SEKARANG"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

# 3. RENDER DOKUMEN
if daftar:
    # --- 1. SPT (TANPA MENIMBANG) ---
    st.markdown(f"""<div class="kertas-a4">
        <div class="kop-surat"></div>
        <h3 align="center" class="text-underline">SURAT PERINTAH TUGAS</h3>
        <p align="center" style="margin-top:-10px;">Nomor: {no_spt}</p><br>
        <table class="tabel-excel no-border">
            <tr><td width="15%">Dasar</td><td width="2%">:</td><td>DPA Satuan Kerja Perangkat Daerah Sekretariat Daerah Kabupaten Ngada Tahun Anggaran 2026.</td></tr>
        </table>
        <p align="center" class="text-bold" style="margin:25px 0;">MEMERINTAHKAN:</p>
        <table class="tabel-excel">
            <tr align="center" style="background:#f2f2f2; font-weight:bold;">
                <td width="8%">No</td><td>Nama / NIP</td><td>Pangkat / Gol</td><td>Jabatan</td>
            </tr>
            {"".join([f"<tr><td align='center'>{i+1}</td><td>{p['nama']}<br>NIP. {p['nip']}</td><td align='center'>{p['gol']}</td><td>{p['jab']}</td></tr>" for i, p in enumerate(daftar)])}
        </table>
        <p style="margin-top:20px;">Untuk: {maksud} ke {tujuan} selama {lama} hari kerja terhitung mulai tanggal {format_indo(tgl_p)} s/d {format_indo(tgl_k)}.</p>
        <div style="margin-left:55%; margin-top:50px; text-align:center;">
            <p>Dikeluarkan di: Bajawa</p>
            <p>Pada Tanggal: {format_indo(datetime.now())}</p>
            <b>{pemberi.upper()}</b><br><br><br><br><b>{nama_ttd}</b>
        </div>
    </div>""", unsafe_allow_html=True)

    for p in daftar:
        # --- 2. SPD DEPAN ---
        st.markdown(f"""<div class="kertas-a4">
            <div class="kop-surat
