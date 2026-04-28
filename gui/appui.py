import customtkinter
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x250")
        self.title("Sudoku Master")
        self.button = customtkinter.CTkButton(self, command=self.button_click)
        self.button.configure(text="Solve")
        self.button.grid(row=0, column=0, padx=20, pady=10,)
    def button_click(self):
        print("button click")