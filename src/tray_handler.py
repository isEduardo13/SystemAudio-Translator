import pystray
from PIL import Image

class TrayIcon:
    def __init__(self, overlay, stop_callback):
        self.overlay = overlay
        self.stop_callback = stop_callback
        self.icon = None
        
    def _switch_state(self):
        if self.overlay.root.state() == 'normal':
            self.overlay.root.withdraw() 
           
        else:
            self.overlay.root.deiconify() 
            self.overlay.root.attributes("-topmost", True)
        self.update_menu()   
    def create_menu(self):
        items = []
        if self.overlay.root.state() == 'normal':
            items.append(pystray.MenuItem("Ocultar", self.toggle_overlay, default=True))
        else:
            items.append(pystray.MenuItem("Mostrar", self.toggle_overlay, default=True))
            items.append(pystray.MenuItem("Salir", self.on_quit))
        return pystray.Menu(*items)
    def update_menu(self):
        if self.icon:
            self.icon.menu = self.create_menu()

    def toggle_overlay(self, icon, item):
      
       self.overlay.root.after(0, self._switch_state)

    def on_quit(self, icon, item):
        self.icon.stop()
        self.stop_callback()

    def run(self):
        
        image = Image.open("../assets/icon.png")
        self.icon = pystray.Icon("SystemAudioTranslator", image, "System Audio Translator", self.create_menu())
        self.icon.run()