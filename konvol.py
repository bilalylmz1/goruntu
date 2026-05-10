import numpy as np
from gri import uygula as to_gray

def uygula(img, boyut=3):
    """NxN ortalama filtre konvolüsyonu (sıfırdan, döngüyle)."""
    boyut = int(boyut)
    if boyut % 2 == 0:
        boyut += 1  # tek yap
    gray = to_gray(img).astype(np.float64)
    h, w = gray.shape
    pad = boyut // 2
    paddli = np.zeros((h + 2 * pad, w + 2 * pad))
    paddli[pad:h + pad, pad:w + pad] = gray
    sonuc = np.zeros_like(gray)
    for i in range(h):
        for j in range(w):
            pencere = paddli[i:i + boyut, j:j + boyut]
            sonuc[i, j] = pencere.sum() / (boyut * boyut)
    return np.clip(sonuc, 0, 255).astype(np.uint8)
