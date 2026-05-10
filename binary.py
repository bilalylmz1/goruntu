import numpy as np
from gri import uygula as to_gray

def uygula(img, esik=128):
    """Gri goruntu uzerinde esikleme: piksel >= esik -> 255, degilse -> 0"""
    gri_img = to_gray(img)
    satir, sutun = gri_img.shape
    binary_img = np.zeros((satir, sutun), dtype=np.uint8)
    esik_degeri = int(esik)
    for i in range(satir):
        for j in range(sutun):
            if gri_img[i, j] >= esik_degeri:
                binary_img[i, j] = 255
            else:
                binary_img[i, j] = 0
    return binary_img
