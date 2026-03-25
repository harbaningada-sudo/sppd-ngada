import streamlit as st
import pandas as pd
from datetime import datetime
import logo 

# 1. KONFIGURASI
st.set_page_config(page_title="Sistem SPD Ngada Pro", layout="wide")

# 2. DATABASE SESSION (Agar data tersimpan selama tab tidak diclose)
if 'db_register' not in st.session_state:
    st.session_state.db_register = []

# CSS UNTUK PRESISI CETAK
st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display:none; }
    .main-container { display: flex; flex-direction: column; align-items: center; width: 100%; padding: 5px 0; }
    .kertas-landscape { 
        background-color: white !important; width: 330mm; min-height: 215.9mm; 
        padding: 15mm; color: black !important; font-family: Arial, sans-serif; 
        box-sizing: border-box; box-shadow: 0 0 20px rgba(0,0,0,0.5); font-size: 10pt;
    }
    .tabel-reg { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; table-layout: fixed; }
    .tabel-reg th, .tabel-reg td { border: 1pt solid black !important; padding: 6px; font-size: 9pt; color: black !important; }
    .text-center { text-align: center; }
    @media print {
        [data-testid="stSidebar"], .stButton, .no-print { display: none !important; }
        .kertas-landscape { box-shadow: none !important; margin: 0 !important; width: 330mm !important; }
        @page { size: legal landscape; margin: 0; }
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 PANEL KONTROL")
    menu = st.radio("Pilih Menu", ["Input Data & Cetak", "Lihat & Kelola Register"])
    
    if menu == "Input Data & Cetak":
        st.markdown("---")
        if 'jml' not in st.session_state: st.session_state.jml = 1
        c1, c2 = st.columns(2)
        if c1.button("➕ Pegawai"): st.session_state.jml += 1
        if c2.button("➖ Hapus") and st.session_state.jml > 1: st.session_state.jml -= 1
        
        daftar = []
        for i in range(st.session_state.jml):
            n = st.text_input(f"Nama P-{i+1}", f"Nama {i+1}", key=f"n{i}")
            ni = st.text_input(f"NIP P-{i+1}", "19XXXXXXXXXXXXXX", key=f"ni{i}")
            s = st.text_input(f"No SPD P-{i+1}", f"530 /02/2026", key=f"s{i}")
            daftar.append({"nama": n, "nip": ni, "spd": s})

        no_spt = st.text_input("Nomor SPT", "094/Prokopim/557/02/2026")
        tujuan = st.text_input("Tujuan", "Kecamatan Riung")
        tgl_bkt = st.date_input("Tanggal Berangkat", datetime.now())
        tgl_kbl = st.date_input("Tanggal Pulang", datetime.now())
        lama = st.text_input("Lama Hari", "1 (Satu) hari")
        ket = st.text_input("Keterangan", "-")

        if st.button("💾 SIMPAN & CETAK"):
            # SIMPAN DATA KE REGISTER
            for p in daftar:
                st.session_state.db_register.append({
                    "Nama": p['nama'],
                    "Nomor SPT": no_spt,
                    "Nomor SPD": p['spd'],
                    "Tujuan": tujuan,
                    "Tgl Berangkat": tgl_bkt.strftime("%d/%m/%Y"),
                    "Tgl Pulang": tgl_kbl.strftime("%d/%m/%Y"),
                    "Lama": lama,
                    "Keterangan": ket
                })
            st.success("Berhasil disimpan!")
            st.components.v1.html("<script>window.parent.print();</script>", height=0)

# --- HALAMAN REGISTER ---
if menu == "Lihat & Kelola Register":
    st.title("📂 Register SPT/SPD")
    
    if not st.session_state.db_register:
        st.info("Belum ada data di register.")
    else:
        # 1. TABEL KELOLA (DENGAN TOMBOL HAPUS)
        df = pd.DataFrame(st.session_state.db_register)
        
        st.subheader("Kelola Arsip")
        for i, row in df.iterrows():
            col1, col2, col3 = st.columns([1, 8, 2])
            col1.write(f"**{i+1}**")
            col2.write(f"{row['Nama']} | {row['Nomor SPT']} | {row['Tujuan']}")
            if col3.button("🗑️ Hapus", key=f"del_{i}"):
                st.session_state.db_register.pop(i)
                st.rerun()

        if st.button("🧹 Kosongkan Semua Data"):
            st.session_state.db_register = []
            st.rerun()

        st.markdown("---")
        # 2. TABEL FORMAT CETAK (HTML)
        st.subheader("Pratinjau Cetak")
        
        header_html = '''
        <div class="kertas-landscape">
            <h3 class="text-center">REGISTER SURAT PERJALANAN DINAS</h3>
            <table class="tabel-reg">
                <thead>
                    <tr style="background:#eee;">
                        <th width="30">No</th>
                        <th>Nama</th>
                        <th>Nomor SPT</th>
                        <th>Nomor SPD</th>
                        <th>Tgl Berangkat</th>
                        <th>Tgl Pulang</th>
                        <th>Lamanya</th>
                        <th>Keterangan</th>
                    </tr>
                </thead>
                <tbody>
        '''
        
        body_html = ""
        for idx, r in df.iterrows():
            body_html += f'''
                <tr>
                    <td class="text-center">{idx+1}</td>
                    <td>{r['Nama']}</td>
                    <td>{r['Nomor SPT']}</td>
                    <td>{r['Nomor SPD']}</td>
                    <td>{r['Tgl Berangkat']}</td>
                    <td>{r['Tgl Pulang']}</td>
                    <td>{r['Lama']}</td>
                    <td>{r['Keterangan']}</td>
                </tr>
            '''
        
        footer_html = "</tbody></table></div>"
        
        # Gabungkan dan tampilkan dengan unsafe_allow_html=True
        full_html = header_html + body_html + footer_html
        st.markdown(full_html, unsafe_allow_html=True)
        
        if st.button("🖨️ Cetak Register"):
            st.components.v1.html("<script>window.parent.print();</script>", height=0)
