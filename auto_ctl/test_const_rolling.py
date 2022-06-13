#ros import
#from csv_pub.csv_pub.swing_csv_make import MAX_INPUT, MAX_PRESS
#import rclpy
#from rclpy.node import Node
#from std_msgs.msg import String
#from tenpa_msgs.msg import Pressure12
#others import
import numpy as np
from numpy import pi
#=====global variables=============
BOARD_NUM = 4
CYLI_NUM = 4
LAYER_NUM = 2
MAX_PRESS = 0.6
MAX_INPUT = 255
#PUB_PERIOD = 10    #ms
QOS = 10    #queue size of Quality of Service
#===================================

class Test:
    def __init__(self):
        self.theta = 4*pi/3

        #========= calculate inputs of omni direction posture ========
        base_agl = 2*pi/CYLI_NUM    # base angle
        # base vector angle
        base_phi = [i*base_agl for i in range(CYLI_NUM)]
        print('base_phi')
        print(np.array(base_phi)*360/(2*pi))
        # pressure vector angle
        press_vol = [1, 0.1, 2, 0.2, 3, 0.3, 4, 0.4,
                     5, 0.5, 6, 0.6, 7, 0.7, 8, 0.8]    # original input pattern
        press_input = np.zeros(2*CYLI_NUM*LAYER_NUM)    # pressure input array
        #test_idx = 0    # TODO
        press_th = [(self.theta + i*base_agl)%(2*pi) for i in range(CYLI_NUM)]  # pressure vector angle

        # disassembly pressure vectors to base vectors
        phase_idx = int(self.theta%(2*pi) / base_agl)  # phase index
        print('phase index = %d' % phase_idx)

        for layer_idx in range(LAYER_NUM):
            for i in range(CYLI_NUM):
                # angle distance
                angle_d = [press_th[i] - base_phi[(phase_idx + i)%CYLI_NUM],
                        base_phi[(phase_idx + i)%CYLI_NUM] + base_agl - press_th[i] ]
                print('angle_d')
                print(np.array(angle_d)*360/(2*pi))
                # disassemblied press vector norm
                press_vec = np.array([
                                [press_vol[2*i+k + 2*CYLI_NUM*layer_idx] * np.sin(angle_d[(j+1)%2])
                                    /(np.sin(angle_d[0]) + np.sin(angle_d[1])) for j in range(2)]
                                for k in range(2)])
                print('press_vec')
                print(press_vec)

                # pressure addition
                for k in range(2):
                    press_input[(2*(phase_idx+i) +k)%(2*CYLI_NUM)   + 2*CYLI_NUM*layer_idx] += press_vec[k,0]
                    press_input[(2*(phase_idx+i+1) +k)%(2*CYLI_NUM) + 2*CYLI_NUM*layer_idx] += press_vec[k,1]
            
        print('press_input =')
        print(press_input)

def main(args=None):
    test = Test()
    test
    print('SUCCESS!!')

if __name__ == '__main__':
    main()