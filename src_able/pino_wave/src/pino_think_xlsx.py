#!/usr/bin/env python
#-*-coding: utf-8

import sys

import rospy
import time
import numpy as np
import random
from std_msgs.msg import Int32
from std_msgs.msg import Bool

from pino_wave.msg import pino_listen
from pino_msgs.msg import PinoAnswer

from pino_message_sturct import *
from datetime import datetime

from openpyxl import load_workbook

think_filepath = "/home/junyoung/google-cloud-speech-to-text/src_pino/"
think_filename = "pino_think.txt"
think_filepath_xlsx = "/home/junyoung/catkin_ws/src/pino/"
think_filename_xlsx = "able_reaction_state.xlsx"
nomatching_filename = "no_matching.txt"

nothing_answer = ""
not_matching_limit = 120

reload(sys)
sys.setdefaultencoding('utf-8')

def matching():
	global listen_sentence, listen_database, answer_database, stand_database, sound_database
	global more_listen_database, more_answer_database, more_stand_database, more_sound_database, select_ratio_database

	for i in range(len(listen_database)):
		if listen_database[i] in listen_sentence:
			state = state_database[i]			
			return state

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
	global able_answer_message, able_node_status
	listen_sentence  = listen_init
	answer_message = PinoAnswer()
	answer_message_for_able = Int32()
	able_node_status = Bool()

def callback(data):
	global listen_sentence
	listen_sentence = data.listen
	print(listen_sentence)

listen_sentence = listen_init

listen_database = []
answer_database = []
stand_database = []
sound_database = []
state_database = []

more_listen_database = []
more_answer_database = []
more_stand_database = []
more_sound_database = []
more_state_dateabse = []
select_ratio_database = []
more_ratio_database = []
tmp_ratio_database = []

answer_message = PinoAnswer()
answer_message_for_able = Int32()
able_node_status = Bool()

not_matching_time_start = time.time()
not_matching_time_end = time.time()

if __name__ == '__main__':
	rospy.init_node('think', anonymous = False)

	rospy.Subscriber('/pino/listen',pino_listen,callback)

	pub_pino        = rospy.Publisher('/pino/answer',PinoAnswer,queue_size=10)
	pub_able_script = rospy.Publisher('/sr_node/script_number', Int32, queue_size=1)
	pub_able_status = rospy.Publisher('/sr_node/status', Bool, queue_size=1)

	print("think text reading ...\n")
	f = open(think_filepath+think_filename, "r")

	load_xlsx = load_workbook(think_filepath_xlsx+think_filename_xlsx, data_only=True)
	load_ws = load_xlsx['Sheet1']

	print('\n-----모든 행과 열 출력-----')
	all_values = []
	for row in load_ws.rows:
	    row_value = []
	    for cell in row:
	        row_value.append(cell.value)
	    all_values.append(row_value)
	for i in range(0,(len(list(load_ws.rows)))):
		print all_values[i]

	print('\n-----None이 제거된 모든 행과 열 출력-----')
	for i in range (len(list(load_ws.rows))):
		all_values[i] = list(filter(None, all_values[i]))
	for i in range(0,(len(list(load_ws.rows)))):
		print all_values[i]

	for row in range (1,(len(list(load_ws.rows)))):
		if len(all_values[row]) == 3:
			listen_database.append(all_values[row][1])
			state_database.append(all_values[row][2])
		else :
			tmp_state_list = []
			tmp_ratio_list = []
			if len(all_values[row]) == 5:
				tmp_state_list.append(all_values[row][2])
				tmp_state_list.append(all_values[row][3])
			elif len(all_values[row]) == 6:
				tmp_state_list.append(all_values[row][2])
				tmp_state_list.append(all_values[row][3])
				tmp_state_list.append(all_values[row][4])
			more_listen_database.append(all_values[row][1])
			more_state_dateabse.append(tmp_state_list)

			integer = all_values[row][-1].encode('utf-8')
			tmp_ratio_database.append(integer)

	print "\n"
	print "listen : ", listen_database
	print "state : ", state_database
	print "more_listen : ", more_listen_database
	print "more_state : ", more_state_dateabse
	print "more_ratio : ", tmp_ratio_database

	print "\nreading think file finish"

	while not rospy.is_shutdown():
		if listen_sentence != listen_init:
			if listen_sentence == listen_reset: #listen nothing
				answer_message.state = answer_state_start
				answer_message.stand = answer_stand_init
				answer_message.answer = nothing_answer
				answer_message.soundnum = answer_sound_reset
			else: #listen something
				state = matching()
				if state != -1: #matching
					not_matching_time_start = time.time() #time initalize
					not_matching_time_end = time.time()
	
					print("sound play : number-"+str(state))
					answer_message_for_able.data = state
				
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

			able_node_status = True
			pub_able_script.publish(answer_message_for_able)
			reset()
		rospy.sleep(0.1)
