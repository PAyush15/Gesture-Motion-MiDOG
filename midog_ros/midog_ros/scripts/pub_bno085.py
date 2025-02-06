import time
import board
import busio
import adafruit_bno08x
from adafruit_bno08x.i2c import BNO08X_I2C
import rospy
from sensor_msgs.msg import Imu

# set up I2C connection to read IMU data
i2c = busio.I2C(board.D23, board.D22)
bno = BNO08X_I2C(i2c)

bno.enable_feature(adafruit_bno08x.BNO_REPORT_GYROSCOPE)
bno.enable_feature(adafruit_bno08x.BNO_REPORT_LINEAR_ACCELERATION)
bno.enable_feature(adafruit_bno08x.BNO_REPORT_ROTATION_VECTOR)

def pub_bno085():
	
	imu_pub = rospy.Publisher('imu/data', Imu, queue_size=10)
	rospy.init_node('pub_bno085', anonymous=True)
	rate = rospy.Rate(50)
	
	while not rospy.is_shutdown():
		
		imu_msg = Imu()
		
		# current timestamp
		imu_msg.header.stamp = rospy.Time.now()
		
		# frame
		imu_msg.header.frame_id = rospy.get_param('tf_prefix') + "/imu_link"
		
		# orientation
		quat_i, quat_j, quat_k, quat_real = bno.quaternion
		imu_msg.orientation.x = quat_i
		imu_msg.orientation.y = quat_j
		imu_msg.orientation.z = quat_k
		imu_msg.orientation.w = quat_real
		
		# angular velocity
		gyro_x, gyro_y, gyro_z = bno.gyro
		imu_msg.angular_velocity.x = gyro_x
		imu_msg.angular_velocity.y = gyro_y
		imu_msg.angular_velocity.z = gyro_z
		
		# linear acceleration
		linear_accel_x, linear_accel_y, linear_accel_z = bno.linear_acceleration
		imu_msg.linear_acceleration.x = linear_accel_x
		imu_msg.linear_acceleration.y = linear_accel_y
		imu_msg.linear_acceleration.z = linear_accel_z
		
		# publish imu message
		imu_pub.publish(imu_msg)
		rate.sleep()

if __name__ == '__main__':
	try:
		pub_bno085()
	except rospy.ROSInterruptException:
		pass
