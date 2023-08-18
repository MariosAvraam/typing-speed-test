import tkinter as tk
from tkinter import Text, Label, Button
import time
import requests


start_time = None
RUN_TIME = 10 * 1000 # in Seconds to Milliseconds
SAMPLE_TEXT_WORDS = 50
FONT = ("Arial", 12, "bold")
TIMER_DURATION = RUN_TIME / 1000
remaining_time = TIMER_DURATION
timer_id = None
stop_timer_id = None



def start_typing_test():
    global start_time, remaining_time, stop_timer_id
    remaining_time = TIMER_DURATION
    timer_label.config(text=f"Time Left: {TIMER_DURATION} seconds")
    update_timer()  # Start the timer

    change_text_button.config(state=tk.DISABLED)  
    stop_button.config(state=tk.NORMAL)  # Enable the Stop button
    user_input.config(state=tk.NORMAL)  # Enable the Text widget
    user_input.delete(1.0, tk.END)
    user_input.focus_set()  # Set focus to the Text widget to start typing immediately
    start_time = time.time()
    stop_timer_id = root.after(RUN_TIME, stop_typing_test)


def stop_typing_test():
    global timer_id, remaining_time, stop_timer_id
    if stop_timer_id:
        root.after_cancel(stop_timer_id)
    remaining_time = 0  # Stop the timer

    change_text_button.config(state=tk.NORMAL)  
    stop_button.config(state=tk.DISABLED)  # Disable the Stop button
    user_input.config(state=tk.DISABLED)  # Disable the Text widget
    if start_time is None:  # Ensure the test was started
        return
    
    elapsed_time = time.time() - start_time  # Calculate the elapsed time in seconds
    typed_text = user_input.get(1.0, tk.END).strip()  # Get the user's typed text
    words_typed = len(typed_text.split())  # Count the number of words typed by the user
    wpm = (words_typed / elapsed_time) * 60  # Calculate words per minute
    user_words = typed_text.split()
    sample_words_up_to_typed_length = sample_label['text'].split()[:len(user_words)]

    correct_words = sum(1 for w1, w2 in zip(user_words, sample_words_up_to_typed_length) if w1 == w2)
    accuracy = (correct_words / len(user_words)) * 100 if user_words else 0

    wpm_label.config(text=f"Words Per Minute: {round(wpm, 2)} | Accuracy: {round(accuracy, 2)}%")


def get_random_words(count=SAMPLE_TEXT_WORDS):
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
    words = get_random_words()
    chosen_text = ' '.join(words)
    
    sample_label.config(text=chosen_text)


def update_timer():
    global remaining_time, timer_id
    print(f"Remaining time: {remaining_time}")
    print(f"Run Time: {RUN_TIME}")
    print(f"TIMER_DURATION: {TIMER_DURATION}")
    print(f"start_time: {start_time}\n")
    if remaining_time > 0:
        remaining_time -= 1
        timer_label.config(text=f"Time Left: {remaining_time} seconds")
        timer_id = root.after(1000, update_timer)



# Create the main window
root = tk.Tk()
root.title("Typing Speed Test")

# Add a label to display the sample text
sample_text = "This is a sample text for the user to type."
sample_label = Label(root, text=sample_text, wraplength=400, padx=10, pady=10, font=FONT)
sample_label.pack(pady=20)

# Add a text widget for the user to type into
user_input = Text(root, wrap="word", height=5, width=50, padx=10, pady=10, state=tk.DISABLED)
user_input.pack(pady=20)

# Create a frame for the buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Add "Start", "Change Text", and "Stop" buttons within the frame
start_button = Button(button_frame, text="Start", command=start_typing_test)
start_button.grid(row=0, column=0, padx=10)

change_text_button = Button(button_frame, text="Change Text", command=change_sample_text)
change_text_button.grid(row=0, column=1, padx=10)

stop_button = Button(button_frame, text="Stop", command=stop_typing_test, state=tk.DISABLED)
stop_button.grid(row=0, column=2, padx=10)

timer_label = Label(root, text=f"Time Left: {TIMER_DURATION} seconds", padx=10, pady=10)
timer_label.pack(pady=10)

# Add a label to display the user's typing speed
wpm_label = Label(root, text="Your WPM will be displayed here.", padx=10, pady=10)
wpm_label.pack(pady=20)

# Start the Tkinter main loop
root.mainloop()
