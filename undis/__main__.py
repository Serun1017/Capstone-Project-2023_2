import customtkinter

from app import App


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("theme.json")
customtkinter.deactivate_automatic_dpi_awareness()

Width = 1024
Height = 600


def test_callback():
    print("what")


def get_x_and_y(event):
    global lasx, lasy
    lasx, lasy = event.x, event.y
    pass


def make_button(self):
    self.playbutton = customtkinter.CTkButton(self, text="play", command=test_callback)
    self.playbutton.place(x=50)
    self.playbutton.pack(side="left", anchor="nw")

    pass


app = App()
app.geometry("1536x1024")
app.mainloop()

# tip
# use dir() function to dump everything of object
