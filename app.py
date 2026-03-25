import streamlit as st
import pandas as pd
from datetime import datetime
import logo  # Memanggil logo.py di repository GitHub kamu

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem SPD Ngada Pro", layout="wide")

# Database Register (Tersimpan selama aplikasi aktif)
if 'db_reg' not in st.session_state:
    st.session_state.db_reg = []

# CSS UNTUK PRESISI CETAK FULL LEGAL & ANTI TERPOTONG
st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    .stApp { background-color: #525659 !important; }

    .main-container {
        display: flex; flex-direction: column; align-items: center; width: 100%; padding: 10px 0;
    }

    /* KERTAS UMUM (PORTRAIT LEGAL) - DITINGGIKAN SEDIKIT */
    .kertas { 
        background-color: white !important; 
        width: 215.9mm; 
        height: 330mm; /* Dikunci tinggi legal agar penuh */
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

    /* KHUSUS REGISTER (LANDSCAPE) */
    .kertas-landscape {
        width: 330mm !important;
        height: 215.9mm !important;
        padding: 15mm !important;
    }

    /* KOP & JUDUL (Line Spacing 1.0 Rapat) */
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
    .tabel-border td, .tabel-border th { border: 1pt solid black !important; padding: 4px 6px !important; vertical-align: top; color: black !important; line-height: 1.1 !important; }
    
    /* FIX NOMOR 1. sd 10. SEJAJAR */
    .col-no { width: 35px !important; text-align: left !important; }

    /* TABEL VISUM (FULL LEGAL SPACE) */
    .visum-table { width: 100%; border: none !important; border-collapse: collapse; margin: 0 !important; }
    .visum-table td { border: none !important; padding: 0 !important; font-size: 10pt; line-height: 1.2; color: black !important; vertical-align: top; }

    /* SPACE TANDA TANGAN */
    .space-ttd { height: 100px; } 

    .text-center { text-align: center; } .text-bold { font-weight: bold; } .underline { text-decoration: underline; }

    @media print {
        [data-testid="stSidebar"], .stButton, .no-print { display: none !important; }
        .stApp, .main-container { background-color: white !important; padding: 0 !important; margin: 0 !important; }
        .kertas { 
            box-shadow: none !important; margin: 0 !important; width: 215.9mm !important; height: 330mm !important; 
            transform: scale(1.0);
            transform-origin: top center;
        }
        .kertas:last-child { page-break-after: avoid !important; }
        @page { size: legal; margin: 0; }
        .register-page { @page { size: legal landscape; } }
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 PANEL KONTROL")
    menu = st.radio("Menu", ["Input & Cetak", "Lihat & Hapus Register"])
    
    if menu == "Input & Cetak":
        opsi = st.multiselect("Cetak Dokumen", ["SPT", "SPD Depan", "SPD Belakang"], default=["SPT", "SPD Depan", "SPD Belakang"])
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
                    "gol": st.text_input("Gol", "III/a", key=f"g{i}"),
                    "jab": st.text_input("Jabatan", "Pelaksana", key=f"j{i}")
                })

        with st.expander("📄 DATA UTAMA"):
            no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
            tujuan = st.text_input("Tujuan", "Kecamatan Riung")
            maksud = st.text_area("Maksud", "Tugas...")
            tgl_bkt = st.date_input("Berangkat", datetime.now())
            tgl_kbl = st.date_input("Kembali", datetime.now())
            lama = st.text_input("Lama", "1 (Satu) hari")
            ket = st.text_input("Keterangan Reg", "-")
            anggaran = st.text_input("Anggaran", "DPA Bagian Perekonomian dan SDA 2026")

        st.subheader("🖋️ TANDA TANGAN")
        pjb = st.text_input("Nama Pejabat Ngada", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
        jab = st.text_input("Jabatan Utama", "Pj. Sekretaris Daerah")
        ub = st.text_input("Ub.", "Asisten Perekonomian dan Pembangunan")

        if st.button("💾 SIMPAN & PROSES CETAK"):
            for p in daftar:
                st.session_state.db_reg.append({
                    "Nama": p['nama'], "SPT": no_spt, "Tujuan": tujuan,
                    "Berangkat": tgl_bkt.strftime("%d/%m/%Y"),
                    "Kembali": tgl_kbl.strftime("%d/%m/%Y"), "Lama": lama, "Ket": ket
                })
            st.components.v1.html("<script>setTimeout(function(){ window.parent.print(); }, 1200);</script>", height=0)

# --- KONSTRUKSI SURAT ---
kop = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="70"></td><td class="stTeks" style="text-align:center;"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>Bajawa</p></td></tr></table>'''

def ttd(space):
    return f'''<div style="margin-left:55%; text-align:center; line-height:1.2;"><b>An. BUPATI NGADA</b><br>{jab},<br>{f"Ub. {ub}," if ub else ""}<div style="height:{space}px;"></div><b><u>{pjb}</u></b><br>NIP. 19710328 199203 1 011</div>'''

if menu == "Input & Cetak":
    html_out = '<div class="main-container">'
    
    # 1. SPT (Kolektif)
    if "SPT" in opsi:
        p_rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{idx+1}.</td><td width='20%'>Nama</td><td width='5%'>:</td><td><b>{p['nama']}</b><br>NIP. {p['nip']}</td></tr>" for idx, p in enumerate(daftar)])
        html_out += f'<div class="kertas">{kop}<div class="judul-rapat"><u><b>SURAT PERINTAH TUGAS</b></u><br>Nomor: {no_spt}</div><div style="line-height:1.5; margin-top:10px;"><table class="visum-table"><tr><td width="12%">Dasar</td><td width="5%">:</td><td>{anggaran}</td></tr></table><p class="text-center text-bold" style="margin:10px 0;">M E M E R I N T A H K A N</p><table class="visum-table">{p_rows}</table><table class="visum-table" style="margin-top:10px;"><tr><td width="12%">Untuk</td><td width="5%">:</td><td>{maksud} ke {tujuan}</td></tr></table></div>{ttd(90)}</div>'
    
    # 2. SPD DEPAN (Per Orang)
    for p in daftar:
        if "SPD Depan" in opsi:
            html_out += f'''<div class="kertas">{kop}<div style="margin-left:60%; line-height:1.0;">Kode No: 094<br>Nomor: ...</div><div class="judul-rapat"><u><b>SURAT PERJALANAN DINAS</b></u><br>(SPD)</div><table class="tabel-border" style="margin-top:10px;">
                <tr><td class="col-no">1.</td><td width="42%">Pejabat pemberi perintah</td><td>BUPATI NGADA</td></tr>
                <tr><td class="col-no">2.</td><td>Nama Pegawai diperintah</td><td><b>{p['nama']}</b></td></tr>
                <tr><td class="col-no" rowspan="3">3.</td><td>a. Pangkat / Jabatan</td><td>{p['gol']} / {p['jab']}</td></tr>
                <tr><td>b. Jabatan</td><td>{p['jab']}</td></tr>
                <tr><td>c. Tingkat Peraturan</td><td>-</td></tr>
                <tr><td class="col-no">4.</td><td>Maksud Perjalanan</td><td>{maksud}</td></tr>
                <tr><td class="col-no">5.</td><td>Alat angkut</td><td>Mobil Dinas</td></tr>
                <tr><td class="col-no">6.</td><td>Tempat Tujuan</td><td>{tujuan}</td></tr>
                <tr><td class="col-no">7.</td><td>Lama / Tgl Berangkat</td><td>{lama} / {tgl_bkt.strftime("%d/%m/%Y")}</td></tr>
                <tr><td class="col-no">10.</td><td>Keterangan</td><td>-</td></tr>
            </table>{ttd(70)}</div>'''
    
    # 3. SPD BELAKANG (Cuma 1 Lembar)
    if "SPD Belakang" in opsi:
        def rv(n, l, v, d, is_n=True):
            n_c = f'<td width="10%">{n}</td>' if is_n else ""
            return f'''<table class="visum-table"><tr>{n_c}<td width="35%">{l}</td><td width="5%">:</td><td>{v}</td></tr><tr>{"<td></td>" if is_n else ""}<td>Pada Tanggal</td><td>:</td><td>{d}</td></tr></table>'''
        
        ttd_bk = f'<div style="text-align:center; line-height:1.2; font-size:10pt;"><br><b>An. BUPATI NGADA</b><br>{jab},<br>{f"Ub. {ub}," if ub else ""}<div style="height:90px;"></div><b><u>{pjb}</u></b><br>NIP. 19710328 199203 1 011</div>'
        
        html_out += f'''<div class="kertas"><table class="tabel-border" style="height:92%;">
            <tr style="height: 220px;"><td width="50%"></td><td style="padding:10px;">{rv("I.", "Berangkat dari", "Bajawa", tgl_bkt.strftime("%d/%m/%Y"))}<table class="visum-table"><tr><td width="10%"></td><td width="35%">Ke</td><td width="5%">:</td><td>{tujuan}</td></tr></table>{ttd_bk}</td></tr>
            <tr style="height: 190px;"><td>{rv("II.", "Tiba di", tujuan, tgl_bkt.strftime("%d/%m/%Y"))}</td><td style="padding:10px;">{rv("", "Berangkat dari", tujuan, tgl_kbl.strftime("%d/%m/%Y"), False)}<table class="visum-table"><tr><td width="35%">Ke</td><td width="5%">:</td><td>Bajawa</td></tr></table></td></tr>
            <tr style="height: 190px;"><td>III.</td><td></td></tr>
            <tr style="height: 220px;"><td>{rv("V.", "Tiba di Kembali", "Bajawa", tgl_kbl.strftime("%d/%m/%Y"))}</td><td style="padding:10px;"><p style="font-style:italic; font-size:9.2pt; line-height:1.2;">Telah diperiksa, dengan keterangan perjalanan atas perintahnya...</p>{ttd_bk}</td></tr>
        </table><div style="border:1pt solid black; border-top:none; padding:8px; font-size:10.5pt;"><b>VI. Catatan Lain-lain</b></div><div style="border:1pt solid black; border-top:none; padding:8px; font-size:8.8pt; text-align:justify; color:black; line-height:1.3;"><b>VII. Perhatian :</b> Pejabat yang menerbitkan SPD, pegawai yang melakukan perjalanan dinas, para pejabat yang mengesahkan tanggal berangkat/tiba, serta Bendahara Pengeluaran bertanggung jawab berdasarkan peraturan-peraturan Keuangan Negara apabila negara menderita rugi akibat kesalahan, kelalaian dan kealpaannya.</div></div>'''

    html_out += '</div>'
    st.markdown(html_out, unsafe_allow_html=True)

# 4. HALAMAN REGISTER
if menu == "Lihat & Hapus Register":
    st.title("📂 Arsip Register")
    if not st.session_state.db_reg: st.warning("Kosong")
    else:
        for i, r in enumerate(st.session_state.db_reg):
            c1, c2 = st.columns([9, 1])
            c1.write(f"{i+1}. {r['Nama']} | {r['SPT']} | {r['Tujuan']}")
            if c2.button("🗑️", key=f"d{i}"):
                st.session_state.db_reg.pop(i)
                st.rerun()
        
        st.markdown("---")
        tr_h = "".join([f"<tr><td>{idx+1}</td><td>{r['Nama']}</td><td>{r['SPT']}</td><td>{r['Berangkat']}</td><td>{r['Kembali']}</td><td>{r['Lama']}</td><td>{r['Ket']}</td></tr>" for idx, r in enumerate(st.session_state.db_reg)])
        st.markdown(f'''<div class="kertas kertas-landscape reg-landscape"><h3 class="text-center text-bold">REGISTER SPD</h3><table class="tabel-border" style="width:100%; font-size:9pt;"><thead><tr><th>No</th><th>Nama</th><th>No SPT</th><th>Berangkat</th><th>Kembali</th><th>Lama</th><th>Ket</th></tr></thead><tbody>{tr_h}</tbody></table></div>''', unsafe_allow_html=True)
        if st.button("🖨️ Cetak Register"): st.components.v1.html("<script>window.parent.print();</script>", height=0)
