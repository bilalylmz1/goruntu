import numpy as np
import random

def _mean_filtre(kanal_img, boyut=3):
    satir, sutun = kanal_img.shape
    pad = boyut // 2

    paddli_img = np.zeros((satir + 2 * pad, sutun + 2 * pad), dtype=np.float64)
    for i in range(satir):
        for j in range(sutun):
            paddli_img[i + pad, j + pad] = kanal_img[i, j]

    sonuc_img = np.zeros((satir, sutun), dtype=np.uint8)
    for i in range(satir):
        for j in range(sutun):
            toplam = 0.0
            for ki in range(boyut):
                for kj in range(boyut):
                    toplam += paddli_img[i + ki, j + kj]
            deger = toplam / (boyut * boyut)
            sonuc_img[i, j] = int(deger)
    return sonuc_img

def _median_filtre(kanal_img, boyut=3):
    satir, sutun = kanal_img.shape
    pad = boyut // 2

    paddli_img = np.zeros((satir + 2 * pad, sutun + 2 * pad), dtype=np.float64)
    for i in range(satir):
        for j in range(sutun):
            paddli_img[i + pad, j + pad] = kanal_img[i, j]

    sonuc_img = np.zeros((satir, sutun), dtype=np.uint8)
    for i in range(satir):
        for j in range(sutun):
            pencere = []
            for ki in range(boyut):
                for kj in range(boyut):
                    pencere.append(paddli_img[i + ki, j + kj])
            n = len(pencere)
            for p in range(n):
                for q in range(0, n - p - 1):
                    if pencere[q] > pencere[q + 1]:
                        pencere[q], pencere[q + 1] = pencere[q + 1], pencere[q]
            sonuc_img[i, j] = int(pencere[n // 2])
    return sonuc_img

def uygula(img, oran=0.05):
    satir, sutun, kanal_sayisi = img.shape

    gurultulu_img = np.zeros((satir, sutun, kanal_sayisi), dtype=np.uint8)
    for i in range(satir):
        for j in range(sutun):
            gurultulu_img[i, j] = img[i, j]

    random.seed(42)
    n_piksel = int(satir * sutun * float(oran))
    for _ in range(n_piksel):
        pi = random.randint(0, satir - 1)
        pj = random.randint(0, sutun - 1)
        for k in range(kanal_sayisi):
            gurultulu_img[pi, pj, k] = 0
    for _ in range(n_piksel):
        pi = random.randint(0, satir - 1)
        pj = random.randint(0, sutun - 1)
        for k in range(kanal_sayisi):
            gurultulu_img[pi, pj, k] = 255

    mean_img   = np.zeros((satir, sutun, kanal_sayisi), dtype=np.uint8)
    median_img = np.zeros((satir, sutun, kanal_sayisi), dtype=np.uint8)
    for k in range(kanal_sayisi):
        kanal_img = np.zeros((satir, sutun), dtype=np.uint8)
        for i in range(satir):
            for j in range(sutun):
                kanal_img[i, j] = gurultulu_img[i, j, k]
        kanal_mean   = _mean_filtre(kanal_img)
        kanal_median = _median_filtre(kanal_img)
        for i in range(satir):
            for j in range(sutun):
                mean_img[i, j, k]   = kanal_mean[i, j]
                median_img[i, j, k] = kanal_median[i, j]

    return {
        'Gürültülü':        gurultulu_img,
        'Ortalama Filtre':  mean_img,
        'Medyan Filtre':    median_img,
    }
