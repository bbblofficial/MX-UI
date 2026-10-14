# qr_generator.py — local QR generation (no external services)
import base64
import io

import qrcode
from qrcode.constants import ERROR_CORRECT_M


def qr_png_bytes(data: str, size: int = 300, dark: str = "#0f1d1c", light: str = "#ffffff") -> bytes:
    qr = qrcode.QRCode(version=None, error_correction=ERROR_CORRECT_M, box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=dark, back_color=light).convert("RGB")
    size = max(120, min(int(size or 300), 1024))
    img = img.resize((size, size), resample=0)  # nearest: keeps modules crisp
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def generate_qr_base64(data: str, size: int = 300) -> str:
    return "data:image/png;base64," + base64.b64encode(qr_png_bytes(data, size)).decode()
