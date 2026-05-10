import numpy as np
from gri import uygula as to_gray

def uygula(img, mod='ekle', alfa=0.5):
    """
    Aritmetik işlemler.
    mod='ekle'  -> C = alfa*A + (1-alfa)*B  (A: gri, B: negatifi)
    mod='bol'   -> piksel değerleri 2'ye bölünür
    """
    gray = to_gray(img)
    h, w = gray.shape
    sonuc = np.zeros((h, w), dtype=np.uint8)
    alfa = float(alfa)
    for i in range(h):
        for j in range(w):
            if mod == 'ekle':
                negatif = 255 - gray[i, j]
                deger = alfa * gray[i, j] + (1 - alfa) * negatif
            else:  # bol
                deger = gray[i, j] / 2.0
            if deger > 255:
                deger = 255
            elif deger < 0:
                deger = 0
            sonuc[i, j] = int(deger)
    return sonuc
