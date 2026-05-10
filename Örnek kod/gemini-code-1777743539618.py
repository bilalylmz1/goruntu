import cv2
import numpy as np

img = cv2.imread('deneme.jpg')

satir, sutun, kanal = img.shape

gri_img = np.zeros((satir, sutun), dtype=np.uint8)

for i in range(satir):
    for j in range(sutun):
        b = img[i, j, 0]
        g = img[i, j, 1]
        r = img[i, j, 2]
        gri_img[i, j] = int(0.299 * r + 0.587 * g + 0.114 * b)

esik_degeri = 128

binary_img = np.zeros((satir, sutun), dtype=np.uint8)

for i in range(satir):
    for j in range(sutun):
        if gri_img[i, j] >= esik_degeri:
            binary_img[i, j] = 255
        else:
            binary_img[i, j] = 0

cv2.imshow('Gri Goruntu', gri_img)
cv2.imshow('Binary Goruntu', binary_img)

cv2.waitKey(0)
cv2.destroyAllWindows()