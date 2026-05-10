import numpy as np
from gri import uygula as to_gray

def uygula(img, aci=45):
    """2D rotasyon matrisi + en yakın komşu interpolasyonu ile döndürme."""
    gray = to_gray(img)
    rad = float(aci) * np.pi / 180.0
    cos_a, sin_a = np.cos(rad), np.sin(rad)
    h, w = gray.shape
    cx, cy = w / 2, h / 2
    sonuc = np.zeros_like(gray)
    for yi in range(h):
        for xi in range(w):
            # Ters dönüşüm: hedef piksel -> kaynak piksel
            x0 = cos_a * (xi - cx) + sin_a * (yi - cy) + cx
            y0 = -sin_a * (xi - cx) + cos_a * (yi - cy) + cy
            xr, yr = int(round(x0)), int(round(y0))
            if 0 <= xr < w and 0 <= yr < h:
                sonuc[yi, xi] = gray[yr, xr]
    return sonuc
