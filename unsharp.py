import numpy as np
from gri import uygula as to_gray

def uygula(img, k=1.0):
    """Unsharp maskeleme: keskin = orijinal + k*(orijinal - bulanik)"""
    gray = to_gray(img)
    h, w = gray.shape
    boyut = 5
    pad = boyut // 2
    # Sıfır dolgulu genişletilmiş matris
    paddli = np.zeros((h + 2 * pad, w + 2 * pad), dtype=np.float64)
    for i in range(h):
        for j in range(w):
            paddli[i + pad, j + pad] = gray[i, j]
    # 5x5 mean filtre ile bulanıklaştır
    bulanik = np.zeros((h, w), dtype=np.float64)
    for i in range(h):
        for j in range(w):
            toplam = 0.0
            for ki in range(boyut):
                for kj in range(boyut):
                    toplam += paddli[i + ki, j + kj]
            bulanik[i, j] = toplam / (boyut * boyut)
    # Keskinleştir: orijinal + k * (orijinal - bulanik)
    sonuc = np.zeros((h, w), dtype=np.uint8)
    k = float(k)
    for i in range(h):
        for j in range(w):
            deger = gray[i, j] + k * (gray[i, j] - bulanik[i, j])
            if deger > 255:
                deger = 255
            elif deger < 0:
                deger = 0
            sonuc[i, j] = int(deger)
    return sonuc
