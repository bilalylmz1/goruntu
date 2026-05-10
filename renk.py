import numpy as np

def uygula(img, mod='hsv'):
    """
    Renk uzayi donusumu (piksel piksel dongu).
    mod='hsv'   -> H, S, V kanallari yan yana
    mod='ycbcr' -> Y, Cb, Cr kanallari yan yana
    """
    satir, sutun = img.shape[:2]

    # Her kanal icin ayri matris
    kanal1_img = np.zeros((satir, sutun), dtype=np.uint8)
    kanal2_img = np.zeros((satir, sutun), dtype=np.uint8)
    kanal3_img = np.zeros((satir, sutun), dtype=np.uint8)

    for i in range(satir):
        for j in range(sutun):
            # OpenCV BGR sirasi: indeks 0=B, 1=G, 2=R
            b = img[i, j, 0] / 255.0
            g = img[i, j, 1] / 255.0
            r = img[i, j, 2] / 255.0

            if mod == 'hsv':
                # --- HSV Donusumu ---
                maks_kanal = r
                if g > maks_kanal:
                    maks_kanal = g
                if b > maks_kanal:
                    maks_kanal = b

                min_kanal = r
                if g < min_kanal:
                    min_kanal = g
                if b < min_kanal:
                    min_kanal = b

                delta = maks_kanal - min_kanal

                # Value (Parlaklik)
                V = maks_kanal

                # Saturation (Doygunluk)
                if maks_kanal != 0:
                    S = delta / maks_kanal
                else:
                    S = 0.0

                # Hue (Ton)
                if delta == 0:
                    H = 0.0
                elif maks_kanal == r:
                    H = (60.0 * ((g - b) / delta)) % 360
                elif maks_kanal == g:
                    H = 60.0 * ((b - r) / delta + 2)
                else:
                    H = 60.0 * ((r - g) / delta + 4)

                kanal1_img[i, j] = int(H * 255.0 / 360.0)
                kanal2_img[i, j] = int(S * 255.0)
                kanal3_img[i, j] = int(V * 255.0)

            else:  # ycbcr
                # --- YCbCr Donusumu ---
                # ITU-R BT.601 normalize formulleri (0-1 araliginda)
                Y  =  0.299   * r + 0.587   * g + 0.114   * b
                Cb = -0.168736 * r - 0.331264 * g + 0.5     * b + 0.5
                Cr =  0.5     * r - 0.418688 * g - 0.081312 * b + 0.5

                # 0-1 araligina sikistir
                if Y < 0:
                    Y = 0.0
                elif Y > 1:
                    Y = 1.0
                if Cb < 0:
                    Cb = 0.0
                elif Cb > 1:
                    Cb = 1.0
                if Cr < 0:
                    Cr = 0.0
                elif Cr > 1:
                    Cr = 1.0

                kanal1_img[i, j] = int(Y  * 255)
                kanal2_img[i, j] = int(Cb * 255)
                kanal3_img[i, j] = int(Cr * 255)

    # --- Kanallari etiketleriyle sozluk olarak dondur ---
    if mod == 'hsv':
        return {'H': kanal1_img, 'S': kanal2_img, 'V': kanal3_img}
    else:
        return {'Y': kanal1_img, 'Cb': kanal2_img, 'Cr': kanal3_img}
