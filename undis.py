import os
import customtkinter as ctk
from undis.app import App


ctk.deactivate_automatic_dpi_awareness()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme(os.path.join(os.path.dirname(__file__), "assets", "theme.json"))

app = App()
app.geometry("800x600")
app.mainloop()

# tip
# use dir() function to dump everything of object
