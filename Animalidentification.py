import os
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# ==========================================
# GAME SETUP & DATA
# ==========================================
# Replace these image paths with actual image files in your folder!
# Options list format: [Image_Path, Correct_Answer, Option1, Option2, Option3, Option4]
QUESTIONS_DATA = [
    {
        "image": "lion.jpg",
        "answer": "Lion",
        "options": ["Tiger", "Lion", "Leopard", "Cheetah"],
    },
    {
        "image": "elephant.jpg",
        "answer": "Elephant",
        "options": ["Rhino", "Hippo", "Elephant", "Giraffe"],
    },
    {
        "image": "penguin.jpg",
        "answer": "Penguin",
        "options": ["Puffin", "Penguin", "Seagull", "Ostrich"],
    },
]


class AnimalQuizGame:

    def __init__(self, root):
        self.root = root
        self.root.title("Animal Identification Game")
        self.root.geometry("450x600")
        self.root.configure(bg="#f0f4f8")

        # Game State Variables
        self.score = 0
        self.current_question = 0
        self.questions = QUESTIONS_DATA.copy()
        random.shuffle(self.questions)  # Shuffle questions each time

        # Setup GUI Widgets
        self.create_widgets()
        self.load_question()

    def create_widgets(self):
        # 1. Score & Progress Display
        self.score_label = tk.Label(
            self.root,
            text=f"Score: {self.score}",
            font=("Helvetica", 14, "bold"),
            bg="#f0f4f8",
            fg="#333333",
        )
        self.score_label.pack(pady=10)

        # 2. Image Display Canvas/Label
        self.image_label = tk.Label(self.root, bg="#f0f4f8")
        self.image_label.pack(pady=10)

        # 3. Question Prompt
        self.prompt_label = tk.Label(
            self.root,
            text="Which animal is this?",
            font=("Helvetica", 12),
            bg="#f0f4f8",
        )
        self.prompt_label.pack(pady=5)

        # 4. Buttons Frame
        self.buttons_frame = tk.Frame(self.root, bg="#f0f4f8")
        self.buttons_frame.pack(pady=20)

        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(
                self.buttons_frame,
                text="",
                font=("Helvetica", 11, "bold"),
                width=18,
                height=2,
                bg="#4a90e2",
                fg="white",
                activebackground="#357abd",
                activeforeground="white",
                command=lambda idx=i: self.check_answer(idx),
            )
            # Grid layout for 2x2 button grid
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=10)
            self.option_buttons.append(btn)

    def load_question(self):
        # Check if game is over
        if self.current_question >= len(self.questions):
            self.end_game()
            return

        q_data = self.questions[self.current_question]

        # Load and resize image safely
        try:
            img_path = q_data["image"]
            if os.path.exists(img_path):
                raw_img = Image.open(img_path)
                raw_img = raw_img.resize((250, 200), Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(raw_img)
                self.image_label.config(image=self.photo, text="")
            else:
                self.image_label.config(
                    text=f"[ Missing Image:\n{img_path} ]",
                    font=("Helvetica", 12, "italic"),
                    image="",
                )
        except Exception as e:
            self.image_label.config(text="Error loading image", image="")

        # Update button text options
        options = q_data["options"]
        for i in range(4):
            self.option_buttons[i].config(text=options[i], state=tk.NORMAL)

    def check_answer(self, button_idx):
        q_data = self.questions[self.current_question]
        selected_option = q_data["options"][button_idx]

        # Scoring Logic
        if selected_option == q_data["answer"]:
            self.score += 10
            messagebox.showinfo("Correct!", "🎉 Great job! That's correct.")
        else:
            messagebox.showerror(
                "Wrong!", f"❌ Oops! That was a {q_data['answer']}."
            )

        # Update Scoreboard & Move to Next Question
        self.score_label.config(text=f"Score: {self.score}")
        self.current_question += 1
        self.load_question()

    def end_game(self):
        messagebox.showinfo(
            "Game Over!",
            f"🏆 Final Score: {self.score} / {len(self.questions) * 10}",
        )
        self.root.quit()


# ==========================================
# MAIN APPLICATION LOOP
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    game = AnimalQuizGame(root)
    root.mainloop()