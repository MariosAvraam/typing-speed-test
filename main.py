import tkinter as tk
from tkinter import Text, Label, Button
import time
import requests

# Constants
RUN_TIME = 10 * 1000
SAMPLE_TEXT_WORDS = 50
FONT = ("Arial", 12, "bold")
MILLISECONDS_IN_SECOND = 1000

class TypingTestApp:
    def __init__(self, root):
        """Initializes the Typing Test App."""
        self.root = root
        self.start_time = None
        self.TIMER_DURATION = RUN_TIME / MILLISECONDS_IN_SECOND
        self.remaining_time = self.TIMER_DURATION
        self.timer_id = None
        self.update_timer_id = None

        self.setup_gui()


    def setup_gui(self):
        """Sets up the GUI elements."""
        self.sample_label = Label(self.root, text="This is a sample text for the user to type.", wraplength=400, padx=10, pady=10, font=FONT)
        self.sample_label.pack(pady=20)

        self.user_input = Text(self.root, wrap="word", height=5, width=50, padx=10, pady=10, state=tk.DISABLED)
        self.user_input.pack(pady=20)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.start_button = Button(self.button_frame, text="Start", command=self.start_typing_test)
        self.start_button.grid(row=0, column=0, padx=10)

        self.change_text_button = Button(self.button_frame, text="Change Text", command=self.change_sample_text)
        self.change_text_button.grid(row=0, column=1, padx=10)

        self.stop_button = Button(self.button_frame, text="Stop", command=self.stop_typing_test, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=2, padx=10)

        self.timer_label = Label(self.root, text=f"Time Left: {self.TIMER_DURATION} seconds", padx=10, pady=10)
        self.timer_label.pack(pady=10)

        self.wpm_label = Label(self.root, text="Your WPM will be displayed here.", padx=10, pady=10)
        self.wpm_label.pack(pady=20)

    def start_typing_test(self):
        """Begins the typing test."""

        self.start_button.config(state=tk.DISABLED)
        self.change_text_button.config(state=tk.DISABLED)

        self.remaining_time = self.TIMER_DURATION
        self.timer_label.config(text=f"Time Left: {self.TIMER_DURATION} seconds")
        self.update_timer()

        # Button configurations
        self.stop_button.config(state=tk.NORMAL)
        self.user_input.config(state=tk.NORMAL)
        self.user_input.delete(1.0, tk.END)
        self.user_input.focus_set()
        self.start_time = time.time()
        self.timer_id = self.root.after(RUN_TIME, self.stop_typing_test)

    def stop_typing_test(self):
        # Enable the start and change text buttons
        self.start_button.config(state=tk.NORMAL)
        self.change_text_button.config(state=tk.NORMAL)

        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        if self.update_timer_id:  # Cancel the recurring timer updates
            self.root.after_cancel(self.update_timer_id)
        self.remaining_time = 0

        # Button configurations
        self.stop_button.config(state=tk.DISABLED)
        self.user_input.config(state=tk.DISABLED)

        if self.start_time:
            self.calculate_wpm_and_accuracy()

        # Reset the start_time
        self.start_time = None


    def calculate_wpm_and_accuracy(self):
        elapsed_time = time.time() - self.start_time
        typed_text = self.user_input.get(1.0, tk.END).strip()
        user_words = typed_text.split()
        sample_words_up_to_typed_length = self.sample_label['text'].split()[:len(user_words)]

        correct_words_count = sum(w1 == w2 for w1, w2 in zip(user_words, sample_words_up_to_typed_length))
        accuracy = (correct_words_count / len(user_words)) * 100 if user_words else 0
        wpm = (len(user_words) / elapsed_time) * 60

        self.wpm_label.config(text=f"Words Per Minute: {round(wpm, 2)} | Accuracy: {round(accuracy, 2)}%")

        # After calculating, enable the start and change text buttons
        self.start_button.config(state=tk.NORMAL)
        self.change_text_button.config(state=tk.NORMAL)

    def get_random_words(self, count=50):
        """Fetches random words for the typing test."""
        url = f"https://random-word-api.herokuapp.com/word?number={count}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return [f"Error: {e}. Please try again."]

    def change_sample_text(self):
        words = self.get_random_words()
        chosen_text = ' '.join(words)
        self.sample_label.config(text=chosen_text)

    def update_timer(self):
        self.remaining_time -= 1
        self.timer_label.config(text=f"Time Left: {self.remaining_time} seconds")
        if self.remaining_time > 0:
            self.update_timer_id = self.root.after(1000, self.update_timer)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Typing Speed Test")
    app = TypingTestApp(root)
    root.mainloop()
