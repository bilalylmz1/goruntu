import numpy as np


def resim_toplama(resim_matrisi1, resim_matrisi2):
    satir, sutun, kanal_sayisi = resim_matrisi1.shape
    sonuc_img = np.zeros((satir, sutun, kanal_sayisi), dtype=np.uint8)

    for i in range(satir):
        for j in range(sutun):
            for kanal in range(kanal_sayisi):
                toplam = int(resim_matrisi1[i, j, kanal]) + int(resim_matrisi2[i, j, kanal])
                if toplam > 255:
                    sonuc_img[i, j, kanal] = 255
                else:
                    sonuc_img[i, j, kanal] = toplam
    return sonuc_img


def resim_bolme(resim_matrisi1, resim_matrisi2):
    satir, sutun, kanal_sayisi = resim_matrisi1.shape
    sonuc_img = np.zeros((satir, sutun, kanal_sayisi), dtype=np.uint8)

    for i in range(satir):
        for j in range(sutun):
            for kanal in range(kanal_sayisi):
                pay   = resim_matrisi1[i, j, kanal]
                payda = resim_matrisi2[i, j, kanal]

                if payda == 0:
                    sonuc_img[i, j, kanal] = int(pay / 1)
                else:
                    deger = pay / payda
                    if deger > 255:
                        deger = 255
                    sonuc_img[i, j, kanal] = int(deger)
    return sonuc_img


def uygula(img1, img2, mod='ekle', alfa=0.5):
    """
    Aritmetik islemler iki resim arasinda.
    mod='ekle' -> resim_toplama: C[k] = img1[k] + img2[k]  (255'te kesilir)
    mod='bol'  -> resim_bolme:   C[k] = img1[k] / img2[k]  (payda=0 ise 1 kullan)
    """
    # Iki goruntu farkli boyuttaysa kucuk olani al
    satir = min(img1.shape[0], img2.shape[0])
    sutun = min(img1.shape[1], img2.shape[1])
    resim_matrisi1 = img1[:satir, :sutun]
    resim_matrisi2 = img2[:satir, :sutun]

    if mod == 'ekle':
        return resim_toplama(resim_matrisi1, resim_matrisi2)
    else:  # bol
        return resim_bolme(resim_matrisi1, resim_matrisi2)
