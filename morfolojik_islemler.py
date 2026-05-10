import numpy as np
from gri import uygula as to_gray

def _binary(gri_img):
    """Gri goruntuyu sabit esikle (128) binary goruntüye donustur"""
    satir, sutun = gri_img.shape
    binary_img = np.zeros((satir, sutun), dtype=np.uint8)
    esik_degeri = 128
    for i in range(satir):
        for j in range(sutun):
            if gri_img[i, j] >= esik_degeri:
                binary_img[i, j] = 255
            else:
                binary_img[i, j] = 0
    return binary_img

def _genisle(binary_img):
    """Genisleme (dilation): 3x3 komsulukta en az bir 255 varsa merkezi 255 yap"""
    satir, sutun = binary_img.shape
    sonuc_img = np.zeros((satir, sutun), dtype=np.uint8)
    for i in range(1, satir - 1):
        for j in range(1, sutun - 1):
            # 3x3 penceredeki herhangi bir piksel 255 ise genislet
            bulundu = False
            for ki in range(-1, 2):
                for kj in range(-1, 2):
                    if binary_img[i + ki, j + kj] == 255:
                        bulundu = True
            if bulundu:
                sonuc_img[i, j] = 255
    return sonuc_img

def _asindır(binary_img):
    """Asindirma (erosion): 3x3 komsulukta tumu 255 ise merkezi 255 yap"""
    satir, sutun = binary_img.shape
    sonuc_img = np.zeros((satir, sutun), dtype=np.uint8)
    for i in range(1, satir - 1):
        for j in range(1, sutun - 1):
            # 3x3 penceredeki tum pikseller 255 ise asindirma sonucu 255 kalir
            hepsi_255 = True
            for ki in range(-1, 2):
                for kj in range(-1, 2):
                    if binary_img[i + ki, j + kj] != 255:
                        hepsi_255 = False
            if hepsi_255:
                sonuc_img[i, j] = 255
    return sonuc_img

def uygula(img, islem='d'):
    """
    Morfolojik islemler (3x3 yapisal eleman, binary uzerinde):
    islem='d'  -> Genisleme (dilation)
    islem='a'  -> Asindirma (erosion)
    islem='ac' -> Acma (opening)  = once asindirma, sonra genisleme
    islem='ka' -> Kapama (closing) = once genisleme, sonra asindirma
    """
    gri_img = to_gray(img)
    binary_img = _binary(gri_img)

    if islem == 'd':
        return _genisle(binary_img)
    elif islem == 'a':
        return _asindır(binary_img)
    elif islem == 'ac':
        # Acma: asindirma -> genisleme
        return _genisle(_asindır(binary_img))
    else:  # 'ka'
        # Kapama: genisleme -> asindirma
        return _asindır(_genisle(binary_img))
