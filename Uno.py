from naoqi import ALProxy
import vision_definitions
import time
import Tkinter as tk
import imageio
from Tkinter import *
import numpy as np
from PIL import Image, ImageTk


IP = "10.100.110.136"
PORT = 9559
tts = ALProxy("ALTextToSpeech", IP, PORT)
print("Connected!")
motionProxy = ALProxy("ALMotion", IP, PORT)
camProxy = ALProxy("ALVideoDevice", IP, PORT)


win = tk.Tk()
win.geometry("1200x700+30+30")
win.title("NAO plays UNO")

def headMovementUp():
    print("head moves up")

def headMovementDown():
    print("head moves down")

def headMovementLeft():
    print("head moves left")

def headMovementRight():
    print("head moves right")

def armMovementUp():
    print("Arm moves up")

def armMovementDown():
    print("Arm moves down")

def armMovementLeft():
    print("Arm moves left")

def armMovementRight():
    print("Arm moves right")




# Vision stream method
def visionStream(vision_image):
    visual = np.asarray(vision_image)

    # Convert image format to tkinter compatible image
    frame_image = ImageTk.PhotoImage(image=vision_image)
    # Display image to frame
    vLabel.frame_image = frame_image
    vLabel.config(image=frame_image)
    vLabel.image = frame_image
    vLabel.after(1, visionStream)

#Vision window initialization

#Work in Progress
textLabel = Label(win, text="Nao Vision")
textLabel.pack(side=TOP, pady=10)
winVision = Frame(win)
winVision.pack(side=TOP)
# Label in frame
vLabel = Label(winVision)

resolution = vision_definitions.kQQVGA
colorSpace = vision_definitions.kYUVColorSpace
fps = 20

nameId = camProxy.subscribe("python_client", resolution, colorSpace, fps)

# for i in range(0, 20):
#     image = camProxy.getImageRemote(nameId)
#     visionStream(image)
#     time.sleep(0.05)
camProxy.setResolution(nameId, resolution)
while True:
    image = camProxy.getImageRemote(nameId)
    print image
    im = Image.frombytes('RGB', (image[0], image[1]), image[6])
    # im.show()
    print visionStream(im)




# Text input
winInput = Frame(win)
winInput.pack(side=BOTTOM)
inputField = tk.Entry(winInput)


#Head window initialization
winButton = Frame(win)
winButton.pack(side=BOTTOM)

winHead = Frame(winButton)
winHead.pack(side=LEFT, padx=20)

headUp = tk.Frame(winHead)
headUp.pack(side=tk.TOP)

headDown = tk.Frame(winHead)
headDown.pack(side=tk.BOTTOM)

headLeft = tk.Frame(winHead)
headLeft.pack(side=tk.LEFT)

headRight = tk.Frame(winHead)
headRight.pack(side=tk.RIGHT)

#Head Up Button setup
headUpButton = tk.Button(headUp, text="Head Up", bg='black',
                         command=headMovementUp)
headUpButton.config(height=2, width=10, font='system 15')
headUpButton.pack(side=TOP, pady=5, padx=5)

#Head Down Button setup
headDownButton = tk.Button(headDown, text="Head Down", bg='white',
                           command=headMovementDown)
headDownButton.config(height=2, width=10, font='system 15')
headDownButton.pack(side=BOTTOM, pady=5, padx=5)

#Head Left Button setup
headLeftButton = tk.Button(headLeft, text="Head Left", bg='white',
                           command=headMovementLeft)
headLeftButton.config(height=2, width=10, font='system 15')
headLeftButton.pack(side=LEFT, pady=5, padx=5)

#Head Right Button setup
headRightButton = tk.Button(headRight, text="Head Right", bg='white',
                            command=headMovementRight)
headRightButton.config(height=2, width=10, font='system 15')
headRightButton.pack(side=RIGHT, pady=5, padx=5)

#Arm window initialization
winArm = Frame(winButton)
winArm.pack(side=RIGHT, padx=20)

armUp = tk.Frame(winArm)
armUp.pack(side=tk.TOP)

armDown = tk.Frame(winArm)
armDown.pack(side=tk.BOTTOM)

armLeft = tk.Frame(winArm)
armLeft.pack(side=tk.LEFT)

armRight = tk.Frame(winArm)
armRight.pack(side=tk.RIGHT)

#Arm UP Button setup
armUpButton = tk.Button(armUp, text="Arm Up", bg='white',
                        command=armMovementUp)
armUpButton.config(height=2, width=10, font='system 15')
armUpButton.pack(side=TOP, pady=5, padx=5)

#Arm Down Button setup
armDownButton = tk.Button(armDown, text="Arm Down", bg='white',
                          command=armMovementDown)
armDownButton.config(height=2, width=10, font='system 15')
armDownButton.pack(side=BOTTOM, pady=5, padx=5)

#Arm Left Button setup
armLeftButton = tk.Button(armLeft, text="Arm Left", bg='white',
                          command=armMovementLeft)
armLeftButton.config(height=2, width=10, font='system 15')
armLeftButton.pack(side=LEFT, pady=5, padx=5)

#Arm Right Button setup
armRightButton = tk.Button(armRight, text="Arm Right", bg='white',
                           command=armMovementRight)
armRightButton.config(height=2, width=10, font='system 15')
armRightButton.pack(side=RIGHT, pady=5, padx=5)

# camProxy.unsubscribe()
#Main window loop
win.mainloop()
