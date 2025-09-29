import pyperclip
from pynput.keyboard import Controller
import time

def auto_type():
    """
    Types out the text from the clipboard with a delay.
    """
    try:
        text_to_type = pyperclip.paste()
    except pyperclip.PyperclipException as e:
        print(f"Could not find a copy/paste mechanism on your system.")
        print(f"Please install one of the following packages:")
        print(f"  - xclip (on Linux)")
        print(f"  - pywin32 (on Windows)")
        print(f"  - or see the pyperclip documentation for more options.")
        return

    if not text_to_type:
        print("Clipboard is empty.")
        return

    keyboard = Controller()

    print("You have 5 seconds to focus the text box...")
    time.sleep(5)
    print("Typing...")

    for char in text_to_type:
        keyboard.press(char)
        keyboard.release(char)
        time.sleep(0.05)  # Adjust delay if needed

    print("Done typing.")

if __name__ == "__main__":
    auto_type()
