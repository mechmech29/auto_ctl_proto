import numpy as np
import csv 
import pandas as pd

#===== Global variables =========
#BASEPOS_NUM = 5
INPUT_DIM = 48
FREQ = 20 #Hz
REACH_TIME = 3 #s
MAX_PRESS = 0.6 #MPa
MAX_INPUT = 255
#================================
#==== file path =======
SRC_DIR = '/home/yuhex/Documents/ROS/tensegrity_robot/test_tenpa_ws/src/csv_pub/resource/swing_base/'
SAVE_DIR = '/home/yuhex/Documents/ROS/tensegrity_robot/test_tenpa_ws/src/csv_pub/resource/'

FILE = 'swing_base_1.csv'
#===========================
#base_postures = np.zeros((BASEPOS_NUM,INPUT_DIM))
#print(base_postures)
#==== read file ============
path = SRC_DIR + FILE
with open(path, 'r') as f:
    record = f.readlines()
    base_data = np.asfarray(
        [record[i].split(',') for i in range(len(record))]
    )
#====== change file value =======
base_data = base_data * 300/255

print(base_data)

#==== save file ===============
#np.savetxt(SRC_DIR + 'swing_base_1_cp.csv', base_data, delimiter=',')
