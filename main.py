import tkinter as tk
from tkinter import Text, Label, Button, StringVar
import time

start_time = None
RUN_TIME = 10 * 1000 # in Seconds to Milliseconds

def start_typing_test():
    global start_time
    user_input.delete(1.0, tk.END)
    start_time = time.time()  # Record the current time as the start time
    print(start_time)
    root.after(RUN_TIME, stop_typing_test)  # Schedule the stop_typing_test to run after 1 minute

def stop_typing_test():
    if start_time is None:  # Ensure the test was started
        return
    
    elapsed_time = time.time() - start_time  # Calculate the elapsed time in seconds
    typed_text = user_input.get(1.0, tk.END).strip()  # Get the user's typed text
    words_typed = len(typed_text.split())  # Count the number of words typed by the user
    wpm = (words_typed / elapsed_time) * 60  # Calculate words per minute
    
    # Here, you can display the WPM to the user using a label or a messagebox
    print(f"Words Per Minute: {wpm}")

# Create the main window
root = tk.Tk()
root.title("Typing Speed Test")

# Add a label to display the sample text
sample_text = "This is a sample text for the user to type."
sample_label = Label(root, text=sample_text, wraplength=400, padx=10, pady=10)
sample_label.pack(pady=20)

# Add a text widget for the user to type into
user_input = Text(root, wrap="word", height=5, width=50, padx=10, pady=10)
user_input.pack(pady=20)

# Add "Start" and "Stop" buttons
start_button = Button(root, text="Start", command=start_typing_test)
start_button.pack(pady=10, side="left", padx=50)

stop_button = Button(root, text="Stop", command=stop_typing_test)
stop_button.pack(pady=10, side="right", padx=50)

# Start the Tkinter main loop
root.mainloop()
