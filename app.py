import streamlit as st
import pandas as pd
from datetime import datetime
import logo 

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="SPD Ngada Pro", layout="wide")

# Database Register (Tersimpan selama aplikasi aktif)
if 'db_reg' not in st.session_state:
    st.session_state.db_reg = []

# CSS UNTUK PRESISI CETAK & FULL LEGAL
st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .main-container { display: flex; flex-direction: column; align-items: center; color: black; }
    
    /* KERTAS LEGAL PORTRAIT */
    .kertas { 
        background: white !important; width: 215.9mm; height: 330mm; 
        padding: 10mm 15mm; margin-bottom: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.5);
        font-family: Arial; font-size: 10.5pt; page-break-after: always; overflow: hidden;
    }
    
    /* KERTAS LEGAL LANDSCAPE (REGISTER) */
    .kertas-landscape { width: 330mm !important; height: 215.9mm !important; padding: 15mm !important; }

    /* LINE SPACING 1.0 (KOP & JUDUL) */
    .kop-table { width: 100%; border-bottom: 3.5pt solid black; margin-bottom: 5px; line-height: 1.0 !important; }
    .judul-rapat { text-align: center; line-height: 1.0 !important; margin: 5px 0; }
    
    /* TABEL SPD DEPAN & REGISTER */
    .tabel-border { width: 100%; border-collapse: collapse; border: 1pt solid black; }
    .tabel-border td, .tabel-border th { border: 1pt solid black; padding: 5px; vertical-align: top; line-height: 1.1; }
    
    .col-no { width: 35px; text-align: left; }

    /* TABEL VISUM BELAKANG */
    .visum-table { width: 100%; border-collapse: collapse; }
    .visum-table td { padding: 0; line-height: 1.1; vertical-align: top; }

    @media print {
        [data-testid="stSidebar"], .stButton, .no-print { display: none !important; }
        .stApp { background: white !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; }
        @page { size: legal; margin: 0; }
        .reg-landscape { @page { size: legal landscape; } }
    }
</style>
""", unsafe_allow_html=True)

# 2. PANEL KONTROL SIDEBAR
with st.sidebar:
    st.header("📋 PANEL KONTROL")
    menu = st.radio("Menu Utama", ["Input Data & Cetak", "Lihat & Hapus Register"])
    
    if menu == "Input Data & Cetak":
        opsi_cetak = st.multiselect("Pilih Dokumen", ["SPT", "SPD Depan", "SPD Belakang"], default=["SPT", "SPD Depan", "SPD Belakang"])
        
        with st.expander("👤 DATA PEGAWAI", expanded=True):
            if 'jml' not in st.session_state: st.session_state.jml = 1
            c1, c2 = st.columns(2)
            if c1.button("➕"): st.session_state.jml += 1
            if c2.button("➖") and st.session_state.jml > 1: st.session_state.jml -= 1
            
            daftar_pegawai = []
            for i in range(st.session_state.jml):
                st.write(f"**Pegawai {i+1}**")
                daftar_pegawai.append({
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
            tgl_bkt = st.date_input("Tanggal Berangkat", datetime.now())
            tgl_kbl = st.date_input("Tanggal Pulang", datetime.now())
            lama = st.text_input("Lama Hari", "1 (Satu) hari")
            ket_reg = st.text_input("Keterangan", "-")

        st.subheader("🖋️ PENANDATANGAN")
        pjb = st.text_input("Pejabat Bajawa", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
        jab_pjb = st.text_input("Jabatan", "Pj. Sekretaris Daerah")
        ub = st.text_input("Ub.", "Asisten Perekonomian dan Pembangunan")

        if st.button("💾 SIMPAN & PROSES CETAK"):
            for p in daftar_pegawai:
                st.session_state.db_reg.append({
                    "Nama": p['nama'], "SPT": no_spt, "SPD": p['spd'],
                    "Tujuan": tujuan, "Bkt": tgl_bkt.strftime("%d/%m/%Y"),
                    "Kbl": tgl_kbl.strftime("%d/%m/%Y"), "Lama": lama, "Ket": ket_reg
                })
            st.components.v1.html("<script>setTimeout(function(){ window.parent.print(); }, 800);</script>", height=0)

# --- KONSTRUKSI HALAMAN CETAK ---
kop = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="70"></td><td class="text-center"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>Jln. Soekarno - Hatta No. 1 Bajawa</p></td><td width="15%"></td></tr></table>'''

def render_ttd(nama, space=80):
    return f'''<div style="margin-left:55%; text-align:center; line-height:1.2;"><b>An. BUPATI NGADA</b><br>{jab_pjb},<br>Ub. {ub},<div style="height:{space}px;"></div><b><u>{nama}</u></b><br>NIP. 19710328 199203 1 011</div>'''

if menu == "Input Data & Cetak":
    html_all = '<div class="main-container">'
    
    # 1. SPT (KOLEKTIF)
    if "SPT" in opsi_cetak:
        p_rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{idx+1}.</td><td>Nama: <b>{p['nama']}</b><br>NIP: {p['nip']}</td></tr>" for idx, p in enumerate(daftar_pegawai)])
        html_all += f'<div class="kertas">{kop}<div class="judul-rapat"><u><b>SURAT PERINTAH TUGAS</b></u><br>Nomor: {no_spt}</div><div style="line-height:1.5; margin-top:10px;"><table class="visum-table">{p_rows}</table><p>Untuk: {maksud} ke {tujuan}</p></div>{render_ttd(pjb)}</div>'
    
    # 2. SPD DEPAN (PER ORANG)
    for p in daftar_pegawai:
        if "SPD Depan" in opsi_cetak:
            html_all += f'''<div class="kertas">{kop}<div style="margin-left:60%; line-height:1.0;">Kode No: 094<br>Nomor: {p['spd']}</div><div class="judul-rapat"><u><b>SURAT PERJALANAN DINAS</b></u><br>(SPD)</div><table class="tabel-border">
                <tr><td class="col-no">1.</td><td width="42%">Pejabat pemberi perintah</td><td>BUPATI NGADA</td></tr>
                <tr><td class="col-no">2.</td><td>Nama Pegawai diperintah</td><td><b>{p['nama']}</b></td></tr>
                <tr><td class="col-no">3.</td><td>Pangkat / Jabatan</td><td>{p['gol']} / {p['jab']}</td></tr>
                <tr><td class="col-no">4.</td><td>Maksud Perjalanan</td><td>{maksud}</td></tr>
                <tr><td class="col-no">5.</td><td>Alat angkut</td><td>Mobil Dinas</td></tr>
                <tr><td class="col-no">6.</td><td>Tempat Tujuan</td><td>{tujuan}</td></tr>
                <tr><td class="col-no">7.</td><td>Lama / Tgl Berangkat</td><td>{lama} / {tgl_bkt.strftime("%d/%m/%Y")}</td></tr>
                <tr><td class="col-no">10.</td><td>Keterangan</td><td>-</td></tr>
            </table>{render_ttd(pjb, 70)}</div>'''
    
    # 3. SPD BELAKANG (CUMA 1 LEMBAR DI AKHIR)
    if "SPD Belakang" in opsi_cetak:
        ttd_bk = f'<div style="text-align:center; line-height:1.2; font-size:10pt;"><br><b>An. BUPATI NGADA</b><br>{jab_pjb},<br>Ub. {ub},<div style="height:90px;"></div><b><u>{pjb}</u></b><br>NIP. 19710328 199203 1 011</div>'
        html_all += f'''<div class="kertas"><table class="tabel-border" style="height:90%;">
            <tr style="height:210px;"><td width="50%"></td><td style="padding:10px;">I. Berangkat dari: Bajawa<br>Ke: {tujuan}<br>Tgl: {tgl_bkt.strftime("%d/%m/%Y")}{ttd_bk}</td></tr>
            <tr style="height:180px;"><td>II. Tiba di: {tujuan}</td><td>Berangkat dari: {tujuan}<br>Ke: Bajawa</td></tr>
            <tr style="height:180px;"><td>III.</td><td></td></tr>
            <tr style="height:210px;"><td>V. Tiba di: Bajawa<br>Tgl: {tgl_kbl.strftime("%d/%m/%Y")}{ttd_bk}</td><td style="padding:10px; font-style:italic; font-size:9pt;">Telah diperiksa dengan keterangan perjalanan atas perintahnya...</td></tr>
        </table><div style="border:1pt solid black; border-top:none; padding:5px; font-size:8.5pt;"><b>VII. Perhatian:</b> Pejabat yang menerbitkan SPD... bertanggung jawab...</div></div>'''
    
    html_all += '</div>'
    st.markdown(html_all, unsafe_allow_html=True)

# 4. MENU REGISTER (DENGAN FITUR HAPUS)
if menu == "Lihat & Hapus Register":
    st.title("📂 Register Riwayat")
    if not st.session_state.db_reg: st.info("Belum ada riwayat.")
    else:
        # Tombol Hapus per baris
        for i, r in enumerate(st.session_state.db_reg):
            c1, c2 = st.columns([9, 1])
            c1.write(f"{i+1}. {r['Nama']} - {r['Tujuan']} ({r['Bkt']})")
            if c2.button("🗑️", key=f"del_{i}"):
                st.session_state.db_reg.pop(i)
                st.rerun()
        
        st.markdown("---")
        # Tabel Landscape untuk Cetak
        rows = "".join([f"<tr><td>{idx+1}</td><td>{r['Nama']}</td><td>{r['SPT']}</td><td>{r['SPD']}</td><td>{r['Bkt']}</td><td>{r['Kbl']}</td><td>{r['Lama']}</td><td>{r['Ket']}</td></tr>" for idx, r in enumerate(st.session_state.db_reg)])
        st.markdown(f'''<div class="kertas kertas-landscape reg-landscape"><h3 class="text-center">REGISTER SURAT PERJALANAN DINAS</h3><table class="tabel-border" style="width:100%; font-size:9pt;"><thead><tr><th>No</th><th>Nama</th><th>No SPT</th><th>No SPD</th><th>Berangkat</th><th>Kembali</th><th>Lama</th><th>Ket</th></tr></thead><tbody>{rows}</tbody></table></div>''', unsafe_allow_html=True)
        if st.button("🖨️ Cetak Register"): st.components.v1.html("<script>window.parent.print();</script>", height=0)
