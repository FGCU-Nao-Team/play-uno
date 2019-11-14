from NAO import NAO
from UI import UIThread
from Tkinter import *
import Tkinter as tk
win = tk.Tk()
win.geometry("1200x700+30+30")
win.title("NAO plays UNO")

naoRobot = NAO("10.100.140.239", 9559)

guiThread = UIThread()
guiThread.run(naoRobot, win)
