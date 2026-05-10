import numpy as np

def uygula(img):
    """Ağırlıklı ortalama ile gri dönüşüm: 0.299R + 0.587G + 0.114B"""
    b = img[:, :, 0].astype(np.float64)
    g = img[:, :, 1].astype(np.float64)
    r = img[:, :, 2].astype(np.float64)
    return (0.299 * r + 0.587 * g + 0.114 * b).astype(np.uint8)
