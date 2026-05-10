import numpy as np
from gri import uygula as to_gray

# Prewitt cekirdekleri (elle tanimlanmis 3x3 matrisler)
# Yatay kenar algilama icin x-yonu cekirdegi
Kx = [[-1, 0, 1],
      [-1, 0, 1],
      [-1, 0, 1]]

# Dikey kenar algilama icin y-yonu cekirdegi
Ky = [[-1, -1, -1],
      [ 0,  0,  0],
      [ 1,  1,  1]]

def _konvol(gri_img, kernel, satir, sutun):
    """3x3 cekirdekle konvolusyon (sifir padding, piksel piksel dongu)"""
    # Sonuc matrisi (float hassasiyette)
    sonuc_img = np.zeros((satir, sutun), dtype=np.float64)

    # Kenardan 1 piksel ic kismi isliyoruz (sifir padding simule edilmis)
    for i in range(1, satir - 1):
        for j in range(1, sutun - 1):
            toplam = 0.0
            for ki in range(3):
                for kj in range(3):
                    toplam += gri_img[i - 1 + ki, j - 1 + kj] * kernel[ki][kj]
            sonuc_img[i, j] = toplam
    return sonuc_img

def uygula(img):
    """Prewitt operatoru ile kenar tespiti: gradyan = |Gx| + |Gy|"""
    gri_img = to_gray(img)
    satir, sutun = gri_img.shape

    # --- Adim 1: Yatay ve dikey gradyan haritalarini hesapla ---
    Gx = _konvol(gri_img, Kx, satir, sutun)
    Gy = _konvol(gri_img, Ky, satir, sutun)

    # --- Adim 2: Gradyan buyuklugunu hesapla ve 0-255 araligina sikistir ---
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
