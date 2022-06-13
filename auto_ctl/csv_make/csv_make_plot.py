import numpy as np
import csv 
import pandas as pd

#===== Global variables =========
#BASEPOS_NUM = 5
INPUT_DIM = 48
FREQ = 20 #Hz
REACH_TIME = 2 #s
MAX_PRESS = 0.6 #MPa
MAX_INPUT = 255
#================================
#==== file path =======
FILE_GLP = 1
FILE_NUM = 7
SRC_DIR = '/home/yuhex/Documents/ROS/tensegrity_robot/test_tenpa_ws/src/csv_pub2/resource/tuka_rotate_original/'
SAVE_DIR = '/home/yuhex/Documents/ROS/tensegrity_robot/test_tenpa_ws/src/csv_pub2/resource/'
PATH1 = ['tuka_rotate_1.csv',  #1
        'tuka_rotate_2.csv',  #2
        'tuka_rotate_3.csv',  #3
        'tuka_rotate_4.csv',  #4
        'tuka_rotate_5.csv',  #5
        'tuka_rotate_6.csv',    #6
        'IROS_demo_move.csv']  #7
PATH2 = ['tuka_rotate_3d_1.csv',
         'tuka_rotate_3d_2.csv',
         'tuka_rotate_3d_3.csv'] #1

PATH = [PATH1, PATH2]
#===========================
#base_postures = np.zeros((BASEPOS_NUM,INPUT_DIM))
#print(base_postures)
#==== read file ============
path = SRC_DIR + PATH[FILE_GLP-1][FILE_NUM-1]
with open(path, 'r') as f:
    record = f.readlines()
    base_data = np.asfarray(
        [record[i].split(',') for i in range(len(record))]
    )
#====== change file value =======
base_data = base_data / MAX_PRESS * MAX_INPUT

N_phase = REACH_TIME*FREQ
rotate_data = np.array([base_data[0]])#initial input
for i in range(len(base_data)):
    #sin change
    mini_change = (base_data[(i+1)%len(base_data),:]-base_data[i,:])/N_phase
    change = [list(base_data[i,:] + mini_change*(j+1)) for j in range(N_phase)]
    #change = [list( base_data[i,:] + (mini_change*N_phase) * np.sin(j * np.pi/2 / N_phase) ) for j in range(N_phase)]
    
    rotate_data = np.append(rotate_data, np.array(change), axis=0)
print(rotate_data.shape)

if(FILE_GLP == 1):
    #np.savetxt(SAVE_DIR + 'tuka_rotate_'+str(FILE_NUM)+'_exe.csv', rotate_data, delimiter=',')
    np.savetxt(SAVE_DIR + 'tuka_rotate_'+str(FILE_NUM)+'_1_exe.csv', rotate_data, delimiter=',')
elif(FILE_GLP == 2):
    np.savetxt(SAVE_DIR + 'tuka_rotate_3d_'+str(FILE_NUM)+'_exe.csv', rotate_data, delimiter=',')