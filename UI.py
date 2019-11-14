import Tkinter as tk
import threading
from Tkinter import *
import numpy as np
import vision_definitions
from PIL import Image, ImageTk




class UIThread(threading.Thread):

    def run(self, bot, win):

        textLabel = Label(win, text="Nao Vision")
        textLabel.pack(side=TOP, pady=10)
        winVision = Frame(win)
        winVision.pack(side=TOP)
        # Label in frame
        vLabel = Label(winVision)
        vLabel.pack()
        print 'UI Thread started'
        resolution = vision_definitions.kQVGA
        colorSpace = vision_definitions.kRGBColorSpace
        fps = 20

        nameID = bot.camProxy.subscribe("python_client", resolution, colorSpace, fps)
        bot.camProxy.setResolution(nameID, resolution)

        print 'Loop'
        while True:
            image = bot.camProxy.getImageRemote(nameID)
            im = Image.frombytes('RGB', (image[0], image[1]), image[6])

            print im
            visual = np.asarray(im)
            # Convert image format to tkinter compatible image
            frame_image = ImageTk.PhotoImage(image=im)
            # Display image to frame
            vLabel.frame_image = frame_image
            vLabel.config(image=frame_image)
            vLabel.image = frame_image
            win.mainloop()










