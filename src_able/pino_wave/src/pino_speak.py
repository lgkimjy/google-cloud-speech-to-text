#!/usr/bin/env python
#-*-coding: utf-8

import rospy

from pino_msgs.msg import PinoAnswer

from pino_message_sturct import *

import pyaudio
import wave
import time
import os
from natsort import natsorted, ns

sounddirpath = "/home/pino/"
sounddir = "pino_voice"

Chunk = 1024

def callback(data):
	global answer_text, soundnum, answer_message
	if data.state == answer_state_start:
		answer_text = data.answer
		soundnum = data.soundnum
		answer_message = data

def reset():
	global answer_text, soundnum, answer_message
	answer_text = answer_init
	soundnum = answer_sound_reset
	answer_message = PinoAnswer()

answer_text = answer_init
soundnum = answer_sound_reset
answer_message = PinoAnswer()

if __name__ == '__main__':
	rospy.init_node('speaking', anonymous = False)
	rospy.Subscriber('/pino/answer', PinoAnswer, callback)
	pub = rospy.Publisher('/pino/answer',PinoAnswer,queue_size=10)

	soundfiles = os.listdir(sounddirpath+sounddir)
	soundfiles = natsorted(soundfiles, alg=ns.IGNORECASE)
	print("sound file : ", soundfiles)

	while not rospy.is_shutdown():
		if answer_text != answer_init:
			if soundnum != answer_sound_reset:
				if answer_text == listen_nothing: 
					print(listen_nothing)
					answer_message.state = answer_state_finish
				else:
					wavefile = wave.open(sounddirpath+sounddir+'/'+soundfiles[soundnum])
					audio = pyaudio.PyAudio()
					stream = audio.open(format=audio.get_format_from_width(wavefile.getsampwidth()),
										channels=wavefile.getnchannels(),
										rate=wavefile.getframerate(),
										output=True)
					sound_data = wavefile.readframes(Chunk)
					while sound_data != '':
						stream.write(sound_data)
						sound_data = wavefile.readframes(Chunk)
					stream.close()
					audio.terminate()
					answer_message.state = answer_state_finish
				print("sound track : ", soundnum)

			else:
				answer_message.state = answer_state_finish
				rospy.loginfo(answer_message)

			rospy.loginfo(answer_message)
			pub.publish(answer_message)
			reset()
		rospy.sleep(0.1)
