import numpy as np
from gri import uygula as to_gray

def uygula(img):
    """Histogram analizi ve germe. Matplotlib ile grafik acar, geri germe sonucu doner."""
    import matplotlib.pyplot as plt

    gri_img = to_gray(img)
    satir, sutun = gri_img.shape

    # --- Adim 1: Orijinal histogram hesapla (sifirdan sayac ile) ---
    hist = [0] * 256
    for i in range(satir):
        for j in range(sutun):
            hist[gri_img[i, j]] += 1

    # --- Adim 2: Min ve max piksel degerlerini bul ---
    min_deger = 255
    maks_deger = 0
    for i in range(satir):
        for j in range(sutun):
            if gri_img[i, j] < min_deger:
                min_deger = gri_img[i, j]
            if gri_img[i, j] > maks_deger:
                maks_deger = gri_img[i, j]

    # --- Adim 3: Histogram germe uygula ---
    # Formul: yeni = (piksel - min) / (maks - min) * 255
    gerilmis_img = np.zeros((satir, sutun), dtype=np.uint8)
    if maks_deger == min_deger:
        for i in range(satir):
            for j in range(sutun):
                gerilmis_img[i, j] = gri_img[i, j]
    else:
        for i in range(satir):
            for j in range(sutun):
                deger = int((gri_img[i, j] - min_deger) / (maks_deger - min_deger) * 255)
                gerilmis_img[i, j] = deger

    # --- Adim 4: Gerilmis histogram hesapla ---
    hist_gerilmis = [0] * 256
    for i in range(satir):
        for j in range(sutun):
            hist_gerilmis[gerilmis_img[i, j]] += 1

    # --- Grafik goster ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    ax1.bar(range(256), hist, width=1, color='steelblue')
    ax1.set_title('Orijinal Histogram')
    ax2.bar(range(256), hist_gerilmis, width=1, color='tomato')
    ax2.set_title('Gerilmis Histogram')
    plt.tight_layout()
    plt.show()

    return gerilmis_img
