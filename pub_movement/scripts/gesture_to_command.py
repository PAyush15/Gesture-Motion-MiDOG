#!/usr/bin/env python3
import rospy
import sys
from opencat import roscat
from opencat.roscat import Command, Task
from std_msgs.msg import Int64

class Controller:

    def __init__(self, robot_name):
        self.robot_name = robot_name
        self.sc = roscat.ServiceClient(self.robot_name)


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

    gesture = data.data
    
    if(gesture==0):
        dog.sc.SendTask(roscat.Task(roscat.Command.PAUSE_MOTION, [], 5))
    elif(gesture==1):
        dog.sc.SendTask(roscat.Task(roscat.Command.WALK, [], 5))
    elif(gesture==3):
        dog.sc.SendTask(roscat.Task(roscat.Command.GREETING, [], 5))
    elif(gesture==5):
        dog.sc.SendTask(roscat.Task(roscat.Command.STRETCH, [], 5))
    elif(gesture==6):
        dog.sc.SendTask(roscat.Task(roscat.Command.SIT, [], 5))
    elif(gesture==2):
        dog.sc.SendTask(roscat.Task(roscat.Command.CRAWL_LEFT, [], 5))
    elif(gesture==4):
        dog.sc.SendTask(roscat.Task(roscat.Command.CRAWL_RIGHT, [], 5))
    elif(gesture==7):
        dog.sc.SendTask(roscat.Task(roscat.Command.BACK, [], 5))

    
    rate = rospy.Rate(0.5)
    rate.sleep()
    
def listener():
    rospy.init_node('command_executor', anonymous=True)
    rospy.Subscriber("gesture_topic", Int64, callback, queue_size=1)

    rospy.spin()

    
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        rospy.ERROR("Need robot name")

    robot_name = str(sys.argv[1])    
    dog = Controller(robot_name)

    listener()