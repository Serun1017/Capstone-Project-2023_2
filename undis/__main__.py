import customtkinter


customtkinter.set_appearance_mode("system")


def test_callback():
    print("what")


class ResultFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)

        self.button = customtkinter.CTkButton(self, text="test", command=test_callback)
        self.button.pack()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("undis")

        self.frame = ResultFrame(self)
        self.frame.pack()


app = App()
app.title("undis")
app.geometry("400x300")

app.mainloop()
