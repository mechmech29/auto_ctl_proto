import numpy as np
from numpy import pi
import csv 
import pandas as pd

#===== Global variables =========
#BASEPOS_NUM = 5
INPUT_DIM = 48
FREQ = 20 #Hz
REACH_TIME = 6 #s
MAX_PRESS = 0.6 #MPa
MAX_INPUT = 255
#================================
#==== file path =======
FILE_GLP = 2
FILE_NUM = 1
SRC_DIR = '/home/yuhex/Documents/ROS/tensegrity_robot/test_tenpa_ws/src/csv_pub/resource/swing_base/'
SAVE_DIR = '/home/yuhex/Documents/ROS/tensegrity_robot/test_tenpa_ws/src/csv_pub/resource/'
PATH1 = ['swing_base_1.csv']

PATH = [PATH1, PATH1]
#=================================
#==== read file ============
path = SRC_DIR + PATH[FILE_GLP-1][FILE_NUM-1]
with open(path, 'r') as f:
    record = f.readlines()
    base_data = np.asfarray(
        [record[i].split(',') for i in range(len(record))]
    )
#====== change file value =======
base_data = base_data / MAX_PRESS * MAX_INPUT
#===============================
N_phase = REACH_TIME*FREQ
rotate_data = np.array([base_data[0]])#initial input
for i in range(len(base_data)):
    diff = (base_data[(i+1)%len(base_data),:]-base_data[i,:])
    
    change = [list(base_data[i,:] + diff * np.sin((pi/2)/N_phase * (j+1)) ) for j in range(N_phase)]
    
    rotate_data = np.append(rotate_data, np.array(change), axis=0)
#print(rotate_data.shape)
#print(rotate_data)
np.savetxt(SAVE_DIR + 'swing_1_exe.csv', rotate_data, delimiter=',')

if(FILE_GLP == 1):
    np.savetxt(SAVE_DIR + 'swing_1_exe.csv', rotate_data, delimiter=',')
elif(FILE_GLP == 2):
    np.savetxt(SAVE_DIR + 'swing_1_' + str(REACH_TIME) + 's_exe.csv', rotate_data, delimiter=',')