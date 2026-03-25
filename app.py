import streamlit as st
import pandas as pd
from datetime import datetime
import logo 

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Ngada Pro", layout="wide")

# INISIALISASI DATABASE REGISTER
if 'arsip_register' not in st.session_state:
    st.session_state.arsip_register = []

# CSS UNTUK PRESISI CETAK FULL LEGAL & LANDSCAPE REGISTER
st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    .stApp { background-color: #525659 !important; }
    .main-container { display: flex; flex-direction: column; align-items: center; width: 100%; padding: 10px 0; }

    .kertas { 
        background-color: white !important; width: 215.9mm; height: 330mm; 
        padding: 10mm 15mm; margin-bottom: 20px; color: black !important; 
        font-family: Arial, sans-serif; box-sizing: border-box; box-shadow: 0 0 20px rgba(0,0,0,0.8);
        font-size: 10.5pt; page-break-after: always; overflow: hidden; position: relative;
    }

    .kertas-landscape { width: 355.6mm !important; height: 215.9mm !important; padding: 15mm !important; }

    .kop-table { width: 100%; border: none !important; border-bottom: 3.5pt solid black !important; margin-bottom: 5px; }
    .kop-table td { border: none !important; padding: 0 !important; vertical-align: middle; }
    .kop-teks { text-align: center; line-height: 1.0 !important; } 
    .kop-teks h3, .kop-teks h2, .kop-teks p { margin: 0; line-height: 1.0 !important; padding: 1px 0; }
    .judul-rapat { text-align: center; line-height: 1.0 !important; margin-top: 5px; }
    .isi-surat-spt { line-height: 1.5 !important; margin-top: 10px; }

    .tabel-border { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; table-layout: fixed; }
    .tabel-border td { border: 1pt solid black !important; padding: 4px 8px !important; vertical-align: top; color: black !important; font-size: 10pt; line-height: 1.1 !important; }
    .col-no { width: 35px !important; text-align: left !important; }

    .visum-table { width: 100%; border: none !important; border-collapse: collapse; margin: 0 !important; }
    .visum-table td { border: none !important; padding: 0 !important; font-size: 10pt; line-height: 1.2; color: black !important; vertical-align: top; }

    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }

    @media print {
        [data-testid="stSidebar"], .stButton, .no-print { display: none !important; }
        .stApp, .main-container { background-color: white !important; padding: 0 !important; margin: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; width: 215.9mm !important; height: 330mm !important; }
        .kertas-landscape { width: 355.6mm !important; height: 215.9mm !important; }
        @page { size: legal portrait; margin: 0; }
        .register-page { @page { size: legal landscape; } }
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 PANEL KONTROL")
    tab_menu = st.radio("Menu", ["Input & Cetak", "Kelola Register"])
    
    if tab_menu == "Input & Cetak":
        jenis_spd = st.selectbox("Jenis Perjalanan", ["Dalam Daerah", "Luar Daerah"])
        opsi_cetak = st.multiselect("Pilih Dokumen", ["SPT", "SPD Depan", "SPD Belakang", "Register"], default=["SPT", "SPD Depan", "SPD Belakang"])
        
        with st.expander("👤 DATA PEGAWAI", expanded=True):
            if 'jml' not in st.session_state: st.session_state.jml = 1
            c1, c2 = st.columns(2)
            if c1.button("➕ Tambah"): st.session_state.jml += 1
            if c2.button("➖ Hapus") and st.session_state.jml > 1: st.session_state.jml -= 1
            
            daftar = []
            for i in range(st.session_state.jml):
                st.markdown(f"**Pegawai {i+1}**")
                daftar.append({
                    "nama": st.text_input(f"Nama", f"Nama {i+1}", key=f"n{i}"),
                    "nip": st.text_input(f"NIP", "19XXXXXXXXXXXXXX", key=f"nip{i}"),
                    "gol": st.text_input(f"Gol", "III/a", key=f"g{i}"),
                    "jab": st.text_input(f"Jabatan", "Pelaksana", key=f"j{i}"),
                    "spd": st.text_input(f"No SPD", f"530 /02/2026", key=f"spd{i}"),
                    "lembar": st.text_input(f"Lembar ke", "I", key=f"lbr{i}")
                })

        with st.expander("📄 DATA UTAMA"):
            no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
            kode_spd = st.text_input("Kode No SPD", "094/Prokopim")
            maksud = st.text_area("Maksud Perjalanan", "Dalam rangka mendampingi...")
            tujuan = st.text_input("Tujuan", "Kecamatan Riung")
            alat = st.text_input("Alat Angkut", "Mobil Dinas")
            lama = st.text_input("Lama Hari", "1 (Satu) hari")
            tgl_bkt = st.text_input("Tanggal Berangkat", "17 Maret 2026")
            tgl_kbl = st.text_input("Tanggal Pulang", "17 Maret 2026")
            ket_reg = st.text_input("Keterangan Register", "-")
            anggaran = st.text_input("Dasar Anggaran", "DPA Bagian Perekonomian dan SDA Setda Ngada 2026")

        if jenis_spd == "Luar Daerah":
            with st.expander("🏢 TUJUAN LUAR DAERAH"):
                instansi_tujuan = st.text_input("Instansi Tujuan", "Kantor Gubernur NTT")
                pjb_tujuan = st.text_input("Pejabat Pengesah", "Nama Pejabat Tujuan")
                gol_tujuan = st.text_input("Pangkat/Gol Tujuan", "Pembina Utama Muda, IV/c")
                nip_tujuan = st.text_input("NIP Pejabat Tujuan", "19XXXXXXXXXXXXXX")

        st.subheader("🖋️ TANDA TANGAN ASAL")
        pjb = st.text_input("Nama Pejabat", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
        gol_pjb = st.text_input("Pangkat/Gol", "Pembina Utama Muda - IV/c")
        jab_ttd = st.text_input("Jabatan Utama", "Pj. Sekretaris Daerah")
        ub = st.text_input("Ub.", "Asisten Perekonomian dan Pembangunan")
        nip_ttd = st.text_input("NIP", "19710328 199203 1 011")

        if st.button("🖨️ PROSES CETAK & SIMPAN"):
            for p in daftar:
                st.session_state.arsip_register.append({
                    "Nama": p['nama'], "No SPT": no_spt, "No SPD": p['spd'],
                    "Berangkat": tgl_bkt, "Pulang": tgl_kbl, "Lama": lama, "Ket": ket_reg
                })
            st.components.v1.html("<script>setTimeout(function(){ window.parent.print(); }, 1200);</script>", height=0)

    elif tab_menu == "Kelola Register":
        st.subheader("📂 RIWAYAT INPUT REGISTER")
        if st.session_state.arsip_register:
            df_reg = pd.DataFrame(st.session_state.arsip_register)
            st.dataframe(df_reg, use_container_width=True)
            idx_hapus = st.number_input("Pilih Indeks", min_value=0, max_value=len(df_reg)-1, step=1)
            if st.button("🗑️ Hapus Baris"):
                st.session_state.arsip_register.pop(idx_hapus)
                st.rerun()
        else: st.info("Kosong.")

# --- TEMPLATE KOMPONEN ---
kop_pemda = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834</p><p class="text-bold">BAJAWA</p></td><td width="15%"></td></tr></table>'''

def get_ttd_statis(nama, gol, nip, space):
    return f'''<div style="text-align:center; line-height:1.2; font-size:10pt;"><b>An. BUPATI NGADA</b><br>{jab_ttd},<br>{f"Ub. {ub}," if ub else ""}<div style="height:{space}px;"></div><b><u>{nama}</u></b><br>{gol}<br>NIP. {nip}</div>'''

html_out = '<div class="main-container">'

if tab_menu == "Input & Cetak":
    # 1. SPT
    if "SPT" in opsi_cetak:
        p_rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{i+1}.</td><td width='20%'>Nama</td><td width='5%'>:</td><td><b>{p['nama']}</b></td></tr><tr><td></td><td></td><td></td><td>Pangkat/Gol</td><td>:</td><td>{p['gol']}</td></tr><tr><td></td><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr><tr><td></td><td></td><td></td><td>Jabatan</td><td>:</td><td>{p['jab']}</td></tr>" for i, p in enumerate(daftar)])
        html_out += f'<div class="kertas">{kop_pemda}<div class="judul-rapat"><h3 class="text-bold underline">SURAT PERINTAH TUGAS</h3><p>NOMOR : {no_spt}</p></div><div class="isi-surat-spt"><table class="visum-table"><tr><td width="12%">Dasar</td><td width="5%">:</td><td>{anggaran}</td></tr></table><p class="text-center text-bold" style="margin:10px 0;">M E M E R I N T A H K A N</p><table class="visum-table">{p_rows}</table><table class="visum-table" style="margin-top:10px;"><tr><td width="12%">Untuk</td><td width="5%">:</td><td>{maksud} ke {tujuan}</td></tr></table></div><div style="margin-left:55%;">{get_ttd_statis(pjb, gol_pjb, nip_ttd, 80)}</div></div>'

    # 2. SPD DEPAN
    for p in daftar:
        if "SPD Depan" in opsi_cetak:
            html_out += f'''<div class="kertas">{kop_pemda}<div style="margin-left:60%; line-height:1.0;"><table class="visum-table"><tr><td width="40%">Lembar ke</td><td width="5%">:</td><td>{p["lembar"]}</td></tr><tr><td>Kode No</td><td>:</td><td>{kode_spd}</td></tr><tr><td>Nomor</td><td>:</td><td>{p["spd"]}</td></tr></table></div><div class="judul-rapat" style="margin-top:5px;"><h3 class="text-bold underline">SURAT PERJALANAN DINAS</h3><h3 class="text-bold">(SPD)</h3></div><table class="tabel-border">
                <tr><td class="col-no">1.</td><td width="42%">Pejabat pemberi perintah</td><td colspan="3"><b>BUPATI NGADA</b></td></tr>
                <tr><td class="col-no">2.</td><td>Nama Pegawai diperintah</td><td colspan="3"><b>{p['nama']}</b></td></tr>
                <tr><td class="col-no" rowspan="3">3.</td><td>a. Pangkat/Golongan</td><td colspan="3">{p['gol']}</td></tr>
                <tr><td>b. Jabatan</td><td colspan="3">{p['jab']}</td></tr>
                <tr><td>c. Tingkat Menurut Peraturan</td><td colspan="3"></td></tr>
                <tr><td class="col-no">4.</td><td>Maksud Perjalanan Dinas</td><td colspan="3">{maksud}</td></tr>
                <tr><td class="col-no">5.</td><td>Alat angkut</td><td colspan="3">{alat}</td></tr>
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
            </table><div style="margin-left:55%;">{get_ttd_statis(pjb, gol_pjb, nip_ttd, 65)}</div></div>'''

    # 3. SPD BELAKANG (VISUM)
    if "SPD Belakang" in opsi_cetak:
        ttd_asal = get_ttd_statis(pjb, gol_pjb, nip_ttd, 65)
        
        # TTD TUJUAN (Hanya muncul jika jenis_spd == "Luar Daerah")
        if jenis_spd == "Luar Daerah":
            ttd_tujuan = f'''<div style="text-align:center; line-height:1.2; font-size:10pt;"><br><b>Mengesahkan</b><br>{instansi_tujuan}<div style="height:65px;"></div><b><u>{pjb_tujuan}</u></b><br>{gol_tujuan}<br>NIP. {nip_tujuan}</div>'''
        else:
            ttd_tujuan = ""

        def rv(num, label, val, d_v, is_n=True):
            n_c = f'<td width="10%">{num}</td>' if is_n else ""
            return f'''<table class="visum-table"><tr>{n_c}<td width="35%">{label}</td><td width="5%">:</td><td>{val}</td></tr><tr>{"<td></td>" if is_n else ""}<td>Pada Tanggal</td><td>:</td><td>{d_v}</td></tr></table>'''

        html_out += f'''<div class="kertas"><table class="tabel-border" style="height:88%;">
            <tr style="height: 220px;"><td width="50%"></td><td style="padding:10px;">{rv("I.", "Berangkat dari", "Bajawa", tgl_bkt)}<table class="visum-table"><tr><td width="10%"></td><td width="35%">Ke</td><td width="5%">:</td><td>{tujuan}</td></tr></table>{ttd_asal}</td></tr>
            <tr style="height: 190px;"><td>{rv("II.", "Tiba di", tujuan, tgl_bkt)}</td><td style="padding:10px;">{rv("", "Berangkat dari", tujuan, tgl_kbl, False)}<table class="visum-table"><tr><td width="35%">Ke</td><td width="5%">:</td><td>Bajawa</td></tr></table>{ttd_tujuan}</td></tr>
            <tr style="height: 190px;"><td>{rv("III.", "Tiba di", "", "")}</td><td style="padding:10px;">{rv("", "Berangkat dari", "", "", False)}</td></tr>
            <tr style="height: 190px;"><td>{rv("IV.", "Tiba di", "", "")}</td><td style="padding:10px;">{rv("", "Berangkat dari", "", "", False)}</td></tr>
            <tr style="height: 220px;"><td>{rv("V.", "Tiba Kembali", "Bajawa", tgl_kbl)}</td><td style="padding:10px;"><p style="font-style:italic; font-size:9.2pt; line-height:1.2; margin-top:5px;">Telah diperiksa, dengan keterangan bahwa perjalanan tersebut atas perintahnya dan semata-mata untuk kepentingan jabatan</p>{ttd_asal}</td></tr>
        </table>
        <div style="border:1pt solid black; border-top:none; padding:8px; font-size:10.5pt;"><b>VI. Catatan Lain-lain</b></div>
        <div style="border:1pt solid black; border-top:none; padding:8px; font-size:8.6pt; text-align:justify; color:black; line-height:1.2;">
            <b>VII. Perhatian :</b><br>
            Pejabat yang menerbitkan SPD, pegawai yang melakukan perjalanan dinas, para pejabat yang mengesahkan tanggal berangkat/tiba, serta Bendahara Pengeluaran bertanggung jawab berdasarkan peraturan-peraturan Keuangan Negara apabila negara menderita rugi akibat kesalahan, kelalaian dan kealpaannya.
        </div></div>'''

    # 4. REGISTER
    if "Register" in opsi_cetak:
        r_rows = "".join([f"<tr><td class='text-center'>{i+1}</td><td>{r['Nama']}</td><td>{r['No SPT']}</td><td>{r['No SPD']}</td><td>{r['Berangkat']}</td><td>{r['Pulang']}</td><td>{r['Lama']}</td><td>-</td></tr>" for i, r in enumerate(st.session_state.arsip_register)])
        html_out += f'''<div class="kertas kertas-landscape register-page"><h3 class="text-center text-bold">REGISTER SURAT PERJALANAN DINAS</h3><br><table class="tabel-border" style="font-size:9pt; width:100%;"><thead><tr style="background:#eee;"><th>No</th><th>Nama Pegawai</th><th>Nomor SPT</th><th>Nomor SPD</th><th>Tgl Bkt</th><th>Tgl Kbl</th><th>Lamanya</th><th>Ket</th></tr></thead><tbody>{r_rows}</tbody></table></div>'''

html_out += '</div>'
st.markdown(html_out, unsafe_allow_html=True)
