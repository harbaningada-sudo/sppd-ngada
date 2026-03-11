import streamlit as st
from datetime import datetime

# 1. KONFIGURASI HALAMAN & HILANGKAN SIDEBAR STREAMLIT
st.set_page_config(page_title="Sistem SPT & SPPD Ngada", layout="wide")

st.markdown("""
<style>
    /* Menghilangkan elemen default Streamlit agar bersih */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Layout Berdampingan */
    .container {
        display: flex;
        flex-direction: row;
        gap: 20px;
    }
    
    /* Area Input (Kiri) */
    .input-panel {
        width: 30%;
        padding: 20px;
        background-color: #f8f9fa;
        border-right: 1px solid #ddd;
        position: sticky;
        top: 0;
        height: 100vh;
        overflow-y: auto;
    }
    
    /* Area Preview (Kanan) */
    .preview-panel {
        width: 70%;
        background-color: #525659; /* Warna gelap seperti PDF viewer */
        padding: 20px;
        overflow-y: auto;
    }

    /* Kertas A4 Presisi */
    .kertas-a4 {
        background-color: white;
        width: 210mm;
        min-height: 297mm;
        padding: 15mm 20mm;
        margin: 0 auto 20px auto;
        color: black;
        font-family: "Arial", sans-serif;
        font-size: 11pt;
        box-shadow: 0 0 15px rgba(0,0,0,0.5);
        box-sizing: border-box;
    }

    .tabel-sppd {
        width: 100%;
        border: 1.5px solid black;
        border-collapse: collapse;
        table-layout: fixed;
    }
    .tabel-sppd td {
        border: 1.5px solid black;
        padding: 8px;
        vertical-align: top;
        height: 4.5cm;
    }

    /* CSS Khusus Cetak */
    @media print {
        .no-print, .stButton, .input-panel { display: none !important; }
        .preview-panel { width: 100% !important; background: none !important; padding: 0 !important; }
        .kertas-a4 { 
            margin: 0 !important; 
            box-shadow: none !important; 
            border: none !important;
            page-break-after: always;
        }
        @page { size: A4; margin: 0; }
    }
</style>
""", unsafe_allow_html=True)

# 2. FUNGSI TANGGAL INDONESIA
def format_indo(tgl):
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    return f"{tgl.day} {bulan[tgl.month-1]} {tgl.year}"

# 3. STRUKTUR APLIKASI
# Menggunakan kolom streamlit agar tetap responsif tapi dengan style kita
col_kiri, col_kanan = st.columns([1, 2.5])

with col_kiri:
    st.subheader("📋 Input Data")
    no_spt = st.text_input("Nomor SPT", "094/Perekonomian/2026")
    maksud = st.text_area("Maksud Tugas", "Perjalanan Dinas...")
    tujuan = st.text_input("Tujuan", "Kupang")
    tgl_pergi = st.date_input("Berangkat", datetime(2026, 2, 9))
    tgl_kembali = st.date_input("Kembali", datetime(2026, 2, 11))
    
    st.markdown("---")
    st.write("👥 **Daftar Pegawai**")
    input_pegawai = st.text_area("Nama | NIP (Per Baris)", 
                                 "RAYMUNDUS BENA, S.S., M.Hum | 19XXXXXXXXXXXXXX\nNAMA PEGAWAI LAIN | 19YYYYYYYYYYYYYY")
    
    daftar_pegawai = []
    for line in input_pegawai.split('\n'):
        if '|' in line:
            n, ni = line.split('|')
            daftar_pegawai.append({"nama": n.strip(), "nip": ni.strip()})

    st.markdown("---")
    if st.button("🖨️ CETAK SEKARANG"):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

with col_kanan:
    if daftar_pegawai:
        # --- HALAMAN DEPAN ---
        rows = "".join([f"<tr><td style='text-align:center;'>{i+1}</td><td>{p['nama']}</td><td>{p['nip']}</td></tr>" for i, p in enumerate(daftar_pegawai)])
        st.markdown(f"""
        <div class="kertas-a4">
            <h3 style="text-align:center; text-decoration:underline; margin-bottom:5px;">SURAT PERINTAH TUGAS</h3>
            <p style="text-align:center; margin-top:0;">Nomor: {no_spt}</p>
            <br>
            <p><b>MEMERINTAHKAN:</b></p>
            <table border="1" style="width:100%; border-collapse:collapse;">
                <tr style="background:#eee;">
                    <th style="width:10%;">No</th><th>Nama</th><th>NIP</th>
                </tr>
                {rows}
            </table>
            <br>
            <p>Untuk: {maksud} ke {tujuan} pada tanggal {format_indo(tgl_pergi)} s/d {format_indo(tgl_kembali)}.</p>
            <div style="margin-left:55%; margin-top:50px; text-align:center;">
                <p>Bajawa, {format_indo(datetime.now())}</p>
                <b>BUPATI NGADA</b><br><br><br><br>
                <u><b>RAYMUNDUS BENA, S.S., M.Hum</b></u>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # --- HALAMAN BELAKANG (PER PEGAWAI) ---
        for p in daftar_pegawai:
            st.markdown(f"""
            <div class="kertas-a4">
                <table class="tabel-sppd">
                    <tr style="height: 5cm;">
                        <td style="width: 45%;"></td>
                        <td>
                            I. &nbsp; Berangkat dari : Bajawa <br>
                            &nbsp;&nbsp;&nbsp;&nbsp; Ke : {tujuan} <br>
                            &nbsp;&nbsp;&nbsp;&nbsp; Pada Tanggal : {format_indo(tgl_pergi)} <br>
                            <div style="text-align:center; margin-top:20px;">
                                <b>BUPATI NGADA</b><br><br><br><br>
                                <u><b>{p['nama']}</b></u>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td>II. Tiba : {tujuan}<br>Tgl: {format_indo(tgl_pergi)}</td>
                        <td>Berangkat dari : {tujuan}<br>Ke: Bajawa<br>Tgl: {format_indo(tgl_kembali)}</td>
                    </tr>
                    <tr><td>III. Tiba di :</td><td>Berangkat dari :</td></tr>
                    <tr><td>IV. Tiba di :</td><td>Berangkat dari :</td></tr>
                    <tr style="height: 5cm;">
                        <td>V. Tiba Kembali : Bajawa<br>Tgl: {format_indo(tgl_kembali)}</td>
                        <td>
                            <div style="font-style:italic; font-size:9pt;">Telah diperiksa...</div>
                            <div style="text-align:center; margin-top:20px;">
                                <b>BUPATI NGADA</b><br><br><br>
                                <b>.......................................</b>
                            </div>
                        </td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
