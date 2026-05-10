import numpy as np
from gri import uygula as to_gray

def _mean_filtre(img, boyut=3):
    h, w = img.shape
    pad = boyut // 2
    paddli = np.zeros((h + 2 * pad, w + 2 * pad), dtype=np.float64)
    for i in range(h):
        for j in range(w):
            paddli[i + pad, j + pad] = img[i, j]
    sonuc = np.zeros((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            toplam = 0.0
            for ki in range(boyut):
                for kj in range(boyut):
                    toplam += paddli[i + ki, j + kj]
            deger = toplam / (boyut * boyut)
            if deger > 255:
                deger = 255
            sonuc[i, j] = int(deger)
    return sonuc

def _median_filtre(img, boyut=3):
    h, w = img.shape
    pad = boyut // 2
    paddli = np.zeros((h + 2 * pad, w + 2 * pad), dtype=np.float64)
    for i in range(h):
        for j in range(w):
            paddli[i + pad, j + pad] = img[i, j]
    sonuc = np.zeros((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            pencere = []
            for ki in range(boyut):
                for kj in range(boyut):
                    pencere.append(paddli[i + ki, j + kj])
            pencere.sort()
            sonuc[i, j] = int(pencere[len(pencere) // 2])
    return sonuc

def uygula(img, oran=0.05):
    """Tuz-biber gürültüsü ekle, ardından mean ve median filtrelerini uygula.
    Üç görüntüyü yan yana döndürür: gürültülü | mean | median"""
    gray = to_gray(img)
    h, w = gray.shape
    gurultulu = np.zeros((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            gurultulu[i, j] = gray[i, j]
    # Tuz-biber: rastgele pikselleri 0 veya 255 yap
    import random
    random.seed(42)
    n_piksel = int(h * w * float(oran))
    for _ in range(n_piksel):
        pi = random.randint(0, h - 1)
        pj = random.randint(0, w - 1)
        gurultulu[pi, pj] = 0
    for _ in range(n_piksel):
        pi = random.randint(0, h - 1)
        pj = random.randint(0, w - 1)
        gurultulu[pi, pj] = 255

    mean_sonuc   = _mean_filtre(gurultulu)
    median_sonuc = _median_filtre(gurultulu)

    # Üç sonucu yan yana birleştir
    sonuc = np.zeros((h, w * 3), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            sonuc[i, j]           = gurultulu[i, j]
            sonuc[i, j + w]       = mean_sonuc[i, j]
            sonuc[i, j + 2 * w]   = median_sonuc[i, j]
    return sonuc
