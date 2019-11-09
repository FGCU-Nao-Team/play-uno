from naoqi import ALProxy

class NAO:

    def __init__(self, address, portNumber):

        self.IP = address
        self.PORT = portNumber

        self.ttsProxy = ALProxy("ALTextToSpeech", self.IP, self.PORT)
        self.motionProxy = ALProxy("ALMotion", self.IP, self.PORT)
        self.camProxy = ALProxy("ALVideoDevice", self.IP, self.PORT)
