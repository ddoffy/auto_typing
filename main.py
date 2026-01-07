import pyperclip
from pynput.keyboard import Controller
import time
import platform
import os
import subprocess

def get_clipboard_content():
    """
    Get clipboard content with platform-specific handling.
    Supports Kubuntu Wayland 24 and Windows 11.
    """
    system = platform.system()
    
    # Detect Wayland on Linux
    is_wayland = False
    if system == "Linux":
        session_type = os.environ.get('XDG_SESSION_TYPE', '').lower()
        wayland_display = os.environ.get('WAYLAND_DISPLAY', '')
        is_wayland = session_type == 'wayland' or wayland_display != ''
    
    # Try Wayland-specific clipboard tools first on Wayland
    if is_wayland:
        try:
            # Try wl-paste (wl-clipboard package)
            result = subprocess.run(['wl-paste'], capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                return result.stdout
        except (FileNotFoundError, subprocess.TimeoutExpired):
            print("Info: wl-paste not available. Install wl-clipboard for better Wayland support.")
            print("      Run: sudo apt install wl-clipboard")
    
    # Fall back to pyperclip (works on X11, Windows 11, macOS)
    try:
        return pyperclip.paste()
    except pyperclip.PyperclipException as e:
        print(f"Could not access clipboard on your system.")
        if system == "Linux":
            if is_wayland:
                print(f"For Kubuntu Wayland 24, install: sudo apt install wl-clipboard")
            else:
                print(f"For X11/X.Org, install: sudo apt install xclip or xsel")
        elif system == "Windows":
            print(f"For Windows 11, pyperclip should work by default.")
            print(f"If issues persist, try: pip install pywin32")
        else:
            print(f"See pyperclip documentation for your platform.")
        return None

def auto_type():
    """
    Types out the text from the clipboard with a delay.
    Supports Kubuntu Wayland 24 and Windows 11.
    """
    text_to_type = get_clipboard_content()
    
    if text_to_type is None:
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
