from NAO import NAO
from UI import UIThread


naoRobot = NAO("10.100.164.55", 9559)

guiThread = UIThread()
guiThread.run(naoRobot)
