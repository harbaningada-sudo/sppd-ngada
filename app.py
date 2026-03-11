import streamlit as st
from datetime import datetime

# 1. KONFIGURASI HALAMAN WIDE & BERSIH
st.set_page_config(page_title="Sistem SPT & SPPD Ngada", layout="wide")

st.markdown("""
<style>
    /* Sembunyikan elemen Streamlit */
    header, footer, #MainMenu {visibility: hidden;}
    
    /* Layout Kiri-Kanan */
    .main-container {
        display: flex;
        gap: 20px;
    }
    
    /* Kertas Preview (Kanan) */
    .preview-area {
        background-color: #525659;
        padding: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    /* FORMAT KERTAS A4 SESUAI TEMPLATE */
    .kertas-a4 {
        background-color: white;
        width: 210mm;
        min-height: 297mm;
        padding: 10mm 15mm;
        margin-bottom: 20px;
        color: black;
        font-family: Arial, sans-serif;
        font-size: 10pt;
        box-shadow: 0 0 10px rgba(0,0,0,0.5);
        box-sizing: border-box;
    }

    /* TABEL SPPD BELAKANG (SANGAT PRESISI) */
    .tabel-template {
        width: 100%;
        border: 1.5px solid black;
        border-collapse: collapse;
        table-layout: fixed;
    }
    .tabel-template td {
        border: 1.5px solid black;
        padding: 10px;
        vertical-align: top;
    }

    /* Pembagian kolom agar garis tengah agak ke kanan (sesuai gambar) */
    .col-kiri { width: 45%; }
    .col-kanan { width: 55%; }

    /* Pengaturan Tinggi Baris agar pas 1 halaman */
    .row-stempel { height: 5.2cm; }
    .row-biasa { height: 4.5cm; }

    @media print {
        .no-print, .stSidebar, .stButton { display: none !important; }
        @page { size: A4; margin: 0; }
        .kertas-a4 { 
            margin: 0 !important; 
            box-shadow: none !important; 
            border: none !important;
            page-break-after: always;
        }
    }
</style>
""", unsafe_allow_html=True)

def format_indo(tgl):
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    return f"{tgl.day} {bulan[tgl.month-1]} {tgl.year}"

# 2. PANEL INPUT (KIRI)
with st.sidebar:
    st.header("📋 Data Surat")
    no_spt = st.text_input("Nomor SPT", "094/Perekonomian/2026")
    maksud = st.text_area("Maksud Tugas", "Perjalanan Dinas...")
    tujuan = st.text_input("Tujuan", "Kupang")
    tgl_p = st.date_input("Berangkat", datetime(2026, 2, 9))
    tgl_k = st.date_input("Kembali", datetime(2026, 2, 11))
    
    st.markdown("---")
    st.write("👥 **Data Pegawai**")
    input_pegawai = st.text_area("Nama | NIP (Per Baris)", 
                                 "RAYMUNDUS BENA, S.S., M.Hum | 19XXXXXXXXXXXXXX")
    
    daftar = []
    for line in input_pegawai.split('\n'):
        if '|' in line:
            n, ni = line.split('|')
            daftar.append({"nama": n.strip(), "nip": ni.strip()})

    if st.button("🖨️ CETAK SEKARANG"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

# 3. PANEL PREVIEW (KANAN)
if daftar:
    # --- HALAMAN SPT ---
    st.markdown(f"""
    <div class="kertas-a4">
        <h3 style="text-align:center; text-decoration:underline;">SURAT PERINTAH TUGAS</h3>
        <p style="text-align:center;">Nomor: {no_spt}</p>
        <br><br>
        <p><b>MEMERINTAHKAN:</b></p>
        <table border="1" style="width:100%; border-collapse:collapse;">
            <tr style="background:#eee;"><th>No</th><th>Nama</th><th>NIP</th></tr>
            {"".join([f"<tr><td align='center'>{i+1}</td><td>{p['nama']}</td><td>{p['nip']}</td></tr>" for i, p in enumerate(daftar)])}
        </table>
        <br>
        <p>Untuk: {maksud} ke {tujuan} pada tanggal {format_indo(tgl_p)} s/d {format_indo(tgl_k)}.</p>
        <div style="margin-left:55%; margin-top:50px; text-align:center;">
            <p>Bajawa, {format_indo(datetime.now())}</p>
            <b>BUPATI NGADA</b><br><br><br><br>
            <u><b>RAYMUNDUS BENA, S.S., M.Hum</b></u>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- HALAMAN BELAKANG (PER PEGAWAI) ---
    for p in daftar:
        st.markdown(f"""
        <div class="kertas-a4">
            <table class="tabel-template">
                <tr class="row-stempel">
                    <td class="col-kiri"></td>
                    <td class="col-kanan">
                        I. &nbsp; Berangkat dari : Bajawa <br>
                        &nbsp;&nbsp;&nbsp;&nbsp; Ke : {tujuan} <br>
                        &nbsp;&nbsp;&nbsp;&nbsp; Pada Tanggal : {format_indo(tgl_p)} <br>
                        <div style="text-align:center; margin-top:15px;">
                            <b>BUPATI NGADA</b><br><br><br><br>
                            <u><b>{p['nama']}</b></u>
                        </div>
                    </td>
                </tr>
                <tr class="row-biasa">
                    <td>II. Tiba : {tujuan}<br>Tgl: {format_indo(tgl_p)}</td>
                    <td>Berangkat dari : {tujuan}<br>Ke: Bajawa<br>Tgl: {format_indo(tgl_k)}</td>
                </tr>
                <tr class="row-biasa"><td>III. Tiba di :</td><td>Berangkat dari :</td></tr>
                <tr class="row-biasa"><td>IV. Tiba di :</td><td>Berangkat dari :</td></tr>
                <tr class="row-stempel">
                    <td>V. Tiba Kembali : Bajawa<br>Tgl: {format_indo(tgl_k)}</td>
                    <td>
                        <div style="font-style:italic; font-size:8.5pt;">Telah diperiksa, dengan keterangan bahwa perjalanan tersebut atas perintahnya dan semata-mata untuk kepentingan jabatan.</div>
                        <div style="text-align:center; margin-top:15px;">
                            <b>BUPATI NGADA</b><br><br><br>
                            <b>.......................................</b>
                        </div>
                    </td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
