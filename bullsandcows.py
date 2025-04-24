import customtkinter as ctk
import random
import time
import threading

# Configurare temă
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# -----------------------------
# Jocul Bulls and Cows
# -----------------------------

def generate_number():
    number = f"{random.randint(0, 9999):04}"
    print(f"Număr generat: {number}")
    return number


def calculate_bulls_and_cows(secret, guess):
    bulls = sum(s == g for s, g in zip(secret, guess))
    cows = sum(min(secret.count(d), guess.count(d)) for d in set(guess)) - bulls
    return bulls, cows

# -----------------------------
# Fereastra de dificultate
# -----------------------------

class DifficultyWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Bulls and Cows")
        self.geometry("400x300")
        self.resizable(True, True)

        self.create_widgets()

    def create_widgets(self):
        title_label = ctk.CTkLabel(self, text="Alege dificultatea", font=("Helvetica", 26, "bold"))
        title_label.pack(pady=20)

        difficulty_frame = ctk.CTkFrame(self)
        difficulty_frame.pack(pady=10)

        ctk.CTkButton(difficulty_frame, text="Easy", command=lambda: self.start_game(None), width=120, fg_color="green").pack(pady=5)
        ctk.CTkButton(difficulty_frame, text="Medium", command=lambda: self.start_game(10), width=120, fg_color="orange").pack(pady=5)
        ctk.CTkButton(difficulty_frame, text="Hard", command=lambda: self.start_game(5), width=120, fg_color="red").pack(pady=5)

    def start_game(self, attempts_limit):
        self.destroy()
        app = BullsAndCowsApp(attempts_limit)
        app.mainloop()

# -----------------------------
# Fereastra jocului
# -----------------------------

class BullsAndCowsApp(ctk.CTk):
    def __init__(self, attempts_limit):
        super().__init__()
        self.title("🐂 Bulls and Cows")
        self.geometry("550x650")
        self.resizable(True, True)

        self.secret = generate_number()
        self.max_attempts = attempts_limit
        self.attempts = 0
        self.game_over = False

        self.create_widgets()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="🐂 Bulls and Cows", font=("Helvetica", 26, "bold"))
        self.title_label.pack(pady=20)

        self.input_entry = ctk.CTkEntry(self, font=("Helvetica", 22), width=200, placeholder_text="Introdu numar")
        self.input_entry.pack(pady=15)
        self.input_entry.focus()

        self.check_button = ctk.CTkButton(self, text="Verifică", command=self.check_guess)
        self.check_button.pack(pady=5)

        self.output_box = ctk.CTkTextbox(self, width=500, height=300, font=("Courier", 16))
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
        self.output_box.insert("end", f"{guess} → {'🐂-bulls' * bulls}{'🐄-cows' * cows}\n")
        self.output_box.configure(state="disabled")

        if bulls == 4:
            self.game_over = True
            self.show_message("🎉 Ai ghicit! Bravo!")
        elif self.max_attempts and self.attempts >= self.max_attempts:
            self.game_over = True
            self.show_message(f"💀 Ai pierdut! Numărul era {self.secret}")
        else:
            remaining = self.max_attempts - self.attempts if self.max_attempts else "∞"
            self.show_message(f"🔁 Încercare {self.attempts}. Rămase: {remaining}")

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
        DifficultyWindow().mainloop()

# -----------------------------
# Pornirea aplicației
# -----------------------------

if __name__ == "__main__":
    DifficultyWindow().mainloop()
