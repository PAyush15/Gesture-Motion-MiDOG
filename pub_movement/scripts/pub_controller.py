#!/usr/bin/env python3
import rospy
import sys
from opencat import roscat
from opencat.roscat import Command, Task

class Controller:
    def __init__(self, robot_name):
        # Initialize the ROS node
        rospy.init_node('Controller_node')
        self.robot_name = robot_name
        self.sc = roscat.ServiceClient(self.robot_name)


if __name__ == "__main__":
    if(len(sys.argv) != 2):
        rospy.ERROR("need robot name")
    
    robot_name = str(sys.argv[1])    
    dog = Controller(robot_name)
    dog.sc.SendTask(roscat.Task(roscat.Command.SIT, [], 5))