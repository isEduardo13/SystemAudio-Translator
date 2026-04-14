import customtkinter as ctk

class TranslationOverlay:
    def run(self):
        self.root.mainloop()
    def _start_drag(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def _do_drag(self, event):
        x = self.root.winfo_x() + (event.x - self._drag_x)
        y = self.root.winfo_y() + (event.y - self._drag_y)
        self.root.geometry(f"+{x}+{y}")
    def __init__(self):
        self.root = ctk.CTk()
        
        # Configuración de ventana transparente y sin bordes
        self.root.title("SystemAudio-Translator Overlay")
        self.root.overrideredirect(True)  # Quita la barra de título y bordes
        self.root.attributes("-topmost", True)  # Siempre encima
        self.root.attributes("-alpha", 0.8)     # Transparencia (0.0 a 1.0)
        self.root.config(bg='black')
        self.root.wm_attributes("-transparentcolor", "black") # Hace el fondo negro invisible
        
        # Posicionamiento (Parte inferior de la pantalla)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width, height = 800, 150
        x = (screen_width // 2) - (width // 2)
        y = screen_height - 200
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # Etiqueta de texto (Donde aparecerán las instrucciones)
        self.label = ctk.CTkLabel(
            self.root, 
            text="Esperando audio...", 
            font=("Consolas", 24, "bold"),
            text_color="white",
            wraplength=750
        )
        self.label.pack(expand=True, fill="both", padx=20, pady=20)

        # Vincular eventos de arrastre
        self.label.bind("<Button-1>", self._start_drag)
        self.label.bind("<B1-Motion>", self._do_drag)

    def update_text(self, new_text):
        if new_text.strip():
            self.root.after(0, lambda: self.label.configure(text=new_text))