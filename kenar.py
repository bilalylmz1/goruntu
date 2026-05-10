import numpy as np
from gri import uygula as to_gray

Kx = [[-1, 0, 1],
      [-1, 0, 1],
      [-1, 0, 1]]

Ky = [[-1, -1, -1],
      [ 0,  0,  0],
      [ 1,  1,  1]]

def _konvol(gri_img, kernel, satir, sutun):
    sonuc_img = np.zeros((satir, sutun), dtype=np.float64)

    for i in range(1, satir - 1):
        for j in range(1, sutun - 1):
            toplam = 0.0
            for ki in range(3):
                for kj in range(3):
                    toplam += float(gri_img[i - 1 + ki, j - 1 + kj]) * kernel[ki][kj]
            sonuc_img[i, j] = toplam
    return sonuc_img

def uygula(img):
    gri_img = to_gray(img)
    satir, sutun = gri_img.shape

    Gx = _konvol(gri_img, Kx, satir, sutun)
    Gy = _konvol(gri_img, Ky, satir, sutun)

    sonuc_img = np.zeros((satir, sutun), dtype=np.uint8)
    for i in range(satir):
        for j in range(sutun):
            deger = abs(Gx[i, j]) + abs(Gy[i, j])
            if deger > 255:
                deger = 255
            elif deger < 0:
                deger = 0
            sonuc_img[i, j] = int(deger)
    return sonuc_img
