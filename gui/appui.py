import customtkinter as ctk
BUTTON = "Solve"
NAME = "Sudoku Master"
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.geometry("400x500")
        self.title("Sudoku Master")
        container = ctk.CTkFrame(self, width=250, height=200, corner_radius=10)
        container.grid(row=0,rowspan=2, column=1, padx=10, pady=10,sticky="ns")
        self.logbox = ctk.CTkTextbox(container, width=190, height=400)
        self.logbox.insert("end", f"[{NAME}]: Welcome to {NAME}! The bot can solve Sudoku puzzles directly in the open application.\n")
        self.logbox.configure(state="disabled")
        self.logbox.grid(row=0, column=0, padx=5, pady=10,)
        title = ctk.CTkLabel(self, text="Sudoku Master", font=ctk.CTkFont(size=20, weight="bold"))
        title.grid(row=0, column=0, padx=10, pady=10,sticky="n")
        self.button = ctk.CTkButton(self, command=self.button_click)
        self.button.configure(text=BUTTON)
        self.button.grid(row=1, column=0, padx=10, pady=10,sticky="n")
    def logbox_insert(self, text):
        self.logbox.configure(state="normal")
        self.logbox.insert("end", text)
        self.logbox.see("end")
        self.logbox.configure(state="disabled")
    def button_click(self):
        self.button.configure(state="disabled",text="Solving...")
        self.logbox_insert(f"[{NAME}]: Trying to solve...\n")
        self.after(2000, self.reset)
    def reset(self):
        self.logbox_insert(f"[{NAME}]: Bot is waiting for next one\n")
        self.button.configure(state="normal",text=BUTTON)