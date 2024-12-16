import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# List of words for the game
word_list = ["python", "hangman", "padlock", "unlock", "secure", "cipher", "algorithm"]

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game - Padlock Edition")
        self.root.geometry("400x400")
        
        # Game variables
        self.word_to_guess = random.choice(word_list).lower()
        self.guessed_letters = []
        self.incorrect_guesses = 0
        self.max_attempts = 6  # The number of wrong guesses before game over
        
        # GUI Components
        self.create_widgets()

    def create_widgets(self):
        # Word display (with blanks for unguessed letters)
        self.word_label = tk.Label(self.root, text=self.get_display_word(), font=("Arial", 24))
        self.word_label.pack(pady=20)

        # Padlock image (representing the state of the lock)
        self.padlock_label = tk.Label(self.root)
        self.padlock_label.pack()

        self.update_padlock_image()

        # Input field for guesses
        self.guess_entry = tk.Entry(self.root, font=("Arial", 14))
        self.guess_entry.pack(pady=10)
        self.guess_entry.focus()

        # Button to submit the guess
        self.submit_button = tk.Button(self.root, text="Submit Guess", command=self.submit_guess, font=("Arial", 14))
        self.submit_button.pack(pady=5)

        # Remaining attempts display
        self.attempts_label = tk.Label(self.root, text=f"Remaining attempts: {self.max_attempts - self.incorrect_guesses}", font=("Arial", 14))
        self.attempts_label.pack(pady=10)

    def get_display_word(self):
        """Return the word with blanks for unguessed letters."""
        return " ".join([letter if letter in self.guessed_letters else "_" for letter in self.word_to_guess])

    def submit_guess(self):
        guess = self.guess_entry.get().lower()

        if len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Invalid input", "Please enter a single letter.")
            return

        if guess in self.guessed_letters:
            messagebox.showinfo("Already guessed", "You already guessed that letter!")
            return

        self.guessed_letters.append(guess)

        if guess not in self.word_to_guess:
            self.incorrect_guesses += 1

        self.update_game()

    def update_game(self):
        """Update the game state after a guess."""
        # Update word display
        self.word_label.config(text=self.get_display_word())

        # Update remaining attempts
        self.attempts_label.config(text=f"Remaining attempts: {self.max_attempts - self.incorrect_guesses}")

        # Update the padlock image based on incorrect guesses
        self.update_padlock_image()

        # Check if the game is over or won
        if self.incorrect_guesses >= self.max_attempts:
            messagebox.showinfo("Game Over", "You have lost! The word was: " + self.word_to_guess)
            self.reset_game()
        elif all(letter in self.guessed_letters for letter in self.word_to_guess):
            messagebox.showinfo("You Win!", "Congratulations! You've guessed the word!")
            self.reset_game()

    def update_padlock_image(self):
        """Update the padlock image based on the number of incorrect guesses."""
        # Load the padlock image that corresponds to the number of incorrect guesses
        image_path = f"padlock_{self.incorrect_guesses}.png"  # Assumes images named padlock_0.png, padlock_1.png, etc.
        
        try:
            img = Image.open(image_path)
            img = img.resize((100, 100))  # Resize to fit the GUI
            img = ImageTk.PhotoImage(img)
            self.padlock_label.config(image=img)
            self.padlock_label.image = img
        except FileNotFoundError:
            pass  # If image file not found, just skip to the next one

    def reset_game(self):
        """Reset the game to a new word."""
        self.word_to_guess = random.choice(word_list).lower()
        self.guessed_letters = []
        self.incorrect_guesses = 0
        self.word_label.config(text=self.get_display_word())
        self.attempts_label.config(text=f"Remaining attempts: {self.max_attempts}")
        self.update_padlock_image()


# Create the main window
root = tk.Tk()

# Create an instance of the HangmanGame
game = HangmanGame(root)

# Run the application
root.mainloop()
