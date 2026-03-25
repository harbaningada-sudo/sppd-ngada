import streamlit as st
import pandas as pd
from datetime import datetime
import logo 

# 1. SETUP
st.set_page_config(page_title="SPD Ngada Pro", layout="wide")

if 'db_reg' not in st.session_state: st.session_state.db_reg = []

st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .main-container { display: flex; flex-direction: column; align-items: center; color: black; }
    .kertas { 
        background: white !important; width: 215.9mm; height: 330mm; 
        padding: 10mm 15mm; margin-bottom: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.5);
        font-family: Arial; font-size: 10pt; page-break-after: always; overflow: hidden;
    }
    .kertas-landscape { width: 330mm !important; height: 215.9mm !important; }
    .kop-table { width: 100%; border-bottom: 3pt solid black; margin-bottom: 5px; line-height: 1.0; }
    .tabel-border { width: 100%; border-collapse: collapse; border: 1pt solid black; }
    .tabel-border td, .tabel-border th { border: 1pt solid black; padding: 4px; vertical-align: top; }
    .tabel-no-border td { border: none !important; }
    .col-no { width: 30px; text-align: left; }
    @media print {
        [data-testid="stSidebar"], .stButton, .no-print { display: none !important; }
        .stApp { background: white !important; }
        @page { size: legal; margin: 0; }
        .reg-page { @page { size: legal landscape; } }
    }
</style>
""", unsafe_allow_html=True)

# 2. PANEL KONTROL
with st.sidebar:
    st.header("📋 PANEL KONTROL")
    menu = st.radio("Menu", ["Input & Cetak", "Register"])
    
    if menu == "Input & Cetak":
        opsi = st.multiselect("Cetak", ["SPT", "SPD Depan", "SPD Belakang", "SPD Belakang (Tendes)"], default=["SPT", "SPD Depan", "SPD Belakang"])
        if 'jml' not in st.session_state: st.session_state.jml = 1
        c1, c2 = st.columns(2)
        if c1.button("➕"): st.session_state.jml += 1
        if c2.button("➖") and st.session_state.jml > 1: st.session_state.jml -= 1
        
        pegawai = []
        for i in range(st.session_state.jml):
            st.write(f"Pegawai {i+1}")
            pegawai.append({
                "nama": st.text_input("Nama", f"Nama {i+1}", key=f"n{i}"),
                "nip": st.text_input("NIP", "19XXXXXXXX", key=f"ni{i}"),
                "spd": st.text_input("No SPD", "530 /02/2026", key=f"s{i}"),
                "gol": st.text_input("Gol", "III/a", key=f"g{i}"),
                "jab": st.text_input("Jab", "Pelaksana", key=f"j{i}")
            })
        
        tujuan = st.text_input("Tujuan", "Riung")
        maksud = st.text_area("Maksud", "Tugas...")
        tgl_bkt = st.date_input("Berangkat", datetime.now())
        tgl_kbl = st.date_input("Pulang", datetime.now())
        lama = st.text_input("Lama", "1 (Satu) hari")
        
        st.subheader("🖋️ TTD")
        pjb_tujuan = st.text_input("Nama Pejabat Tujuan", "....................")
        pjb_ngada = st.text_input("Pejabat Bajawa", "Yohanes C. Watu Ngebu, S.Sos., M.Si")
        jab_ngada = st.text_input("Jabatan", "Pj. Sekretaris Daerah")
        ub = st.text_input("Ub.", "Asisten Perekonomian dan Pembangunan")

        if st.button("💾 SIMPAN & CETAK"):
            for p in pegawai:
                st.session_state.db_reg.append({
                    "Nama": p['nama'], "SPT": "094/Prokopim/557/02/2026", "SPD": p['spd'],
                    "Tujuan": tujuan, "Bkt": tgl_bkt.strftime("%d/%m/%Y"), "Kbl": tgl_kbl.strftime("%d/%m/%Y"), "Lama": lama
                })
            st.components.v1.html("<script>setTimeout(function(){ window.parent.print(); }, 500);</script>", height=0)

# 3. LOGIKA HALAMAN
kop = f'''<table class="kop-table"><tr><td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="70"></td><td style="text-align:center;"><h3>PEMERINTAH KABUPATEN NGADA</h3><h2>SEKRETARIAT DAERAH</h2><p>Bajawa</p></td></tr></table>'''

def ttd(nama, space=70):
    return f'''<div style="text-align:center; margin-left:55%;"><b>An. BUPATI NGADA</b><br>{jab_ngada},<br>Ub. {ub},<div style="height:{space}px;"></div><b><u>{nama}</u></b><br>NIP. 19710328 199203 1 011</div>'''

if menu == "Input & Cetak":
    html_all = '<div class="main-container">'
    # SPT
    if "SPT" in opsi:
        rows = "".join([f"<tr><td width='12%'>Kepada</td><td width='5%'>:</td><td width='5%'>{idx+1}.</td><td>Nama: <b>{p['nama']}</b><br>NIP: {p['nip']}</td></tr>" for idx, p in enumerate(pegawai)])
        html_all += f'<div class="kertas">{kop}<div class="text-center"><u><b>SURAT PERINTAH TUGAS</b></u><br>Nomor: 094/...</div><div style="line-height:1.5; margin-top:10px;"><table class="visum-table">{rows}</table><p>Untuk: {maksud} ke {tujuan}</p></div>{ttd(pjb_ngada)}</div>'
    
    # SPD DEPAN
    for p in pegawai:
        if "SPD Depan" in opsi:
            html_all += f'''<div class="kertas">{kop}<div style="margin-left:60%; line-height:1.0;">Kode No: 094<br>Nomor: {p['spd']}</div><div class="text-center"><u><b>SURAT PERJALANAN DINAS</b></u><br>(SPD)</div><table class="tabel-border" style="margin-top:10px;">
                <tr><td class="col-no">1.</td><td width="42%">Pejabat pemberi perintah</td><td>BUPATI NGADA</td></tr>
                <tr><td class="col-no">2.</td><td>Nama Pegawai</td><td><b>{p['nama']}</b></td></tr>
                <tr><td class="col-no">3.</td><td>Pangkat / Jabatan</td><td>{p['gol']} / {p['jab']}</td></tr>
                <tr><td class="col-no">4.</td><td>Maksud</td><td>{maksud}</td></tr>
                <tr><td class="col-no">5.</td><td>Alat Angkut</td><td>Mobil Dinas</td></tr>
                <tr><td class="col-no">6.</td><td>Tempat Tujuan</td><td>{tujuan}</td></tr>
                <tr><td class="col-no">7.</td><td>Lama / Tgl Berangkat</td><td>{lama} / {tgl_bkt.strftime("%d/%m/%Y")}</td></tr>
                <tr><td class="col-no">10.</td><td>Keterangan</td><td>-</td></tr>
            </table>{ttd(pjb_ngada, 60)}</div>'''
    
    # SPD BELAKANG (1 Lembar)
    if any(x in opsi for x in ["SPD Belakang", "SPD Belakang (Tendes)"]):
        is_t = "SPD Belakang (Tendes)" in opsi and "SPD Belakang" not in opsi
        st_t = "tabel-no-border" if is_t else "tabel-border"
        html_all += f'''<div class="kertas"><table class="{st_t}" style="height:88%;">
            <tr style="height:200px;"><td></td><td style="padding:10px;">I. Berangkat dari: Bajawa<br>Tgl: {tgl_bkt.strftime("%d/%m/%Y")}<br>{ttd(pjb_ngada, 60)}</td></tr>
            <tr style="height:170px;"><td>II. Tiba di: {tujuan}<br>Tgl: {tgl_bkt.strftime("%d/%m/%Y")}<br><b>{pjb_tujuan}</b></td><td>Berangkat dari: {tujuan}<br>Tgl: {tgl_kbl.strftime("%d/%m/%Y")}</td></tr>
            <tr style="height:200px;"><td>V. Tiba di: Bajawa<br>Tgl: {tgl_kbl.strftime("%d/%m/%Y")}<br><b>{pjb_ngada}</b></td><td>{ttd(pjb_ngada, 60)}</td></tr>
        </table><div style="border:{"none" if is_t else "1pt solid black"}; padding:5px; font-size:8pt;">VI. Catatan | VII. Perhatian: Pejabat bertanggung jawab...</div></div>'''
    
    html_all += '</div>'
    st.markdown(html_all, unsafe_allow_html=True)

# 4. MENU REGISTER
if menu == "Register":
    st.title("📂 Register Riwayat")
    if not st.session_state.db_reg: st.info("Kosong")
    else:
        df = pd.DataFrame(st.session_state.db_reg)
        for i, r in df.iterrows():
            c1, c2 = st.columns([9, 1])
            c1.write(f"{i+1}. {r['Nama']} - {r['Tujuan']} ({r['Bkt']})")
            if c2.button("🗑️", key=f"d{i}"):
                st.session_state.db_reg.pop(i)
                st.rerun()
        
        st.markdown("---")
        tr = "".join([f"<tr><td>{idx+1}</td><td>{r['Nama']}</td><td>{r['SPT']}</td><td>{r['SPD']}</td><td>{r['Bkt']}</td><td>{r['Kbl']}</td><td>{r['Lama']}</td></tr>" for idx, r in df.iterrows()])
        st.markdown(f'''<div class="kertas kertas-landscape reg-page"><h3 class="text-center">REGISTER SPT/SPD</h3><table class="tabel-border" style="width:100%;"><thead><tr><th>No</th><th>Nama</th><th>No SPT</th><th>No SPD</th><th>Bkt</th><th>Kbl</th><th>Lama</th></tr></thead><tbody>{tr}</tbody></table></div>''', unsafe_allow_html=True)
        if st.button("🖨️ Cetak Register"): st.components.v1.html("<script>window.parent.print();</script>", height=0)
