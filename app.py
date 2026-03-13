# FUNGSI UNTUK MENGUBAH GAMBAR MENJADI BASE64
def get_image_as_base64(path):
    try:
        # Kita paksa sistem mencari file di folder kerja saat ini
        if path.exists():
            with open(str(path), "rb") as image_file:
                return base64.b64encode(image_file.read()).decode()
        return None
    except Exception as e:
        return None

# MENCARI LOGO - Pastikan nama di GitHub persis: logo_ngada.jpg
logo_path = Path(__file__).parent / "logo_ngada.jpg"
logo_base64 = get_image_as_base64(logo_path)

if logo_base64:
    logo_html = f'<img src="data:image/jpeg;base64,{logo_base64}" class="logo-img">'
else:
    # Jika tetap tidak muncul, kita munculkan teks error kecil tersembunyi untuk debug
    logo_html = '<div style="width: 75px; color: red; font-size: 8pt;">Logo Kosong</div>'
