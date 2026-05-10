import numpy as np

def uygula(img, mod='hsv'):
    """
    Renk uzayı dönüşümü (piksel piksel döngü).
    mod='hsv'   -> H, S, V kanalları yan yana
    mod='ycbcr' -> Y, Cb, Cr kanalları yan yana
    """
    h_img, w_img = img.shape[:2]
    kanal1 = np.zeros((h_img, w_img), dtype=np.uint8)
    kanal2 = np.zeros((h_img, w_img), dtype=np.uint8)
    kanal3 = np.zeros((h_img, w_img), dtype=np.uint8)

    for i in range(h_img):
        for j in range(w_img):
            b = img[i, j, 0] / 255.0
            g = img[i, j, 1] / 255.0
            r = img[i, j, 2] / 255.0

            if mod == 'hsv':
                maxc = max(r, g, b)
                minc = min(r, g, b)
                delta = maxc - minc
                V = maxc
                S = (delta / maxc) if maxc != 0 else 0.0
                if delta == 0:
                    H = 0.0
                elif maxc == r:
                    H = (60 * ((g - b) / delta)) % 360
                elif maxc == g:
                    H = 60 * ((b - r) / delta + 2)
                else:
                    H = 60 * ((r - g) / delta + 4)
                kanal1[i, j] = int(H * 255 / 360)
                kanal2[i, j] = int(S * 255)
                kanal3[i, j] = int(V * 255)
            else:  # ycbcr
                Y  =  0.299   * r + 0.587   * g + 0.114   * b
                Cb = -0.168736 * r - 0.331264 * g + 0.5     * b + 0.5
                Cr =  0.5     * r - 0.418688 * g - 0.081312 * b + 0.5
                kanal1[i, j] = int(max(0, min(1, Y))  * 255)
                kanal2[i, j] = int(max(0, min(1, Cb)) * 255)
                kanal3[i, j] = int(max(0, min(1, Cr)) * 255)

    # Yan yana: kanal1 | kanal2 | kanal3
    sonuc = np.zeros((h_img, w_img * 3), dtype=np.uint8)
    for i in range(h_img):
        for j in range(w_img):
            sonuc[i, j]           = kanal1[i, j]
            sonuc[i, j + w_img]   = kanal2[i, j]
            sonuc[i, j + 2*w_img] = kanal3[i, j]
    return sonuc
