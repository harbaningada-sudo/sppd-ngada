import streamlit as st
import pandas as pd
from datetime import datetime
import io

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Export SPD Excel - Ngada", layout="wide")

st.title("📂 Export SPPD ke Excel")
st.write("Isi data di sidebar, lalu unduh file Excel yang sudah terformat rapi.")

# 2. PANEL INPUT SIDEBAR
with st.sidebar:
    st.header("📋 INPUT DATA")
    
    with st.expander("📄 DATA SURAT", expanded=True):
        no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
        kode_no = st.text_input("Kode No", "094/Prokopim")
        maksud = st.text_area("Maksud", "Monitoring dan Pendataan Pemilik Tambang Pasir...")
        tujuan = st.text_input("Tempat Tujuan", "Kecamatan Golewa")
        alat = st.text_input("Alat Angkut", "Mobil")
        lama = st.text_input("Lama Hari", "1 (Satu) hari")
        mata_anggaran = st.text_input("Mata Anggaran (9b)", "1.02.01.2.01.0001")

    with st.expander("👤 DATA PEGAWAI", expanded=True):
        if 'jml' not in st.session_state: st.session_state.jml = 1
        c1, c2 = st.columns(2)
        if c1.button("➕"): st.session_state.jml += 1
        if c2.button("➖") and st.session_state.jml > 1: st.session_state.jml -= 1
        
        daftar = []
        for i in range(st.session_state.jml):
            st.markdown(f"**Pegawai {i+1}**")
            p_n = st.text_input(f"Nama P-{i+1}", f"Nama Pegawai {i+1}", key=f"n{i}")
            p_nip = st.text_input(f"NIP P-{i+1}", "19XXXXXXXXXXXXXX", key=f"nip{i}")
            p_gol = st.text_input(f"Gol P-{i+1}", "Penata Muda - III/a", key=f"g{i}")
            p_jab = st.text_input(f"Jabatan P-{i+1}", "Perencana Ahli Pertama", key=f"j{i}")
            p_spd = st.text_input(f"No SPD P-{i+1}", f"531 /02/2026", key=f"spd{i}")
            p_lbr = st.text_input(f"Lembar P-{i+1}", "I", key=f"lbr{i}")
            daftar.append({"nama": p_n, "nip": p_nip, "gol": p_gol, "jab": p_jab, "spd": p_spd, "lembar": p_lbr})

    with st.expander("🕒 TANDA TANGAN", expanded=False):
        tgl_ctk = st.date_input("Tanggal Cetak", datetime.now())
        pjb_nama = st.text_input("Nama Pejabat", "Dr. Nicolaus Noywuli, S.Pt, M.Si")
        pjb_nip = st.text_input("NIP Pejabat", "19720921 200012 1 004")

# 3. FUNGSI GENERATE EXCEL
def buat_excel():
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    
    # FORMATTING
    f_bold = workbook.add_format({'bold': True, 'font_name': 'Arial', 'font_size': 11})
    f_center = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'font_name': 'Arial'})
    f_header = workbook.add_format({'align': 'center', 'bold': True, 'font_size': 12, 'font_name': 'Arial'})
    f_border = workbook.add_format({'border': 1, 'valign': 'top', 'font_name': 'Arial', 'font_size': 10, 'text_wrap': True})
    f_ttd = workbook.add_format({'font_name': 'Arial', 'font_size': 11})
    f_underline = workbook.add_format({'bold': True, 'underline': True, 'font_name': 'Arial', 'font_size': 11})

    for idx, p in enumerate(daftar):
        sheet_name = f"SPD_{idx+1}"
        worksheet = workbook.add_worksheet(sheet_name[:31])
        
        # Atur Lebar Kolom
        worksheet.set_column('A:A', 4)   # No
        worksheet.set_column('B:B', 30)  # Item
        worksheet.set_column('C:C', 15)  # Data 1
        worksheet.set_column('D:E', 15)  # Data 2
        
        # KOP SURAT (Simulasi teks karena gambar sulit di excel otomatis)
        worksheet.merge_range('A1:E1', 'PEMERINTAH KABUPATEN NGADA', f_header)
        worksheet.merge_range('A2:E2', 'SEKRETARIAT DAERAH', f_header)
        worksheet.merge_range('A3:E3', 'Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834 BAJAWA', f_center)
        worksheet.set_row(3, 15, None, {'level': 0, 'hidden': False, 'bottom': 5}) # Garis bawah kop

        # INFO LEMBAR
        worksheet.write('D5', 'Lembar Ke', f_ttd)
        worksheet.write('E5', f": {p['lembar']}", f_ttd)
        worksheet.write('D6', 'Kode No', f_ttd)
        worksheet.write('E6', f": {kode_no}", f_ttd)
        worksheet.write('D7', 'Nomor', f_ttd)
        worksheet.write('E7', f": {p['spd']}", f_ttd)

        worksheet.merge_range('A9:E9', 'SURAT PERINTAH DINAS (SPD)', f_underline)
        worksheet.write('A9', 'SURAT PERINTAH DINAS (SPD)', workbook.add_format({'align': 'center', 'bold': True, 'underline': True}))

        # TABEL SPD
        data_spd = [
            ['1.', 'Pejabat pemberi perintah', 'BUPATI NGADA'],
            ['2.', 'Nama Pegawai diperintah', p['nama']],
            ['3.', 'a. Pangkat/Golongan', p['gol']],
            ['', 'b. Jabatan', p['jab']],
            ['', 'c. Tingkat Peraturan', ''],
            ['4.', 'Maksud Perjalanan', maksud],
            ['5.', 'Alat angkut', alat],
            ['6.', 'a. Tempat Berangkat', 'Bajawa'],
            ['', 'b. Tempat Tujuan', tujuan],
            ['7.', 'Lamanya Perjalanan', lama],
            ['', 'a. Tanggal Berangkat', str(datetime.now().date())],
            ['', 'b. Tanggal Harus Kembali', str(datetime.now().date())],
            ['8.', 'Pengikut: Nama', 'Tgl Lahir', 'Ket'],
            ['9.', 'Pembebanan Anggaran', ''],
            ['', 'a. Instansi', 'Bagian Perekonomian dan SDA'],
            ['', 'b. Mata Anggaran', mata_anggaran],
            ['10.', 'Keterangan lain-lain', '']
        ]

        row = 10
        for item in data_spd:
            worksheet.write(row, 0, item[0], f_border)
            worksheet.write(row, 1, item[1], f_border)
            if len(item) == 3:
                worksheet.merge_range(row, 2, row, 4, item[2], f_border)
            row += 1

        # TANDA TANGAN
        row += 2
        worksheet.write(row, 3, 'Ditetapkan di : Bajawa', f_ttd)
        worksheet.write(row+1, 3, f"Pada Tanggal : {tgl_ctk}", f_ttd)
        worksheet.write(row+3, 3, 'a.n. BUPATI NGADA', f_bold)
        worksheet.write(row+4, 3, 'Sekretaris Daerah', f_bold)
        worksheet.write(row+7, 3, pjb_nama, f_underline)
        worksheet.write(row+8, 3, f"NIP. {pjb_nip}", f_ttd)

    workbook.close()
    return output.getvalue()

# 4. TOMBOL DOWNLOAD
excel_data = buat_excel()
st.download_button(
    label="📥 Download SPPD (Excel)",
    data=excel_data,
    file_name=f"SPPD_NGADA_{datetime.now().strftime('%Y%m%d')}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.info("💡 Setelah download, buka di Excel dan atur 'Print Area' ke A4 untuk hasil maksimal.")
