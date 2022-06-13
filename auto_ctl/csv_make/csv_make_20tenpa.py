from re import S
import numpy as np
import csv 
import pandas as pd

#===== Global variables =========
#BASEPOS_NUM = 5
INPUT_DIM = 48
FREQ = 20 #Hz
REACH_TIME = 1 #s
MAX_PRESS = 0.6 #MPa
MAX_INPUT = 255
#================================
#SRC_DIR = '/home/yuhex/Documents/ROS/tensegrity_robot/test_tenpa_ws/src/csv_pub2/resource/tuka_rotate_original/'
SAVE_DIR = '/home/yuhex/Documents/ROS/tensegrity_robot/test_tenpa_ws/src/csv_pub2/resource/swing_base/'
#===========================
const_press = 0.1
#const_press = 0.2
#const_press = 0.3
#const_press = 0.45
#const_press = 0.5
#const_press = 0.45

max_press = [0.6, 0.6, 0.6, 0.6, 0.6]
min_press = [0.3, 0.3, 0.3, 0.3, 0.3]

input_48 = np.zeros((2,48))
input_20 = np.ones((2,20))
for i in range(5):
    if(i%2 == 0):
        for k in range(2):
            input_20[:, 2*k + 4*i] = const_press
            input_20[k, 1 + 2*k + 4*i] = max_press[i]
            input_20[(k+1)%2, 1 + 2*k + 4*i] = min_press[i]
    if(i%2 != 0):
            for k in range(2):
                input_20[:, 2*k+1 + 4*i] = const_press
                input_20[k, 2*k + 4*i] = max_press[i]
                input_20[(k+1)%2, 2*k + 4*i] = min_press[i]
                #input_20[k, 4*i+2*k : 4*i+2+2*k] = max_press[i]
                #input_20[(k+1)%2, 4*i+2*k : 4*i+2+2*k] = min_press[i]
            
for i in range(2):
    input_48[:, 12*i:10+12*i] = input_20[:, 10*i:10+10*i]

for i in range(4):
    print(pd.DataFrame(input_48[:,12*i : 12+12*i]))

np.savetxt(SAVE_DIR + 'swing_base_20tenpa_01mp.csv', input_48, delimiter=',')
#np.savetxt(SAVE_DIR + 'swing_base_20tenpa_02mp.csv', input_48, delimiter=',')
#np.savetxt(SAVE_DIR + 'swing_base_20tenpa_03mp.csv', input_48, delimiter=',')
#np.savetxt(SAVE_DIR + 'swing_base_20tenpa_045mp.csv', input_48, delimiter=',')
#np.savetxt(SAVE_DIR + 'swing_base_20tenpa_05mp.csv', input_48, delimiter=',')
#np.savetxt(SAVE_DIR + 'swing_base_20tenpa_06mp.csv', input_48, delimiter=',')

#np.savetxt(SAVE_DIR + 'swing_base_20tenpa_allmax.csv', input_48, delimiter=',')

