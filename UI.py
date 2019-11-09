import Tkinter as tk
import threading
from Tkinter import *

import vision_definitions
from PIL import Image

win = tk.Tk()
win.geometry("1200x700+30+30")
win.title("NAO plays UNO")


class UIThread(threading.Thread):
    def run(self, bot):
        print 'UI Thread started'
        resolution = vision_definitions.kQVGA
        colorSpace = vision_definitions.kRGBColorSpace
        fps = 20

        nameID = bot.camProxy.subscribe("python_client", resolution, colorSpace, fps)
        bot.camProxy.setResolution(nameID, resolution)

        while True:
            image = bot.camProxy.getImageRemote(nameID)
            im = Image.frombytes('RGB', (image[0], image[1]), image[6])
            im.save("camImage.png", "PNG")
            im.show()
