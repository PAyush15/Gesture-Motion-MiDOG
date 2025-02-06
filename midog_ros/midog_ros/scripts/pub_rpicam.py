import cv2
import numpy as np
import time
import rospy
from sensor_msgs.msg import CompressedImage

def pub_rpicam():
	
	stream = cv2.VideoCapture(0)
	cam_pub = rospy.Publisher('camera/image_raw/compressed', CompressedImage, queue_size=1)
	rospy.init_node('pub_rpicam', anonymous=True)
	rate = rospy.Rate(20)
	
	while not rospy.is_shutdown():
		(grabbed, frame) = stream.read()
		if grabbed:
			cam_msg = CompressedImage()
			cam_msg.header.stamp = rospy.Time.now()
			cam_msg.header.frame_id = rospy.get_param('tf_prefix') + "/camera_link"
			cam_msg.format = "jpeg"
			cam_msg.data = np.array(cv2.imencode('.jpg',frame)[1]).tobytes()
			cam_pub.publish(cam_msg)
		rate.sleep()

if __name__ == '__main__':
	try:
		pub_rpicam()
	except rospy.ROSInterruptException:
		pass
