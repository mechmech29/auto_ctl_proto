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
#TestData
TEST_PRESSURE = np.ones(12) * 150.0
TEST_PRESSURE[10] = 0.0
TEST_PRESSURE[11] = 0.0
FILE_NUM = 3
#test_csv_path
#PATH = '/home/yuhex/Documents/ROS/tensegrity_robot/test_tenpa_ws/src/csv_pub/csv_pub/test_csv.csv'
PATH = '/home/yuhex/OneDrive/ドキュメント/研究/ソフトロボティクス研究/TensegrityRobotArm/tenpa_v2.0/source_data/input_data/tuka_rotate_'+str(FILE_NUM)+'_exe.csv'
#PATH = '/home/yuhex/OneDrive/ドキュメント/研究/ソフトロボティクス研究/TensegrityRobotArm/tenpa_v2.0/source_data/input_data/tuka_rotate_3d_'+str(FILE_NUM)+'_exe.csv'
#PATH = '/home/yuhex/OneDrive/ドキュメント/研究/ソフトロボティクス研究/TensegrityRobotArm/tenpa_v2.0/source_data/input_data/tuka_rotate_1_exe_test2.csv'
#PATH = 'test_csv.csv'
#===================================

class TenpaPublisher(Node):
    def __init__(self):
        super().__init__('tenpa_ws')
        topicname_base = '/tenpa/pressure/desired'  #define topic name
        self.publisher_ = []
        self.count = 0     #csv_raw count
        #read csv
        path = PATH     #testdata TO DO
        with open(path, "r") as f:
            record = f.readlines()
            self.dataset = np.asfarray(
                [record[i].split(',') for i in range(len(record))]
            )
        for i in range(BOARD_NUM):
            self.publisher_.append(self.create_publisher(Pressure12, topicname_base+str(i), QOS))
        timer_period = 0.05 #s #interval
        #generate a timer and execute timer_callback at every timer_perioid
        self.timer = self.create_timer(timer_period, self.timer_callback)
    
    def timer_callback(self):
        currentTime = self.get_clock().now().to_msg()   #for sampled_stamp
        self.get_logger().info('Publishing: input pressure %d' % self.count)
        for i in range(BOARD_NUM):
            msg = Pressure12()
            msg.pressure = np.uint16(self.dataset[self.count, 0+12*i:12+12*i]) #input desired pressure from csv file

            msg.sampled_stamp = currentTime
            self.publisher_[i].publish(msg) #No.i valve board pub
            #self.get_logger().info('Publishing: to board%d' % i)
        if(self.count < len(self.dataset)-1):
            self.count += 1

def main(args=None):
    rclpy.init(args=args)
    publisher = TenpaPublisher()
    rclpy.spin(publisher)

    #destory
    publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()



