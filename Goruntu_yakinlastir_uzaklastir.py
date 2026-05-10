import numpy as np


def uygula(img, olcek=1.5):
    """En yakin komsu interpolasyonu ile olceklendirme."""
    olcek = float(olcek)
    satir, sutun = img.shape[:2]
    yeni_satir = int(satir * olcek)
    yeni_sutun = int(sutun * olcek)
    kanal = 1 if img.ndim == 2 else img.shape[2]

    if kanal == 1:
        sonuc_img = np.zeros((yeni_satir, yeni_sutun), dtype=img.dtype)
        for i in range(yeni_satir):
            for j in range(yeni_sutun):
                # En yakin komsu: hedef koordinatini kaynaga donustur
                src_satir = int(i * satir / yeni_satir)
                src_sutun = int(j * sutun / yeni_sutun)
                sonuc_img[i, j] = img[src_satir, src_sutun]
    else:
        sonuc_img = np.zeros((yeni_satir, yeni_sutun, kanal), dtype=img.dtype)
        for i in range(yeni_satir):
            for j in range(yeni_sutun):
                src_satir = int(i * satir / yeni_satir)
                src_sutun = int(j * sutun / yeni_sutun)
                for k in range(kanal):
                    sonuc_img[i, j, k] = img[src_satir, src_sutun, k]
    return sonuc_img
