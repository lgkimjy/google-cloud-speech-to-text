#!/usr/bin/env python
#-*-coding: utf-8

#init
init_no = 0
init_ok = 1

#listen
listen_init = "듣는 말에 대한 초기화 상태입니다."
listen_reset = "리셋 상태입니다. 해당 상태는 아무것도 듣지 못한 상황입니다."
listen_nothing = "2분동안 아무것도 듣지 못했습니다. 아무것도 못들은 행동을 취합니다."

#answer
answer_state_start = 0
answer_state_finish = 1

answer_stand_init = 1
answer_stand_pos = 2
answer_stand_neg = 3
answer_stand_netural = 4
answer_stand_what = 5

answer_init = "대답에 대한 초기화 상태입니다."
answer_reset = "리셋 상태입니다. 해당 상태는 아무것도 대답하지 않습니다"
answer_sound_reset = -1
