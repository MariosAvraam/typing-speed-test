# Typing Speed Test App

This is a simple desktop application to test your typing speed and accuracy. Users can type out randomly generated words and receive feedback on their words per minute (WPM) and typing accuracy.

## Features

- Dynamically generated words for users to type.
- Display the time remaining for the typing test.
- Calculate and display the user's WPM and accuracy.
- Save and display the highest WPM and accuracy achieved.
  
## Installation

1. Clone this repository:
```bash
git clone https://github.com/MariosAvraam/typing-speed-test.git
```


2. Navigate to the cloned directory and create a virtual environment (optional, but recommended):
```bash
cd typing-speed-test
python -m venv venv
source venv/bin/activate # On Windows use: .\venv\Scripts\activate
```


3. Install the required packages:
```bash
pip install -r requirements.txt
```


4. Run the application:
```bash
python main.py
```


## Dependencies

This application depends on:

- `tkinter` for the GUI.
- `requests` to fetch random words from an external API.

All dependencies can be installed using `pip` from the provided `requirements.txt` file.

## License

[MIT](LICENSE)


