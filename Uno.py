from naoqi import ALProxy 

tts = ALProxy("ALTextToSpeech", "10.100.150.11", 9559)

tts.say("How much could a woodchuck chuck if a woodchuck could chuck wood?")



