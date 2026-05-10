import numpy as np
from gri import uygula as to_gray

def uygula(img):
    import matplotlib.pyplot as plt

    gri_img = to_gray(img)
    satir, sutun = gri_img.shape

    hist = [0] * 256
    for i in range(satir):
        for j in range(sutun):
            hist[int(gri_img[i, j])] += 1

    toplam = satir * sutun
    kesme  = toplam // 100

    kumulatif = 0
    low_cut = 0
    for v in range(256):
        kumulatif += hist[v]
        if kumulatif >= kesme:
            low_cut = v
            break

    kumulatif = 0
    high_cut = 255
    for v in range(255, -1, -1):
        kumulatif += hist[v]
        if kumulatif >= kesme:
            high_cut = v
            break

    gerilmis_img = np.zeros((satir, sutun), dtype=np.uint8)
    hist_sonra   = [0] * 256
    aralik = high_cut - low_cut

    for i in range(satir):
        for j in range(sutun):
            if aralik == 0:
                yeni = int(gri_img[i, j])
            else:
                yeni = int((int(gri_img[i, j]) - low_cut) / aralik * 255)
                if yeni < 0:
                    yeni = 0
                elif yeni > 255:
                    yeni = 255
            gerilmis_img[i, j] = yeni
            hist_sonra[yeni] += 1

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    ax1.bar(range(256), hist,       width=1, color='steelblue')
    ax1.set_title('Gri Orijinal Histogram')
    ax1.set_xlabel('Piksel Degeri')
    ax1.set_ylabel('Piksel Sayisi')
    ax2.bar(range(256), hist_sonra, width=1, color='tomato')
    ax2.set_title('Gerilmis Histogram')
    ax2.set_xlabel('Piksel Degeri')
    plt.tight_layout()
    plt.show()

    return {'Gri Orijinal': gri_img, 'Gerilmis': gerilmis_img}
