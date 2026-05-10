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
    "3. Görüntü Döndürme":         ("dondur",    [("Açı (90/180/270)", "90")]),
    "4. Görüntü Kırpma":           ("kirp",      [("x1", "0"), ("y1", "0"), ("x2", "200"), ("y2", "200")]),
    "5. Yakınlaştırma/Uzaklaştırma":("Goruntu_yakinlastir_uzaklastir",  [("Ölçek (0.5-3.0)", "1.5")]),
    "6. Renk Uzayı Dönüşümü":      ("renk",      [("Mod (hsv/ycbcr)", "hsv")]),
    "7. Histogram Analizi & Germe":("histogram",  []),
    "8. Aritmetik İşlemler":       ("aritmetik", [("Mod (ekle/bol)", "ekle")]),
    "9. Kontrast Artırma":         ("kontrast",  [("Alfa", "1.5"), ("Beta", "0")]),
    "10. Konvolüsyon (Mean)":      ("konvol",    [("Çekirdek boyutu (3/5/7/9/11)", "3")]),
    "11. Tek Eşikleme":            ("esikle",    [("Eşik (0-255)", "128")]),
    "12. Kenar Bulma (Prewitt)":   ("kenar",     []),
    "13. Gürültü & Filtreleme":    ("gurultu",   [("Gürültü oranı (0-1)", "0.05")]),
    "14. Unsharp Maskeleme":       ("unsharp",   [("k katsayısı", "1.0")]),
    "15. Morfolojik İşlemler":     ("morfolojik_islemler", [("İşlem (d/a/ac/ka)", "d"), ("Eşik (0-255)", "128")]),
}

class Uygulama:
    def __init__(self, pencere):
        self.pencere = pencere
        pencere.title("Görüntü İşleme Görselleştirme")
        pencere.configure(bg="#2b2b2b")
        self.img        = None   # cv2 BGR görüntü (1. resim)
        self.img2       = None   # cv2 BGR görüntü (2. resim — yalnızca aritmetik)
        self.photo_ori  = None
        self.photo_ori2 = None
        self.photo_son  = None
        self.entry_widgets = []

        self._arayuz_olustur()

    def _arayuz_olustur(self):
        p   = self.pencere
        bg  = "#2b2b2b"
        fg  = "#ffffff"

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
        self.panel = tk.Frame(p, bg=bg)
        self.panel.pack(fill="both", expand=True, padx=10, pady=6)

        # 1. resim paneli
        sol = tk.Frame(self.panel, bg="#1e1e1e", bd=1, relief="solid")
        sol.pack(side="left", fill="both", expand=True, padx=4)
        tk.Label(sol, text="Orijinal", bg="#1e1e1e", fg="#aaaaaa").pack()
        self.sol_label = tk.Label(sol, bg="#1e1e1e")
        self.sol_label.pack(expand=True)

        # 2. resim paneli (yalnızca aritmetik modunda görünür)
        self.ikinci_panel = tk.Frame(self.panel, bg="#1e1e1e", bd=1, relief="solid")
        tk.Label(self.ikinci_panel, text="2. Resim", bg="#1e1e1e", fg="#aaaaaa").pack()
        self.ikinci_label = tk.Label(self.ikinci_panel, bg="#1e1e1e")
        self.ikinci_label.pack(expand=True)

        # Sonuç paneli
        sag = tk.Frame(self.panel, bg="#1e1e1e", bd=1, relief="solid")
        sag.pack(side="left", fill="both", expand=True, padx=4)
        tk.Label(sag, text="Sonuç", bg="#1e1e1e", fg="#aaaaaa").pack()
        self.sag_label = tk.Label(sag, bg="#1e1e1e")
        self.sag_label.pack(expand=True)

        # ── Parametre alanı ───────────────────────────────────────────────────
        self.param_cerceve = tk.Frame(p, bg=bg, pady=6)
        self.param_cerceve.pack(fill="x", padx=10)

        self.parametre_guncelle()

    def parametre_guncelle(self, *_):
        """Seçilen işleme göre Entry kutularını ve ikinci resim alanını yeniden oluştur."""
        for w in self.param_cerceve.winfo_children():
            w.destroy()
        self.entry_widgets.clear()

        islem_adi = self.secim.get()
        modul_adi, parametreler = ISLEMLER[islem_adi]

        # Aritmetik seçiliyse: ikinci resim panelini ve yükleme butonunu göster
        if modul_adi == "aritmetik":
            self.ikinci_panel.pack(side="left", fill="both", expand=True, padx=4,
                                   before=self.panel.winfo_children()[-1])
            tk.Button(self.param_cerceve, text="📂 2. Resim Yükle",
                      command=self.resim_yukle2,
                      bg="#c0392b", fg="white", relief="flat", padx=10, pady=4
                      ).pack(side="left", padx=8)
        else:
            self.ikinci_panel.pack_forget()
            self.img2 = None

        for etiket, varsayilan in parametreler:
            satir_frame = tk.Frame(self.param_cerceve, bg="#2b2b2b")
            satir_frame.pack(side="left", padx=8)
            tk.Label(satir_frame, text=etiket, bg="#2b2b2b", fg="#cccccc", font=("Helvetica", 9)
                     ).pack(anchor="w")
            e = tk.Entry(satir_frame, width=12, bg="#3c3c3c", fg="white", insertbackground="white")
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

    def resim_yukle2(self):
        """Yalnızca aritmetik işlem için ikinci resmi yükler."""
        dosya = filedialog.askopenfilename(
            filetypes=[("Görüntü dosyaları", "*.jpg *.jpeg *.png *.bmp *.tiff")])
        if not dosya:
            return
        self.img2 = cv2.imread(dosya)
        if self.img2 is None:
            messagebox.showerror("Hata", "İkinci görüntü yüklenemedi.")
            return
        self.photo_ori2 = to_photoimage(self.img2)
        self.ikinci_label.configure(image=self.photo_ori2)

    def uygula(self):
        if self.img is None:
            messagebox.showwarning("Uyarı", "Önce bir resim yükleyin.")
            return

        islem_adi = self.secim.get()
        modul_adi, parametreler = ISLEMLER[islem_adi]

        # Parametreleri oku
        kwargs = {}
        try:
            for (etiket, entry), (et, _) in zip(self.entry_widgets, parametreler):
                deger  = entry.get().strip()
                anahtar = self._etiket_to_anahtar(modul_adi, et)
                kwargs[anahtar] = deger
        except Exception as ex:
            messagebox.showerror("Parametre Hatası", str(ex))
            return

        # Modülü yükle ve uygula
        try:
            modul = importlib.import_module(modul_adi)
            importlib.reload(modul)

            if modul_adi == "aritmetik":
                # Aritmetik: iki resim gerekli
                if self.img2 is None:
                    messagebox.showwarning("Uyarı", "Aritmetik işlem için 2. resmi yükleyin.")
                    return
                sonuc = modul.uygula(self.img, self.img2, **self._tip_donustur(modul_adi, kwargs))
            elif kwargs:
                sonuc = modul.uygula(self.img, **self._tip_donustur(modul_adi, kwargs))
            else:
                sonuc = modul.uygula(self.img)
        except Exception as ex:
            messagebox.showerror("İşlem Hatası", str(ex))
            return

        if modul_adi == "Goruntu_yakinlastir_uzaklastir":
            self._yakinlastirma_penceresi_goster(sonuc)
        else:
            self.photo_son = to_photoimage(sonuc)
            self.sag_label.configure(image=self.photo_son)

    def _etiket_to_anahtar(self, modul, etiket):
        """Etiket -> modül fonksiyon parametresi adı eşlemesi."""
        harita = {
            "binary":    {"Eşik (0-255)": "esik"},
            "dondur":    {"Açı (90/180/270)": "aci"},
            "kirp":      {"x1": "x1", "y1": "y1", "x2": "x2", "y2": "y2"},
            "Goruntu_yakinlastir_uzaklastir": {"Ölçek (0.5-3.0)": "olcek"},
            "renk":      {"Mod (hsv/ycbcr)": "mod"},
            "aritmetik": {"Mod (ekle/bol)": "mod"},
            "kontrast":  {"Alfa": "alfa", "Beta": "beta"},
            "konvol":    {"Çekirdek boyutu (3/5/7/9/11)": "boyut"},
            "esikle":    {"Eşik (0-255)": "esik"},
            "gurultu":   {"Gürültü oranı (0-1)": "oran"},
            "unsharp":   {"k katsayısı": "k"},
            "morfolojik_islemler": {"İşlem (d/a/ac/ka)": "islem", "Eşik (0-255)": "esik"},
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

    def _yakinlastirma_penceresi_goster(self, sonuc):
        """Yakınlaştırma/uzaklaştırma sonucunu gerçek boyutunda ayrı pencerede gösterir."""
        pencere = tk.Toplevel(self.pencere)
        pencere.configure(bg="#1e1e1e")

        ori_h, ori_w = self.img.shape[:2]
        son_h, son_w = sonuc.shape[:2]
        olcek_x = son_w / ori_w
        olcek_y = son_h / ori_h

        pencere.title(f"Yakınlaştırma Sonucu  |  {ori_w}×{ori_h}  →  {son_w}×{son_h}  (×{olcek_x:.2f})")

        # Ekran boyutunu al, pencereyi sığdır
        ekran_gen = self.pencere.winfo_screenwidth()
        ekran_yuk = self.pencere.winfo_screenheight()
        kenar_bosluk = 80  # başlık çubuğu + bilgi alanı için

        # Her panel için maksimum gösterim alanı (ekranın yarısına sığdır)
        max_panel_gen = (ekran_gen - 60) // 2
        max_panel_yuk = ekran_yuk - kenar_bosluk - 100

        def panel_boyutla(img_array):
            """Görüntüyü panel sınırlarına sığacak şekilde PIL'e çevirir."""
            if img_array.dtype != np.uint8:
                img_array = np.clip(img_array, 0, 255).astype(np.uint8)
            if img_array.ndim == 2:
                pil = Image.fromarray(img_array, mode='L')
            else:
                pil = Image.fromarray(img_array[:, :, ::-1])
            w, h = pil.size
            oran = min(max_panel_gen / w, max_panel_yuk / h, 1.0)  # büyütme yok
            if oran < 1.0:
                pil = pil.resize((int(w * oran), int(h * oran)), Image.NEAREST)
            return ImageTk.PhotoImage(pil), pil.size

        photo_ori, (go_w, go_h) = panel_boyutla(self.img)
        photo_son, (gs_w, gs_h) = panel_boyutla(sonuc)

        # Pencere boyutu: iki panel yan yana + boşluklar
        pen_gen = go_w + gs_w + 60
        pen_yuk = max(go_h, gs_h) + kenar_bosluk
        # Ekrana sığdır
        pen_gen = min(pen_gen, ekran_gen - 40)
        pen_yuk = min(pen_yuk, ekran_yuk - 60)

        # Ekranın ortasına konumlandır
        x = (ekran_gen - pen_gen) // 2
        y = (ekran_yuk - pen_yuk) // 2
        pencere.geometry(f"{pen_gen}x{pen_yuk}+{x}+{y}")

        # İçerik çerçevesi
        cerceve = tk.Frame(pencere, bg="#1e1e1e")
        cerceve.pack(fill="both", expand=True, padx=10, pady=10)

        # Orijinal panel
        sol = tk.Frame(cerceve, bg="#2b2b2b", bd=1, relief="solid")
        sol.pack(side="left", fill="both", expand=True, padx=(0, 5))
        tk.Label(sol, text=f"Orijinal  {ori_w}×{ori_h}",
                 bg="#2b2b2b", fg="#aaaaaa", font=("Helvetica", 10, "bold")).pack(pady=(6, 2))
        lbl_ori = tk.Label(sol, image=photo_ori, bg="#2b2b2b")
        lbl_ori.image = photo_ori  # referans tut
        lbl_ori.pack(padx=6, pady=(0, 6))

        # Sonuç paneli
        sag = tk.Frame(cerceve, bg="#2b2b2b", bd=1, relief="solid")
        sag.pack(side="left", fill="both", expand=True, padx=(5, 0))
        tk.Label(sag, text=f"Sonuç  {son_w}×{son_h}  (ölçek ×{olcek_x:.2f})",
                 bg="#2b2b2b", fg="#27ae60", font=("Helvetica", 10, "bold")).pack(pady=(6, 2))
        lbl_son = tk.Label(sag, image=photo_son, bg="#2b2b2b")
        lbl_son.image = photo_son  # referans tut
        lbl_son.pack(padx=6, pady=(0, 6))

        # Ana panelde de küçük önizleme göster
        self.photo_son = to_photoimage(sonuc)
        self.sag_label.configure(image=self.photo_son)


if __name__ == "__main__":
    pencere = tk.Tk()
    pencere.geometry("900x620")
    app = Uygulama(pencere)
    pencere.mainloop()
