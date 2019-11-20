from naoqi import ALProxy
import qi
import argparse
import sys
import os
import time
import vision_definitions
import time
import almath
import motion
import Tkinter as tk
import imageio
from Tkinter import *
import numpy as np
from PIL import Image, ImageTk


IP = "192.168.0.103"
PORT = 9559
tts = ALProxy("ALTextToSpeech", IP, PORT)
motionProxy = ALProxy("ALMotion", IP, PORT)
camProxy = ALProxy("ALVideoDevice", IP, PORT)
lifeProxy = ALProxy("ALAutonomousLife", IP, PORT)
lifeProxy.setAutonomousAbilityEnabled("BackgroundMovement", False)
motionProxy.wakeUp()

win = tk.Tk()
win.geometry("1200x700+30+30")
win.title("NAO plays UNO")

Title = Label(win,
              font='arial 24 bold',
              text="NAO Networking Project")
Title.pack()

headYaw = 0
headPitch = 0
ArmZ = 0
ArmY = 0


def armMovementUp(ArmZ):
    print("Arm moves up")

    ArmZ+=.25
    motionProxy.setStiffnesses("LArm", 1.0)
    motionProxy.angleInterpolation(
        ["LShoulderPitch"],
        [0.0, -float(ArmZ)],
        [1, 2],
        False,
        _async=True
    )


def armMovementDown(ArmZ):
    print("Arm moves down")

    ArmZ +=.25
    motionProxy.setStiffnesses("LArm", 1.0)
    motionProxy.angleInterpolation(
        ["LShoulderPitch"],
        [0.0, float(ArmZ)],
        [1, 2],
        False,
        _async=True
    )


def armMovementLeft(ArmY):
    print("Arm moves left")

    ArmY +=.25
    motionProxy.setStiffnesses("LArm", 1.0)
    motionProxy.angleInterpolation(
        ["LShoulderRoll"],
        [0.0, float(ArmY)],
        [1, 2],
        False,
        _async=True
    )


def armMovementRight(ArmY):
    print("Arm moves right")

    ArmY +=.25
    motionProxy.setStiffnesses("LArm", 1.0)
    motionProxy.angleInterpolation(
        ["LShoulderRoll"],
        [0.0, -float(ArmY)],
        [1, 2],
        False,
        _async=True
    )


def headMovementUp(headPitch):
    print("head moves up")

    headPitch+=.25
    motionProxy.setStiffnesses("Head", 1.0)
    # Will go to 1.0 then 0 radian  in two seconds
    motionProxy.angleInterpolation(
        ["HeadPitch"],
        [0.0, -float(headPitch)],
        [1, 2],
        False,
        _async=True
    )


def headMovementDown(headPitch):
    print("head moves down")

    headPitch+=.25
    motionProxy.setStiffnesses("Head", 1.0)
    # Will go to 1.0 then 0 radian  in two seconds
    motionProxy.angleInterpolation(
        ["HeadPitch"],
        [0.0, float(headPitch)],
        [1, 2],
        False,
        _async=True
    )


def headMovementLeft(headYaw):
    print("head moves left")

    headYaw+=.25
    motionProxy.setStiffnesses("Head", 1.0)
    # Will go to 1.0 then 0 radian  in two seconds
    motionProxy.angleInterpolation(
        ["HeadYaw"],
        [0.0, float(headYaw)],
        [1 , 2],
        False,
        _async=True
    )


def headMovementRight(headYaw):
    print("head moves right")

    headYaw+=.25
    motionProxy.setStiffnesses("Head", 1.0)
    # Will go to 1.0 then 0 radian  in two seconds
    motionProxy.angleInterpolation(
        ["HeadYaw"],
        [0.0, -float(headYaw)],
        [1, 2],
        False,
        _async=True
    )


# Vision stream method
def visionstream():
    resolution = 2
    colorspace = 11
    fps = 1

    def __getitem__(self, image):
        return self.image[6]

    nameid = camProxy.subscribe("python_client", resolution, colorspace, fps)
    image = camProxy.getImageRemote(nameid)
    camProxy.unsubscribe(nameid)

    imagewidth = image[0]
    imageheight = image[1]

    im = Image.frombytes('RGB', (imagewidth, imageheight), image[6])
    im.save('camImage.JPG')

    path2 = 'camImage.JPG'
    img2 = ImageTk.PhotoImage(Image.open(path2))
    panel.configure(image=img2)
    panel.image = img2

    win.after(300, visionstream)


# Vision window
path = 'camImage.JPG'
img = ImageTk.PhotoImage(Image.open(path))
panel = Label(win,
              image=img)
panel.pack()

# Communication function
def communication():
    comment = entryText.get()
    tts.say(comment)

# Communcation fields
entryText = Entry(win,
                  text='Communicate with NAO',
                  background='gray'
                  )
entryText.place(x=600, y=650, anchor='s')

ttsbutton = Button(win,
                   text='Submit',
                   command=communication
                   )
ttsbutton.place(x=735, y=650, anchor='s')


# Quit Button
quitButton = Button(win,
                    text='Quit',
                    command=win.quit
                    )
quitButton.config(height=2,
                  width=10,
                  font='system 15')
quitButton.place(x=1125, y=25, anchor='ne')


# Head Up Button setup
headUpButton = tk.Button(win,
                         text="Head Up",
                         bg='white',
                         command=lambda: headMovementUp(headPitch)
                         )
headUpButton.config(height=2,
                    width=10,
                    font='system 15'
                    )
headUpButton.place(x=100,
                   y=550,
                   anchor='sw'
                   )


# Head Down Button setup
headDownButton = tk.Button(win,
                           text="Head Down",
                           bg='white',
                           command=lambda: headMovementDown(headPitch)
                           )
headDownButton.config(height=2,
                      width=10,
                      font='system 15'
                      )
headDownButton.place(x=100,
                     y=650,
                     anchor='sw'
                     )


# Head Left Button setup
headLeftButton = tk.Button(win,
                           text="Head Left",
                           bg='white',
                           command=lambda: headMovementLeft(headYaw)
                           )
headLeftButton.config(height=2,
                      width=10,
                      font='system 15'
                      )
headLeftButton.place(x=25,
                     y=600,
                     anchor='sw'
                     )


# Head Right Button setup
headRightButton = tk.Button(win,
                            text="Head Right",
                            bg='white',
                            command=lambda: headMovementRight(headYaw)
                            )
headRightButton.config(height=2,
                       width=10,
                       font='system 15'
                       )
headRightButton.place(x=175,
                      y=600,
                      anchor='sw'
                      )


# Arm UP Button setup
armUpButton = tk.Button(win,
                        text="Arm Up",
                        bg='white',
                        command=lambda: armMovementUp(ArmZ)
                        )
armUpButton.config(height=2,
                   width=10,
                   font='system 15'
                   )
armUpButton.place(x=1100,
                  y=550,
                  anchor='se'
                  )


# Arm Down Button setup
armDownButton = tk.Button(win,
                          text="Arm Down",
                          bg='white',
                          command=lambda: armMovementDown(ArmZ)
                          )
armDownButton.config(height=2,
                     width=10,
                     font='system 15'
                     )
armDownButton.place(x=1100,
                    y=650,
                    anchor='se'
                    )


# Arm Left Button setup
armLeftButton = tk.Button(win,
                          text="Arm Left",
                          bg='white',
                          command=lambda: armMovementLeft(ArmY)
                          )
armLeftButton.config(height=2,
                     width=10,
                     font='system 15'
                     )
armLeftButton.place(x=1175,
                    y=600,
                    anchor='se'
                    )


# Arm Right Button setup
armRightButton = tk.Button(win,
                           text="Arm Right",
                           bg='white',
                           command=lambda: armMovementRight(ArmY)
                           )
armRightButton.config(height=2,
                      width=10,
                      font='system 15'
                      )
armRightButton.place(x=1025,
                     y=600,
                     anchor='se'
                     )

# call to visionstream() method
visionstream()

# Main window loop
win.mainloop()
