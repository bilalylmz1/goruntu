import numpy as np

def uygula(img):
    """RGB kanal bazli histogram analizi. Her kanal icin ayri piksel dagilimini gosterir."""
    import matplotlib.pyplot as plt

    satir, sutun = img.shape[:2]

    # --- Her kanal icin ayri sayac (OpenCV BGR sirasi: 0=B, 1=G, 2=R) ---
    hist_b = [0] * 256
    hist_g = [0] * 256
    hist_r = [0] * 256

    for i in range(satir):
        for j in range(sutun):
            hist_b[img[i, j, 0]] += 1
            hist_g[img[i, j, 1]] += 1
            hist_r[img[i, j, 2]] += 1

    # --- Grafik: uc kanal tek eksende, renkleriyle ---
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(range(256), hist_r, color='red',   alpha=0.8, label='Kirmizi (R)')
    ax.plot(range(256), hist_g, color='green', alpha=0.8, label='Yesil (G)')
    ax.plot(range(256), hist_b, color='blue',  alpha=0.8, label='Mavi (B)')
    ax.set_title('RGB Kanal Histogramlari')
    ax.set_xlabel('Piksel Degeri (0-255)')
    ax.set_ylabel('Piksel Sayisi')
    ax.legend()
    plt.tight_layout()
    plt.show()

    return img
