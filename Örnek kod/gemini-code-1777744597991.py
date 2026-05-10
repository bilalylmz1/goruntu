import cv2
import numpy as np

# 1. Görüntüyü oku (Temel okuma metodu)
img = cv2.imread('deneme.jpg')
if img is None:
    print("Görüntü bulunamadı!")
else:
    satir, sutun, kanal = img.shape

    # Hesaplamalarda hassasiyet için float (double) tipine geçiyoruz
    img_float = img.astype(float)

    # Sonuçları saklamak için boş matrisler oluşturuyoruz
    Y = np.zeros((satir, sutun), dtype=np.float64)
    Cb = np.zeros((satir, sutun), dtype=np.float64)
    Cr = np.zeros((satir, sutun), dtype=np.float64)

    # --- Matris Düzeyinde İşlem (Döngü ile) ---
    for i in range(satir):
        for j in range(sutun):
            # OpenCV BGR okuduğu için:
            b = img_float[i, j, 0]
            g = img_float[i, j, 1]
            r = img_float[i, j, 2]

            # ITU-R BT.601 standart formülleri
            Y[i, j] = 16 + (65.481 * r + 128.553 * g + 24.966 * b) / 256
            Cb[i, j] = 128 + (-37.797 * r - 74.203 * g + 112.0 * b) / 256
            Cr[i, j] = 128 + (112.0 * r - 93.786 * g - 18.214 * b) / 256

    # Görselleştirmek için 0-255 arasına sabitleyip uint8'e geri dönüyoruz
    Y = np.uint8(np.clip(Y, 0, 255))
    Cb = np.uint8(np.clip(Cb, 0, 255))
    Cr = np.uint8(np.clip(Cr, 0, 255))

    # Pencereleri göster
    cv2.imshow('Parlaklik (Y)', Y)
    cv2.imshow('Mavi Fark (Cb)', Cb)
    cv2.imshow('Kirmizi Fark (Cr)', Cr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()