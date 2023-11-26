import customtkinter as ctk
from undis.app import App


ctk.deactivate_automatic_dpi_awareness()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("assets/theme.json")

app = App()
app.geometry("800x600")
app.mainloop()

print(__file__)

# tip
# use dir() function to dump everything of object
