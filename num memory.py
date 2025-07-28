import tkinter as tk
import random

class NumberMemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Memory Game")
        self.root.geometry("400x300")
        self.root.configure(bg="#222")

        self.level = 1
        self.number = ""

        # Label for instructions and feedback
        self.label = tk.Label(
            root,
            text="Click Start to begin",
            font=("Arial", 18),
            fg="white",
            bg="#222"
        )
        self.label.pack(pady=40)

        #Place to input number
        self.entry = tk.Entry(
            root,
            font=("Arial", 18),
            justify="center"
        )
        self.entry.place(x=100, y=130, width=200)
        self.entry.place_forget()

        #"Start" button
        self.button = tk.Button(
            root,
            text="Start",
            font=("Arial", 14, "bold"),
            command=self.start_game,
            bg="#388E3C",
            fg="#483C32",
            activebackground="#2E7D32",
            activeforeground="white",
            relief="raised",
            bd=3
        )
        self.button.place(x=150, y=220, width=100, height=40)

        # Bind Return key to input submission
        self.root.bind("<Return>", self.check_input)

    def start_game(self):
        self.label.config(text=f"Level {self.level}")
        self.button.config(state="disabled", text="Playing...")
        self.entry.place_forget()
        self.root.after(1000, self.show_number)

    def show_number(self):
        if self.level == 1:
            self.number = random.choice('0123456789')
        else:
            self.number += random.choice('0123456789')

        self.label.config(text=self.number)
        self.root.after(200 + self.level * 200, self.hide_number)

    def hide_number(self):
        self.label.config(text="Enter the number:")
        self.entry.delete(0, tk.END)
        self.entry.place(x=100, y=130, width=200)
        self.entry.focus_set()

    def check_input(self, event=None):
        guess = self.entry.get()
        if guess == self.number:
            self.level += 1
            self.label.config(text="Correct!")
            self.entry.place_forget()
            self.root.after(1000, self.start_game)
        else:
            self.label.config(
                text=f"Wrong! It was {self.number}\nYou reached level {self.level}"
            )
            self.entry.place_forget()
            self.button.config(text="Restart", state="normal")
            self.level = 1
            self.number = ""

if __name__ == "__main__":
    root = tk.Tk()
    game = NumberMemoryGame(root)
    root.mainloop()
