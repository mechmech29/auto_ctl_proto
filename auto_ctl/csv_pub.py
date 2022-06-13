#ros import
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from tenpa_msgs.msg import Pressure12
#others import
import numpy as np
#=====global variables=============
BOARD_NUM = 4
#PUB_PERIOD = 10    #ms
QOS = 10    #queue size of Quality of Service
#===================================

class TenpaPublisher(Node):
    def __init__(self):
        super().__init__('tenpa_ws')
        topicname_base = '/tenpa/pressure/desired'  #define topic name
        self.publisher_ = []
        self.count = 0     #csv_raw count
        self.keep_count = 0
        self.pos_num = 0
        #declare parameters
        self.declare_parameter('source_dir', '/home/yuhex/Documents/ROS/tensegrity_robot/test_tenpa_ws/src/csv_pub2/resource/')
        self.declare_parameter('source_file', 'stdby.csv')
        self.declare_parameter('timer_period', 0.05)
        self.declare_parameter('loop', False)
        self.declare_parameter('keep_pos', False)
        self.declare_parameter('keep_time', 2)  #s
        self.declare_parameter('keep_period', 60)
        #read parameters from console or launch file
        self.src_dir = self.get_parameter('source_dir').get_parameter_value().string_value
        self.src_file = self.get_parameter('source_file').get_parameter_value().string_value
        self.timer_period = self.get_parameter('timer_period').value
        self.loop = self.get_parameter('loop').value
        self.keep_pos = self.get_parameter('keep_pos').value
        self.keep_time = self.get_parameter('keep_time').value
        self.keep_period = self.get_parameter('keep_period').value
        
        #read csv
        path = self.src_dir + self.src_file
        self.get_logger().info('Lording......')
        with open(path, "r") as f:
            record = f.readlines()
            self.dataset = np.asfarray(
                [record[i].split(',') for i in range(len(record))]
            ) #*300/255
        for i in range(BOARD_NUM):
            self.publisher_.append(self.create_publisher(Pressure12, topicname_base+str(i), QOS))
        
        
        self.get_logger().info('START UP')
        #generate a timer and execute timer_callback at every timer_perioid
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
    
    def timer_callback(self):
        #read parameters
        self.src_dir = self.get_parameter('source_dir').get_parameter_value().string_value
        self.src_file = self.get_parameter('source_file').get_parameter_value().string_value

        currentTime = self.get_clock().now().to_msg()   #for sampled_stamp
        self.get_logger().info('Publishing: input pressure %d' % self.count)
        self.get_logger().info('Loading:    %s' % self.src_file)

        for i in range(BOARD_NUM):
            msg = Pressure12()
            msg.pressure = np.uint16(self.dataset[self.count, 0+12*i:12+12*i]) #input desired pressure from csv file

            msg.sampled_stamp = currentTime
            self.publisher_[i].publish(msg) #No.i valve board pub
        
        pre_count = self.count #save previout count
        if(self.count < len(self.dataset)-1):
            self.count += 1
        elif(self.loop==True):
            self.count = 1
        
        if(self.keep_pos==True):
            if(pre_count%self.keep_period == 0):    #per getting keep_period
                if(self.keep_count <  self.keep_time / self.timer_period):
                    self.count = pre_count  #keep count during keeping posture
                    self.keep_count += 1
                else:
                    self.keep_count = 0


def main(args=None):
    rclpy.init(args=args)
    publisher = TenpaPublisher()
    rclpy.spin(publisher)

    #destory
    publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()



