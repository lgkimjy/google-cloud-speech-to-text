#!/usr/bin/env python
#-*-coding: utf-8

import rospy

from datetime import datetime
import pyaudio
import wave

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  
CHUNK = 1024
RECORD_SECONDS = 300
filepath = "/home/pino/voice_recoding/"

rospy.init_node('recording', anonymous=False)

while not rospy.is_shutdown():
	audio = pyaudio.PyAudio()
	datetoday = datetime.today()
	date = str(datetoday.year)+"_"+str(datetoday.month)+"_"+str(datetoday.day)+"_"+str(datetoday.hour)+"_"+str(datetoday.minute)+"_"+str(datetoday.second)+".wav"
	 
	# start Recording
	stream = audio.open(format=FORMAT, channels=CHANNELS,
						rate=RATE, input=True,
						frames_per_buffer=CHUNK)
	print ("recording...")
	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)
	print ("finished recording")

	# stop Recording
	stream.stop_stream()
	stream.close()
	audio.terminate()
	
	waveFile = wave.open(filepath+date, 'wb')
	waveFile.setnchannels(CHANNELS)
	waveFile.setsampwidth(audio.get_sample_size(FORMAT))
	waveFile.setframerate(RATE)
	waveFile.writeframes(b''.join(frames))
	waveFile.close()
	rospy.sleep(0.1)
