import numpy as np
from gri import uygula as to_gray

def _binary(gri_img, esik=128):
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

def _genisle(binary_img):
    satir, sutun = binary_img.shape
    sonuc_img = np.zeros((satir, sutun), dtype=np.uint8)
    for i in range(1, satir - 1):
        for j in range(1, sutun - 1):
            bulundu = False
            for ki in range(-1, 2):
                for kj in range(-1, 2):
                    if binary_img[i + ki, j + kj] == 255:
                        bulundu = True
            if bulundu:
                sonuc_img[i, j] = 255
    return sonuc_img

def _asindır(binary_img):
    satir, sutun = binary_img.shape
    sonuc_img = np.zeros((satir, sutun), dtype=np.uint8)
    for i in range(1, satir - 1):
        for j in range(1, sutun - 1):
            hepsi_255 = True
            for ki in range(-1, 2):
                for kj in range(-1, 2):
                    if binary_img[i + ki, j + kj] != 255:
                        hepsi_255 = False
            if hepsi_255:
                sonuc_img[i, j] = 255
    return sonuc_img

def uygula(img, esik=128):
    gri_img = to_gray(img)
    binary_img = _binary(gri_img, esik)

    return {
        'Genişleme': _genisle(binary_img),
        'Aşınma':    _asindır(binary_img),
        'Açma':      _genisle(_asindır(binary_img)),
        'Kapama':    _asindır(_genisle(binary_img)),
    }
