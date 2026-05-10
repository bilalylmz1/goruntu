import numpy as np

def uygula(img, boyut=3):
    """NxN ortalama filtre konvolusyonu (mean filter, sifirdan, donguyle).
    Renkli goruntu girdisi: her kanal (B, G, R) ayri ayri filtrelenir."""
    boyut = int(boyut)
    if boyut % 2 == 0:
        boyut += 1          # Filtre boyutu tek olmali

    satir, sutun, kanal_sayisi = img.shape
    f_boyut = boyut
    pay = f_boyut // 2

    sonuc_img = np.zeros((satir, sutun, kanal_sayisi), dtype=np.uint8)

    # Her renk kanali icin ayri ayri konvolusyon uygula
    for k in range(kanal_sayisi):

        # --- Adim 1: Padding (kenar doldurma) ---
        # Goruntunun etrafini sifirla sararak filtre kenardan tasmasi engellenir
        paddli_img = np.zeros((satir + 2 * pay, sutun + 2 * pay), dtype=np.float64)
        for i in range(satir):
            for j in range(sutun):
                paddli_img[i + pay, j + pay] = img[i, j, k]

        # --- Adim 2: Konvolusyon (piksel piksel, pencere ortalamasi) ---
        for i in range(satir):
            for j in range(sutun):
                toplam = 0.0
                for ki in range(f_boyut):
                    for kj in range(f_boyut):
                        toplam += paddli_img[i + ki, j + kj]
                deger = toplam / (f_boyut * f_boyut)
                if deger > 255:
                    deger = 255
                elif deger < 0:
                    deger = 0
                sonuc_img[i, j, k] = int(deger)

    return sonuc_img
