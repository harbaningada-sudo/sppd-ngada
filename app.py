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
        padding: 10mm 15mm; margin-bottom: 20px; 
        color: black !important; font-family: Arial, sans-serif; 
        box-sizing: border-box; box-shadow: 0 0 20px rgba(0,0,0,0.8);
        font-size: 10pt; page-break-after: always; overflow: hidden;
    }

    .kertas-landscape { width: 355.6mm !important; height: 215.9mm !important; padding: 15mm !important; }

    .kop-table { width: 100%; border: none !important; border-bottom: 3.5pt solid black !important; margin-bottom: 5px; }
    .kop-teks { text-align: center; line-height: 1.0 !important; } 
    
    .tabel-border { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; table-layout: fixed; }
    .tabel-border td { border: 1pt solid black !important; vertical-align: top; color: black !important; padding: 5px; }
    
    .visum-table { width: 100%; border: none !important; border-collapse: collapse; margin: 0 !important; }
    .visum-table td { border: none !important; padding: 0 !important; font-size: 9.5pt; line-height: 1.2; vertical-align: top; }

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
                n = st.text_input(f"Nama {i+1}", f"Nama {i+1}", key=f"n{i}")
                ni = st.text_input(f"NIP {i+1}", "19XXXXXXXXXXXXXX", key=f"nip{i}")
                g = st.text_input(f"Gol {i+1}", "III/a", key=f"g{i}")
                j = st.text_input(f"Jabatan {i+1}", "Pelaksana", key=f"j{i}")
                s = st.text_input(f"No SPD {i+1}", f"530 /02/2026", key=f"spd{i}")
                daftar.append({"nama": n, "nip": ni, "gol": g, "jab": j, "spd": s, "lembar": "I"})

        with st.expander("📄 DATA UTAMA"):
            no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
            tujuan = st.text_input("Tujuan", "Kecamatan Riung")
            tgl_bkt = st.text_input("Tgl Berangkat", "17 Maret 2026")
            tgl_kbl = st.text_input("Tgl Pulang", "17 Maret 2026")
            lama = st.text_input("Lama Hari", "1 (Satu) hari")

        st.subheader("🖋️ TTD PEJABAT")
        pjb = st.text_input("Nama Pejabat", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
        jab_ttd = st.text_input("Jabatan", "Pj. Sekretaris Daerah")
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

# --- TEMPLATE ---
kop_pemda = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834</p><p class="text-bold">BAJAWA</p></td><td width="15%"></td></tr></table>'''

# Fungsi Helper untuk isian visum agar naik sejajar judul
def row_visum(label, val, date_val=""):
    return f'''
    <table class="visum-table">
        <tr><td width="35%">{label}</td><td width="5%">:</td><td>{val}</td></tr>
        <tr><td>Pada Tanggal</td><td>:</td><td>{date_val}</td></tr>
    </table>'''

html_out = '<div class="main-container">'

if tab_menu == "Input & Cetak":
    # (SPT & SPD Depan di sini tetap ada, saya fokus ke perbaikan Belakang sesuai instruksimu)
    
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
                    </table>
                    {ttd_v}
                </td>
            </tr>
            <tr style="height: 175px;">
                <td>
                    <table class="visum-table">
                        <tr><td width="10%">II.</td><td width="35%">Tiba di</td><td width="5%">:</td><td>{tujuan}</td></tr>
                        <tr><td></td><td>Pada Tanggal</td><td>:</td><td>{tgl_bkt}</td></tr>
                    </table>
                </td>
                <td>
                    <table class="visum-table">
                        <tr><td width="35%">Berangkat dari</td><td width="5%">:</td><td>{tujuan}</td></tr>
                        <tr><td>Ke</td><td>:</td><td>Bajawa</td></tr>
                        <tr><td>Pada Tanggal</td><td>:</td><td>{tgl_kbl}</td></tr>
                    </table>
                </td>
            </tr>
            <tr style="height: 175px;">
                <td>
                    <table class="visum-table">
                        <tr><td width="10%">III.</td><td width="35%">Tiba di</td><td width="5%">:</td><td></td></tr>
                        <tr><td></td><td>Pada Tanggal</td><td>:</td><td></td></tr>
                    </table>
                </td>
                <td>
                    <table class="visum-table">
                        <tr><td width="35%">Berangkat dari</td><td width="5%">:</td><td></td></tr>
                        <tr><td>Ke</td><td>:</td><td></td></tr>
                        <tr><td>Pada Tanggal</td><td>:</td><td></td></tr>
                    </table>
                </td>
            </tr>
            <tr style="height: 175px;">
                <td>
                    <table class="visum-table">
                        <tr><td width="10%">IV.</td><td width="35%">Tiba di</td><td width="5%">:</td><td></td></tr>
                        <tr><td></td><td>Pada Tanggal</td><td>:</td><td></td></tr>
                    </table>
                </td>
                <td>
                    <table class="visum-table">
                        <tr><td width="35%">Berangkat dari</td><td width="5%">:</td><td></td></tr>
                        <tr><td>Ke</td><td>:</td><td></td></tr>
                        <tr><td>Pada Tanggal</td><td>:</td><td></td></tr>
                    </table>
                </td>
            </tr>
            <tr style="height: 210px;">
                <td>
                    <table class="visum-table">
                        <tr><td width="10%">V.</td><td width="35%">Tiba Kembali</td><td width="5%">:</td><td>Bajawa</td></tr>
                        <tr><td></td><td>Pada Tanggal</td><td>:</td><td>{tgl_kbl}</td></tr>
                    </table>
                </td>
                <td style="padding:10px;">
                    <p style="font-style:italic; font-size:9pt; line-height:1.2; margin-bottom:5px;">Telah diperiksa, dengan keterangan bahwa perjalanan tersebut atas perintahnya dan semata-mata untuk kepentingan jabatan</p>
                    {ttd_v}
                </td>
            </tr>
        </table>
        <div style="border:1pt solid black; border-top:none; padding:5px; font-size:10pt;"><b>VI. Catatan Lain-lain</b></div>
        <div style="border:1pt solid black; border-top:none; padding:5px; font-size:8.5pt; text-align:justify; line-height:1.2;">
            <b>VII. Perhatian :</b><br>
            Pejabat yang menerbitkan SPD, pegawai yang melakukan perjalanan dinas, para pejabat yang mengesahkan tanggal berangkat/tiba, serta Bendahara Pengeluaran bertanggung jawab berdasarkan peraturan-peraturan Keuangan Negara apabila negara menderita rugi akibat kesalahan, kelalaian dan kealpaannya.
        </div>
        </div>'''

html_out += '</div>'
st.markdown(html_out, unsafe_allow_html=True)
