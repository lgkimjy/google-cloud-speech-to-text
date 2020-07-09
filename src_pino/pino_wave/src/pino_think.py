#!/usr/bin/env python
#-*-coding: utf-8

import rospy
import time
import numpy as np
import random

from pino_wave.msg import pino_listen
from pino_msgs.msg import PinoAnswer

from pino_message_sturct import *
from datetime import datetime

think_filepath = "/home/pino/"
think_filename = "pino_think.txt"
nomatching_filename = "no_matching.txt"

nothing_answer = ""
not_matching_limit = 120

def matching():
	global listen_sentence, listen_database, answer_database, stand_database, sound_database
	global more_listen_database, more_answer_database, more_stand_database, more_sound_database, select_ratio_database

	for i in range(len(listen_database)):
		if listen_database[i] in listen_sentence:
			answer = answer_database[i]
			stand = stand_database[i]
			sound = sound_database[i]
			
			return answer, int(stand), int(sound)

	for i in range(len(more_listen_database)):
		if more_listen_database[i] in listen_sentence:
			reaction_num = len(more_answer_database[i])
			randomnum = random.randrange(1,101)
			for j in range(len(select_ratio_database[i])-1):
				if select_ratio_database[i][j] < randomnum <= select_ratio_database[i][j+1]:
					answer = more_answer_database[i][j]
					stand = more_stand_database[i][j]
					sound = more_sound_database[i][j]
					
					return answer, int(stand), int(sound)
			
	
	return -1, -1, -1

def reset():
	global listen_sentence, answer_message
	listen_sentence  = listen_init
	answer_message = PinoAnswer()

def callback(data):
	global listen_sentence
	listen_sentence = data.listen

listen_sentence = listen_init

listen_database = []
answer_database = []
stand_database = []
sound_database = []

more_listen_database = []
more_answer_database = []
more_stand_database = []
more_sound_database = []
select_ratio_database = []

answer_message = PinoAnswer()

not_matching_time_start = time.time()
not_matching_time_end = time.time()

if __name__ == '__main__':
	rospy.init_node('think', anonymous = False)
	rospy.Subscriber('/pino/listen',pino_listen,callback)
	pub = rospy.Publisher('/pino/answer',PinoAnswer,queue_size=10)

	print("think text reading ...")
	f = open(think_filepath+think_filename, "r")
	while True:
		line = f.readline()
		if not line: break
		split_line = line.split(",")
		if len(split_line) == 5:
			listen_database.append(split_line[1][1:-1])
			answer_database.append(split_line[2][1:-1])
			stand_database.append(split_line[3][1:-1])
			sound_database.append(split_line[4][1:-1])
		else:#random answer
			temp_answer_list = []
			temp_stand_list = []
			temp_sound_list = []
			for i in range(int(split_line[0][:-1])):
				temp_answer_list.append(split_line[2+i*3][1:-1])
				temp_stand_list.append(split_line[3+i*3][1:-1])
				temp_sound_list.append(split_line[4+i*3][1:-1])
			more_listen_database.append(split_line[1][1:-1])
			more_answer_database.append(temp_answer_list)
			more_stand_database.append(temp_stand_list)
			more_sound_database.append(temp_sound_list)
			
			temp_ratio = split_line[-1][1:-1].split(':')

			if len(temp_ratio) != int(split_line[0][:-1]):
				print(more_listen_database[-1])
				raise NameError('do not matching answer number and ratio noumber')

			for i in range(len(temp_ratio)-1):
				if i == 0:
					temp_ratio_list = [int(temp_ratio[i][1:])]
				else:
					temp_ratio_list.append(temp_ratio_list[i-1]+int(temp_ratio[i]))
			temp_ratio_list.append(temp_ratio_list[i]+int(temp_ratio[-1][:-1]))
			
			temp_ratio_list = [0] + temp_ratio_list

			if temp_ratio_list[-1] != 100:
				errorname = "listen " + more_listen_database[-1].decode('utf-8') + " sum of ratio is not 100"
				print(errorname)
				raise NameError('sum of ratio is not 100')
			
			select_ratio_database.append(temp_ratio_list)

	print("reading think file finish")

	while not rospy.is_shutdown():
		if listen_sentence != listen_init:
			if listen_sentence == listen_reset: #listen nothing
				answer_message.state = answer_state_start
				answer_message.stand = answer_stand_init
				answer_message.answer = nothing_answer
				answer_message.soundnum = answer_sound_reset
			else: #listen something
				answer, stand, sound = matching()
				if answer != -1: #matching
					not_matching_time_start = time.time() #time initalize
					not_matching_time_end = time.time()
	
					print(answer)
					print("sound play : number-"+str(sound))
					answer_message.state = answer_state_start
					answer_message.stand = stand
					answer_message.answer = answer
					answer_message.soundnum = sound
				
				else: #no matching
					rand = random.randrange(1,101)
					print("what are you saying?")
					if rand <= 30:
						answer_message.state = answer_state_start
						answer_message.stand = answer_stand_what
						answer_message.answer = nothing_answer
						answer_message.soundnum = 48
					else:
						answer_message.state = answer_state_start
						answer_message.stand = answer_stand_what
						answer_message.answer = nothing_answer
						answer_message.soundnum = answer_sound_reset

					datetoday = datetime.today()
					date = str(datetoday.year)+"."+str(datetoday.month)+"."+str(datetoday.day)+" "+str(datetoday.hour)+":"+str(datetoday.minute)+":"+str(datetoday.second)
					no_f = open(think_filepath+nomatching_filename, "a")
					no_f.write(date+" | "+listen_sentence+"\n")
					no_f.close()
					#time limit
					"""
					print("time : ", not_matching_time_end - not_matching_time_start)
					if not_matching_time_end - not_matching_time_start >= not_matching_limit:
						print("what are you saying?")
						not_matching_time_start = time.time() #time initalize
						not_matching_time_end = time.time()
						answer_message.state = answer_state_start
						answer_message.stand = answer_stand_what
						answer_message.answer = nothing_answer
						answer_message.soundnum = answer_sound_reset
					else:
						print("no matching")
						not_matching_time_end = time.time() #end tiem update
						answer_message.state = answer_state_start
						answer_message.stand = answer_stand_init
						answer_message.answer = nothing_answer
						answer_message.soundnum = answer_sound_reset
					"""
			rospy.loginfo(answer_message)
			pub.publish(answer_message)
			reset()
		rospy.sleep(0.1)
