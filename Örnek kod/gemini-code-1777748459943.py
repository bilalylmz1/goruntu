import cv2
import numpy as np

# 1. Görüntüyü oku (Temel metod)
img = cv2.imread('deneme.jpg')
if img is None:
    print("Görüntü bulunamadı!")
else:
    satir, sutun, kanal = img.shape

    # 2. Manuel Gri Seviye Dönüşümü
    # Renkli görüntüyü 0.299*R + 0.587*G + 0.114*B formülüyle griye çeviriyoruz.
    gri_img = np.zeros((satir, sutun), dtype=np.float64)
    for i in range(satir):
        for j in range(sutun):
            b, g, r = img[i, j]
            gri_img[i, j] = 0.299 * r + 0.587 * g + 0.114 * b

    # --- ADIM 1: Görüntüyü Bulanıklaştırma (Mean Filter) ---
    f_boyut = 3
    pay = f_boyut // 2
    # Kenarlarda taşma olmaması için padding yapıyoruz
    paddli_img = np.zeros((satir + 2 * pay, sutun + 2 * pay))
    paddli_img[pay:satir + pay, pay:sutun + pay] = gri_img

    bulanik_img = np.zeros((satir, sutun), dtype=np.float64)

    # Konvolüsyon döngüsü: Her pikselin 3x3 çevresinin ortalamasını al
    for i in range(satir):
        for j in range(sutun):
            toplam = 0
            for m in range(f_boyut):
                for n in range(f_boyut):
                    toplam += paddli_img[i + m, j + n]
            bulanik_img[i, j] = toplam / (f_boyut * f_boyut)

    # --- ADIM 2: Maske Oluşturma (Detayları Yakalama) ---
    # Orijinal görüntüden bulanık halini çıkarınca sadece kenarlar (yüksek frekans) kalır.
    maske = gri_img - bulanik_img

    # --- ADIM 3: Keskinleştirme (Orijinal + k * Maske) ---
    # k = 1 ise standart unsharp, k > 1 ise high-boost filtering olur.
    k = 1.0
    keskin_img = gri_img + (k * maske)

    # --- ADIM 4: Sınır Kontrolü (Clipping) ---
    # Matris işlemleri sonucu 255'i aşan veya 0'ın altına düşen değerleri düzeltiyoruz.
    # Bunu manuel bir döngüyle de yapabiliriz ama np.clip matris düzeyinde bir kısıttır.
    for i in range(satir):
        for j in range(sutun):
            if keskin_img[i, j] > 255:
                keskin_img[i, j] = 255
            elif keskin_img[i, j] < 0:
                keskin_img[i, j] = 0

    # Görselleştirme için veri tiplerini uint8 (8-bit tam sayı) yapıyoruz
    gri_sonuc = np.uint8(gri_img)
    bulanik_sonuc = np.uint8(bulanik_img)
    keskin_sonuc = np.uint8(keskin_img)

    # Maskeyi görebilmek için negatif değerlerden kurtulup normalize ediyoruz
    maske_gorsel = np.uint8(np.abs(maske))

    # Sonuçları pencerelerde göster
    cv2.imshow('1. Orijinal Gri', gri_sonuc)
    cv2.imshow('2. Bulanik (Maske Icin)', bulanik_sonuc)
    cv2.imshow('3. Detay Maskesi (Kenarlar)', maske_gorsel)
    cv2.imshow('4. Keskinlestirilmis Goruntu', keskin_sonuc)

    cv2.waitKey(0)
    cv2.destroyAllWindows()