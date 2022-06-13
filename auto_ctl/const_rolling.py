#ros import
#from csv_pub.csv_pub.swing_csv_make import MAX_INPUT, MAX_PRESS
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from tenpa_msgs.msg import Pressure12
#others import
import numpy as np
from numpy import pi
#=====global variables=============
BOARD_NUM = 4
CYLINDER_NUM = 4
LAYER_NUM = 5
MAX_PRESS = 0.6
MAX_INPUT = 255
#PUB_PERIOD = 10    #ms
QOS = 10    #queue size of Quality of Service
#===================================

class TenpaPublisher(Node):
    def __init__(self):
        #====== declare parameters ===========
        super().__init__('tenpa_ws')
        topicname_base = '/tenpa/pressure/desired'  # define topic name
        self.publisher_ = []
        self.count = 0     # csv_raw count
        self.base_count = 0
        self.keep_count = 0
        self.pos_num = 0
        self.phase_rate = 0
        self.pre_theta = 0
        # declare parameters for parameter communication
        self.declare_parameter('source_dir', '/home/yuhex/Documents/ROS/tensegrity_robot/tenpa2_ws/src/auto_ctl/resource/omni_base/')
        self.declare_parameter('source_file', 'test_base.csv')   #TODO
        self.declare_parameter('timer_period', 0.05)    #s #20Hz
        self.declare_parameter('reach_time', 6)    #s
        self.declare_parameter('loop', False)
        self.declare_parameter('theta', 0)  # rad   # rotate angle
        self.declare_parameter('keep_pos', False)
        self.declare_parameter('keep_time', 2)  #s
        self.declare_parameter('keep_period', 60)
        
        # read parameters from console or launch file
        self.src_dir = self.get_parameter('source_dir').get_parameter_value().string_value
        self.src_file = self.get_parameter('source_file').get_parameter_value().string_value
        self.timer_period = self.get_parameter('timer_period').value
        #self.reach_time = self.get_parameter('reach_time').value
        self.loop = self.get_parameter('loop').value
        self.theta = self.get_parameter('theta').value
        self.keep_pos = self.get_parameter('keep_pos').value
        self.keep_time = self.get_parameter('keep_time').value
        self.keep_period = self.get_parameter('keep_period').value
        
        #========= read base posture data from csv file =======
        path = self.src_dir + self.src_file
        self.get_logger().info('Lording......')
        with open(path, "r") as f:
            record = f.readlines()
            self.dataset = np.asfarray(
                [record[i].split(',') for i in range(len(record))]
            )
            self.base_input = self.dataset / MAX_PRESS * MAX_INPUT

        #========= publish ======================
        for i in range(BOARD_NUM):
            self.publisher_.append(self.create_publisher(Pressure12, topicname_base+str(i), QOS))
        self.get_logger().info('START UP')

        # generate a timer and execute timer_callback at every timer_perioid
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
    
    def timer_callback(self):
        #======== read parameters =============
        self.src_dir = self.get_parameter('source_dir').get_parameter_value().string_value
        self.src_file = self.get_parameter('source_file').get_parameter_value().string_value
        self.reach_time = self.get_parameter('reach_time').value
        self.loop = self.get_parameter('loop').value
        self.keep_pos = self.get_parameter('keep_pos').value
        self.keep_time = self.get_parameter('keep_time').value
        self.keep_period = self.get_parameter('keep_period').value

        currentTime = self.get_clock().now().to_msg()   # for sampled_stamp
        self.get_logger().info('Publishing: input pressure %d' % self.count)
        self.get_logger().info('Loading:    %s' % self.src_file)

        #========= calculate inputs of omni direction posture ========
            #====== theta sigmoid change =========
        N_phase = 1/self.timer_period * self.reach_time
        
        th_diff = self.theta - self.pre_theta
        #freq = 1/self.reach_time
        time = self.timer_period * self.count
        self.get_logger().info('time = %f' % time)
        current_th = self.pre_theta + th_diff * sigmoid(self.count/N_phase, a=8)
        self.get_logger().info('current theta = %f [deg]' % current_th*180/pi)

        test_idx = 0    #TODO for const roll
        input40 = input_roll(current_th, self.base_input[test_idx])
        
        # publish input40
        for i in range(BOARD_NUM):
            input12 = np.zeros(12)  # 12 input per 1 layer
            input12[0:10] = input40[0+10*i : 10+10*i]
            msg = Pressure12()
            msg.pressure = np.uint16(input12)

            msg.sampled_stamp = currentTime
            self.publisher_[i].publish(msg)

        pre_count = self.count # save previous count
        
        # increment
        if(current_th == self.theta):
            self.count = 0
            self.pre_theta = self.theta
        elif(self.count < N_phase):
            self.count += 1
        else:
            self.count = 0

        """
        if(self.phase_rate < 1):
            self.phase_rate += self.timer_period / self.reach_time
            self.count += 1
        elif(self.base_count +1 < len(self.base_data)):
            self.phase_rate = 0
            self.base_count += 1
        elif(self.loop==True):
            self.phase_rate = 0
            self.base_count = 0
            self.count = 0"""
        
        if(self.keep_pos==True):
            if(pre_count%self.keep_period == 0):    #per getting keep_period
                if(self.keep_count <  self.keep_time / self.timer_period):
                    self.count = pre_count  #keep count during keeping posture
                    self.keep_count += 1
                else:
                    self.keep_count = 0
        
        def input_roll(theta, base_input, layer_num=LAYER_NUM, cyli_num=CYLINDER_NUM):
            #========= calculate inputs of omni direction posture input ========
            base_agl = 2*pi/cyli_num    # base angle
            base_phi = [i*base_agl for i in range(cyli_num)]    # base vector angle
            press_vol = base_input    # original input pattern
            press_input = np.zeros(2*cyli_num*layer_num)    # pressure input array
            press_th = [(theta + i*base_agl)%(2*pi) for i in range(cyli_num)]  # pressure vector angle

                #=== disassembly pressure vectors to base vectors ========
            phase_idx = int(theta%(2*pi) / base_agl)  # phase index

            for layer_idx in range(layer_num):
                for i in range(cyli_num):
                    # angle distance between base and pressure vectors
                    angle_d = [press_th[i] - base_phi[(phase_idx + i)%cyli_num],
                            base_phi[(phase_idx + i)%cyli_num] + base_agl - press_th[i]]
                    # disassemblied press vector norm
                    press_vec = np.array([
                                    [press_vol[2*i+k + 2*cyli_num*layer_idx] * np.sin(angle_d[(j+1)%2])
                                        /(np.sin(angle_d[0]) + np.sin(angle_d[1])) for j in range(2)]
                                    for k in range(2)])
                    # pressure addition
                    for k in range(2):
                        press_input[(2*(phase_idx+i) +k)%(2*cyli_num)   + 2*cyli_num*layer_idx] += press_vec[k,0]
                        press_input[(2*(phase_idx+i+1) +k)%(2*cyli_num) + 2*cyli_num*layer_idx] += press_vec[k,1]
            
            return press_input

        def sigmoid(x, a=8):  # 0<x<1, 0<y<1
            A = (1-np.exp(-2*a*(x-1/2)))/(1+np.exp(-2*a*(x-1/2)))
            B = (1+np.exp(-a))/(1-np.exp(-a))
            y = 1/2 * (1 + A*B)
            
            return y
        


def main(args=None):
    rclpy.init(args=args)
    publisher = TenpaPublisher()
    rclpy.spin(publisher)

    #destory
    publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()



