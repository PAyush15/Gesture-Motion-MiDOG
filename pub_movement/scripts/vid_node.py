#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

def image_callback(msg):
    # Convert ROS Image message to OpenCV image
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")

    # Your image processing or display code here
    cv2.imshow("Image from ROS topic", cv_image)
    cv2.waitKey(1)

def main():
    rospy.init_node('image_listener', anonymous=True)

    # Replace 'your_image_topic' with the actual topic name
    image_topic = '/midog1/camera/image_raw'

    # Subscribe to the image topic
    rospy.Subscriber(image_topic, Image, image_callback)

    # Spin to keep the script alive
    rospy.spin()

if __name__ == '__main__':
    main()
