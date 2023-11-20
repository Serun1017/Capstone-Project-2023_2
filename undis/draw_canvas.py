import customtkinter


class DrawCanvas(customtkinter.CTkCanvas):
    def __init__(self, master, w, h):
        super().__init__(master=master, width=w, height=h, bg="white")

    def get_x_and_y(self, event):
        global lasx, lasy
        lasx, lasy = event.x, event.y

    def draw_some(self, event):
        global lasx, lasy
        self.create_line((lasx, lasy, event.x, event.y), fill="black", width=2)
        lasx, lasy = event.x, event.y
