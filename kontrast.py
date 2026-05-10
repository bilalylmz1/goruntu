import numpy as np

def uygula(img, alfa=1.5, beta=0):
    """Lineer kontrast ayarlama: yeni_piksel = alfa * piksel + beta, her kanal ayri."""
    satir, sutun, kanal_sayisi = img.shape
    sonuc_img = np.zeros((satir, sutun, kanal_sayisi), dtype=np.uint8)
    alfa = float(alfa)
    beta = float(beta)
    for i in range(satir):
        for j in range(sutun):
            for k in range(kanal_sayisi):
                deger = alfa * img[i, j, k] + beta
                if deger > 255:
                    deger = 255
                elif deger < 0:
                    deger = 0
                sonuc_img[i, j, k] = int(deger)
    return sonuc_img
