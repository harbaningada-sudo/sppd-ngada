import streamlit as st
import pandas as pd
from datetime import datetime
import logo  # Memanggil file logo.py di GitHub kamu

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Ngada", layout="wide")

# Database Register (Tersimpan otomatis selama sesi aktif)
if 'db_reg' not in st.session_state:
    st.session_state.db_reg = []

# CSS UNTUK PRESISI CETAK LEGAL (FIT TO SHEET)
st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    .main-container { display: flex; flex-direction: column; align-items: center; color: black; background-color: #525659; padding: 20px 0; }
    
    /* KERTAS LEGAL PORTRAIT */
    .kertas { 
        background: white !important; width: 215.9mm; height: 330mm; 
        padding: 12mm 15mm; margin-bottom: 20px; box-shadow: 0 0 15px rgba(0,0,0,0.5);
        font-family: Arial, sans-serif; font-size: 10.5pt; color: black !important;
        page-break-after: always; overflow: hidden; position: relative;
    }
    
    /* KERTAS LANDSCAPE UNTUK REGISTER */
    .kertas-landscape { width: 330mm !important; height: 215.9mm !important; padding: 15mm !important; }

    /* LINE SPACING SESUAI PERMINTAAN */
    .kop-table { width: 100%; border-bottom: 3.5pt solid black; margin-bottom: 8px; border-collapse: collapse; }
    .kop-teks { text-align: center; line-height: 1.0 !important; }
    .kop-teks h3, .kop-teks h2, .kop-teks p { margin: 0; padding: 1px 0; }
    
    .judul-dokumen { text-align: center; line-height: 1.0 !important; margin: 10px 0; font-weight: bold; }
    .judul-dokumen u { font-size: 11pt; }

    /* TABEL SPD DEPAN (Line Spacing 1.0) */
    .tabel-border { width: 100%; border-collapse: collapse; border: 1pt solid black; table-layout: fixed; }
    .tabel-border td { border: 1pt solid black; padding: 4px 6px; vertical-align: top; line-height: 1.0 !important; }
    .col-no { width: 30px !important; text-align: left; }

    /* TABEL VISUM BELAKANG */
    .visum-box { width: 100%; border-collapse: collapse; height: 85%; }
    .visum-box td { border: 1pt solid black; padding: 8px; vertical-align: top; height: 180px; }
    .sub-visum { width: 100%; border: none; }
    .sub-visum td { border: none; padding: 0; height: auto; line-height: 1.2; }

    /* TANDA TANGAN */
    .ttd-box { margin-left: 55%; margin-top: 15px; line-height: 1.2; }

    @media print {
        [data-testid="stSidebar"], .stButton, .no-print { display: none !important; }
        .main-container { background: none !important; padding: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; transform: scale(1.0); }
        @page { size: legal; margin: 0; }
        .reg-landscape { @page { size: legal landscape; } }
    }
</style>
""", unsafe_allow_html=True)

# 2. PANEL KONTROL SIDEBAR
with st.sidebar:
    st.header("📋 PANEL KONTROL")
    menu = st.radio("Menu", ["Input & Cetak", "Register Data"])
    
    if menu == "Input & Cetak":
        with st.expander("👤 DATA PEGAWAI (Dinamis)", expanded=True):
            if 'n_peg' not in st.session_state: st.session_state.n_peg = 1
            c1, c2 = st.columns(2)
            if c1.button("➕ Pegawai"): st.session_state.n_peg += 1
            if c2.button("➖ Hapus") and st.session_state.n_peg > 1: st.session_state.n_peg -= 1
            
            list_pegawai = []
            for i in range(st.session_state.n_peg):
                st.write(f"**Pegawai {i+1}**")
                list_pegawai.append({
                    "nama": st.text_input("Nama/NIP", f"Nama {i+1}", key=f"nm{i}"),
                    "nip": st.text_input("NIP", "19XXXXXXXXXXXXXX", key=f"np{i}"),
                    "spd": st.text_input("No SPD", "530 /.../2026", key=f"sp{i}"),
                    "gol": st.text_input("Gol/Jab", "III/a - Pelaksana", key=f"gj{i}")
                })

        with st.expander("📄 RINCIAN TUGAS"):
            no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
            maksud = st.text_area("Maksud Tugas", "Mendampingi kunjungan...")
            tujuan = st.text_input("Tempat Tujuan", "Riung")
            tgl_bkt = st.date_input("Tgl Berangkat", datetime.now())
            tgl_kbl = st.date_input("Tgl Kembali", datetime.now())
            lama = st.text_input("Lama Perjalanan", "1 (Satu) hari")

        st.subheader("🖋️ PENANDATANGAN")
        pjb = st.text_input("Nama Pejabat", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
        jab = st.text_input("Jabatan", "Pj. Sekretaris Daerah")
        ub = st.text_input("Ub. (Jika ada)", "Asisten Perekonomian dan Pembangunan")

        if st.button("💾 SIMPAN & CETAK"):
            # Auto-save ke Register
            for p in list_pegawai:
                st.session_state.db_reg.append({
                    "Nama": p['nama'], "SPT": no_spt, "SPD": p['spd'],
                    "Tujuan": tujuan, "Bkt": tgl_bkt.strftime("%d/%m/%Y"),
                    "Kbl": tgl_kbl.strftime("%d/%m/%Y"), "Lama": lama
                })
            st.components.v1.html("<script>setTimeout(function(){ window.parent.print(); }, 1000);</script>", height=0)

# --- KONSTRUKSI HTML ---
kop = f'''
<table class="kop-table">
    <tr>
        <td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td>
        <td class="kop-teks">
            <h3>PEMERINTAH KABUPATEN NGADA</h3>
            <h2>SEKRETARIAT DAERAH</h2>
            <p>Jln. Soekarno - Hatta No. 1 Bajawa</p>
        </td>
    </tr>
</table>
'''

def format_ttd(nama, space=80):
    ub_teks = f"Ub. {ub},<br>" if ub else ""
    return f'''<div class="ttd-box"><b>An. BUPATI NGADA</b><br>{jab},<br>{ub_teks}<div style="height:{space}px;"></div><b><u>{nama}</u></b><br>NIP. 19710328 199203 1 011</div>'''

if menu == "Input & Cetak":
    html_final = '<div class="main-container">'
    
    # 1. SPT (KOLEKTIF)
    rows_peg = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{idx+1}.</td><td>Nama: <b>{p['nama']}</b><br>NIP: {p['nip']}</td></tr>" for idx, p in enumerate(list_pegawai)])
    html_final += f'<div class="kertas">{kop}<div class="judul-dokumen"><u>SURAT PERINTAH TUGAS</u><br>Nomor: {no_spt}</div><div style="line-height:1.5; margin-top:15px;"><table class="sub-visum">{rows_peg}</table><p>Untuk: {maksud} ke {tujuan}</p></div>{format_ttd(pjb)}</div>'
    
    # 2. SPD DEPAN (PER ORANG)
    for p in list_pegawai:
        html_final += f'''<div class="kertas">{kop}<div style="margin-left:60%; line-height:1.0;">Kode No: 094<br>Nomor: {p['spd']}</div><div class="judul-dokumen"><u>SURAT PERJALANAN DINAS</u><br>(SPD)</div>
            <table class="tabel-border">
                <tr><td class="col-no">1.</td><td width="42%">Pejabat pemberi perintah</td><td>BUPATI NGADA</td></tr>
                <tr><td class="col-no">2.</td><td>Nama Pegawai diperintah</td><td><b>{p['nama']}</b></td></tr>
                <tr><td class="col-no">3.</td><td>Pangkat / Jabatan / Gol</td><td>{p['gol']}</td></tr>
                <tr><td class="col-no">4.</td><td>Maksud Perjalanan</td><td>{maksud}</td></tr>
                <tr><td class="col-no">6.</td><td>Tempat Tujuan</td><td>{tujuan}</td></tr>
                <tr><td class="col-no">7.</td><td>Lama / Tgl Berangkat</td><td>{lama} / {tgl_bkt.strftime("%d/%m/%Y")}</td></tr>
                <tr><td class="col-no">10.</td><td>Keterangan</td><td>-</td></tr>
            </table>{format_ttd(pjb, 65)}</div>'''
    
    # 3. SPD BELAKANG (CUMA 1 LEMBAR - FULL LEGAL)
    ttd_kecil = f'<div style="text-align:center; line-height:1.1; font-size:9pt;"><br><b>An. BUPATI NGADA</b><br>{jab},<br>Ub. {ub},<div style="height:60px;"></div><b><u>{pjb}</u></b></div>'
    html_final += f'''<div class="kertas"><table class="visum-box">
        <tr><td width="50%"></td><td>I. Berangkat dari: Bajawa<br>Ke: {tujuan}<br>Tgl: {tgl_bkt.strftime("%d/%m/%Y")}{ttd_kecil}</td></tr>
        <tr><td>II. Tiba di: {tujuan}<br>Tgl: {tgl_bkt.strftime("%d/%m/%Y")}</td><td>Berangkat dari: {tujuan}<br>Ke: Bajawa<br>Tgl: {tgl_kbl.strftime("%d/%m/%Y")}</td></tr>
        <tr><td>III. Tiba di:</td><td>Berangkat dari:</td></tr>
        <tr><td>V. Tiba di: Bajawa<br>Tgl: {tgl_kbl.strftime("%d/%m/%Y")}{ttd_kecil}</td><td style="font-size:8pt; font-style:italic;">Telah diperiksa dengan keterangan perjalanan atas perintahnya...</td></tr>
    </table><div style="border:1pt solid black; border-top:none; padding:5px; font-size:8pt; text-align:justify;"><b>VII. Perhatian:</b> Pejabat yang menerbitkan SPD bertanggung jawab atas kerugian negara...</div></div>'''
    
    html_final += '</div>'
    st.markdown(html_final, unsafe_allow_html=True)

# 3. MENU REGISTER
if menu == "Register Data":
    st.title("📂 Register SPD Otomatis")
    if not st.session_state.db_reg:
        st.info("Belum ada data tersimpan.")
    else:
        df = pd.DataFrame(st.session_state.db_reg)
        st.dataframe(df, use_container_width=True)
        
        if st.button("🗑️ Hapus Semua Data"):
            st.session_state.db_reg = []
            st.rerun()
        
        # Format Cetak Register
        rows_reg = "".join([f"<tr><td>{i+1}</td><td>{r['Nama']}</td><td>{r['SPT']}</td><td>{r['SPD']}</td><td>{r['Tujuan']}</td><td>{r['Bkt']}</td><td>{r['Lama']}</td></tr>" for i, r in enumerate(st.session_state.db_reg)])
        st.markdown(f'''<div class="kertas kertas-landscape reg-landscape"><h3>REGISTER PERJALANAN DINAS</h3><table class="tabel-border" style="width:100%; font-size:9pt;">
            <tr><th>No</th><th>Nama</th><th>No SPT</th><th>No SPD</th><th>Tujuan</th><th>Tgl</th><th>Lama</th></tr>{rows_reg}</table></div>''', unsafe_allow_html=True)
