import cv2
import numpy as np

img = cv2.imread('deneme.jpg')
if img is None:
    print("Görüntü bulunamadı!")
else:
    satir, sutun, kanal = img.shape

    gri_img = np.zeros((satir, sutun), dtype=np.float64)
    for i in range(satir):
        for j in range(sutun):
            b, g, r = img[i, j]
            gri_img[i, j] = 0.299 * r + 0.587 * g + 0.114 * b

    f_boyut = 3
    pay = f_boyut // 2
    paddli_img = np.zeros((satir + 2 * pay, sutun + 2 * pay))
    paddli_img[pay:satir + pay, pay:sutun + pay] = gri_img

    bulanik_img = np.zeros((satir, sutun), dtype=np.float64)

    for i in range(satir):
        for j in range(sutun):
            toplam = 0
            for m in range(f_boyut):
                for n in range(f_boyut):
                    toplam += paddli_img[i + m, j + n]
            bulanik_img[i, j] = toplam / (f_boyut * f_boyut)

    maske = gri_img - bulanik_img

    k = 1.0
    keskin_img = gri_img + (k * maske)

    for i in range(satir):
        for j in range(sutun):
            if keskin_img[i, j] > 255:
                keskin_img[i, j] = 255
            elif keskin_img[i, j] < 0:
                keskin_img[i, j] = 0

    gri_sonuc = np.uint8(gri_img)
    bulanik_sonuc = np.uint8(bulanik_img)
    keskin_sonuc = np.uint8(keskin_img)

    maske_gorsel = np.uint8(np.abs(maske))

    cv2.imshow('1. Orijinal Gri', gri_sonuc)
    cv2.imshow('2. Bulanik (Maske Icin)', bulanik_sonuc)
    cv2.imshow('3. Detay Maskesi (Kenarlar)', maske_gorsel)
    cv2.imshow('4. Keskinlestirilmis Goruntu', keskin_sonuc)

    cv2.waitKey(0)
    cv2.destroyAllWindows()