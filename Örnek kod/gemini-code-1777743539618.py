import cv2
import numpy as np

# 1. Görüntüyü okuyoruz (Temel metod, izinli)
img = cv2.imread('deneme.jpg')

# Görüntü boyutlarını alalım
# satir -> yükseklik, sutun -> genişlik, kanal -> RGB (3)
satir, sutun, kanal = img.shape

# 2. Renkli görüntüyü manuel olarak gri seviyeye dönüştürelim
# Python/OpenCV'de renk sırası BGR (Blue-Green-Red) şeklindedir.
# Formül: 0.299*R + 0.587*G + 0.114*B
gri_img = np.zeros((satir, sutun), dtype=np.uint8)

for i in range(satir):
    for j in range(sutun):
        b = img[i, j, 0]
        g = img[i, j, 1]
        r = img[i, j, 2]
        # Gri değeri hesapla ve matrise yerleştir
        gri_img[i, j] = int(0.299 * r + 0.587 * g + 0.114 * b)

# 3. Eşik değerini belirle
esik_degeri = 128

# 4. Binary (ikili) matrisi oluştur
# Başlangıçta her yer siyah (0) olsun
binary_img = np.zeros((satir, sutun), dtype=np.uint8)

# 5. Matris üzerinde tek tek gezerek eşikleme yapıyoruz
for i in range(satir):
    for j in range(sutun):
        if gri_img[i, j] >= esik_degeri:
            binary_img[i, j] = 255  # Beyaz (Python'da görselleştirmek için 255 kullanılır)
        else:
            binary_img[i, j] = 0    # Siyah

# 6. Sonuçları göster
cv2.imshow('Gri Goruntu', gri_img)
cv2.imshow('Binary Goruntu', binary_img)

# Pencerenin kapanması için bir tuşa basılmasını bekle
cv2.waitKey(0)
cv2.destroyAllWindows()