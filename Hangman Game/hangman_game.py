import random
import tkinter as tk
from tkinter import messagebox
import time

# List of words
words_list = ['python', 'hangman', 'challenge', 'developer', 'programming']

# Function to choose a random word
def choose_word():
    return random.choice(words_list)

# Function to update the displayed word with guessed letters
def update_displayed_word():
    displayed_word.set(' '.join([letter.upper() if letter in correct_guesses else '_' for letter in word]))

# Function to handle button click (guessing a letter)
def guess_letter(letter):
    if letter in correct_guesses or letter in incorrect_guesses:
        messagebox.showinfo("Hangman", "You've already guessed that letter.")
        return

    if letter in word:
        correct_guesses.append(letter)
        update_displayed_word()
        if all(l in correct_guesses for l in word):
            show_celebration_animation()  # Trigger celebration on win
    else:
        incorrect_guesses.append(letter)
        incorrect_guesses_label.config(text="Incorrect guesses: " + ', '.join([l.upper() for l in incorrect_guesses]))
        attempts_left.set(attempts_left.get() - 1)
        draw_hangman(len(incorrect_guesses))  # Draw the hangman based on incorrect guesses
        if attempts_left.get() == 0:
            messagebox.showinfo("Hangman", f"Game Over! The word was: {word.upper()}")
            reset_game()

# Function to reset the game
def reset_game():
    global word, correct_guesses, incorrect_guesses
    word = choose_word()
    correct_guesses = []
    incorrect_guesses = []
    update_displayed_word()
    incorrect_guesses_label.config(text="Incorrect guesses: ")
    attempts_left.set(max_attempts)
    canvas.delete("all")  # Clear the hangman figure

# Celebration Animation
def show_celebration_animation():
    # Disable the buttons during animation
    for button in buttons_frame.winfo_children():
        button.config(state="disabled")

    celebration_window = tk.Toplevel(root)
    celebration_window.geometry("400x400")
    celebration_window.title("Congratulations!")
    celebration_window.config(bg='#2c2f33')

    # Center the celebration window
    center_window(celebration_window, 400, 400)

    canvas_confetti = tk.Canvas(celebration_window, width=400, height=400, bg='#2c2f33')
    canvas_confetti.pack()

    # Create the congratulations message
    canvas_confetti.create_text(200, 100, text="Congratulations!", font=("Helvetica", 24, "bold"), fill="#43b581")

    # Create confetti particles
    confetti = []
    colors = ["#f94144", "#f3722c", "#f8961e", "#f9c74f", "#90be6d", "#43aa8b", "#577590"]
    for _ in range(50):
        x = random.randint(0, 400)
        y = random.randint(0, 400)
        size = random.randint(5, 15)
        color = random.choice(colors)
        confetti.append(canvas_confetti.create_oval(x, y, x + size, y + size, fill=color, outline=color))

    # Animate the confetti falling down
    for _ in range(100):  # Repeat animation for 100 frames
        for particle in confetti:
            canvas_confetti.move(particle, random.randint(-3, 3), random.randint(2, 5))
        celebration_window.update()
        time.sleep(0.03)

    # End the game and reset after the celebration
    celebration_window.after(1000, lambda: [celebration_window.destroy(), reset_game()])
    # Re-enable the buttons
    for button in buttons_frame.winfo_children():
        button.config(state="normal")

# Function to center the window
def center_window(window, width, height):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')

# Function to draw the hangman figure step by step
def draw_hangman(stage):
    if stage == 1:
        canvas.create_line(50, 250, 150, 250, fill="#ffffff")  # Base
    elif stage == 2:
        canvas.create_line(100, 250, 100, 50, fill="#ffffff")  # Pole
    elif stage == 3:
        canvas.create_line(100, 50, 200, 50, fill="#ffffff")   # Top bar
    elif stage == 4:
        canvas.create_line(200, 50, 200, 80, fill="#ffffff")   # Rope
    elif stage == 5:
        canvas.create_oval(180, 80, 220, 120, outline="#ffffff")  # Head
    elif stage == 6:
        canvas.create_line(200, 120, 200, 180, fill="#ffffff")  # Body
    elif stage == 7:
        canvas.create_line(200, 130, 180, 160, fill="#ffffff")  # Left arm
    elif stage == 8:
        canvas.create_line(200, 130, 220, 160, fill="#ffffff")  # Right arm
    elif stage == 9:
        canvas.create_line(200, 180, 180, 220, fill="#ffffff")  # Left leg
    elif stage == 10:
        canvas.create_line(200, 180, 220, 220, fill="#ffffff")  # Right leg

# Initialize the main window
root = tk.Tk()
root.title("Hangman Game")

# Set the dimensions of the main window and center it
window_width = 900
window_height = 600
center_window(root, window_width, window_height)
root.config(bg='#2c2f33')  # Dark background

# Variables
correct_guesses = []
incorrect_guesses = []
max_attempts = 10  # Updated to match the number of hangman parts
attempts_left = tk.IntVar(value=max_attempts)
displayed_word = tk.StringVar()

# Choose a random word to start
word = choose_word()

# GUI Layout
top_frame = tk.Frame(root, bg='#2c2f33')
top_frame.pack(pady=20)

# Word display and attempts left labels
word_label = tk.Label(top_frame, textvariable=displayed_word, font=('Helvetica', 28, 'bold'), fg="#ffffff", bg='#2c2f33')
word_label.pack(pady=10)

attempts_label = tk.Label(top_frame, text="Attempts left:", font=('Helvetica', 18), fg="#ffffff", bg='#2c2f33')
attempts_label.pack()

attempts_left_label = tk.Label(top_frame, textvariable=attempts_left, font=('Helvetica', 18, 'bold'), fg="#f94144", bg='#2c2f33')
attempts_left_label.pack()

incorrect_guesses_label = tk.Label(top_frame, text="Incorrect guesses: ", font=('Helvetica', 16), fg="#ffffff", bg='#2c2f33')
incorrect_guesses_label.pack(pady=10)

# Canvas for drawing the hangman
canvas_frame = tk.Frame(root, bg='#2c2f33')
canvas_frame.pack(side=tk.LEFT, padx=40, pady=20)
canvas = tk.Canvas(canvas_frame, width=300, height=300, bg='#2c2f33', highlightthickness=0)
canvas.pack()

# Alphabet buttons for guessing letters
buttons_frame = tk.Frame(root, bg='#2c2f33')
buttons_frame.pack(side=tk.RIGHT, padx=20, pady=20)

# Create buttons for each letter
for index, letter in enumerate('abcdefghijklmnopqrstuvwxyz'):
    btn = tk.Button(buttons_frame, text=letter.upper(), width=4, height=2,
                   command=lambda l=letter: guess_letter(l),
                   bg='#23272a', fg='#ffffff', activebackground='#7289da', activeforeground='#ffffff',
                   font=('Helvetica', 12, 'bold'), bd=0, highlightthickness=0, cursor="hand2")
    row = index // 9
    col = index % 9
    btn.grid(row=row, column=col, padx=5, pady=5)

# Reset button to start a new game (with larger size and padding for visual width)
reset_button = tk.Button(root, text="Reset Game", command=reset_game, font=('Helvetica', 16, 'bold'),
                         bg='#7289da', fg='#ffffff', activebackground='#99aab5', activeforeground='#ffffff',
                         height=2, width=20, bd=0, cursor="hand2")
reset_button.pack(pady=20, padx=10, side=tk.BOTTOM, fill=tk.X)

# Initial word display
update_displayed_word()

# Run the main application loop
root.mainloop()
