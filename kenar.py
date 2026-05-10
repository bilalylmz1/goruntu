import numpy as np
from gri import uygula as to_gray

# Prewitt çekirdekleri (elle tanımlanmış matrisler)
Kx = [[-1, 0, 1],
      [-1, 0, 1],
      [-1, 0, 1]]

Ky = [[-1, -1, -1],
      [ 0,  0,  0],
      [ 1,  1,  1]]

def _konvol(gray, kernel, h, w):
    """3x3 çekirdekle konvolüsyon (sıfır padding, piksel piksel döngü)"""
    sonuc = np.zeros((h, w), dtype=np.float64)
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            toplam = 0.0
            for ki in range(3):
                for kj in range(3):
                    toplam += gray[i - 1 + ki, j - 1 + kj] * kernel[ki][kj]
            sonuc[i, j] = toplam
    return sonuc

def uygula(img):
    """Prewitt operatörü ile kenar tespiti: |Gx| + |Gy|"""
    gray = to_gray(img)
    h, w = gray.shape
    Gx = _konvol(gray, Kx, h, w)
    Gy = _konvol(gray, Ky, h, w)
    sonuc = np.zeros((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            deger = abs(Gx[i, j]) + abs(Gy[i, j])
            if deger > 255:
                deger = 255
            sonuc[i, j] = int(deger)
    return sonuc
