import customtkinter as ctk
import random
import time
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Jocul Bulls and Cows

def generate_number():
    number = f"{random.randint(0, 9999):04}"
    print(number)
    return number


def calculate_bulls_and_cows(secret, guess):
    bulls = sum(s == g for s, g in zip(secret, guess))
    cows = sum(min(secret.count(d), guess.count(d)) for d in set(guess)) - bulls
    return bulls, cows

# Prima pagina

class primapagina(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🐂 Bulls and Cows")
        self.geometry("600x400")
        self.resizable(True, True)

        self.create_widgets()

    def create_widgets(self):
        title_label = ctk.CTkLabel(self, text="Bulls and Cows", font=("Ravie", 26, "bold"))
        title_label.pack(pady=15)
        rules_label = ctk.CTkLabel(
            self, 
            text="Reguli: Ghicește numărul secret format din 4 cifre.\n"
             "🐂 - Bulls: cifre corecte pe poziția corectă.\n"
             "🐄 - Cows: cifre corecte pe poziția greșită.\n"
             "❌ - None: cifre care nu sunt in numar"
             "Jocul are trei nivele de dificultate:\n"
             "Easy - ai incercari infinite de ghicit\n"
             "Medium - ai 10 incercari de ghicit\n"
             "Hard - ai 5 incercari de ghicit", 
            font=("Comic Sans MS", 14), 
            justify="center"
        )
        rules_label.pack(pady=20)
        difficulty_frame = ctk.CTkFrame(self)
        difficulty_frame.pack(pady=10)

        ctk.CTkButton(difficulty_frame, text="Easy", command=lambda: self.start_game(None), width=150, height=100, fg_color="green").grid(row=0, column=0, padx=10)
        ctk.CTkButton(difficulty_frame, text="Medium", command=lambda: self.start_game(10), width=150, height=100, fg_color="orange").grid(row=0, column=1, padx=10)
        ctk.CTkButton(difficulty_frame, text="Hard", command=lambda: self.start_game(5), width=150, height=100, fg_color="red").grid(row=0, column=2, padx=10)

    def start_game(self, attempts_limit):
        self.destroy()
        app = BullsAndCows(attempts_limit)
        app.mainloop()

# Fereastra jocului dupa ce alegi nivelul

class BullsAndCows(ctk.CTk):
    def __init__(self, attempts_limit):
        super().__init__()
        self.title("🐂 Bulls and Cows")
        self.geometry("550x550")
        self.resizable(True, True)

        self.secret = generate_number()
        self.max_attempts = attempts_limit
        self.attempts = 0
        self.game_over = False

        self.create_widgets()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="🐂 Bulls and Cows", font=("Ravie", 26))
        self.title_label.pack(pady=20)

        self.input_entry = ctk.CTkEntry(self, font=("Comic Sans MS", 22), width=200, placeholder_text="Introdu numar")
        self.input_entry.pack(pady=15)
        self.input_entry.focus()

        self.check_button = ctk.CTkButton(
            self, 
            text="Verifică", 
            command=self.check_guess, 
            font=("Comic Sans MS", 18),
            fg_color="gray", 
            text_color="white"
        )
        self.check_button.pack(pady=5)

        self.output_box = ctk.CTkTextbox(self, width=500, height=300, font=("Comic Sans MS", 16))
        self.output_box.pack(pady=10)
        self.output_box.configure(state="normal")
        self.output_box.insert("end", f"🎮 Joc început! Număr secret generat.\n")
        if self.max_attempts:
            self.output_box.insert("end", f"🧠 Ai {self.max_attempts} încercări.\n")
        else:
            self.output_box.insert("end", f"♾️ Încercări nelimitate (Easy Mode).\n")
        self.output_box.configure(state="disabled")

        self.reset_button = ctk.CTkButton(self, text="🔄 Joc Nou", command=self.reset_game)
        self.reset_button.pack(pady=10)

    def check_guess(self):
        if self.game_over:
            return

        guess = self.input_entry.get().strip()
        self.input_entry.delete(0, "end")

        if len(guess) != 4 or not guess.isdigit():
            self.show_message("⚠️ Introdu un număr de 4 cifre (ex: 0423)!")
            return

        self.attempts += 1
        bulls, cows = calculate_bulls_and_cows(self.secret, guess)

        self.output_box.configure(state="normal")
        if bulls == 0 and cows == 0:
            self.output_box.insert("end", f"{guess} → ❌\n")
        else:
            self.output_box.insert("end", f"{guess} → {'🐂' * bulls} {'🐄' * cows}\n")
        self.output_box.configure(state="disabled")
       

        if bulls == 4:
            self.game_over = True
            self.show_message("🎉 Ai ghicit! Bravo!")
        elif self.max_attempts and self.attempts >= self.max_attempts:
            self.game_over = True
            self.show_message(f"💀 Ai pierdut! Numărul era {self.secret}")
        else:
            remaining = self.max_attempts - self.attempts if self.max_attempts else "∞"
            self.show_message(f" Încercari rămase: {remaining}")

    def show_message(self, msg):
        self.animate_title(msg)

    def animate_title(self, text):
        def animation():
            self.title_label.configure(text="")
            for char in text:
                current = self.title_label.cget("text")
                self.title_label.configure(text=current + char)
                time.sleep(0.05)

        threading.Thread(target=animation).start()

    def reset_game(self):
        self.destroy()
        primapagina().mainloop()

# Pornirea aplicației

if __name__ == "__main__":
    primapagina().mainloop()
