import streamlit as st
import pandas as pd
from datetime import datetime
import logo
from io import BytesIO
import json, os

# ─────────────────────────────────────────────
# 1. KONFIGURASI HALAMAN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Sistem SPD Ngada Pro",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── PERSISTENT STORAGE ───────────────────────
REGISTER_FILE = "register_spd.json"

def load_register():
    if os.path.exists(REGISTER_FILE):
        try:
            with open(REGISTER_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_register(data):
    try:
        with open(REGISTER_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.warning(f"Gagal simpan: {e}")

if "arsip_register" not in st.session_state:
    st.session_state.arsip_register = load_register()
if "jml" not in st.session_state:
    st.session_state.jml = 1

# ─────────────────────────────────────────────
# 2. CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    header, footer, #MainMenu { visibility: hidden; }
    .stDeployButton { display: none; }
    .stApp { background-color: #525659 !important; }

    /* PAKSA SIDEBAR SELALU TAMPIL */
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stSidebar"] {
        min-width: 340px !important;
        max-width: 340px !important;
        transform: translateX(0) !important;
        visibility: visible !important;
    }

    .main-container {
        display: flex; flex-direction: column;
        align-items: center; width: 100%; padding: 10px 0;
    }

    /* KERTAS LEGAL PORTRAIT */
    .kertas {
        background-color: white !important;
        width: 215.9mm; min-height: 330mm;
        padding: 10mm 15mm; margin-bottom: 20px;
        color: black !important; font-family: Arial, sans-serif;
        box-sizing: border-box; box-shadow: 0 0 20px rgba(0,0,0,0.8);
        font-size: 10.5pt; page-break-after: always;
        overflow: hidden; position: relative;
    }

    /* KOP SURAT */
    .kop-table { width: 100%; border: none !important; border-bottom: 3.5pt solid black !important; margin-bottom: 5px; }
    .kop-table td { border: none !important; padding: 0 !important; vertical-align: middle; }
    .kop-teks { text-align: center; line-height: 1.0 !important; }
    .kop-teks h3, .kop-teks h2, .kop-teks p { margin: 0; line-height: 1.0 !important; padding: 1px 0; }

    /* KOP GARUDA */
    .kop-garuda { text-align: center; margin-bottom: 10px; line-height: 1.0; width: 100%; }
    .kop-garuda img { width: 70px; margin-bottom: 5px; }
    .kop-garuda h2 { margin: 0; font-size: 16pt; font-weight: bold; letter-spacing: 2px; }

    .judul-rapat { text-align: center; line-height: 1.0 !important; margin-top: 5px; }
    .judul-rapat h3, .judul-rapat p { margin: 0; line-height: 1.0 !important; }

    /* TABEL ISI */
    .tabel-border { width: 100%; border-collapse: collapse !important; border: 1pt solid black !important; table-layout: fixed; }
    .tabel-border td { border: 1pt solid black !important; padding: 4px 8px !important; vertical-align: top; color: black !important; font-size: 9.5pt; line-height: 1.1 !important; }
    .col-no { width: 30px !important; text-align: left !important; padding-left: 8px !important; }

    .visum-table { width: 100%; border: none !important; border-collapse: collapse; margin: 0 !important; }
    .visum-table td { border: none !important; padding: 0 !important; font-size: 10pt; line-height: 1.2; color: black !important; vertical-align: top; }

    .text-center { text-align: center; }
    .text-bold { font-weight: bold; }
    .underline { text-decoration: underline; }

    /* REGISTER */
    .register-wrap {
        background: white; border-radius: 10px; padding: 30px;
        margin: 20px auto; width: 95%; max-width: 1200px;
        box-shadow: 0 0 20px rgba(0,0,0,0.5);
    }

    /* CETAK */
    @media print {
        [data-testid="stSidebar"], .stButton, .no-print, .register-wrap { display: none !important; }
        .stApp, .main-container { background-color: white !important; padding: 0 !important; margin: 0 !important; }
        .kertas { box-shadow: none !important; margin: 0 !important; width: 215.9mm !important; min-height: 330mm !important; }
        @page { size: legal portrait; margin: 0; }
    }

    /* RESPONSIF LAYAR KECIL */
    @media screen and (max-width: 900px) {
        .kertas { width: 100% !important; min-height: auto !important; padding: 5mm 5mm !important; }
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 3. HELPER FUNCTIONS
# ─────────────────────────────────────────────
def get_ttd(space_px, ttd_label, jab_ttd, ub, pjb, gol_pjb, nip_ttd):
    lbl      = ttd_label
    jab_line = f"{jab_ttd}," if lbl == "An. BUPATI NGADA" else ""
    ub_line  = f"Ub. {ub},"  if (ub and lbl == "An. BUPATI NGADA") else ""
    return (
        f'<div style="margin-left:55%;margin-top:10px;line-height:1.2;text-align:center;">'
        f'<b>{lbl}</b><br>{jab_line}<br>{ub_line}'
        f'<div style="height:{space_px}px;"></div>'
        f'<b><u>{pjb}</u></b><br>{gol_pjb}<br>NIP. {nip_ttd}</div>'
    )

def render_visum(num, label, nilai, tanggal, show_num=True):
    num_td = f'<td width="10%">{num}</td>' if show_num else '<td width="10%"></td>'
    return (
        f'<table class="visum-table">'
        f'<tr>{num_td}<td width="35%">{label}</td><td width="5%">:</td><td>{nilai}</td></tr>'
        f'<tr><td></td><td>Pada Tanggal</td><td>:</td><td>{tanggal}</td></tr>'
        f'</table>'
    )


# ─────────────────────────────────────────────
# 4. SIDEBAR — SEMUA VARIABEL SELALU TERDEFINISI
# ─────────────────────────────────────────────
with st.sidebar:
    st.header("📋 PANEL KONTROL")
    wilayah  = st.selectbox("Jenis Wilayah", ["Dalam Daerah", "Luar Daerah"])
    tab_menu = st.radio("Menu", ["Input & Cetak", "Kelola Register"])

    show_input = (tab_menu == "Input & Cetak")

    if show_input:
        opsi_cetak = st.multiselect(
            "Pilih Dokumen",
            ["SPT", "SPD Depan", "SPD Belakang"],
            default=["SPT", "SPD Depan", "SPD Belakang"],
        )
    else:
        opsi_cetak = []

    # DATA PEGAWAI — selalu render agar session_state konsisten
    with st.expander("👤 DATA PEGAWAI", expanded=show_input):
        c1, c2 = st.columns(2)
        if c1.button("➕ Tambah"): st.session_state.jml += 1
        if c2.button("➖ Hapus") and st.session_state.jml > 1: st.session_state.jml -= 1

        daftar = []
        for i in range(st.session_state.jml):
            st.markdown(f"**Pegawai {i+1}**")
            daftar.append({
                "nama":   st.text_input("Nama",      f"Nama Pegawai {i+1}", key=f"n{i}"),
                "nip":    st.text_input("NIP",       "19XXXXXXXXXXXXXX",    key=f"nip{i}"),
                "gol":    st.text_input("Gol",       "III/a",               key=f"g{i}"),
                "jab":    st.text_input("Jabatan",   "Pelaksana",           key=f"j{i}"),
                "spd":    st.text_input("No SPD",    "530/02/2026",         key=f"spd{i}"),
                "lembar": st.text_input("Lembar ke", "I",                   key=f"lbr{i}"),
            })

    # DATA PERJALANAN — selalu render
    with st.expander("📄 DATA PERJALANAN", expanded=False):
        no_spt   = st.text_input("Nomor SPT",         "094/Prokopim/557/02/2026")
        kode_spd = st.text_input("Kode No SPD",       "094/Prokopim")
        maksud   = st.text_area( "Maksud Perjalanan", "Dalam rangka mendampingi...")
        tujuan   = st.text_input("Tujuan",            "Kecamatan Riung")
        alat     = st.text_input("Alat Angkut",       "Mobil Dinas")
        lama     = st.text_input("Lama Hari",         "1 (Satu) hari")
        tgl_bkt  = st.text_input("Tanggal Berangkat", "17 Maret 2026")
        tgl_kbl  = st.text_input("Tanggal Pulang",    "17 Maret 2026")
        default_dasar = "DPA Bagian Perekonomian dan SDA Setda Ngada 2026" if wilayah == "Dalam Daerah" else ""
        anggaran = st.text_area("Dasar Anggaran", value=default_dasar)

    # TANDA TANGAN — selalu render
    with st.expander("🖋️ TANDA TANGAN", expanded=False):
        ttd_label = st.selectbox("Penandatangan", ["An. BUPATI NGADA", "WAKIL BUPATI NGADA", "BUPATI NGADA"])
        pjb       = st.text_input("Nama Pejabat",  "Yohanes C. Watu Ngebu, S.Sos., M.Si")
        gol_pjb   = st.text_input("Pangkat/Gol",   "Pembina Utama Muda - IV/c")
        jab_ttd   = st.text_input("Jabatan Utama", "Pj. Sekretaris Daerah")
        ub        = st.text_input("Ub.",            "Asisten Perekonomian dan Pembangunan")
        nip_ttd   = st.text_input("NIP",           "19710328 199203 1 011")

    st.markdown("---")

    if show_input:
        # Tombol cetak
        if st.button("🖨️ PROSES CETAK & SIMPAN", use_container_width=True):
            if not tujuan.strip():
                st.warning("Isi kolom Tujuan terlebih dahulu.")
            else:
                for p in daftar:
                    st.session_state.arsip_register.append({
                        "Nama":      p["nama"],
                        "No SPT":    no_spt,
                        "No SPD":    p["spd"],
                        "Tujuan":    tujuan,
                        "Berangkat": tgl_bkt,
                        "Pulang":    tgl_kbl,
                        "Lama":      lama,
                        "Ket":       wilayah,
                    })
                st.success(f"✅ {len(daftar)} data tersimpan.")
                save_register(st.session_state.arsip_register)
                st.components.v1.html(
                    "<script>setTimeout(function(){ window.parent.print(); }, 1200);</script>",
                    height=0,
                )
    else:
        # Tombol kosongkan di tab register
        if st.session_state.arsip_register:
            if st.button("🧹 Kosongkan Semua Data", use_container_width=True):
                st.session_state.arsip_register = []
                save_register([])
                st.rerun()

    # Download Excel — muncul di kedua tab jika ada data
    if st.session_state.arsip_register:
        df_xl  = pd.DataFrame(st.session_state.arsip_register)
        buf    = BytesIO()
        with pd.ExcelWriter(buf, engine="xlsxwriter") as writer:
            df_xl.to_excel(writer, index=False, sheet_name="Register_SPD")
        st.markdown("---")
        st.download_button(
            label="📥 DOWNLOAD REGISTER (EXCEL)",
            data=buf.getvalue(),
            file_name=f"Register_SPD_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )


# ─────────────────────────────────────────────
# 5. AREA UTAMA
# ─────────────────────────────────────────────

# ══ TAB KELOLA REGISTER ══════════════════════
if tab_menu == "Kelola Register":
    st.markdown("## 📂 Riwayat Register SPD")

    data = st.session_state.arsip_register
    if data:
        df_reg = pd.DataFrame(data)

        # Tampilkan ringkasan metrik
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Perjalanan", len(df_reg))
        c2.metric("Dalam Daerah",  len(df_reg[df_reg["Ket"] == "Dalam Daerah"]))
        c3.metric("Luar Daerah",   len(df_reg[df_reg["Ket"] == "Luar Daerah"]))

        st.markdown("---")

        # Tabel lengkap
        st.dataframe(
            df_reg,
            use_container_width=True,
            height=400,
            column_config={
                "Nama":      st.column_config.TextColumn("Nama Pegawai", width="medium"),
                "No SPT":    st.column_config.TextColumn("No. SPT",      width="medium"),
                "No SPD":    st.column_config.TextColumn("No. SPD",      width="small"),
                "Tujuan":    st.column_config.TextColumn("Tujuan",       width="medium"),
                "Berangkat": st.column_config.TextColumn("Tgl Berangkat",width="small"),
                "Pulang":    st.column_config.TextColumn("Tgl Pulang",   width="small"),
                "Lama":      st.column_config.TextColumn("Lama",         width="small"),
                "Ket":       st.column_config.TextColumn("Jenis",        width="small"),
            },
            hide_index=False,
        )
        st.caption(f"Menampilkan **{len(df_reg)}** data tersimpan. Data bertahan walau halaman di-refresh.")

    else:
        st.info(
            "📭 Belum ada data register.\n\n"
            "Pilih **Input & Cetak** di sidebar → isi form → tekan **🖨️ Proses Cetak & Simpan**."
        )

# ══ TAB INPUT & CETAK — render dokumen ═══════
else:
    ttd_args = (ttd_label, jab_ttd, ub, pjb, gol_pjb, nip_ttd)

    kop_pemda = (
        f'<table class="kop-table"><tr>'
        f'<td width="15%"><img src="data:image/png;base64,{logo.PEMDA}" width="75"></td>'
        f'<td class="kop-teks"><h3>PEMERINTAH KABUPATEN NGADA</h3>'
        f'<h2>SEKRETARIAT DAERAH</h2>'
        f'<p>Jln. Soekarno - Hatta No. 1 Telp (0384) 2225834</p>'
        f'<p class="text-bold">BAJAWA</p></td>'
        f'<td width="15%"></td></tr></table>'
    )
    kop_garuda = (
        f'<div class="kop-garuda">'
        f'<img src="data:image/png;base64,{logo.GARUDA}"><h2>BUPATI NGADA</h2></div>'
    )
    kop_aktif = kop_garuda if wilayah == "Luar Daerah" else kop_pemda

    html_out = '<div class="main-container">'

    # ── SPT ──────────────────────────────────────
    if "SPT" in opsi_cetak:
        baris_pegawai = ""
        for i, p in enumerate(daftar):
            baris_pegawai += (
                f"<tr>"
                f"<td width='12%'>{'Kepada' if i == 0 else ''}</td>"
                f"<td width='5%'>{'  :' if i == 0 else ''}</td>"
                f"<td width='5%'>{i+1}.</td>"
                f"<td width='20%'>Nama</td><td width='5%'>:</td>"
                f"<td><b>{p['nama']}</b></td></tr>"
                f"<tr><td></td><td></td><td></td><td>Pangkat/Gol</td><td>:</td><td>{p['gol']}</td></tr>"
                f"<tr><td></td><td></td><td></td><td>NIP</td><td>:</td><td>{p['nip']}</td></tr>"
                f"<tr><td></td><td></td><td></td><td>Jabatan</td><td>:</td><td>{p['jab']}</td></tr>"
            )

        html_out += f"""
        <div class="kertas">
            {kop_aktif}
            <div class="judul-rapat">
                <h3 class="text-bold underline">SURAT PERINTAH TUGAS</h3>
                <p>NOMOR : {no_spt}</p>
            </div>
            <div style="margin-top:10px;">
                <table class="visum-table">
                    <tr><td width="12%">Dasar</td><td width="5%">:</td><td>{anggaran}</td></tr>
                </table>
                <p class="text-center text-bold" style="margin:10px 0;">M E M E R I N T A H K A N</p>
                <table class="visum-table">{baris_pegawai}</table>
                <table class="visum-table" style="margin-top:25px;">
                    <tr><td width="12%">Untuk</td><td width="5%">:</td><td>{maksud} ke {tujuan}</td></tr>
                </table>
            </div>
            {get_ttd(90, *ttd_args)}
        </div>"""

    # ── SPD DEPAN ─────────────────────────────────
    if "SPD Depan" in opsi_cetak:
        for p in daftar:
            html_out += f"""
            <div class="kertas">
                {kop_pemda}
                <div style="margin-left:60%; line-height:1.0;">
                    <table class="visum-table">
                        <tr><td width="40%">Lembar ke</td><td width="5%">:</td><td>{p['lembar']}</td></tr>
                        <tr><td>Kode No</td><td>:</td><td>{kode_spd}</td></tr>
                        <tr><td>Nomor</td><td>:</td><td>{p['spd']}</td></tr>
                    </table>
                </div>
                <div class="judul-rapat" style="margin-top:5px;">
                    <h3 class="text-bold underline">SURAT PERJALANAN DINAS</h3>
                    <h3 class="text-bold">(SPD)</h3>
                </div>
                <table class="tabel-border" style="margin-top:10px;">
                    <tr><td class="col-no">1.</td><td width="42%">Pejabat pemberi perintah</td><td colspan="3"><b>BUPATI NGADA</b></td></tr>
                    <tr><td class="col-no">2.</td><td>Nama Pegawai diperintah</td><td colspan="3"><b>{p['nama']}</b></td></tr>
                    <tr><td class="col-no" rowspan="3">3.</td><td>a. Pangkat/Golongan</td><td colspan="3">{p['gol']}</td></tr>
                    <tr><td>b. Jabatan</td><td colspan="3">{p['jab']}</td></tr>
                    <tr><td>c. Tingkat Menurut Peraturan</td><td colspan="3">-</td></tr>
                    <tr><td class="col-no">4.</td><td>Maksud Perjalanan Dinas</td><td colspan="3">{maksud}</td></tr>
                    <tr><td class="col-no">5.</td><td>Alat angkut</td><td colspan="3">{alat}</td></tr>
                    <tr><td class="col-no" rowspan="2">6.</td><td>a. Tempat Berangkat</td><td colspan="3">Bajawa</td></tr>
                    <tr><td>b. Tempat Tujuan</td><td colspan="3">{tujuan}</td></tr>
                    <tr><td class="col-no" rowspan="3">7.</td><td>Lamanya Perjalanan Dinas</td><td colspan="3">{lama}</td></tr>
                    <tr><td>a. Tanggal Berangkat</td><td colspan="3">{tgl_bkt}</td></tr>
                    <tr><td>b. Tanggal Harus Kembali</td><td colspan="3">{tgl_kbl}</td></tr>
                    <tr><td class="col-no">8.</td><td>Pengikut: Nama</td><td class="text-center">Tgl Lahir</td><td colspan="2" class="text-center">Keterangan</td></tr>
                    <tr style="height:20px;"><td></td><td>1.</td><td></td><td colspan="2"></td></tr>
                    <tr><td class="col-no" rowspan="3">9.</td><td>Pembebanan Anggaran</td><td colspan="3"></td></tr>
                    <tr><td>a. Instansi</td><td colspan="3">a. Bagian Perekonomian dan SDA</td></tr>
                    <tr><td>b. Mata Anggaran</td><td colspan="3"></td></tr>
                    <tr><td class="col-no">10.</td><td>Keterangan lain-lain</td><td colspan="3">-</td></tr>
                </table>
                {get_ttd(65, *ttd_args)}
            </div>"""

    # ── SPD BELAKANG ──────────────────────────────
    if "SPD Belakang" in opsi_cetak:
        ttd_belakang = (
            f'<div style="text-align:center;line-height:1.2;font-size:10pt;margin-top:5px;">'
            f'<b>An. BUPATI NGADA</b><br>{jab_ttd},'
            f'<div style="height:55px;"></div>'
            f'<b><u>{pjb}</u></b><br>{gol_pjb}<br>NIP. {nip_ttd}</div>'
        )

        if wilayah == "Dalam Daerah":
            blok_ii_kiri = render_visum("II.", "Tiba di", tujuan, tgl_bkt)
        else:
            blok_ii_kiri = (
                f'<table class="visum-table">'
                f'<tr><td width="10%">II.</td><td width="35%">Tiba di</td>'
                f'<td width="5%">:</td><td>{tujuan}</td></tr>'
                f'</table>'
            )

        html_out += f"""
        <div class="kertas">
            <table class="tabel-border" style="height:82%;">
                <tr style="height:180px;">
                    <td width="50%"></td>
                    <td style="padding:10px;">
                        {render_visum("I.", "Berangkat dari", "Bajawa", tgl_bkt)}
                        <table class="visum-table">
                            <tr><td width="10%"></td><td width="35%">Ke</td><td width="5%">:</td><td>{tujuan}</td></tr>
                        </table>
                        {ttd_belakang}
                    </td>
                </tr>
                <tr style="height:160px;">
                    <td>{blok_ii_kiri}</td>
                    <td style="padding:10px;">
                        {render_visum("", "Berangkat dari", tujuan, tgl_kbl, show_num=False)}
                        <table class="visum-table">
                            <tr><td width="10%"></td><td width="35%">Ke</td><td width="5%">:</td><td>Bajawa</td></tr>
                        </table>
                    </td>
                </tr>
                <tr style="height:160px;">
                    <td>{render_visum("III.", "Tiba di", "", "")}</td>
                    <td style="padding:10px;">{render_visum("", "Berangkat dari", "", "", show_num=False)}</td>
                </tr>
                <tr style="height:160px;">
                    <td>{render_visum("IV.", "Tiba di", "", "")}</td>
                    <td style="padding:10px;">{render_visum("", "Berangkat dari", "", "", show_num=False)}</td>
                </tr>
                <tr style="height:180px;">
                    <td>{render_visum("V.", "Tiba Kembali", "Bajawa", tgl_kbl)}</td>
                    <td style="padding:10px;">
                        <p style="font-style:italic;font-size:9.2pt;line-height:1.2;margin-top:5px;">
                            Telah diperiksa, dengan keterangan bahwa perjalanan tersebut atas perintahnya
                            dan semata-mata untuk kepentingan jabatan
                        </p>
                        {ttd_belakang}
                    </td>
                </tr>
            </table>
            <div style="border:1pt solid black;border-top:none;padding:8px;font-size:10pt;">
                <b>VI. Catatan Lain-lain</b>
            </div>
            <div style="border:1pt solid black;border-top:none;padding:8px;font-size:8pt;text-align:justify;color:black;line-height:1.2;">
                <b>VII. Perhatian :</b><br>
                Pejabat yang menerbitkan SPD, pegawai yang melakukan perjalanan dinas, para pejabat yang mengesahkan
                tanggal berangkat/tiba, serta Bendahara Pengeluaran bertanggung jawab berdasarkan peraturan-peraturan
                Keuangan Negara apabila negara menderita rugi akibat kesalahan, kelalaian dan kealpaannya.
            </div>
        </div>"""

    html_out += "</div>"
    st.markdown(html_out, unsafe_allow_html=True)
