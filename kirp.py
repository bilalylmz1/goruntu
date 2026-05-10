import numpy as np

def uygula(img, x1=0, y1=0, x2=100, y2=100):
    """Görüntüyü (x1,y1)-(x2,y2) koordinatlarına göre kırpar."""
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    h, w = img.shape[:2]
    x1 = max(0, min(x1, w - 1))
    x2 = max(x1 + 1, min(x2, w))
    y1 = max(0, min(y1, h - 1))
    y2 = max(y1 + 1, min(y2, h))
    return img[y1:y2, x1:x2]
