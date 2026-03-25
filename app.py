import streamlit as st
import pandas as pd
from datetime import datetime
import logo  # Memanggil file logo.py di repository kamu

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Ngada Pro", layout="wide")

# 2. DATABASE REGISTER (Session State)
if 'db_register' not in st.session_state:
    st.session_state.db_register = []

# CSS UNTUK PRESISI CETAK FULL LEGAL & LANDSCAPE
st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    .stApp { background-color: #525659 !important; }

    .main-container {
        display: flex; flex-direction: column; align-items: center; width: 100%; padding: 10px 0;
    }

    /* KERTAS UMUM (PORTRAIT LEGAL) */
    .kertas { 
        background-color: white !important; 
        width: 215.9mm; height: 330mm; 
        padding: 12mm 15mm; margin-bottom: 20px; 
        color: black !important; font-family: Arial, sans-serif; 
        box-sizing: border-box; box-shadow: 0 0 20px rgba(0,0,0,0.8);
        font-size: 10.5pt; page-break-after: always; overflow: hidden;
    }

    /* KHUSUS REGISTER (LANDSCAPE) */
    .kertas-landscape { width: 330mm !important; height: 215.9mm !important; padding: 15mm !important; }

    /* KOP & JUDUL (1.0 Rapat) */
    .kop-table { width: 100%; border: none !important; border-bottom: 3.5pt solid black !important; margin-bottom: 5px; }
    .kop-table td { border: none !important; padding: 0 !important; vertical-align: middle; }
    .kop-teks { text-align: center; line-height: 1.0 !important; } 
    .kop-teks h3, .kop-teks h2, .kop-teks p { margin: 0; line-height: 1.0 !important; padding: 1px 0; }
    
    .judul-rapat { text-align: center; line-height: 1.0 !important; margin-top: 5px; }
    .judul-rapat h3, .judul-rapat p { margin: 0; line-height: 1.0 !important; }

    /* ISI NARASI SPT (Line Spacing 1.5) */
    .isi-surat-spt { line-height: 1.5 !important; margin-top: 10px; }

    /* TABEL SPD DEPAN (Line Spacing 1.0) */
    .tabel-border { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; table-layout: fixed; }
    .tabel-border td, .tabel-border th { border: 1pt solid black !important; padding: 5px 8px !important; vertical-align: top; color: black !important; line-height: 1.1 !important; }
    
    /* FIX NOMOR 1. sd 10. */
    .col-no { width: 35px !important; text-align: left !important; }

    /* TABEL VISUM */
    .visum-table { width: 100%; border: none !important; border-collapse: collapse; margin: 0 !important; }
    .visum-table td { border: none !important; padding: 0 !important; line-height: 1.2; color: black !important; vertical-align: top; }

    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }

    @media print {
        [data-testid="stSidebar"], .stButton, .no-print { display: none !important; }
        .stApp, .main-container { background-color: white !important; padding: 0 !important; margin: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; width: 215.9mm !important; height: 330mm !important; }
        .kertas-landscape { width: 330mm !important; height: 215.9mm !important; }
        @page { size: legal portrait; margin: 0; }
        .register-page { @page { size: legal landscape; } }
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 PANEL KONTROL")
    menu = st.radio("Pilih Menu", ["Input & Cetak", "Lihat & Hapus Register"])
    
    if menu == "Input & Cetak":
        opsi = st.multiselect("Dokumen Dicetak", ["SPT", "SPD Depan", "SPD Belakang"], default=["SPT", "SPD Depan", "SPD Belakang"])
        with st.expander("👤 DATA PEGAWAI", expanded=True):
            if 'jml' not in st.session_state: st.session_state.jml = 1
            c1, c2 = st.columns(2)
            if c1.button("➕ Tambah"): st.session_state.jml += 1
            if c2.button("➖ Hapus") and st.session_state.jml > 1: st.session_state.jml -= 1
            
            daftar = []
            for i in range(st.session_state.jml):
                n = st.text_input(f"Nama P-{i+1}", f"Nama {i+1}", key=f"n{i}")
                ni = st.text_input(f"NIP P-{i+1}", "19XXXXXXXXXXXXXX", key=f"ni{i}")
                g = st.text_input(f"Gol P-{i+1}", "III/a", key=f"g{i}")
                j = st.text_input(f"Jabatan P-{i+1}", "Pelaksana", key=f"j{i}")
                s = st.text_input(f"No SPD P-{i+1}", f"530 /02/2026", key=f"s{i}")
                daftar.append({"nama": n, "nip": ni, "gol": g, "jab": j, "spd": s})

        with st.expander("📄 DATA UTAMA"):
            no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
            tujuan = st.text_input("Tujuan", "Riung")
            tgl_bkt = st.date_input("Tanggal Berangkat", datetime.now())
            tgl_kbl = st.date_input("Tanggal Pulang", datetime.now())
            lama = st.text_input("Lama Hari", "1 (Satu) hari")
            ket = st.text_input("Keterangan", "-")

    st.subheader("🖋️ PENANDATANGAN")
    pjb = st.text_input("Nama Pejabat", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
    jab_ttd = st.text_input("Jabatan Utama", "Pj. Sekretaris Daerah")
    ub = st.text_input("Ub.", "Asisten Perekonomian dan Pembangunan")

    if st.button("💾 SIMPAN & PROSES CETAK"):
        # SIMPAN KE REGISTER
        for p in daftar:
            st.session_state.db_register.append({
                "Nama": p['nama'], "SPT": no_spt, "SPD": p['spd'],
                "Tujuan": tujuan, "Berangkat": tgl_bkt.strftime("%d/%m/%Y"),
                "Pulang": tgl_kbl.strftime("%d/%m/%Y"), "Lama": lama, "Ket": ket
            })
        st.components.v1.html("<script>setTimeout(function(){ window.parent.print(); }, 1200);</script>", height=0)

# --- HALAMAN REGISTER ---
if menu == "Lihat & Hapus Register":
    st.title("📂 Register Riwayat SPT/SPD")
    if not st.session_state.db_register:
        st.warning("Belum ada data.")
    else:
        df = pd.DataFrame(st.session_state.db_register)
        
        # Tabel Interaktif dengan Tombol Hapus
        for i, row in df.iterrows():
            col1, col2, col3 = st.columns([1, 8, 2])
            col1.write(f"**{i+1}**")
            col2.write(f"{row['Nama']} | {row['SPT']} | {row['Tujuan']}")
            if col3.button("🗑️ Hapus", key=f"del_{i}"):
                st.session_state.db_register.pop(i)
                st.rerun()

        st.markdown("---")
        # FORMAT CETAK REGISTER LANDSCAPE
        st.subheader("Pratinjau Cetak Register")
        rows_html = "".join([f"<tr><td class='text-center'>{idx+1}</td><td>{r['Nama']}</td><td>{r['SPT']}</td><td>{r['SPD']}</td><td>{r['Berangkat']}</td><td>{r['Pulang']}</td><td>{r['Lama']}</td><td>{r['Ket']}</td></tr>" for idx, r in df.iterrows()])
        
        reg_html = f'''<div class="kertas kertas-landscape register-page"><h3 class="text-center text-bold">REGISTER SURAT PERJALANAN DINAS</h3><br><table class="tabel-border" style="width:100%; font-size:9pt;"><thead><tr style="background:#eee;"><th>No</th><th>Nama</th><th>Nomor SPT</th><th>Nomor SPD</th><th>Tgl Berangkat</th><th>Tgl Pulang</th><th>Lamanya</th><th>Keterangan</th></tr></thead><tbody>{rows_html}</tbody></table></div>'''
        st.markdown(reg_html, unsafe_allow_html=True)
        
        if st.button("🖨️ Cetak Tabel Register"):
            st.components.v1.html("<script>window.parent.print();</script>", height=0)

# --- LOGIKA SURAT (Hanya muncul jika di menu Input) ---
if menu == "Input & Cetak":
    kop_pemda = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td><td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834</p><p class="text-bold">BAJAWA</p></td><td width="15%"></td></tr></table>'''
    ttd_v = f'<div style="margin-left:55%; margin-top:10px; line-height:1.2;"><b>An. BUPATI NGADA</b><br>{jab_ttd},<br>{f"Ub. {ub}," if ub else ""}<div style="height:80px;"></div><b><u>{pjb}</u></b><br>NIP. 19710328 199203 1 011</div>'

    html_out = '<div class="main-container">'
    # SPT
    if "SPT" in opsi:
        p_rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{idx+1}.</td><td width='20%'>Nama</td><td width='5%'>:</td><td><b>{p['nama']}</b></td></tr><tr><td></td><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr>" for idx, p in enumerate(daftar)])
        html_out += f'<div class="kertas">{kop_pemda}<div class="judul-rapat"><h3 class="text-bold underline">SURAT PERINTAH TUGAS</h3><p>NOMOR : {no_spt}</p></div><div class="isi-surat-spt"><table class="visum-table"><tr><td width="12%">Dasar</td><td width="3%">:</td><td>DPA Bagian Perekonomian dan SDA 2026</td></tr></table><p class="text-center text-bold" style="margin:10px 0;">M E M E R I N T A H K A N</p><table class="visum-table">{p_rows}</table><table class="visum-table" style="margin-top:10px;"><tr><td width="12%">Untuk</td><td width="5%">:</td><td>{maksud} ke {tujuan}</td></tr></table></div>{ttd_v}</div>'
    
    # SPD DEPAN
    for p in daftar:
        if "SPD Depan" in opsi:
            html_out += f'''<div class="kertas">{kop_pemda}<div style="margin-left:60%; line-height:1.0;"><table class="visum-table"><tr><td width="40%">Lembar ke</td><td width="5%">:</td><td>I</td></tr><tr><td>Kode No</td><td>:</td><td>094/Prokopim</td></tr><tr><td>Nomor</td><td>:</td><td>{p["spd"]}</td></tr></table></div><div class="judul-rapat" style="margin-top:5px;"><h3 class="text-bold underline">SURAT PERJALANAN DINAS</h3><h3 class="text-bold">(SPD)</h3></div><table class="tabel-border">
                <tr><td class="col-no">1.</td><td width="42%">Pejabat pemberi perintah</td><td colspan="3"><b>BUPATI NGADA</b></td></tr>
                <tr><td class="col-no">2.</td><td>Nama Pegawai diperintah</td><td colspan="3"><b>{p['nama']}</b></td></tr>
                <tr><td class="col-no" rowspan="3">3.</td><td>a. Pangkat/Golongan</td><td colspan="3">{p['gol']}</td></tr>
                <tr><td>b. Jabatan</td><td colspan="3">{p['jab']}</td></tr>
                <tr><td>c. Tingkat Peraturan</td><td colspan="3">-</td></tr>
                <tr><td class="col-no">4.</td><td>Maksud Perjalanan Dinas</td><td colspan="3">{maksud}</td></tr>
                <tr><td class="col-no">5.</td><td>Alat angkut</td><td colspan="3">Mobil Dinas</td></tr>
                <tr><td class="col-no" rowspan="2">6.</td><td>a. Tempat Berangkat</td><td colspan="3">Bajawa</td></tr>
                <tr><td>b. Tempat Tujuan</td><td colspan="3">{tujuan}</td></tr>
                <tr><td class="col-no" rowspan="3">7.</td><td>Lamanya Perjalanan Dinas</td><td colspan="3">{lama}</td></tr>
                <tr><td>a. Tanggal Berangkat</td><td colspan="3">{tgl_bkt.strftime("%d/%m/%Y")}</td></tr>
                <tr><td>b. Tanggal Kembali</td><td colspan="3">{tgl_kbl.strftime("%d/%m/%Y")}</td></tr>
                <tr><td class="col-no">8.</td><td>Pengikut</td><td colspan="3">-</td></tr>
                <tr><td class="col-no" rowspan="3">9.</td><td>Pembebanan Anggaran</td><td colspan="3"></td></tr>
                <tr><td>a. Instansi</td><td colspan="3">a. Bagian Perekonomian dan SDA</td></tr>
                <tr><td>b. Mata Anggaran</td><td colspan="3"></td></tr>
                <tr><td class="col-no">10.</td><td>Keterangan lain-lain</td><td colspan="3"></td></tr>
            </table>{ttd_v}</div>'''
    
    # SPD BELAKANG (CUMA 1 LEMBAR)
    if "SPD Belakang" in opsi:
        def rv(n, l, v, d, is_n=True):
            n_c = f'<td width="10%">{n}</td>' if is_n else ""
            return f'''<table class="visum-table"><tr>{n_c}<td width="35%">{l}</td><td width="5%">:</td><td>{v}</td></tr><tr>{"<td></td>" if is_n else ""}<td>Pada Tanggal</td><td>:</td><td>{d}</td></tr></table>'''
        
        ttd_bk = f'<div style="text-align:center; line-height:1.2; font-size:10pt;"><br><b>An. BUPATI NGADA</b><br>{jab_ttd},<br>{f"Ub. {ub}," if ub else ""}<div style="height:90px;"></div><b><u>{pjb}</u></b><br>NIP. 19710328 199203 1 011</div>'
        
        html_out += f'''<div class="kertas"><table class="tabel-border" style="height:88%;">
            <tr style="height: 220px;"><td width="50%"></td><td style="padding:10px;">{rv("I.", "Berangkat dari", "Bajawa", tgl_bkt.strftime("%d/%m/%Y"))}<table class="visum-table"><tr><td width="10%"></td><td width="35%">Ke</td><td width="5%">:</td><td>{tujuan}</td></tr></table>{ttd_bk}</td></tr>
            <tr style="height: 190px;"><td>{rv("II.", "Tiba di", tujuan, tgl_bkt.strftime("%d/%m/%Y"))}</td><td style="padding:10px;">{rv("", "Berangkat dari", tujuan, tgl_kbl.strftime("%d/%m/%Y"), False)}<table class="visum-table"><tr><td width="35%">Ke</td><td width="5%">:</td><td>Bajawa</td></tr></table></td></tr>
            <tr style="height: 190px;"><td>{rv("III.", "Tiba di", "", "")}</td><td style="padding:10px;">{rv("", "Berangkat dari", "", "", False)}</td></tr>
            <tr style="height: 190px;"><td>{rv("IV.", "Tiba di", "", "")}</td><td style="padding:10px;">{rv("", "Berangkat dari", "", "", False)}</td></tr>
            <tr style="height: 220px;"><td>{rv("V.", "Tiba Kembali", "Bajawa", tgl_kbl.strftime("%d/%m/%Y"))}</td><td style="padding:10px;"><p style="font-style:italic; font-size:9.2pt; line-height:1.2;">Telah diperiksa, dengan keterangan perjalanan atas perintahnya...</p>{ttd_bk}</td></tr>
        </table><div style="border:1pt solid black; border-top:none; padding:8px; font-size:10.5pt;"><b>VI. Catatan Lain-lain</b></div><div style="border:1pt solid black; border-top:none; padding:8px; font-size:8.8pt; text-align:justify; color:black; line-height:1.3;"><b>VII. Perhatian :</b> Pejabat yang menerbitkan SPD... bertanggung jawab... apabila negara menderita rugi...</div></div>'''

    html_out += '</div>'
    st.markdown(html_out, unsafe_allow_html=True)
