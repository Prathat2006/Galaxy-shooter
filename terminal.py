import os
import subprocess
import time
import ctypes

def get_terminal_size():
    """Get the terminal size after ensuring the terminal is maximized."""
    if os.name == "nt":  # Only runs on Windows
        fullscreen_terminal()  # Maximize the terminal
        time.sleep(0.1)  # Allow time for the terminal to resize
    size = os.get_terminal_size()
    return size.columns, size.lines


FULLSCREEN_COLUMNS = 156  # Your full-screen width
FULLSCREEN_LINES = 46     # Your full-screen height

def is_terminal_fullscreen():
    """Checks if the terminal is already in full-screen mode based on size."""
    try:
        size = os.get_terminal_size()
        return size.columns == FULLSCREEN_COLUMNS and size.lines == FULLSCREEN_LINES
    except OSError:
        return False  # Fallback if terminal size can't be determined

def exit_fullscreen():
    """Exits full-screen mode by resizing the terminal."""
    if is_terminal_fullscreen():
        # Resize to a smaller size (e.g., 80x24) to exit full-screen mode
        alt_key = 0x12  # Virtual key code for Alt
        enter_key = 0x0D  # Virtual key code for Enter
    
        # Simulate Alt + Enter key press
        ctypes.windll.user32.keybd_event(alt_key, 0, 0, 0)  # Press Alt
        ctypes.windll.user32.keybd_event(enter_key, 0, 0, 0)  # Press Enter
        time.sleep(0.1)  # Short delay to register key press
        ctypes.windll.user32.keybd_event(enter_key, 0, 2, 0)  # Release Enter
        ctypes.windll.user32.keybd_event(alt_key, 0, 2, 0)  # Release Alt
        print("Exited full-screen mode.")
    else:
        print("Terminal is not in full-screen mode. Skipping...")

def fullscreen_terminal():
    """Simulates Alt + Enter only if the terminal is not already fullscreen."""
    if is_terminal_fullscreen():
        print("Terminal is already in full-screen mode. Skipping...")
        return

    alt_key = 0x12  # Virtual key code for Alt
    enter_key = 0x0D  # Virtual key code for Enter

    # Simulate Alt + Enter key press
    ctypes.windll.user32.keybd_event(alt_key, 0, 0, 0)  # Press Alt
    ctypes.windll.user32.keybd_event(enter_key, 0, 0, 0)  # Press Enter
    time.sleep(0.1)  # Short delay to register key press
    ctypes.windll.user32.keybd_event(enter_key, 0, 2, 0)  # Release Enter
    ctypes.windll.user32.keybd_event(alt_key, 0, 2, 0)  # Release Alt

# if __name__ == "__main__":
#     fullscreen_terminal()