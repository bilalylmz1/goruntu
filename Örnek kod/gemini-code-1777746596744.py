import cv2
import numpy as np

# 1. Görüntüyü oku (Temel metod)
img = cv2.imread('deneme.jpg')
if img is None:
    print("Görüntü bulunamadı!")
else:
    satir, sutun, kanal = img.shape

    # 2. Manuel Gri Seviye Dönüşümü
    # (Konvülasyon genellikle tek kanal üzerinde uygulanır)
    gri_img = np.zeros((satir, sutun), dtype=np.float64)
    for i in range(satir):
        for j in range(sutun):
            b, g, r = img[i, j]
            gri_img[i, j] = 0.299 * r + 0.587 * g + 0.114 * b

    # 3. Filtre (Kernel) Hazırlığı
    # 3x3 boyutunda bir ortalama filtresi: Her hücre 1/9 değerinde.
    f_boyut = 3
    kernel = np.ones((f_boyut, f_boyut)) / (f_boyut * f_boyut)

    # 4. Padding (Kenar Doldurma) İşlemi
    # Filtre kenarlardayken dışarı taşmasın diye görüntünün etrafını 0 ile sarıyoruz.
    pay = f_boyut // 2
    # np.zeros ile orijinalden biraz daha büyük bir matris oluşturuyoruz
    paddli_img = np.zeros((satir + 2 * pay, sutun + 2 * pay))
    # Orijinal görüntüyü merkeze yerleştiriyoruz
    paddli_img[pay:satir + pay, pay:sutun + pay] = gri_img

    # 5. Sonuç Matrisini Oluştur
    sonuc_img = np.zeros((satir, sutun), dtype=np.float64)

    # 6. Ana Konvülasyon Döngüsü (Piksel piksel gezinti)
    for i in range(satir):
        for j in range(sutun):
            # Görüntü üzerinde filtrenin altına denk gelen 3x3'lük bölgeyi kesip alıyoruz
            pencere = paddli_img[i : i + f_boyut, j : j + f_boyut]
            
            # Matris düzeyinde çarpım ve toplam:
            # Filtre (kernel) ile penceredeki değerleri tek tek çarpıp topluyoruz
            toplam = 0
            for m in range(f_boyut):
                for n in range(f_boyut):
                    toplam += pencere[m, n] * kernel[m, n]
            
            # Bulduğumuz değeri yeni görüntünün ilgili hücresine yazıyoruz
            sonuc_img[i, j] = toplam

    # 7. Görselleştirme Hazırlığı
    # Değerleri 0-255 arasına sığdır ve tam sayıya çevir
    sonuc_img = np.uint8(np.clip(sonuc_img, 0, 255))
    gri_img_uint8 = np.uint8(gri_img)

    # Sonuçları göster
    cv2.imshow('Orijinal Gri', gri_img_uint8)
    cv2.imshow('Mean Filtre Sonucu (Python)', sonuc_img)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()