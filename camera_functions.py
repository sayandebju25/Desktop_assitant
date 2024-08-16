import pyautogui
import subprocess
import time
from tkinter import messagebox

def open_camera_and_take_photo():
    # Open the camera app
    subprocess.Popen('start microsoft.windows.camera:', shell=True)
    time.sleep(3)  # Give it some time to open

    # Simulate pressing the enter key to take a photo
    pyautogui.press("enter")
    time.sleep(2)  # Wait for the photo to be taken
    messagebox.showinfo("Photo Captured", "Photo captured successfully!")

def close_camera():
    # Close the camera app (using Alt + F4 to close it)
    pyautogui.hotkey('alt', 'f4')
