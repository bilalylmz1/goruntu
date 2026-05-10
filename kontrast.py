import numpy as np
from gri import uygula as to_gray

def uygula(img, alfa=1.5, beta=0):
    """Lineer kontrast ayarlama: yeni_piksel = alfa * piksel + beta, 0-255 arasına sıkıştır"""
    gray = to_gray(img)
    h, w = gray.shape
    sonuc = np.zeros((h, w), dtype=np.uint8)
    alfa = float(alfa)
    beta = float(beta)
    for i in range(h):
        for j in range(w):
            deger = alfa * gray[i, j] + beta
            if deger > 255:
                deger = 255
            elif deger < 0:
                deger = 0
            sonuc[i, j] = int(deger)
    return sonuc
