from naoqi import ALProxy
import qi
import vision_definitions
import almath
import motion
import Tkinter as tk
import imageio
from Tkinter import *
import numpy as np
from PIL import Image, ImageTk

# NAO Proxy Setup
IP = "192.168.0.103"
PORT = 9559
tts = ALProxy("ALTextToSpeech", IP, PORT)
motionProxy = ALProxy("ALMotion", IP, PORT)
camProxy = ALProxy("ALVideoDevice", IP, PORT)
lifeProxy = ALProxy("ALAutonomousLife", IP, PORT)
lifeProxy.setAutonomousAbilityEnabled("BackgroundMovement", False)
motionProxy.wakeUp()

# Main window configurations
color = 'gray28'
win = tk.Tk()
win.geometry("1200x700+30+30")
win.title("NAO Networking Project")
win.configure(background=color)
Title = Label(win,
              font='arial 24 bold',
              background=color,
              highlightbackground=color,
              text="NAO Networking Project")
Title.pack()

# Head movement variables
head_yaw = 0
head_pitch = 0

# Left hand movement variables
l_arm_z = 0
l_arm_y = 0
l_elbow_roll = 0
l_wrist_yaw = 0
l_hand_move = 0

# Right hand movement variables
r_arm_z = 0
r_arm_y = 0
r_elbow_roll = 0
r_wrist_yaw = 0
r_hand_move = 0


# Right hand open function
def r_hand_open(r_hand_move):

    r_hand_move += .5
    motionProxy.angleInterpolation(
        ["RHand"],
        [float(r_hand_move)],
        [1.0],
        False,
        _async=True
    )


# Right hand close function
def r_hand_close(r_hand_move):

    r_hand_move += .5
    motionProxy.angleInterpolation(
        ["RHand"],
        [-float(r_hand_move)],
        [1.0],
        False,
        _async=True
    )


# Right wrist yaw to left function
def r_twist_wrist_left(r_wrist_yaw):

    r_wrist_yaw += .5
    motionProxy.angleInterpolation(
        ["RWristYaw"],
        [float(r_wrist_yaw)],
        [1.0],
        False,
        _async=True
    )


# Right wrist yaw to right function
def r_twist_wrist_right(r_wrist_yaw):

    r_wrist_yaw += .5
    motionProxy.angleInterpolation(
        ["RWristYaw"],
        [-float(r_wrist_yaw)],
        [1.0],
        False,
        _async=True
    )


# Right arm up movement function
def r_arm_movement_up(r_arm_z, r_elbow_roll):
    print("Arm moves up")

    r_arm_z += .25
    motionProxy.setStiffnesses("RArm", 1.0)
    motionProxy.angleInterpolation(
        ["RShoulderPitch"],
        [-float(r_arm_z)],
        [1.0],
        False,
        _async=True
    )

    r_elbow_roll += .3
    motionProxy.angleInterpolation(
        ["RElbowRoll"],
        [float(r_elbow_roll)],
        [1.0],
        False,
        _async=True
    )


# Right arm down movement function
def r_arm_movement_down(r_arm_z, r_elbow_roll):
    print("Arm moves down")

    r_arm_z += .25
    motionProxy.setStiffnesses("RArm", 1.0)
    motionProxy.angleInterpolation(
        ["RShoulderPitch"],
        [float(r_arm_z)],
        [1.0],
        False,
        _async=True
    )

    r_elbow_roll += .3
    motionProxy.angleInterpolation(
        ["RElbowRoll"],
        [-float(r_elbow_roll)],
        [1.0],
        False,
        _async=True
    )


# Right arm left movement function
def r_arm_movement_left(r_arm_y):
    print("Arm moves left")

    r_arm_y += .25
    motionProxy.setStiffnesses("RArm", 1.0)
    motionProxy.angleInterpolation(
        ["RShoulderRoll"],
        [-float(r_arm_y)],
        [1.0],
        False,
        _async=True
    )


# Right arm right movement function
def r_arm_movement_right(r_arm_y):
    print("Arm moves right")

    r_arm_y += .25
    motionProxy.setStiffnesses("RArm", 1.0)
    motionProxy.angleInterpolation(
        ["RShoulderRoll"],
        [float(r_arm_y)],
        [1.0],
        False,
        _async=True
    )


# Left hand open function
def l_hand_open(l_hand_move):

    l_hand_move += .5
    motionProxy.angleInterpolation(
        ["LHand"],
        [float(l_hand_move)],
        [1.0],
        False,
        _async=True
    )


# Left hand close function
def l_hand_close(l_hand_move):

    l_hand_move += .5
    motionProxy.angleInterpolation(
        ["LHand"],
        [-float(l_hand_move)],
        [1.0],
        False,
        _async=True
    )


# Left arm wrist yaw left function
def l_twist_wrist_left(l_wrist_yaw):

    l_wrist_yaw += .5
    motionProxy.angleInterpolation(
        ["LWristYaw"],
        [-float(l_wrist_yaw)],
        [1.0],
        False,
        _async=True
    )


# Left arm wrist yaw right function
def l_twist_wrist_right(l_wrist_yaw):

    l_wrist_yaw += .5
    motionProxy.angleInterpolation(
        ["LWristYaw"],
        [float(l_wrist_yaw)],
        [1.0],
        False,
        _async=True
    )


# Left arm up movement function
def l_arm_movement_up(l_arm_z, l_elbow_roll):
    print("Arm moves up")

    l_arm_z += .25
    motionProxy.setStiffnesses("LArm", 1.0)
    motionProxy.angleInterpolation(
        ["LShoulderPitch"],
        [-float(l_arm_z)],
        [1.0],
        False,
        _async=True
    )

    l_elbow_roll += .3
    motionProxy.angleInterpolation(
        ["LElbowRoll"],
        [-float(l_elbow_roll)],
        [1.0],
        False,
        _async=True
    )


# Left arm down movement function
def l_arm_movement_down(l_arm_z, l_elbow_roll):
    print("Arm moves down")

    l_arm_z += .25
    motionProxy.setStiffnesses("LArm", 1.0)
    motionProxy.angleInterpolation(
        ["LShoulderPitch"],
        [float(l_arm_z)],
        [1.0],
        False,
        _async=True
    )

    l_elbow_roll += .3
    motionProxy.angleInterpolation(
        ["LElbowRoll"],
        [float(l_elbow_roll)],
        [1.0],
        False,
        _async=True
    )


# Left arm left movement function
def l_arm_movement_left(l_arm_y):
    print("Arm moves left")

    l_arm_y += .25
    motionProxy.setStiffnesses("LArm", 1.0)
    motionProxy.angleInterpolation(
        ["LShoulderRoll"],
        [float(l_arm_y)],
        [1.0],
        False,
        _async=True
    )


# Left arm right movement function
def l_arm_movement_right(l_arm_y):
    print("Arm moves right")

    l_arm_y += .25
    motionProxy.setStiffnesses("LArm", 1.0)
    motionProxy.angleInterpolation(
        ["LShoulderRoll"],
        [-float(l_arm_y)],
        [1.0],
        False,
        _async=True
    )


# Head movement up function
def head_movement_up(head_pitch):
    print("head moves up")

    head_pitch += .25
    # Will go to 1.0 then 0 radian  in two seconds
    motionProxy.angleInterpolation(
        ["HeadPitch"],
        [-float(head_pitch)],
        [1.0],
        False,
        _async=True
    )


# Head movement down function
def head_movement_down(head_pitch):
    print("head moves down")

    head_pitch += .25
    # Will go to 1.0 then 0 radian  in two seconds
    motionProxy.angleInterpolation(
        ["HeadPitch"],
        [float(head_pitch)],
        [1.0],
        False,
        _async=True
    )


# Head movement left function
def head_movement_left(head_yaw):
    print("head moves left")

    head_yaw += .25
    # Will go to 1.0 then 0 radian  in two seconds
    motionProxy.angleInterpolation(
        ["HeadYaw"],
        [float(head_yaw)],
        [1.0],
        False,
        _async=True
    )


# Head movement right function
def head_movement_right(head_yaw):
    print("head moves right")

    head_yaw += .25
    # Will go to 1.0 then 0 radian  in two seconds
    motionProxy.angleInterpolation(
        ["HeadYaw"],
        [-float(head_yaw)],
        [1.0],
        False,
        _async=True
    )


# Vision stream function
def vision_stream():
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

    win.after(300, vision_stream)


# function for communication from NAO
def communication():
    comment = entryText.get()
    tts.say(comment)


# function to quit program
def quit_program():
    win.quit()


# Vision window
path = 'camImage.JPG'
img = ImageTk.PhotoImage(Image.open(path))
panel = Label(win,
              image=img)
panel.pack()


# Entry field title
ttsTitle = Label(win,
                 font='arial 14 bold',
                 background=color,
                 highlightbackground=color,
                 text="Tell NAO what to say!"
                 )
ttsTitle.place(x=515,
               y=655,
               anchor='se'
               )


# Entry Field
entryText = Entry(win,
                  background='gray',
                  width=40,
                  highlightbackground=color
                  )
entryText.place(x=550,
                y=680,
                anchor='s'
                )


# Button to submit Entry field
ttsbutton = Button(win,
                   text='Submit',
                   command=communication,
                   highlightbackground=color
                   )
ttsbutton.place(x=785,
                y=680,
                anchor='s'
                )


# Quit Button
quitButton = Button(win,
                    text='Quit',
                    command=quit_program,
                    highlightbackground=color
                    )
quitButton.config(height=2,
                  width=10,
                  font='system 15')
quitButton.place(x=1125,
                 y=25,
                 anchor='ne'
                 )


# Head controls title
HeadTitle = Label(win,
                  font='arial 18 bold',
                  background=color,
                  highlightbackground=color,
                  text="Head Controls"
                  )
HeadTitle.place(x=643,
                y=550,
                anchor='se'
                )


# Head Up Button setup
headUpButton = tk.Button(win,
                         text="Head Up",
                         bg='black',
                         highlightbackground=color,
                         bd=-2,
                         command=lambda: head_movement_up(head_pitch)
                         )
headUpButton.config(height=2,
                    width=10,
                    font='system 15'
                    )
headUpButton.place(x=520,
                   y=595,
                   anchor='sw'
                   )


# Head Down Button setup
headDownButton = tk.Button(win,
                           text="Head Down",
                           bg='white',
                           highlightbackground=color,
                           command=lambda: head_movement_down(head_pitch)
                           )
headDownButton.config(height=2,
                      width=10,
                      font='system 15'
                      )
headDownButton.place(x=520,
                     y=640,
                     anchor='sw'
                     )


# Head Left Button setup
headLeftButton = tk.Button(win,
                           text="Head Left",
                           bg='white',
                           highlightbackground=color,
                           command=lambda: head_movement_left(head_yaw)
                           )
headLeftButton.config(height=2,
                      width=10,
                      font='system 15'
                      )
headLeftButton.place(x=400,
                     y=620,
                     anchor='sw'
                     )


# Head Right Button setup
headRightButton = tk.Button(win,
                            text="Head Right",
                            bg='white',
                            highlightbackground=color,
                            command=lambda: head_movement_right(head_yaw)
                            )
headRightButton.config(height=2,
                       width=10,
                       font='system 15'
                       )
headRightButton.place(x=640,
                      y=620,
                      anchor='sw'
                      )


# Left hand controls title
LeftHandTitle = Label(win,
                      font='arial 18 bold',
                      background=color,
                      highlightbackground=color,
                      text="Left Hand Controls"
                      )
LeftHandTitle.place(x=220,
                    y=270,
                    anchor='se'
                    )


# Left hand open button
LHandOpenButton = Button(win,
                         text='Hand Open',
                         font='system 15',
                         highlightbackground=color,
                         command=lambda: l_hand_open(l_hand_move)
                         )
LHandOpenButton.place(x=135,
                      y=300,
                      anchor='s'
                      )


# Left hand close button
LHandCloseButton = Button(win,
                          text='Hand Close',
                          highlightbackground=color,
                          command=lambda: l_hand_close(l_hand_move)
                          )
LHandCloseButton.place(x=135,
                       y=350,
                       anchor='s'
                       )


# Left arm button to Yaw Wrist to the left
LWristYawLeftButton = Button(win,
                             text='Twist Wrist Left',
                             font='system 15',
                             highlightbackground=color,
                             command=lambda: l_twist_wrist_left(l_wrist_yaw)
                             )
LWristYawLeftButton.place(x=135,
                          y=400,
                          anchor='s'
                          )


# Left arm button to Yaw Wrist to the right
LWristYawRightButton = Button(win,
                              text='Twist Wrist Right',
                              font='system 15',
                              highlightbackground=color,
                              command=lambda: l_twist_wrist_right(l_wrist_yaw)
                              )
LWristYawRightButton.place(x=135,
                           y=450,
                           anchor='s'
                           )


# Left arm up control Button setup
LarmUpButton = tk.Button(win,
                         text="Arm Up",
                         bg='white',
                         highlightbackground=color,
                         command=lambda: l_arm_movement_up(l_arm_z, l_elbow_roll)
                         )
LarmUpButton.config(height=2,
                    width=10,
                    font='system 15'
                    )
LarmUpButton.place(x=200,
                   y=550,
                   anchor='se'
                   )


# Left arm down control button setup
LarmDownButton = tk.Button(win,
                           text="Arm Down",
                           bg='white',
                           highlightbackground=color,
                           command=lambda: l_arm_movement_down(l_arm_z, l_elbow_roll)
                           )
LarmDownButton.config(height=2,
                      width=10,
                      font='system 15'
                      )
LarmDownButton.place(x=200,
                     y=650,
                     anchor='se'
                     )


# Left arm left control button setup
LarmLeftButton = tk.Button(win,
                           text="Arm Left",
                           bg='white',
                           highlightbackground=color,
                           command=lambda: l_arm_movement_left(l_arm_y)
                           )
LarmLeftButton.config(height=2,
                      width=10,
                      font='system 15'
                      )
LarmLeftButton.place(x=125,
                     y=600,
                     anchor='se'
                     )


# Left arm right control button setup
LarmRightButton = tk.Button(win,
                            text="Arm Right",
                            bg='white',
                            highlightbackground=color,
                            command=lambda: l_arm_movement_right(l_arm_y)
                            )
LarmRightButton.config(height=2,
                       width=10,
                       font='system 15'
                       )
LarmRightButton.place(x=275,
                      y=600,
                      anchor='se'
                      )


# Left hand controls title
LeftHandTitle = Label(win,
                      font='arial 18 bold',
                      background=color,
                      highlightbackground=color,
                      text="Right Hand Controls"
                      )
LeftHandTitle.place(x=1150,
                    y=270,
                    anchor='se'
                    )


# Right hand open button
RHandOpenButton = Button(win,
                         text='Hand Open',
                         font='system 15',
                         highlightbackground=color,
                         command=lambda: r_hand_open(r_hand_move)
                         )
RHandOpenButton.place(x=1060,
                      y=300,
                      anchor='s'
                      )


# Right hand close button
RHandCloseButton = Button(win,
                          text='Hand Close',
                          highlightbackground=color,
                          command=lambda: r_hand_close(r_hand_move)
                          )
RHandCloseButton.place(x=1060,
                       y=350,
                       anchor='s'
                       )


# Right arm button to Yaw Wrist to the left
RWristYawLeftButton = Button(win,
                             text='Twist Wrist Left',
                             font='system 15',
                             highlightbackground=color,
                             command=lambda: r_twist_wrist_left(r_wrist_yaw)
                             )
RWristYawLeftButton.place(x=1060,
                          y=400,
                          anchor='s'
                          )


# Right arm button to Yaw Wrist to the right
RWristYawRightButton = Button(win,
                              text='Twist Wrist Right',
                              font='system 15',
                              highlightbackground=color,
                              command=lambda: r_twist_wrist_right(r_wrist_yaw)
                              )
RWristYawRightButton.place(x=1060,
                           y=450,
                           anchor='s'
                           )


# Right arm up button setup
RarmUpButton = tk.Button(win,
                         text="Arm Up",
                         bg='white',
                         highlightbackground=color,
                         command=lambda: r_arm_movement_up(r_arm_z, r_elbow_roll)
                         )
RarmUpButton.config(height=2,
                    width=10,
                    font='system 15'
                    )
RarmUpButton.place(x=1115,
                   y=550,
                   anchor='se'
                   )


# Right arm down button setup
RarmDownButton = tk.Button(win,
                           text="Arm Down",
                           bg='white',
                           highlightbackground=color,
                           command=lambda: r_arm_movement_down(r_arm_z, r_elbow_roll)
                           )
RarmDownButton.config(height=2,
                      width=10,
                      font='system 15'
                      )
RarmDownButton.place(x=1115,
                     y=650,
                     anchor='se'
                     )


# Right arm left button setup
RarmLeftButton = tk.Button(win,
                           text="Arm Left",
                           bg='white',
                           highlightbackground=color,
                           command=lambda: r_arm_movement_left(r_arm_y)
                           )
RarmLeftButton.config(height=2,
                      width=10,
                      font='system 15'
                      )
RarmLeftButton.place(x=1190,
                     y=600,
                     anchor='se'
                     )


# Right arm right button setup
RarmRightButton = tk.Button(win,
                            text="Arm Right",
                            bg='white',
                            highlightbackground=color,
                            command=lambda: r_arm_movement_right(r_arm_y)
                            )
RarmRightButton.config(height=2,
                       width=10,
                       font='system 15'
                       )
RarmRightButton.place(x=1040,
                      y=600,
                      anchor='se'
                      )


# call to visionstream() method
vision_stream()

# Main window loop
win.mainloop()
