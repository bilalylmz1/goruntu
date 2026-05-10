import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import importlib
import sys, os
import numpy as np
from PIL import Image, ImageTk

def to_photoimage(img_array, max_size=400):
    """NumPy dizisini Tkinter PhotoImage'e çevirir."""
    if img_array.dtype != np.uint8:
        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
    if img_array.ndim == 2:
        pil_img = Image.fromarray(img_array, mode='L')
    else:
        pil_img = Image.fromarray(img_array[:, :, ::-1])  # BGR -> RGB
    w, h = pil_img.size
    if max(w, h) > max_size:
        scale = max_size / max(w, h)
        pil_img = pil_img.resize((int(w * scale), int(h * scale)), Image.NEAREST)
    return ImageTk.PhotoImage(pil_img)

# ── İşlem tanımları ──────────────────────────────────────────────────────────
# Her işlem: (modül_adı, [(etiket, varsayılan), ...])
ISLEMLER = {
    "1. Gri Dönüşüm":              ("gri",       []),
    "2. Binary Dönüşüm":           ("binary",    [("Eşik (0-255)", "128")]),
    "3. Görüntü Döndürme":         ("dondur",    [("Açı (-180/+180)", "45")]),
    "4. Görüntü Kırpma":           ("kirp",      [("x1", "0"), ("y1", "0"), ("x2", "200"), ("y2", "200")]),
    "5. Yakınlaştırma/Uzaklaştırma":("olcekle",  [("Ölçek (0.5-3.0)", "1.5")]),
    "6. Renk Uzayı Dönüşümü":      ("renk",      [("Mod (hsv/ycbcr)", "hsv")]),
    "7. Histogram Analizi & Germe":("histogram",  []),
    "8. Aritmetik İşlemler":       ("aritmetik", [("Mod (ekle/bol)", "ekle"), ("Alfa (0-1)", "0.5")]),
    "9. Kontrast Artırma":         ("kontrast",  [("Alfa", "1.5"), ("Beta", "0")]),
    "10. Konvolüsyon (Mean)":      ("konvol",    [("Çekirdek boyutu (3/5/7/9/11)", "3")]),
    "11. Tek Eşikleme":            ("esikle",    [("Eşik (0-255)", "128")]),
    "12. Kenar Bulma (Prewitt)":   ("kenar",     []),
    "13. Gürültü & Filtreleme":    ("gurultu",   [("Gürültü oranı (0-1)", "0.05")]),
    "14. Unsharp Maskeleme":       ("unsharp",   [("k katsayısı", "1.0")]),
    "15. Morfolojik İşlemler":     ("morfoloji", [("İşlem (d/a/ac/ka)", "d")]),
}

class Uygulama:
    def __init__(self, pencere):
        self.pencere = pencere
        pencere.title("Görüntü İşleme Görselleştirme")
        pencere.configure(bg="#2b2b2b")
        self.img = None          # cv2 BGR görüntü
        self.photo_ori = None    # Tkinter PhotoImage (referans tut)
        self.photo_son = None
        self.entry_widgets = []  # dinamik Entry kutuları

        self._arayuz_olustur()

    def _arayuz_olustur(self):
        p = self.pencere
        bg = "#2b2b2b"
        fg = "#ffffff"

        # ── Üst çubuk ────────────────────────────────────────────────────────
        ust = tk.Frame(p, bg=bg, pady=6)
        ust.pack(fill="x", padx=10)

        tk.Button(ust, text="📂 Resim Yükle", command=self.resim_yukle,
                  bg="#4a90d9", fg="white", relief="flat", padx=10, pady=4
                  ).pack(side="left", padx=4)

        self.secim = tk.StringVar(value=list(ISLEMLER.keys())[0])
        islem_menu = ttk.Combobox(ust, textvariable=self.secim,
                                   values=list(ISLEMLER.keys()), width=30, state="readonly")
        islem_menu.pack(side="left", padx=4)
        islem_menu.bind("<<ComboboxSelected>>", lambda e: self.parametre_guncelle())

        tk.Button(ust, text="▶ Uygula", command=self.uygula,
                  bg="#27ae60", fg="white", relief="flat", padx=10, pady=4
                  ).pack(side="left", padx=4)

        # ── Görüntü panelleri ─────────────────────────────────────────────────
        panel = tk.Frame(p, bg=bg)
        panel.pack(fill="both", expand=True, padx=10, pady=6)

        sol = tk.Frame(panel, bg="#1e1e1e", bd=1, relief="solid")
        sol.pack(side="left", fill="both", expand=True, padx=4)
        tk.Label(sol, text="Orijinal", bg="#1e1e1e", fg="#aaaaaa").pack()
        self.sol_label = tk.Label(sol, bg="#1e1e1e")
        self.sol_label.pack(expand=True)

        sag = tk.Frame(panel, bg="#1e1e1e", bd=1, relief="solid")
        sag.pack(side="left", fill="both", expand=True, padx=4)
        tk.Label(sag, text="Sonuç", bg="#1e1e1e", fg="#aaaaaa").pack()
        self.sag_label = tk.Label(sag, bg="#1e1e1e")
        self.sag_label.pack(expand=True)

        # ── Parametre alanı ───────────────────────────────────────────────────
        self.param_cerceve = tk.Frame(p, bg=bg, pady=6)
        self.param_cerceve.pack(fill="x", padx=10)

        self.parametre_guncelle()

    def parametre_guncelle(self, *_):
        """Seçilen işleme göre Entry kutularını yeniden oluştur."""
        for w in self.param_cerceve.winfo_children():
            w.destroy()
        self.entry_widgets.clear()

        islem_adi = self.secim.get()
        _, parametreler = ISLEMLER[islem_adi]

        for etiket, varsayilan in parametreler:
            satir = tk.Frame(self.param_cerceve, bg="#2b2b2b")
            satir.pack(side="left", padx=8)
            tk.Label(satir, text=etiket, bg="#2b2b2b", fg="#cccccc", font=("Helvetica", 9)
                     ).pack(anchor="w")
            e = tk.Entry(satir, width=12, bg="#3c3c3c", fg="white", insertbackground="white")
            e.insert(0, varsayilan)
            e.pack()
            self.entry_widgets.append((etiket, e))

    def resim_yukle(self):
        dosya = filedialog.askopenfilename(
            filetypes=[("Görüntü dosyaları", "*.jpg *.jpeg *.png *.bmp *.tiff")])
        if not dosya:
            return
        self.img = cv2.imread(dosya)
        if self.img is None:
            messagebox.showerror("Hata", "Görüntü yüklenemedi.")
            return
        self.photo_ori = to_photoimage(self.img)
        self.sol_label.configure(image=self.photo_ori)
        self.sag_label.configure(image="")

    def uygula(self):
        if self.img is None:
            messagebox.showwarning("Uyarı", "Önce bir resim yükleyin.")
            return

        islem_adi = self.secim.get()
        modul_adi, parametreler = ISLEMLER[islem_adi]

        # Parametreleri oku
        kwargs = {}
        try:
            param_adlari = [et for et, _ in parametreler]
            for (etiket, entry), (et, _) in zip(self.entry_widgets, parametreler):
                deger = entry.get().strip()
                # Parametre adını belirle
                anahtar = self._etiket_to_anahtar(modul_adi, et)
                kwargs[anahtar] = deger
        except Exception as ex:
            messagebox.showerror("Parametre Hatası", str(ex))
            return

        # Modülü yükle ve uygula
        try:
            modul = importlib.import_module(modul_adi)
            importlib.reload(modul)  # değişiklikler anında yansısın
            if kwargs:
                sonuc = modul.uygula(self.img, **self._tip_donustur(modul_adi, kwargs))
            else:
                sonuc = modul.uygula(self.img)
        except Exception as ex:
            messagebox.showerror("İşlem Hatası", str(ex))
            return

        self.photo_son = to_photoimage(sonuc)
        self.sag_label.configure(image=self.photo_son)

    def _etiket_to_anahtar(self, modul, etiket):
        """Etiket -> modül fonksiyon parametresi adı eşlemesi."""
        harita = {
            "binary":    {"Eşik (0-255)": "esik"},
            "dondur":    {"Açı (-180/+180)": "aci"},
            "kirp":      {"x1": "x1", "y1": "y1", "x2": "x2", "y2": "y2"},
            "olcekle":   {"Ölçek (0.5-3.0)": "olcek"},
            "renk":      {"Mod (hsv/ycbcr)": "mod"},
            "aritmetik": {"Mod (ekle/bol)": "mod", "Alfa (0-1)": "alfa"},
            "kontrast":  {"Alfa": "alfa", "Beta": "beta"},
            "konvol":    {"Çekirdek boyutu (3/5/7/9/11)": "boyut"},
            "esikle":    {"Eşik (0-255)": "esik"},
            "gurultu":   {"Gürültü oranı (0-1)": "oran"},
            "unsharp":   {"k katsayısı": "k"},
            "morfoloji": {"İşlem (d/a/ac/ka)": "islem"},
        }
        return harita.get(modul, {}).get(etiket, etiket)

    def _tip_donustur(self, modul, kwargs):
        """String değerleri uygun tipe çevir."""
        str_parametreler = {"mod", "islem"}
        sonuc = {}
        for k, v in kwargs.items():
            if k in str_parametreler:
                sonuc[k] = v
            else:
                try:
                    sonuc[k] = float(v) if '.' in v else int(v)
                except ValueError:
                    sonuc[k] = v
        return sonuc


if __name__ == "__main__":
    pencere = tk.Tk()
    pencere.geometry("900x620")
    app = Uygulama(pencere)
    pencere.mainloop()
