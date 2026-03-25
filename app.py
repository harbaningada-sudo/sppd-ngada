import streamlit as st
import pandas as pd
from datetime import datetime
import logo 

# 1. SETUP HALAMAN
st.set_page_config(page_title="SPD Ngada Pro", layout="wide")

if 'db_reg' not in st.session_state:
    st.session_state.db_reg = []

# CSS UNTUK PRESISI CETAK FULL LEGAL & LANDSCAPE
st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .main-container { display: flex; flex-direction: column; align-items: center; color: black; }
    
    /* KERTAS LEGAL PORTRAIT */
    .kertas { 
        background: white !important; width: 215.9mm; height: 330mm; 
        padding: 12mm 15mm; margin-bottom: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.5);
        font-family: Arial; font-size: 10.5pt; page-break-after: always; overflow: hidden;
    }
    
    /* KERTAS LEGAL LANDSCAPE (REGISTER) */
    .kertas-landscape { width: 330mm !important; height: 215.9mm !important; padding: 15mm !important; }

    /* LINE SPACING 1.0 (KOP & JUDUL) */
    .kop-table { width: 100%; border-bottom: 3.5pt solid black; margin-bottom: 5px; line-height: 1.0 !important; border-collapse: collapse; }
    .judul-rapat { text-align: center; line-height: 1.0 !important; margin: 5px 0; font-weight: bold; }
    
    /* TABEL SPD DEPAN */
    .tabel-border { width: 100%; border-collapse: collapse; border: 1pt solid black; table-layout: fixed; }
    .tabel-border td, .tabel-border th { border: 1pt solid black; padding: 5px 8px; vertical-align: top; line-height: 1.1; }
    
    .col-no { width: 35px !important; text-align: left; }

    /* TABEL VISUM BELAKANG */
    .visum-table { width: 100%; border-collapse: collapse; border: none; }
    .visum-table td { padding: 0; line-height: 1.1; vertical-align: top; border: none; }

    @media print {
        [data-testid="stSidebar"], .stButton, .no-print { display: none !important; }
        .stApp { background: white !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; width: 215.9mm !important; height: 330mm !important; }
        @page { size: legal; margin: 0; }
        .reg-landscape { @page { size: legal landscape; } }
    }
</style>
""", unsafe_allow_html=True)

# 2. PANEL KONTROL SIDEBAR
with st.sidebar:
    st.header("📋 PANEL KONTROL")
    menu = st.radio("Pilih Menu", ["Input & Cetak", "Lihat Register"])
    
    if menu == "Input & Cetak":
        opsi_cetak = st.multiselect("Cetak Dokumen", ["SPT", "SPD Depan", "SPD Belakang"], default=["SPT", "SPD Depan", "SPD Belakang"])
        
        with st.expander("👤 DATA PEGAWAI", expanded=True):
            if 'jml' not in st.session_state: st.session_state.jml = 1
            c1, c2 = st.columns(2)
            if c1.button("➕"): st.session_state.jml += 1
            if c2.button("➖") and st.session_state.jml > 1: st.session_state.jml -= 1
            
            daftar = []
            for i in range(st.session_state.jml):
                st.write(f"**Pegawai {i+1}**")
                daftar.append({
                    "nama": st.text_input("Nama", f"Nama {i+1}", key=f"n{i}"),
                    "nip": st.text_input("NIP", "19XXXXXXXXXXXXXX", key=f"ni{i}"),
                    "spd": st.text_input("No SPD", f"530 /02/2026", key=f"s{i}"),
                    "gol": st.text_input("Gol", "III/a", key=f"g{i}"),
                    "jab": st.text_input("Jabatan", "Pelaksana", key=f"j{i}")
                })

        with st.expander("📄 DATA UTAMA"):
            no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
            tujuan = st.text_input("Tujuan", "Riung")
            maksud = st.text_area("Maksud", "Mendampingi kunjungan...")
            tgl_bkt = st.date_input("Tgl Berangkat", datetime.now())
            tgl_kbl = st.date_input("Tgl Kembali", datetime.now())
            lama = st.text_input("Lama Hari", "1 (Satu) hari")
            ket_reg = st.text_input("Keterangan", "-")

        st.subheader("🖋️ TANDA TANGAN")
        pjb = st.text_input("Pejabat Bajawa", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
        jab_pjb = st.text_input("Jabatan Utama", "Pj. Sekretaris Daerah")
        ub = st.text_input("Ub.", "Asisten Perekonomian dan Pembangunan")

        if st.button("💾 SIMPAN & PROSES CETAK"):
            for p in daftar:
                st.session_state.db_reg.append({
                    "Nama": p['nama'], "SPT": no_spt, "SPD": p['spd'],
                    "Tujuan": tujuan, "Bkt": tgl_bkt.strftime("%d/%m/%Y"),
                    "Kbl": tgl_kbl.strftime("%d/%m/%Y"), "Lama": lama, "Ket": ket_reg
                })
            st.components.v1.html("<script>setTimeout(function(){ window.parent.print(); }, 800);</script>", height=0)

# --- KONSTRUKSI SURAT ---
kop = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="70"></td><td class="text-center"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>Jln. Soekarno - Hatta No. 1 Bajawa</p></td><td width="15%"></td></tr></table>'''

def get_ttd(nama, space=80):
    return f'''<div style="margin-left:55%; text-align:center; line-height:1.2;"><b>An. BUPATI NGADA</b><br>{jab_pjb},<br>Ub. {ub},<div style="height:{space}px;"></div><b><u>{nama}</u></b><br>NIP. 19710328 199203 1 011</div>'''

if menu == "Input & Cetak":
    html_all = '<div class="main-container">'
    
    # 1. SPT (Kolektif)
    if "SPT" in opsi_cetak:
        rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{idx+1}.</td><td>Nama: <b>{p['nama']}</b><br>NIP: {p['nip']}</td></tr>" for idx, p in enumerate(daftar)])
        html_all += f'<div class="kertas">{kop}<div class="judul-rapat"><u><b>SURAT PERINTAH TUGAS</b></u><br>Nomor: {no_spt}</div><div style="line-height:1.5; margin-top:10px;"><table class="visum-table">{rows}</table><p>Untuk: {maksud} ke {tujuan}</p></div>{get_ttd(pjb)}</div>'
    
    # 2. SPD DEPAN (Satu Per Orang)
    for p in daftar:
        if "SPD Depan" in opsi_cetak:
            html_all += f'''<div class="kertas">{kop}<div style="margin-left:60%; line-height:1.0;">Kode No: 094<br>Nomor: {p['spd']}</div><div class="judul-rapat"><u><b>SURAT PERJALANAN DINAS</b></u><br>(SPD)</div><table class="tabel-border" style="margin-top:10px;">
                <tr><td class="col-no">1.</td><td width="42%">Pejabat pemberi perintah</td><td>BUPATI NGADA</td></tr>
                <tr><td class="col-no">2.</td><td>Nama Pegawai diperintah</td><td><b>{p['nama']}</b></td></tr>
                <tr><td class="col-no" rowspan="3">3.</td><td>a. Pangkat / Jabatan</td><td>{p['gol']} / {p['jab']}</td></tr>
                <tr><td>b. Jabatan</td><td>{p['jab']}</td></tr>
                <tr><td>c. Tingkat Peraturan</td><td>-</td></tr>
                <tr><td class="col-no">4.</td><td>Maksud Perjalanan</td><td>{maksud}</td></tr>
                <tr><td class="col-no">5.</td><td>Alat angkut</td><td>Mobil Dinas</td></tr>
                <tr><td class="col-no" rowspan="2">6.</td><td>a. Tempat Berangkat</td><td>Bajawa</td></tr>
                <tr><td>b. Tempat Tujuan</td><td>{tujuan}</td></tr>
                <tr><td class="col-no" rowspan="3">7.</td><td>Lamanya Perjalanan</td><td>{lama}</td></tr>
                <tr><td>a. Tanggal Berangkat</td><td>{tgl_bkt.strftime("%d/%m/%Y")}</td></tr>
                <tr><td>b. Tanggal Kembali</td><td>{tgl_kbl.strftime("%d/%m/%Y")}</td></tr>
                <tr><td class="col-no">10.</td><td>Keterangan</td><td>-</td></tr>
            </table>{get_ttd(pjb, 70)}</div>'''
    
    # 3. SPD BELAKANG (Cuma 1 Lembar)
    if "SPD Belakang" in opsi_cetak:
        def rv(n, l, v, d):
            return f'''<table class="visum-table"><tr><td width="10%">{n}</td><td width="35%">{l}</td><td width="5%">:</td><td>{v}</td></tr><tr><td></td><td>Pada Tanggal</td><td>:</td><td>{d}</td></tr></table>'''
        
        ttd_bk = f'<div style="text-align:center; line-height:1.2; font-size:10pt;"><br><b>An. BUPATI NGADA</b><br>{jab_pjb},<br>Ub. {ub},<div style="height:90px;"></div><b><u>{pjb}</u></b><br>NIP. 19710328 199203 1 011</div>'
        
        html_all += f'''<div class="kertas"><table class="tabel-border" style="height:90%;">
            <tr style="height:210px;"><td width="50%"></td><td style="padding:10px;">{rv("I.", "Berangkat dari", "Bajawa", tgl_bkt.strftime("%d/%m/%Y"))}<br>Ke: {tujuan}{ttd_bk}</td></tr>
            <tr style="height:180px;"><td>{rv("II.", "Tiba di", tujuan, tgl_bkt.strftime("%d/%m/%Y"))}</td><td>Berangkat dari: {tujuan}<br>Ke: Bajawa<br>Tgl: {tgl_kbl.strftime("%d/%m/%Y")}</td></tr>
            <tr style="height:180px;"><td>III.</td><td></td></tr>
            <tr style="height:210px;"><td>{rv("V.", "Tiba di Kembali", "Bajawa", tgl_kbl.strftime("%d/%m/%Y"))}</td><td style="padding:10px;">{ttd_bk}</td></tr>
        </table><div style="border:1pt solid black; border-top:none; padding:5px; font-size:8.5pt; text-align:justify;"><b>VII. Perhatian:</b> Pejabat bertanggung jawab... rugi akibat kesalahan...</div></div>'''
    
    html_all += '</div>'
    st.markdown(html_all, unsafe_allow_html=True)

# 3. MENU REGISTER
if menu == "Lihat Register":
    st.title("📂 Arsip Register")
    if not st.session_state.db_reg:
        st.info("Belum ada data.")
    else:
        for i, r in enumerate(st.session_state.db_reg):
            c1, c2 = st.columns([9, 1])
            c1.write(f"{i+1}. {r['Nama']} | {r['SPT']} | {r['Tujuan']}")
            if c2.button("🗑️", key=f"del_{i}"):
                st.session_state.db_reg.pop(i)
                st.rerun()
        
        st.markdown("---")
        tr_html = "".join([f"<tr><td>{idx+1}</td><td>{r['Nama']}</td><td>{r['SPT']}</td><td>{r['SPD']}</td><td>{r['Bkt']}</td><td>{r['Kbl']}</td><td>{r['Lama']}</td><td>{r['Ket']}</td></tr>" for idx, r in enumerate(st.session_state.db_reg)])
        st.markdown(f'''<div class="kertas kertas-landscape reg-landscape"><h3 class="text-center">REGISTER SPD</h3><table class="tabel-border" style="width:100%; font-size:9pt;"><thead><tr><th>No</th><th>Nama</th><th>No SPT</th><th>No SPD</th><th>Bkt</th><th>Kbl</th><th>Lama</th><th>Ket</th></tr></thead><tbody>{tr_html}</tbody></table></div>''', unsafe_allow_html=True)
        if st.button("🖨️ Cetak Register"):
            st.components.v1.html("<script>window.parent.print();</script>", height=0)
