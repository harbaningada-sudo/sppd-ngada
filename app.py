import streamlit as st
import pandas as pd
from datetime import datetime
import logo  # Memanggil file logo.py
from io import BytesIO

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Ngada Pro", layout="wide")

# INISIALISASI STATE (Agar data tidak hilang saat ngetik)
if 'arsip_register' not in st.session_state:
    st.session_state.arsip_register = []
if 'jml' not in st.session_state:
    st.session_state.jml = 1

# CSS UNTUK PRESISI CETAK & TAMPILAN UI
st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    
    /* Background aplikasi agar kontras dengan kertas */
    .stApp { background-color: #525659 !important; }
    
    /* Container Kertas */
    .main-container { 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        width: 100%; 
        padding: 10px 0;
    }

    /* KERTAS LEGAL */
    .kertas { 
        background-color: white !important; 
        width: 215.9mm; 
        height: 330mm; 
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

    .kop-table { width: 100%; border: none !important; border-bottom: 3.5pt solid black !important; margin-bottom: 5px; }
    .kop-teks { text-align: center; line-height: 1.0 !important; } 
    .kop-teks h3, .kop-teks h2, .kop-teks p { margin: 0; padding: 1px 0; }

    .tabel-border { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; table-layout: fixed; }
    .tabel-border td { border: 1pt solid black !important; padding: 4px 8px !important; vertical-align: top; color: black !important; font-size: 9.5pt; line-height: 1.1 !important; }
    
    .visum-table { width: 100%; border: none !important; border-collapse: collapse; margin: 0 !important; }
    .visum-table td { border: none !important; padding: 0 !important; font-size: 10pt; line-height: 1.2; color: black !important; vertical-align: top; }

    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }

    @media print {
        [data-testid="stSidebar"], .stButton, .no-print, .stMarkdown:not(.cetak) { display: none !important; }
        .stApp, .main-container { background-color: white !important; padding: 0 !important; margin: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; width: 215.9mm !important; height: 330mm !important; }
        @page { size: legal portrait; margin: 0; }
    }
</style>
""", unsafe_allow_html=True)

# --- PANEL KONTROL (SIDEBAR) ---
with st.sidebar:
    st.header("📋 PANEL KONTROL")
    wilayah = st.selectbox("Jenis Wilayah", ["Dalam Daerah", "Luar Daerah"])
    tab_menu = st.radio("Menu", ["Input & Cetak", "Kelola Register"])
    
    if tab_menu == "Input & Cetak":
        opsi_cetak = st.multiselect("Pilih Dokumen", ["SPT", "SPD Depan", "SPD Belakang"], default=["SPT", "SPD Depan"])
        
        with st.expander("👤 DATA PEGAWAI", expanded=True):
            c1, c2 = st.columns(2)
            if c1.button("➕ Tambah"): st.session_state.jml += 1
            if c2.button("➖ Hapus") and st.session_state.jml > 1: st.session_state.jml -= 1
            
            daftar = []
            for i in range(st.session_state.jml):
                st.markdown(f"**Pegawai {i+1}**")
                daftar.append({
                    "nama": st.text_input(f"Nama", key=f"n{i}"),
                    "nip": st.text_input(f"NIP", key=f"nip{i}"),
                    "gol": st.text_input(f"Gol", key=f"g{i}"),
                    "jab": st.text_input(f"Jabatan", key=f"j{i}"),
                    "spd": st.text_input(f"No SPD", key=f"spd{i}"),
                    "lembar": st.text_input(f"Lembar ke", "I", key=f"lbr{i}")
                })

        with st.expander("📄 DATA UTAMA"):
            no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
            kode_spd = st.text_input("Kode No SPD", "094/Prokopim")
            maksud = st.text_area("Maksud Perjalanan")
            tujuan = st.text_input("Tujuan")
            alat = st.text_input("Alat Angkut", "Mobil Dinas")
            lama = st.text_input("Lama Hari", "1 (Satu) hari")
            tgl_bkt = st.text_input("Tanggal Berangkat")
            tgl_kbl = st.text_input("Tanggal Pulang")
            default_dasar = "DPA Bagian Perekonomian dan SDA Setda Ngada 2026" if wilayah == "Dalam Daerah" else ""
            anggaran = st.text_area("Dasar Anggaran", value=default_dasar)

        st.subheader("🖋️ TANDA TANGAN")
        ttd_label = st.selectbox("Penandatangan", ["An. BUPATI NGADA", "WAKIL BUPATI NGADA", "BUPATI NGADA"])
        pjb = st.text_input("Nama Pejabat", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
        gol_pjb = st.text_input("Pangkat/Gol", "Pembina Utama Muda - IV/c")
        jab_ttd = st.text_input("Jabatan Utama", "Pj. Sekretaris Daerah")
        ub = st.text_input("Ub.", "Asisten Perekonomian dan Pembangunan")
        nip_ttd = st.text_input("NIP", "19710328 199203 1 011")

        if st.button("🖨️ PROSES CETAK & SIMPAN"):
            for p in daftar:
                st.session_state.arsip_register.append({
                    "Nama": p['nama'], "No SPT": no_spt, "No SPD": p['spd'],
                    "Tujuan": tujuan, "Berangkat": tgl_bkt, "Pulang": tgl_kbl, "Lama": lama, "Ket": wilayah
                })
            st.components.v1.html("<script>setTimeout(function(){ window.parent.print(); }, 500);</script>", height=0)

# --- LOGIKA RENDER (Tampil di Layar Utama) ---
if tab_menu == "Input & Cetak":
    # Template TTD
    def get_ttd_html(space): 
        label_final = f"<b>{ttd_label}</b>"
        jab_final = f"{jab_ttd}," if ttd_label == "An. BUPATI NGADA" else ""
        ub_final = f"Ub. {ub}," if (ub and ttd_label == "An. BUPATI NGADA") else ""
        return f'''<div style="margin-left:55%; margin-top:10px; line-height:1.2; text-align:center;">{label_final}<br>{jab_final}<br>{ub_final}<div style="height:{space}px;"></div><b><u>{pjb}</u></b><br>{gol_pjb}<br>NIP. {nip_ttd}</div>'''

    kop_pemda = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834</p><p class="text-bold">BAJAWA</p></td><td width="15%"></td></tr></table>'''

    html_final = '<div class="main-container">'

    # Render SPT
    if "SPT" in opsi_cetak:
        kop_f = f'<div class="kop-garuda" style="text-align:center;"><img src="data:image/png;base64,{logo.GARUDA}" width="70"><br><h2>BUPATI NGADA</h2></div>' if wilayah == "Luar Daerah" else kop_pemda
        p_rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{i+1}.</td><td width='20%'>Nama</td><td width='5%'>:</td><td><b>{p['nama']}</b></td></tr><tr><td></td><td></td><td></td><td>Pangkat/Gol</td><td>:</td><td>{p['gol']}</td></tr><tr><td></td><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr><tr><td></td><td></td><td></td><td>Jabatan</td><td>:</td><td>{p['jab']}</td></tr>" for i, p in enumerate(daftar)])
        html_final += f'<div class="kertas">{kop_f}<div class="judul-rapat"><h3 class="text-bold underline">SURAT PERINTAH TUGAS</h3><p>NOMOR : {no_spt}</p></div><div class="isi-surat-spt"><table class="visum-table"><tr><td width="12%">Dasar</td><td width="5%">:</td><td>{anggaran}</td></tr></table><p class="text-center text-bold" style="margin:10px 0;">M E M E R I N T A H K A N</p><table class="visum-table">{p_rows}</table><table class="visum-table" style="margin-top:25px;"><tr><td width="12%">Untuk</td><td width="5%">:</td><td>{maksud} ke {tujuan}</td></tr></table></div>{get_ttd_html(90)}</div>'

    # Render SPD Depan
    for p in daftar:
        if "SPD Depan" in opsi_cetak:
            html_final += f'''<div class="kertas">{kop_pemda}
                <div style="margin-left:60%; line-height:1.0;"><table class="visum-table"><tr><td width="40%">Lembar ke</td><td width="5%">:</td><td>{p["lembar"]}</td></tr><tr><td>Kode No</td><td>:</td><td>{kode_spd}</td></tr><tr><td>Nomor</td><td>:</td><td>{p["spd"]}</td></tr></table></div>
                <div class="judul-rapat" style="margin-top:5px;"><h3 class="text-bold underline">SURAT PERJALANAN DINAS</h3><h3 class="text-bold">(SPD)</h3></div>
                <table class="tabel-border" style="margin-top:10px;">
                    <tr><td style="width:30px">1.</td><td width="42%">Pejabat pemberi perintah</td><td colspan="3"><b>BUPATI NGADA</b></td></tr>
                    <tr><td>2.</td><td>Nama Pegawai diperintah</td><td colspan="3"><b>{p['nama']}</b></td></tr>
                    <tr><td rowspan="3">3.</td><td>a. Pangkat/Golongan</td><td colspan="3">{p['gol']}</td></tr>
                    <tr><td>b. Jabatan</td><td colspan="3">{p['jab']}</td></tr>
                    <tr><td>c. Tingkat Menurut Peraturan</td><td colspan="3">-</td></tr>
                    <tr><td>4.</td><td>Maksud Perjalanan Dinas</td><td colspan="3">{maksud}</td></tr>
                    <tr><td>5.</td><td>Alat angkut</td><td colspan="3">{alat}</td></tr>
                    <tr><td rowspan="2">6.</td><td>a. Tempat Berangkat</td><td colspan="3">Bajawa</td></tr>
                    <tr><td>b. Tempat Tujuan</td><td colspan="3">{tujuan}</td></tr>
                    <tr><td rowspan="3">7.</td><td>Lamanya Perjalanan Dinas</td><td colspan="3">{lama}</td></tr>
                    <tr><td>a. Tanggal Berangkat</td><td colspan="3">{tgl_bkt}</td></tr>
                    <tr><td>b. Tanggal Harus Kembali</td><td colspan="3">{tgl_kbl}</td></tr>
                    <tr><td>8.</td><td>Pengikut: Nama</td><td class="text-center">Tgl Lahir</td><td colspan="2" class="text-center">Keterangan</td></tr>
                    <tr style="height:20px;"><td></td><td>1.</td><td></td><td colspan="2"></td></tr>
                    <tr><td rowspan="3">9.</td><td>Pembebanan Anggaran</td><td colspan="3"></td></tr>
                    <tr><td>a. Instansi</td><td colspan="3">a. Bagian Perekonomian dan SDA</td></tr>
                    <tr><td>b. Mata Anggaran</td><td colspan="3"></td></tr>
                    <tr><td>10.</td><td>Keterangan lain-lain</td><td colspan="3">-</td></tr>
                </table>{get_ttd_html(65)}</div>'''

    html_final += '</div>'
    st.markdown(html_final, unsafe_allow_html=True)

elif tab_menu == "Kelola Register":
    st.subheader("📂 RIWAYAT INPUT REGISTER")
    if st.session_state.arsip_register:
        df_reg = pd.DataFrame(st.session_state.arsip_register)
        st.dataframe(df_reg, use_container_width=True)
        
        # Excel Download logic
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_reg.to_excel(writer, index=False, sheet_name='Register_SPD')
        st.download_button(label="📥 DOWNLOAD REGISTER (EXCEL)", data=output.getvalue(), file_name=f"Register_SPD_{datetime.now().strftime('%Y%m%d')}.xlsx")
