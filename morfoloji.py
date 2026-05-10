import numpy as np
from gri import uygula as to_gray

def _binary(img):
    gray = to_gray(img)
    b = np.zeros_like(gray)
    b[gray >= 128] = 255
    return b

def _genisle(b):
    h, w = b.shape
    sonuc = np.zeros_like(b)
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            if b[i-1:i+2, j-1:j+2].max() == 255:
                sonuc[i, j] = 255
    return sonuc

def _asındır(b):
    h, w = b.shape
    sonuc = np.zeros_like(b)
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            if b[i-1:i+2, j-1:j+2].min() == 255:
                sonuc[i, j] = 255
    return sonuc

def uygula(img, islem='d'):
    """
    Morfolojik işlemler (3x3 yapısal eleman):
    islem='d'  -> Genişleme (dilation)
    islem='a'  -> Aşınma (erosion)
    islem='ac' -> Açma (opening)
    islem='ka' -> Kapama (closing)
    """
    b = _binary(img)
    if islem == 'd':
        return _genisle(b)
    elif islem == 'a':
        return _asındır(b)
    elif islem == 'ac':
        return _genisle(_asındır(b))
    else:  # 'ka'
        return _asındır(_genisle(b))
