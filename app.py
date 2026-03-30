import streamlit as st
import pandas as pd
from datetime import datetime
import logo  

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Ngada Pro", layout="wide")

if 'arsip_register' not in st.session_state:
    st.session_state.arsip_register = []

# CSS UNTUK PRESISI CETAK (FIX TERPOTONG)
st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    .stApp { background-color: #525659 !important; }
    .main-container { display: flex; flex-direction: column; align-items: center; width: 100%; padding: 10px 0; }

    /* KERTAS UMUM (PORTRAIT LEGAL) */
    .kertas { 
        background-color: white !important; 
        width: 215.9mm; height: 330mm; 
        padding: 10mm 15mm; margin-bottom: 20px; 
        color: black !important; font-family: Arial, sans-serif; 
        box-sizing: border-box; box-shadow: 0 0 20px rgba(0,0,0,0.8);
        font-size: 10.5pt; page-break-after: always; overflow: hidden; position: relative;
    }

    /* KHUSUS REGISTER LANDSCAPE (FIX TERPOTONG) */
    .kertas-landscape { 
        width: 330mm !important; /* Standar Legal Landscape */
        height: 215.9mm !important; 
        padding: 10mm !important; 
    }

    .kop-table { width: 100%; border: none !important; border-bottom: 3.5pt solid black !important; margin-bottom: 5px; }
    .kop-teks { text-align: center; line-height: 1.0 !important; } 
    
    .judul-rapat { text-align: center; line-height: 1.0 !important; margin-top: 5px; }
    .tabel-border { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; table-layout: fixed; }
    .tabel-border th, .tabel-border td { border: 1pt solid black !important; padding: 4px 6px !important; vertical-align: top; color: black !important; word-wrap: break-word; }

    /* CSS KHUSUS TABLE REGISTER AGAR MUAT */
    .table-reg { font-size: 8pt !important; width: 100% !important; border-collapse: collapse; }
    .table-reg th { background-color: #eeeeee !important; -webkit-print-color-adjust: exact; }

    @media print {
        [data-testid="stSidebar"], .stButton, .no-print { display: none !important; }
        .stApp, .main-container { background-color: white !important; padding: 0 !important; margin: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; }
        @page { size: legal portrait; margin: 0mm; }
        .register-page { @page { size: legal landscape; margin: 5mm; } }
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 PANEL KONTROL")
    wilayah = st.selectbox("Jenis Wilayah", ["Dalam Daerah", "Luar Daerah"])
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
                daftar.append({
                    "nama": st.text_input(f"Nama", f"Nama {i+1}", key=f"n{i}"),
                    "nip": st.text_input(f"NIP", "19XXXXXXXXXXXXXX", key=f"nip{i}"),
                    "gol": st.text_input(f"Gol", "III/a", key=f"g{i}"),
                    "jab": st.text_input(f"Jabatan", "Pelaksana", key=f"j{i}"),
                    "spd": st.text_input(f"No SPD", f"530 /.../2026", key=f"spd{i}"),
                    "lembar": st.text_input(f"Lembar ke", "I", key=f"lbr{i}")
                })

        with st.expander("📄 DATA UTAMA"):
            no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
            kode_spd = st.text_input("Kode SPD", "094/Prokopim")
            maksud = st.text_area("Maksud", "Dalam rangka...")
            tujuan = st.text_input("Tujuan", "Kecamatan Riung")
            tgl_bkt = st.text_input("Tgl Bkt", "17 Maret 2026")
            tgl_kbl = st.text_input("Tgl Kbl", "17 Maret 2026")
            lama = st.text_input("Lama Hari", "1 (Satu) hari")
            
            default_dasar = "DPA Bagian Perekonomian dan SDA Setda Ngada 2026" if wilayah == "Dalam Daerah" else ""
            anggaran = st.text_area("Dasar Anggaran", value=default_dasar)

        st.subheader("🖋️ TANDA TANGAN")
        ttd_label = st.selectbox("Label TTD", ["An. BUPATI NGADA", "WAKIL BUPATI NGADA", "BUPATI NGADA"])
        pjb = st.text_input("Nama Pejabat", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
        gol_pjb = st.text_input("Pangkat/Gol", "Pembina Utama Muda - IV/c")
        jab_ttd = st.text_input("Jabatan", "Pj. Sekretaris Daerah")
        ub = st.text_input("Ub", "Asisten Perekonomian dan Pembangunan")
        nip_ttd = st.text_input("NIP", "19710328 199203 1 011")

        if st.button("🖨️ PROSES CETAK & SIMPAN"):
            for p in daftar:
                st.session_state.arsip_register.append({
                    "Nama": p['nama'], "No SPT": no_spt, "No SPD": p['spd'],
                    "Tujuan": tujuan, "Berangkat": tgl_bkt, "Pulang": tgl_kbl, "Lama": lama, "Ket": wilayah
                })
            st.components.v1.html("<script>setTimeout(function(){ window.parent.print(); }, 1000);</script>", height=0)

    elif tab_menu == "Kelola Register":
        st.subheader("📂 RIWAYAT REGISTER")
        if st.session_state.arsip_register:
            df_reg = pd.DataFrame(st.session_state.arsip_register)
            st.dataframe(df_reg, use_container_width=True)
            if st.button("🧹 Kosongkan Data"):
                st.session_state.arsip_register = []
                st.rerun()

# --- TEMPLATE RENDER ---
def get_ttd(space): 
    lbl = ttd_label
    jab_f = f"{jab_ttd}," if lbl == "An. BUPATI NGADA" else ""
    ub_f = f"Ub. {ub}," if (ub and lbl == "An. BUPATI NGADA") else ""
    return f'''<div style="margin-left:55%; margin-top:10px; line-height:1.2; text-align:center;"><b>{lbl}</b><br>{jab_f}<br>{ub_f}<div style="height:{space}px;"></div><b><u>{pjb}</u></b><br>{gol_pjb}<br>NIP. {nip_ttd}</div>'''

kop_pemda = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p class="text-bold">BAJAWA</p></td><td width="15%"></td></tr></table>'''

html_out = '<div class="main-container">'

if tab_menu == "Input & Cetak":
    # 1. SPT
    if "SPT" in opsi_cetak:
        kop_spt = f'<div class="kop-garuda"><img src="data:image/png;base64,{logo.GARUDA}" width="75"><h2>BUPATI NGADA</h2></div>' if wilayah == "Luar Daerah" else kop_pemda
        p_rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{i+1}.</td><td width='20%'>Nama</td><td width='5%'>:</td><td><b>{p['nama']}</b></td></tr><tr><td></td><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr>" for i, p in enumerate(daftar)])
        html_out += f'<div class="kertas">{kop_spt}<div class="judul-rapat"><h3 class="underline">SURAT PERINTAH TUGAS</h3><p>NOMOR : {no_spt}</p></div><div class="isi-surat-spt"><table class="visum-table"><tr><td width="12%">Dasar</td><td width="5%">:</td><td>{anggaran}</td></tr></table><p class="text-center text-bold" style="margin:10px 0;">M E M E R I N T A H K A N</p><table class="visum-table">{p_rows}</table><div style="height:25px;"></div><table class="visum-table"><tr><td width="12%">Untuk</td><td width="5%">:</td><td>{maksud} ke {tujuan}</td></tr></table></div>{get_ttd(80)}</div>'

    # 2. SPD DEPAN (FULL LENGKAP)
    for p in daftar:
        if "SPD Depan" in opsi_cetak:
            html_out += f'''<div class="kertas">{kop_pemda}<div style="margin-left:60%; line-height:1.0;"><table class="visum-table"><tr><td width="40%">Lembar ke</td><td width="5%">:</td><td>{p["lembar"]}</td></tr><tr><td>Kode No</td><td>:</td><td>{kode_spd}</td></tr><tr><td>Nomor</td><td>:</td><td>{p["spd"]}</td></tr></table></div><div class="judul-rapat"><h3>SURAT PERJALANAN DINAS (SPD)</h3></div><table class="tabel-border" style="margin-top:10px;">
                <tr><td class="col-no">1.</td><td width="42%">Pejabat pemberi perintah</td><td colspan="3"><b>BUPATI NGADA</b></td></tr>
                <tr><td class="col-no">2.</td><td>Nama Pegawai diperintah</td><td colspan="3"><b>{p['nama']}</b></td></tr>
                <tr><td class="col-no">6.</td><td>Tempat Tujuan</td><td colspan="3">{tujuan}</td></tr>
                <tr><td class="col-no">9.</td><td>Pembebanan Anggaran</td><td colspan="3">a. Bagian Perekonomian dan SDA</td></tr>
            </table>{get_ttd(65)}</div>'''

    # 3. SPD BELAKANG (LENGKAP POIN I - VII)
    if "SPD Belakang" in opsi_cetak:
        ttd_bk = get_ttd(50)
        def rv(n, l, v, d, is_n=True):
            n_c = f'<td width="8%">{n}</td>' if is_n else ""
            return f'''<table class="visum-table"><tr>{n_c}<td width="37%">{l}</td><td width="5%">:</td><td>{v}</td></tr><tr>{"<td></td>" if is_n else ""}<td>Pada Tanggal</td><td>:</td><td>{d}</td></tr></table>'''
        kiri_ii = rv("II.", "Tiba di", tujuan, tgl_bkt) if wilayah == "Dalam Daerah" else f'<table class="visum-table"><tr><td width="8%">II.</td><td width="37%">Tiba di</td><td width="5%">:</td><td>{tujuan}</td></tr></table>'
        html_out += f'''<div class="kertas"><table class="tabel-border" style="height:80%;">
            <tr style="height:170px;"><td width="50%"></td><td>{rv("I.", "Berangkat dari", "Bajawa", tgl_bkt)}<br>{ttd_bk}</td></tr>
            <tr style="height:150px;"><td>{kiri_ii}</td><td>{rv("", "Berangkat dari", tujuan, tgl_kbl, False)}</td></tr>
            <tr style="height:150px;"><td>{rv("III.", "Tiba di", "", "")}</td><td>{rv("", "Berangkat dari", "", "", False)}</td></tr>
            <tr style="height:170px;"><td>{rv("V.", "Tiba Kembali", "Bajawa", tgl_kbl)}</td><td><p style="font-style:italic; font-size:9pt;">Telah diperiksa...</p>{ttd_bk}</td></tr>
            </table><div style="border:1pt solid black; border-top:none; padding:5px; font-size:8pt;"><b>VI. Catatan Lain-lain</b><br><b>VII. Perhatian:</b> Pejabat yang menerbitkan SPD... bertanggung jawab...</div></div>'''

    # 4. REGISTER (FIX TERPOTONG)
    if "Register" in opsi_cetak:
        r_rows = "".join([f"<tr><td class='text-center'>{i+1}</td><td>{r['Nama']}</td><td>{r['No SPT']}</td><td>{r['No SPD']}</td><td>{r['Tujuan']}</td><td class='text-center'>{r['Berangkat']}</td><td class='text-center'>{r['Pulang']}</td><td class='text-center'>{r['Lama']}</td><td>{r['Ket']}</td></tr>" for i, r in enumerate(st.session_state.arsip_register)])
        html_out += f'''<div class="kertas kertas-landscape register-page">
            <h3 class="text-center text-bold">REGISTER SURAT PERJALANAN DINAS</h3><br>
            <table class="tabel-border table-reg">
                <thead><tr><th width="30">No</th><th>Nama Pegawai</th><th width="150">Nomor SPT</th><th width="150">Nomor SPD</th><th>Tempat Tujuan</th><th width="80">Tgl Bkt</th><th width="80">Tgl Kbl</th><th width="60">Lama</th><th width="80">Wilayah</th></tr></thead>
                <tbody>{r_rows}</tbody>
            </table>
        </div>'''

html_out += '</div>'
st.markdown(html_out, unsafe_allow_html=True)
