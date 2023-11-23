import customtkinter

from app import App


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("theme.json")
customtkinter.deactivate_automatic_dpi_awareness()

Width = 1024
Height = 600


app = App()
app.geometry("1536x1024")
app.mainloop()

# tip
# use dir() function to dump everything of object
