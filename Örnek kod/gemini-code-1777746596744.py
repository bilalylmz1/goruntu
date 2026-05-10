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
    kernel = np.ones((f_boyut, f_boyut)) / (f_boyut * f_boyut)

    pay = f_boyut // 2
    paddli_img = np.zeros((satir + 2 * pay, sutun + 2 * pay))
    paddli_img[pay:satir + pay, pay:sutun + pay] = gri_img

    sonuc_img = np.zeros((satir, sutun), dtype=np.float64)

    for i in range(satir):
        for j in range(sutun):
            pencere = paddli_img[i : i + f_boyut, j : j + f_boyut]
            
            toplam = 0
            for m in range(f_boyut):
                for n in range(f_boyut):
                    toplam += pencere[m, n] * kernel[m, n]
            
            sonuc_img[i, j] = toplam

    sonuc_img = np.uint8(np.clip(sonuc_img, 0, 255))
    gri_img_uint8 = np.uint8(gri_img)

    cv2.imshow('Orijinal Gri', gri_img_uint8)
    cv2.imshow('Mean Filtre Sonucu (Python)', sonuc_img)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()