import numpy as np
from gri import uygula as to_gray

def uygula(img, esik=128):
    """Tek eşikleme: piksel >= esik -> 255, değilse -> 0"""
    gray = to_gray(img)
    h, w = gray.shape
    sonuc = np.zeros((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            if gray[i, j] >= int(esik):
                sonuc[i, j] = 255
            else:
                sonuc[i, j] = 0
    return sonuc
