import numpy as np

def uygula(img, aci=90):
    satir, sutun, kanal_sayisi = img.shape
    derece = int(aci) % 360

    if derece == 90:
        sonuc_img = np.zeros((sutun, satir, kanal_sayisi), dtype=np.uint8)
        for i in range(satir):
            for j in range(sutun):
                sonuc_img[j, (satir - 1) - i] = img[i, j]

    elif derece == 180:
        sonuc_img = np.zeros((satir, sutun, kanal_sayisi), dtype=np.uint8)
        for i in range(satir):
            for j in range(sutun):
                sonuc_img[(satir - 1) - i, (sutun - 1) - j] = img[i, j]

    elif derece == 270:
        sonuc_img = np.zeros((sutun, satir, kanal_sayisi), dtype=np.uint8)
        for i in range(satir):
            for j in range(sutun):
                sonuc_img[(sutun - 1) - j, i] = img[i, j]

    else:
        sonuc_img = np.zeros((satir, sutun, kanal_sayisi), dtype=np.uint8)
        for i in range(satir):
            for j in range(sutun):
                sonuc_img[i, j] = img[i, j]

    return sonuc_img
