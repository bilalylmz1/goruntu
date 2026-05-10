import cv2
import numpy as np

img = cv2.imread('deneme.jpg')
if img is None:
    print("Görüntü bulunamadı!")
else:
    satir, sutun, kanal = img.shape

    img_float = img.astype(float)

    Y = np.zeros((satir, sutun), dtype=np.float64)
    Cb = np.zeros((satir, sutun), dtype=np.float64)
    Cr = np.zeros((satir, sutun), dtype=np.float64)

    for i in range(satir):
        for j in range(sutun):
            b = img_float[i, j, 0]
            g = img_float[i, j, 1]
            r = img_float[i, j, 2]

            Y[i, j] = 16 + (65.481 * r + 128.553 * g + 24.966 * b) / 256
            Cb[i, j] = 128 + (-37.797 * r - 74.203 * g + 112.0 * b) / 256
            Cr[i, j] = 128 + (112.0 * r - 93.786 * g - 18.214 * b) / 256

    Y = np.uint8(np.clip(Y, 0, 255))
    Cb = np.uint8(np.clip(Cb, 0, 255))
    Cr = np.uint8(np.clip(Cr, 0, 255))

    cv2.imshow('Parlaklik (Y)', Y)
    cv2.imshow('Mavi Fark (Cb)', Cb)
    cv2.imshow('Kirmizi Fark (Cr)', Cr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()