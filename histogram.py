import numpy as np
import matplotlib.pyplot as plt
from gri import uygula as to_gray

def uygula(img):
    """Histogram analizi ve germe. Matplotlib ile grafik açar, geri germe sonucu döner."""
    gray = to_gray(img).astype(np.float64)
    # Histogram hesapla (sıfırdan)
    hist = np.zeros(256, dtype=np.int64)
    for val in gray.flatten():
        hist[int(val)] += 1

    # Histogram germe
    mn, mx = gray.min(), gray.max()
    if mx == mn:
        geri = gray.astype(np.uint8)
    else:
        geri = ((gray - mn) / (mx - mn) * 255).astype(np.uint8)

    hist_geri = np.zeros(256, dtype=np.int64)
    for val in geri.flatten():
        hist_geri[int(val)] += 1

    # Grafik göster
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    ax1.bar(range(256), hist, width=1, color='steelblue')
    ax1.set_title('Orijinal Histogram')
    ax2.bar(range(256), hist_geri, width=1, color='tomato')
    ax2.set_title('Gerilmiş Histogram')
    plt.tight_layout()
    plt.show()

    return geri
