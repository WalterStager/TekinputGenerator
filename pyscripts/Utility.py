import pathlib

import PIL
import os
from PIL import ImageTk,Image

#set current file directory
directory = pathlib.Path(__file__).parent.absolute()

#Centralizing Window to middle of one Screen
def CentraliseWindow(window):
    window.update_idletasks()

    # Tkinter way to find the screen resolution
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    size = tuple(int(_) for _ in window.geometry().split('+')[0].split('x'))
    x = screen_width/2 - size[0]/2
    y = screen_height/2 - size[1]/2

    window.geometry("+%d+%d" % (x, y))


def NewImage(image_type, size_x, size_y):
    return Image.new(image_type, (size_x, size_y))


def MakeTKImage(relative_path,size_x = 0,size_y = 0):
    image = Image.open(relative_path)

    if (size_x !=0 and size_y != 0):
        image = image.resize((size_x,size_y))
        
    return ImageTk.PhotoImage(image)

def MakeTKImageWithImage(image):
    return ImageTk.PhotoImage(image)