import os
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
from rembg import remove, new_session
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AIDatasetPro(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Dataset Master Pro")
        self.geometry("1400x900")

        # Variabili
        self.input_folder = ""
        self.image_list = []
        self.current_idx = 0
        self.processing = False
        self.sessions = {} # Carichiamo i modelli solo al bisogno per risparmiare RAM

        self.setup_ui()

    def setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=320, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(self.sidebar, text="AI DATASET PRO", font=("Impact", 28)).pack(pady=20)
        
        ctk.CTkButton(self.sidebar, text="📁 CARICA DATASET", command=self.load_folder, height=40).pack(padx=20, pady=10, fill="x")
        self.lbl_info = ctk.CTkLabel(self.sidebar, text="Immagini: 0")
        self.lbl_info.pack()

        # TABVIEW PER SETTAGGI
        self.tabs = ctk.CTkTabview(self.sidebar, width=280)
        self.tabs.pack(padx=10, pady=10, expand=True, fill="both")
        self.tab_base = self.tabs.add("Base")
        self.tab_adv = self.tabs.add("Avanzate")

        # --- TAB BASE ---
        ctk.CTkLabel(self.tab_base, text="Modello Consigliato:").pack(anchor="w")
        self.model_var = ctk.StringVar(value="u2net")
        models = [("Generale (u2net)", "u2net"), ("Anime/Art (isnet)", "isnet-anime"), ("Portrait Pro (birefnet)", "birefnet-portrait")]
        for text, val in models:
            ctk.CTkRadioButton(self.tab_base, text=text, variable=self.model_var, value=val, command=self.update_preview).pack(anchor="w", pady=2)

        ctk.CTkLabel(self.tab_base, text="\nErode (Bordi):").pack(anchor="w")
        self.sld_erode = self.add_slider(self.tab_base, 0, 40, 10)
        
        self.crop_switch = ctk.CTkSwitch(self.tab_base, text="Ritaglio Portrait", command=self.update_preview)
        self.crop_switch.pack(pady=10)
        self.sld_crop = self.add_slider(self.tab_base, 10, 100, 100)

        # --- TAB AVANZATE ---
        self.post_process = ctk.CTkSwitch(self.tab_adv, text="Post-Process Mask", command=self.update_preview)
        self.post_process.pack(pady=10)
        
        self.only_mask = ctk.CTkSwitch(self.tab_adv, text="Solo Maschera (B/N)", command=self.update_preview)
        self.only_mask.pack(pady=10)

        ctk.CTkLabel(self.tab_adv, text="Background Thresh:").pack(anchor="w")
        self.sld_bg = self.add_slider(self.tab_adv, 0, 255, 15)

        # PROGRESS & RUN
        self.btn_run = ctk.CTkButton(self.sidebar, text="🚀 AVVIA BATCH", fg_color="#d35400", command=self.start_thread)
        self.btn_run.pack(padx=20, pady=10, fill="x")
        self.progress = ctk.CTkProgressBar(self.sidebar)
        self.progress.pack(padx=20, pady=10); self.progress.set(0)

        # --- PREVIEW AREA ---
        self.prev_frame = ctk.CTkFrame(self, fg_color="#0a0a0a", corner_radius=15)
        self.prev_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.canvas_label = ctk.CTkLabel(self.prev_frame, text="")
        self.canvas_label.pack(expand=True, fill="both")

        # Navigazione
        self.nav = ctk.CTkFrame(self.preview_frame if hasattr(self, 'preview_frame') else self.prev_frame, fg_color="transparent")
        self.nav.pack(fill="x", pady=10)
        ctk.CTkButton(self.nav, text="❮", width=60, command=self.prev_img).pack(side="left", padx=20)
        self.lbl_page = ctk.CTkLabel(self.nav, text="0 / 0"); self.lbl_page.pack(side="left", expand=True)
        ctk.CTkButton(self.nav, text="❯", width=60, command=self.next_img).pack(side="right", padx=20)

    def add_slider(self, parent, f, t, d):
        s = ctk.CTkSlider(parent, from_=f, to=t, command=self.update_preview)
        s.set(d); s.pack(fill="x", pady=5); return s

    def get_session(self, model_name):
        if model_name not in self.sessions:
            self.sessions[model_name] = new_session(model_name)
        return self.sessions[model_name]

    def process_image(self, img):
        res = remove(
            img, 
            session=self.get_session(self.model_var.get()),
            alpha_matting=True,
            alpha_matting_background_threshold=int(self.sld_bg.get()),
            alpha_matting_erode_size=int(self.sld_erode.get()),
            post_process_mask=self.post_process.get(),
            only_mask=self.only_mask.get()
        )
        box = res.getbbox()
        if box: res = res.crop(box)
        if self.crop_switch.get():
            w, h = res.size
            res = res.crop((0, 0, w, int(h * (self.sld_crop.get() / 100.0))))
        return res

    def load_folder(self):
        f = filedialog.askdirectory()
        if f:
            self.input_folder = f
            self.image_list = [x for x in os.listdir(f) if x.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
            self.lbl_info.configure(text=f"Immagini: {len(self.image_list)}")
            self.current_idx = 0; self.update_preview()

    def update_preview(self, e=None):
        # Se non ci sono immagini o stiamo elaborando, non fare nulla
        if not self.image_list or self.processing: 
            return
            
        self.lbl_page.configure(text=f"{self.current_idx + 1} / {len(self.image_list)}")
        
        # Costruiamo il percorso del file
        img_path = os.path.join(self.input_folder, self.image_list[self.current_idx])
        
        # Verifichiamo che il file esista davvero per evitare errori rossi nel terminale
        if not os.path.exists(img_path):
            print(f"File non trovato: {img_path}")
            return

        try:
            # Apriamo l'immagine
            raw = Image.open(img_path).convert("RGB")
            proc = self.process_image(raw)
            
            # Calcoliamo le dimensioni della preview
            w, h = proc.size
            ratio = min(900/w, 750/h)
            new_w, new_h = int(w*ratio), int(h*ratio)
            
            # USIAMO CTKIMAGE (Questo toglie l'errore giallo nel terminale)
            self.ctk_img = ctk.CTkImage(light_image=proc, dark_image=proc, size=(new_w, new_h))
            self.canvas_label.configure(image=self.ctk_img)
        except Exception as err:
            print(f"Errore durante la preview: {err}")

    def prev_img(self): self.current_idx = max(0, self.current_idx-1); self.update_preview()
    def next_img(self): self.current_idx = min(len(self.image_list)-1, self.current_idx+1); self.update_preview()
    def start_thread(self): threading.Thread(target=self.run_batch, daemon=True).start()

    def run_batch(self):
        self.processing = True; self.btn_run.configure(state="disabled")
        out = os.path.join(self.input_folder, "Alpha_Dataset_Output")
        os.makedirs(out, exist_ok=True)
        for i, n in enumerate(self.image_list):
            img = Image.open(os.path.join(self.input_folder, n)).convert("RGB")
            self.process_image(img).save(os.path.join(out, os.path.splitext(n)[0] + ".png"))
            self.progress.set((i+1)/len(self.image_list))
        self.processing = False; self.btn_run.configure(state="normal")

if __name__ == "__main__":
    AIDatasetPro().mainloop()