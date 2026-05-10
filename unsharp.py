import numpy as np

def uygula(img, k=1.0):
    satir, sutun, kanal_sayisi = img.shape
    f_boyut = 5
    pay = f_boyut // 2
    k = float(k)

    sonuc_img = np.zeros((satir, sutun, kanal_sayisi), dtype=np.uint8)

    for kanal in range(kanal_sayisi):

        paddli_img = np.zeros((satir + 2 * pay, sutun + 2 * pay), dtype=np.float64)
        for i in range(satir):
            for j in range(sutun):
                paddli_img[i + pay, j + pay] = img[i, j, kanal]

        bulanik_img = np.zeros((satir, sutun), dtype=np.float64)
        for i in range(satir):
            for j in range(sutun):
                toplam = 0.0
                for ki in range(f_boyut):
                    for kj in range(f_boyut):
                        toplam += paddli_img[i + ki, j + kj]
                bulanik_img[i, j] = toplam / (f_boyut * f_boyut)

        for i in range(satir):
            for j in range(sutun):
                deger = img[i, j, kanal] + k * (img[i, j, kanal] - bulanik_img[i, j])
                if deger > 255:
                    deger = 255
                elif deger < 0:
                    deger = 0
                sonuc_img[i, j, kanal] = int(deger)

    return sonuc_img
