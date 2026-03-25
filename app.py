import streamlit as st
import pandas as pd
from datetime import datetime
import logo 

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Ngada Pro", layout="wide")

if 'arsip_register' not in st.session_state:
    st.session_state.arsip_register = []

# CSS UNTUK PRESISI CETAK FULL LEGAL
st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    .stApp { background-color: #525659 !important; }

    .main-container {
        display: flex; flex-direction: column; align-items: center; width: 100%; padding: 10px 0;
    }

    .kertas { 
        background-color: white !important; 
        width: 215.9mm; height: 330mm; 
        padding: 12mm 15mm; margin-bottom: 20px; 
        color: black !important; font-family: Arial, sans-serif; 
        box-sizing: border-box; box-shadow: 0 0 20px rgba(0,0,0,0.8);
        font-size: 10.5pt; page-break-after: always; overflow: hidden;
    }

    .kertas-landscape { width: 355.6mm !important; height: 215.9mm !important; padding: 15mm !important; }

    .kop-table { width: 100%; border: none !important; border-bottom: 3.5pt solid black !important; margin-bottom: 5px; border-collapse: collapse; }
    .kop-teks { text-align: center; line-height: 1.0 !important; } 
    .kop-teks h3, .kop-teks h2, .kop-teks p { margin: 0; padding: 1px 0; line-height: 1.0; }
    
    .judul-rapat { text-align: center; line-height: 1.0 !important; margin: 10px 0; font-weight: bold; }
    
    .tabel-border { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; table-layout: fixed; }
    .tabel-border td { border: 1pt solid black !important; vertical-align: top; color: black !important; padding: 5px; line-height: 1.0; }
    
    .col-no { width: 35px !important; text-align: left !important; }

    .visum-table { width: 100%; border: none !important; border-collapse: collapse; margin: 0 !important; }
    .visum-table td { border: none !important; padding: 0 !important; font-size: 10pt; line-height: 1.1; vertical-align: top; }

    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }

    @media print {
        [data-testid="stSidebar"], .stButton, .no-print { display: none !important; }
        .stApp, .main-container { background-color: white !important; padding: 0 !important; margin: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; width: 215.9mm !important; height: 330mm !important; }
        @page { size: legal portrait; margin: 0; }
        .register-page { @page { size: legal landscape; } }
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 PANEL KONTROL")
    tab_menu = st.radio("Menu", ["Input & Cetak", "Kelola Register"])
    
    if tab_menu == "Input & Cetak":
        opsi_cetak = st.multiselect("Pilih Dokumen", ["SPT", "SPD Depan", "SPD Belakang", "Register"], default=["SPT", "SPD Depan", "SPD Belakang"])
        
        with st.expander("👤 DATA PEGAWAI", expanded=True):
            if 'jml' not in st.session_state: st.session_state.jml = 1
            c1, c2 = st.columns(2)
            if c1.button("➕ Tambah"): st.session_state.jml += 1
            if c2.button("➖ Hapus") and st.session_state.jml > 1: st.session_state.jml -= 1
            
            daftar = []
            for i in range(st.session_state.jml):
                st.markdown(f"**Pegawai {i+1}**")
                n = st.text_input(f"Nama {i+1}", f"Nama {i+1}", key=f"n{i}")
                ni = st.text_input(f"NIP {i+1}", "19XXXXXXXXXXXXXX", key=f"nip{i}")
                g = st.text_input(f"Gol {i+1}", "III/a", key=f"g{i}")
                j = st.text_input(f"Jabatan {i+1}", "Pelaksana", key=f"j{i}")
                s = st.text_input(f"No SPD {i+1}", f"530 /02/2026", key=f"spd{i}")
                daftar.append({"nama": n, "nip": ni, "gol": g, "jab": j, "spd": s, "lembar": "I"})

        with st.expander("📄 DATA UTAMA"):
            no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
            kode_spd = st.text_input("Kode No SPD", "094/Prokopim")
            maksud = st.text_area("Maksud Perjalanan", "Dalam rangka mendampingi...")
            tujuan = st.text_input("Tujuan", "Kecamatan Riung")
            tgl_bkt = st.text_input("Tgl Berangkat", "17 Maret 2026")
            tgl_kbl = st.text_input("Tgl Pulang", "17 Maret 2026")
            lama = st.text_input("Lama Hari", "1 (Satu) hari")
            anggaran = st.text_input("Dasar Anggaran", "DPA Bagian Perekonomian dan SDA Setda Ngada 2026")

        st.subheader("🖋️ TANDA TANGAN")
        pjb = st.text_input("Nama Pejabat", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
        jab_ttd = st.text_input("Jabatan Utama", "Pj. Sekretaris Daerah")
        ub = st.text_input("Ub.", "Asisten Perekonomian dan Pembangunan")

        if st.button("🖨️ PROSES CETAK & SIMPAN"):
            for p in daftar:
                st.session_state.arsip_register.append({
                    "Nama": p['nama'], "No SPT": no_spt, "No SPD": p['spd'],
                    "Berangkat": tgl_bkt, "Pulang": tgl_kbl, "Lama": lama, "Ket": "-"
                })
            st.components.v1.html("<script>setTimeout(function(){ window.parent.print(); }, 1200);</script>", height=0)

    elif tab_menu == "Kelola Register":
        st.subheader("📂 RIWAYAT REGISTER")
        if st.session_state.arsip_register:
            df_reg = pd.DataFrame(st.session_state.arsip_register)
            st.dataframe(df_reg, use_container_width=True)
            if st.button("🧹 Kosongkan Semua Data"):
                st.session_state.arsip_register = []
                st.rerun()
        else:
            st.info("Belum ada data.")

# --- TEMPLATE KOMPONEN ---
kop_pemda = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834</p><p class="text-bold">BAJAWA</p></td><td width="15%"></td></tr></table>'''

def render_ttd(space=70):
    return f'''<div style="margin-left:55%; text-align:center; line-height:1.2; font-size:10.5pt;"><b>An. BUPATI NGADA</b><br>{jab_ttd},<br>{f"Ub. {ub}," if ub else ""}<div style="height:{space}px;"></div><b><u>{pjb}</u></b><br>NIP. 19710328 199203 1 011</div>'''

html_out = '<div class="main-container">'

if tab_menu == "Input & Cetak":
    # 1. SPT (KOLEKTIF)
    if "SPT" in opsi_cetak:
        p_rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{i+1}.</td><td width='20%'>Nama</td><td width='5%'>:</td><td><b>{p['nama']}</b></td></tr><tr><td></td><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr>" for i, p in enumerate(daftar)])
        html_out += f'<div class="kertas">{kop_pemda}<div class="judul-rapat"><h3 class="text-bold underline">SURAT PERINTAH TUGAS</h3><p>NOMOR : {no_spt}</p></div><div class="isi-surat-spt"><table class="visum-table"><tr><td width="12%">Dasar</td><td width="5%">:</td><td>{anggaran}</td></tr></table><p class="text-center text-bold" style="margin:10px 0;">M E M E R I N T A H K A N</p><table class="visum-table">{p_rows}</table><table class="visum-table" style="margin-top:10px;"><tr><td width="12%">Untuk</td><td width="5%">:</td><td>{maksud} ke {tujuan}</td></tr></table></div>{render_ttd(85)}</div>'

    # 2. SPD DEPAN (PER PEGAWAI)
    for p in daftar:
        if "SPD Depan" in opsi_cetak:
            html_out += f'''<div class="kertas">{kop_pemda}<div style="margin-left:60%; line-height:1.0;"><table class="visum-table"><tr><td width="40%">Lembar ke</td><td width="5%">:</td><td>{p["lembar"]}</td></tr><tr><td>Kode No</td><td>:</td><td>{kode_spd}</td></tr><tr><td>Nomor</td><td>:</td><td>{p["spd"]}</td></tr></table></div><div class="judul-rapat" style="margin-top:5px;"><h3 class="text-bold underline">SURAT PERJALANAN DINAS</h3><h3 class="text-bold">(SPD)</h3></div><table class="tabel-border">
                <tr><td class="col-no">1.</td><td width="42%">Pejabat pemberi perintah</td><td colspan="3"><b>BUPATI NGADA</b></td></tr>
                <tr><td class="col-no">2.</td><td>Nama Pegawai diperintahkan</td><td colspan="3"><b>{p['nama']}</b></td></tr>
                <tr><td class="col-no" rowspan="3">3.</td><td>a. Pangkat/Golongan</td><td colspan="3">{p['gol']}</td></tr>
                <tr><td>b. Jabatan</td><td colspan="3">{p['jab']}</td></tr>
                <tr><td>c. Tingkat Peraturan</td><td colspan="3">-</td></tr>
                <tr><td class="col-no">4.</td><td>Maksud Perjalanan Dinas</td><td colspan="3">{maksud}</td></tr>
                <tr><td class="col-no">5.</td><td>Alat angkut</td><td colspan="3">Mobil Dinas</td></tr>
                <tr><td class="col-no" rowspan="2">6.</td><td>a. Tempat Berangkat</td><td colspan="3">Bajawa</td></tr>
                <tr><td>b. Tempat Tujuan</td><td colspan="3">{tujuan}</td></tr>
                <tr><td class="col-no" rowspan="3">7.</td><td>Lamanya Perjalanan Dinas</td><td colspan="3">{lama}</td></tr>
                <tr><td>a. Tanggal Berangkat</td><td colspan="3">{tgl_bkt}</td></tr>
                <tr><td>b. Tanggal Harus Kembali</td><td colspan="3">{tgl_kbl}</td></tr>
                <tr><td class="col-no">8.</td><td>Pengikut</td><td colspan="3">-</td></tr>
                <tr><td class="col-no" rowspan="3">9.</td><td>Pembebanan Anggaran</td><td colspan="3"></td></tr>
                <tr><td>a. Instansi</td><td colspan="3">a. Bagian Perekonomian dan SDA</td></tr>
                <tr><td>b. Mata Anggaran</td><td colspan="3"></td></tr>
                <tr><td class="col-no">10.</td><td>Keterangan lain-lain</td><td colspan="3"></td></tr>
            </table>{render_ttd(70)}</div>'''

    # 3. SPD BELAKANG (CUMA 1 LEMBAR - LOGIKA GAMBAR)
    if "SPD Belakang" in opsi_cetak:
        ttd_v = f'''<div style="text-align:center; line-height:1.2; font-size:9.5pt;">
            <br><b>An. BUPATI NGADA</b><br>{jab_ttd},<br>{f"Ub. {ub}," if ub else ""}<div style="height:70px;"></div>
            <b><u>{pjb}</u></b><br>NIP. 19710328 199203 1 011</div>'''

        html_out += f'''<div class="kertas">
        <table class="tabel-border" style="height:90%;">
            <tr style="height: 210px;">
                <td width="50%"></td>
                <td style="padding:10px;">
                    <table class="visum-table">
                        <tr><td width="10%">I.</td><td width="35%">Berangkat dari</td><td width="5%">:</td><td>Bajawa</td></tr>
                        <tr><td></td><td>Ke</td><td>:</td><td>{tujuan}</td></tr>
                        <tr><td></td><td>Pada Tanggal</td><td>:</td><td>{tgl_bkt}</td></tr>
                    </table>{ttd_v}
                </td>
            </tr>
            <tr style="height: 175px;">
                <td><table class="visum-table"><tr><td width="10%">II.</td><td width="35%">Tiba di</td><td width="5%">:</td><td>{tujuan}</td></tr><tr><td></td><td>Pada Tanggal</td><td>:</td><td>{tgl_bkt}</td></tr></table></td>
                <td><table class="visum-table"><tr><td width="35%">Berangkat dari</td><td width="5%">:</td><td>{tujuan}</td></tr><tr><td>Ke</td><td>:</td><td>Bajawa</td></tr><tr><td>Pada Tanggal</td><td>:</td><td>{tgl_kbl}</td></tr></table></td>
            </tr>
            <tr style="height: 175px;">
                <td><table class="visum-table"><tr><td width="10%">III.</td><td width="35%">Tiba di</td><td width="5%">:</td><td></td></tr><tr><td></td><td>Pada Tanggal</td><td>:</td><td></td></tr></table></td>
                <td><table class="visum-table"><tr><td width="35%">Berangkat dari</td><td width="5%">:</td><td></td></tr><tr><td>Ke</td><td>:</td><td></td></tr><tr><td>Pada Tanggal</td><td>:</td><td></td></tr></table></td>
            </tr>
            <tr style="height: 175px;">
                <td><table class="visum-table"><tr><td width="10%">IV.</td><td width="35%">Tiba di</td><td width="5%">:</td><td></td></tr><tr><td></td><td>Pada Tanggal</td><td>:</td><td></td></tr></table></td>
                <td><table class="visum-table"><tr><td width="35%">Berangkat dari</td><td width="5%">:</td><td></td></tr><tr><td>Ke</td><td>:</td><td></td></tr><tr><td>Pada Tanggal</td><td>:</td><td></td></tr></table></td>
            </tr>
            <tr style="height: 210px;">
                <td><table class="visum-table"><tr><td width="10%">V.</td><td width="35%">Tiba Kembali</td><td width="5%">:</td><td>Bajawa</td></tr><tr><td></td><td>Pada Tanggal</td><td>:</td><td>{tgl_kbl}</td></tr></table></td>
                <td style="padding:10px;"><p style="font-style:italic; font-size:9pt; line-height:1.2;">Telah diperiksa, dengan keterangan perjalanan atas perintahnya dan semata-mata untuk kepentingan jabatan</p>{ttd_v}</td>
            </tr>
        </table>
        <div style="border:1pt solid black; border-top:none; padding:5px; font-size:10pt;"><b>VI. Catatan Lain-lain</b></div>
        <div style="border:1pt solid black; border-top:none; padding:5px; font-size:8.5pt; text-align:justify; line-height:1.2;">
            <b>VII. Perhatian :</b> Pejabat yang menerbitkan SPD... bertanggung jawab... apabila negara menderita rugi...
        </div></div>'''

    # 4. REGISTER (MENGAMBIL DARI DATABASE)
    if "Register" in opsi_cetak:
        r_rows = "".join([f"<tr><td class='text-center'>{i+1}</td><td>{r['Nama']}</td><td>{r['No SPT']}</td><td>{r['No SPD']}</td><td>{r['Berangkat']}</td><td>{r['Pulang']}</td><td>{r['Lama']}</td><td>-</td></tr>" for i, r in enumerate(st.session_state.arsip_register)])
        html_out += f'''<div class="kertas kertas-landscape register-page"><h3 class="text-center text-bold">REGISTER SURAT PERJALANAN DINAS</h3><br><table class="tabel-border" style="font-size:9pt; width:100%;"><thead><tr style="background:#eee;"><th>No</th><th>Nama</th><th>Nomor SPT</th><th>Nomor SPD</th><th>Tgl Bkt</th><th>Tgl Kbl</th><th>Lama</th><th>Ket</th></tr></thead><tbody>{r_rows}</tbody></table></div>'''

html_out += '</div>'
st.markdown(html_out, unsafe_allow_html=True)
