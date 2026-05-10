import numpy as np
from gri import uygula as to_gray

def uygula(img, x1=0, y1=0, x2=100, y2=100):
    """Goruntu uzerinde piksel piksel gezinerek (x1,y1)-(x2,y2) bolgesini kirpar."""
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    satir, sutun = img.shape[:2]

    # Koordinatlari goruntu sinirlarinda tut
    if x1 < 0:
        x1 = 0
    if x1 > sutun - 1:
        x1 = sutun - 1
    if x2 < x1 + 1:
        x2 = x1 + 1
    if x2 > sutun:
        x2 = sutun
    if y1 < 0:
        y1 = 0
    if y1 > satir - 1:
        y1 = satir - 1
    if y2 < y1 + 1:
        y2 = y1 + 1
    if y2 > satir:
        y2 = satir

    kirp_satir = y2 - y1
    kirp_sutun = x2 - x1

    kanal = 1 if img.ndim == 2 else img.shape[2]

    if kanal == 1:
        sonuc_img = np.zeros((kirp_satir, kirp_sutun), dtype=img.dtype)
        for i in range(kirp_satir):
            for j in range(kirp_sutun):
                sonuc_img[i, j] = img[y1 + i, x1 + j]
    else:
        sonuc_img = np.zeros((kirp_satir, kirp_sutun, kanal), dtype=img.dtype)
        for i in range(kirp_satir):
            for j in range(kirp_sutun):
                for k in range(kanal):
                    sonuc_img[i, j, k] = img[y1 + i, x1 + j, k]
    return sonuc_img
