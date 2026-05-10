import numpy as np

def uygula(img, olcek=1.5):
    """En yakın komşu interpolasyonu ile ölçeklendirme."""
    olcek = float(olcek)
    h, w = img.shape[:2]
    yeni_h = int(h * olcek)
    yeni_w = int(w * olcek)
    kanallar = 1 if img.ndim == 2 else img.shape[2]
    if kanallar == 1:
        sonuc = np.zeros((yeni_h, yeni_w), dtype=img.dtype)
        for yi in range(yeni_h):
            for xi in range(yeni_w):
                src_x = int(xi * w / yeni_w)
                src_y = int(yi * h / yeni_h)
                sonuc[yi, xi] = img[src_y, src_x]
    else:
        sonuc = np.zeros((yeni_h, yeni_w, kanallar), dtype=img.dtype)
        for yi in range(yeni_h):
            for xi in range(yeni_w):
                src_x = int(xi * w / yeni_w)
                src_y = int(yi * h / yeni_h)
                sonuc[yi, xi] = img[src_y, src_x]
    return sonuc
