import streamlit as st
import pandas as pd
from datetime import datetime
import io

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="SPD Ngada - Excel Mode", layout="wide")

st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
</style>
""", unsafe_allow_html=True)

st.title("📂 Export SPPD ke Excel")
st.info("Pastikan sudah membuat file 'requirements.txt' berisi 'xlsxwriter' di GitHub agar tidak error.")

# 2. PANEL INPUT SIDEBAR
with st.sidebar:
    st.header("📋 INPUT DATA")
    
    with st.expander("📄 DATA SURAT", expanded=True):
        no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
        kode_no = st.text_input("Kode No", "094/Prokopim")
        maksud = st.text_area("Maksud", "Monitoring dan Pendataan Pemilik Tambang Pasir...")
        tujuan = st.text_input("Tempat Tujuan", "Kecamatan Golewa")
        alat = st.text_input("Alat Angkut", "Mobil")
        lama_perjalanan = st.text_input("Lama Hari", "1 (Satu) hari")
        mata_anggaran = st.text_input("Mata Anggaran (9b)", "1.02.01.2.01.0001")

    with st.expander("👤 DATA PEGAWAI", expanded=True):
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

    with st.expander("🕒 TTD", expanded=False):
        tgl_ctk = st.date_input("Tanggal Cetak", datetime.now())
        pjb_nama = st.text_input("Nama Pejabat", "Dr. Nicolaus Noywuli, S.Pt, M.Si")
        pjb_nip = st.text_input("NIP Pejabat", "19720921 200012 1 004")

# 3. FUNGSI GENERATE EXCEL
def generate_excel():
    output = io.BytesIO()
    try:
        import xlsxwriter
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        
        # FORMATS
        f_header = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 14, 'font_name': 'Arial'})
        f_sub = workbook.add_format({'align': 'center', 'font_size': 10, 'font_name': 'Arial'})
        f_table = workbook.add_format({'border': 1, 'valign': 'top', 'text_wrap': True, 'font_name': 'Arial', 'font_size': 10})
        f_bold = workbook.add_format({'bold': True, 'font_name': 'Arial', 'font_size': 10})
        f_underline = workbook.add_format({'bold': True, 'underline': True, 'font_name': 'Arial', 'font_size': 11})

        # --- SHEET 1: SPT ---
        ws_spt = workbook.add_worksheet("SPT")
        ws_spt.set_column('A:E', 15)
        ws_spt.merge_range('A1:E1', 'PEMERINTAH KABUPATEN NGADA', f_header)
        ws_spt.merge_range('A2:E2', 'SEKRETARIAT DAERAH', f_header)
        ws_spt.merge_range('A3:E3', 'Jln. Soekarno - Hatta No. 1 BAJAWA', f_sub)
        
        ws_spt.merge_range('A5:E5', 'SURAT PERINTAH TUGAS', f_underline)
        ws_spt.merge_range('A6:E6', f'Nomor : {no_spt}', workbook.add_format({'align': 'center'}))
        
        row_spt = 8
        for i, p in enumerate(daftar):
            ws_spt.write(row_spt, 0, 'Kepada' if i==0 else '', f_bold)
            ws_spt.write(row_spt, 1, f"{i+1}. Nama", f_table)
            ws_spt.merge_range(row_spt, 2, row_spt, 4, p['nama'], f_table)
            ws_spt.write(row_spt+1, 1, "   NIP", f_table)
            ws_spt.merge_range(row_spt+1, 2, row_spt+1, 4, p['nip'], f_table)
            row_spt += 2

        # --- SHEET 2 & 3: SPD ---
        for idx, p in enumerate(daftar):
            ws = workbook.add_worksheet(f"SPD {idx+1}")
            ws.set_column('A:A', 4)
            ws.set_column('B:B', 25)
            ws.set_column('C:E', 18)
            
            ws.merge_range('A1:E1', 'PEMERINTAH KABUPATEN NGADA', f_header)
            ws.merge_range('A2:E2', 'SEKRETARIAT DAERAH', f_header)
            
            items = [
                ['1.', 'Pejabat Pemberi Perintah', 'BUPATI NGADA'],
                ['2.', 'Nama Pegawai', p['nama']],
                ['3.', 'a. Pangkat/Gol', p['gol']],
                ['', 'b. Jabatan', p['jab']],
                ['4.', 'Maksud Perjalanan', maksud],
                ['5.', 'Alat Angkut', alat],
                ['6.', 'Tujuan', tujuan],
                ['7.', 'Lama Hari', lama_perjalanan],
                ['8.', 'Mata Anggaran', mata_anggaran]
            ]
            
            r_spd = 8
            for row_data in items:
                ws.write(r_spd, 0, row_data[0], f_table)
                ws.write(r_spd, 1, row_data[1], f_table)
                ws.merge_range(r_spd, 2, r_spd, 4, row_data[2], f_table)
                r_spd += 1

        workbook.close()
        return output.getvalue()
    except Exception as e:
        return None

# TAMPILKAN TOMBOL DOWNLOAD
excel_data = generate_excel()
if excel_data:
    st.markdown("---")
    st.subheader("✅ File Berhasil Dibuat")
    st.download_button(
        label="📥 Download File Excel Sekarang",
        data=excel_data,
        file_name=f"SPPD_NGADA_{datetime.now().strftime('%d_%m_%Y')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
