import numpy as np

def uygula(img):
    """Agirlikli ortalama ile gri donusum: 0.299*R + 0.587*G + 0.114*B"""
    satir, sutun = img.shape[:2]
    gri_img = np.zeros((satir, sutun), dtype=np.uint8)
    for i in range(satir):
        for j in range(sutun):
            b = img[i, j, 0]
            g = img[i, j, 1]
            r = img[i, j, 2]
            gri_img[i, j] = int(0.299 * r + 0.587 * g + 0.114 * b)
    return gri_img
