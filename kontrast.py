import numpy as np

def uygula(img, alfa=1.5, beta=0):
    satir, sutun = img.shape[:2]
    alfa = float(alfa)
    beta = float(beta)

    if img.ndim == 2:
        sonuc_img = np.zeros((satir, sutun), dtype=np.uint8)
        for i in range(satir):
            for j in range(sutun):
                deger = alfa * img[i, j] + beta
                if deger > 255:
                    deger = 255
                elif deger < 0:
                    deger = 0
                sonuc_img[i, j] = int(deger)
    else:
        kanal_sayisi = img.shape[2]
        sonuc_img = np.zeros((satir, sutun, kanal_sayisi), dtype=np.uint8)
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
