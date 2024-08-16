from tkinter import *  # Tkinter is a standard library, no need to install
from PIL import Image, ImageTk, ImageSequence  # Pillow for image processing
import time
from pygame import mixer  # pygame for playing audio

mixer.init()

root = Tk()
root.geometry("1000x500")

def play_gif():
    root.lift()
    root.attributes("-topmost", True)
    global img
    img = Image.open("iron_man.gif")  # Path to your GIF file
    lbl = Label(root)
    lbl.place(x=0, y=0)
    i = 0
    
    mixer.music.load("marvel_intro.mp3")  # Path to your music file
    mixer.music.play()  # Play the loaded music
    
    for img in ImageSequence.Iterator(img):
        img = img.resize((1000, 500))
        img = ImageTk.PhotoImage(img)
        lbl.config(image=img)
        root.update()
        time.sleep(0.05)
    
    root.destroy()

play_gif()
root.mainloop()
