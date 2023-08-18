import tkinter as tk
from tkinter import Text, Label, Button, StringVar
import time
import requests


start_time = None
RUN_TIME = 10 * 1000 # in Seconds to Milliseconds

def start_typing_test():
    global start_time

    change_text_button.config(state=tk.DISABLED)  
    stop_button.config(state=tk.NORMAL)  # Enable the Stop button
    user_input.config(state=tk.NORMAL)  # Enable the Text widget
    user_input.delete(1.0, tk.END)
    user_input.focus_set()  # Set focus to the Text widget to start typing immediately
    start_time = time.time()
    root.after(RUN_TIME, stop_typing_test)


def stop_typing_test():
    change_text_button.config(state=tk.NORMAL)  
    stop_button.config(state=tk.DISABLED)  # Disable the Stop button
    user_input.config(state=tk.DISABLED)  # Disable the Text widget
    if start_time is None:  # Ensure the test was started
        return
    
    elapsed_time = time.time() - start_time  # Calculate the elapsed time in seconds
    typed_text = user_input.get(1.0, tk.END).strip()  # Get the user's typed text
    words_typed = len(typed_text.split())  # Count the number of words typed by the user
    wpm = (words_typed / elapsed_time) * 60  # Calculate words per minute
    correct_words = sum(1 for w1, w2 in zip(typed_text.split(), sample_label['text'].split()) if w1 == w2)
    accuracy = (correct_words / len(sample_label['text'].split())) * 100
    wpm_label.config(text=f"Words Per Minute: {round(wpm, 2)} | Accuracy: {round(accuracy, 2)}%")


def get_random_words(count=1):
    url = f"https://random-word-api.herokuapp.com/word?number={count}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.RequestException:
        # Return a default list of words in case of an error
        return ["Error", "fetching", "random", "words,", "please", "try", "again."]


def change_sample_text():
    # Fetch 5 random words and form a sample sentence
    words = get_random_words(5)
    chosen_text = ' '.join(words)
    
    sample_label.config(text=chosen_text)


# Create the main window
root = tk.Tk()
root.title("Typing Speed Test")

# Add a label to display the sample text
sample_text = "This is a sample text for the user to type."
sample_label = Label(root, text=sample_text, wraplength=400, padx=10, pady=10)
sample_label.pack(pady=20)

# Add a text widget for the user to type into
user_input = Text(root, wrap="word", height=5, width=50, padx=10, pady=10, state=tk.DISABLED)
user_input.pack(pady=20)

# Add "Start" and "Stop" buttons
start_button = Button(root, text="Start", command=start_typing_test)
start_button.pack(pady=10, side="left", padx=50)

change_text_button = Button(root, text="Change Text", command=change_sample_text)
change_text_button.pack(pady=10, side="bottom", padx=50)

stop_button = Button(root, text="Stop", command=stop_typing_test, state=tk.DISABLED)
stop_button.pack(pady=10, side="right", padx=50)

# Add a label to display the user's typing speed
wpm_label = Label(root, text="Your WPM will be displayed here.", padx=10, pady=10)
wpm_label.pack(pady=20)

# Start the Tkinter main loop
root.mainloop()
