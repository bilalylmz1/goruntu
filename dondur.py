import numpy as np

def uygula(img, aci=90):
    """
    Goruntu dondurme (renkli, piksel piksel dongu).
    90'in katlari desteklenir: 90, 180, 270 derece.
    """
    satir, sutun, kanal_sayisi = img.shape
    derece = int(aci) % 360     # 0-359 araligina normalize et

    if derece == 90:
        # 90 derece saat yonu: boyutlar (sutun, satir) yer degistirir
        sonuc_img = np.zeros((sutun, satir, kanal_sayisi), dtype=np.uint8)
        for i in range(satir):
            for j in range(sutun):
                sonuc_img[j, (satir - 1) - i] = img[i, j]

    elif derece == 180:
        # 180 derece: boyutlar ayni kalir, pikseller hem yatay hem dikey ters doner
        sonuc_img = np.zeros((satir, sutun, kanal_sayisi), dtype=np.uint8)
        for i in range(satir):
            for j in range(sutun):
                sonuc_img[(satir - 1) - i, (sutun - 1) - j] = img[i, j]

    elif derece == 270:
        # 270 derece saat yonu: boyutlar (sutun, satir) yer degistirir
        sonuc_img = np.zeros((sutun, satir, kanal_sayisi), dtype=np.uint8)
        for i in range(satir):
            for j in range(sutun):
                sonuc_img[(sutun - 1) - j, i] = img[i, j]

    else:
        # 0 veya tanimsiz derece: orijinali don
        sonuc_img = np.zeros((satir, sutun, kanal_sayisi), dtype=np.uint8)
        for i in range(satir):
            for j in range(sutun):
                sonuc_img[i, j] = img[i, j]

    return sonuc_img
