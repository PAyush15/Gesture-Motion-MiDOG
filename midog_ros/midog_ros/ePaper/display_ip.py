#!/usr/bin/python
# -*- coding:utf-8 -*-
import rospy
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

print(picdir)
print(libdir)

import logging
import epd1in54b_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import socket

logging.basicConfig(level=logging.DEBUG)

def display_ip():

    try:
        logging.info("Displaying robot name, IP and ROS master")
        
        epd = epd1in54b_V2.EPD()
        epd.init()
        
        blackimage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        redimage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        drawblack = ImageDraw.Draw(blackimage)
        drawred = ImageDraw.Draw(redimage)
        
        font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 22)
        font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
        
        user = rospy.get_param('tf_prefix')
        ip = ''
        ros_master = ''
        change_display = True
        
        drawblack.text((8, 12), user, font = font, fill = 0)
        drawblack.text((8, 80), "ROS master:", font = font, fill = 0)
        
        rospy.init_node('display_ip', anonymous=True)
        rate = rospy.Rate(0.2)
        
        while not rospy.is_shutdown():
            
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            m = os.environ.get("ROS_MASTER_URI")
            if (ip != s.getsockname()[0]):
                ip = s.getsockname()[0]
                logging.info(ip)
                drawblack.text((8, 40), 'IP: ' + s.getsockname()[0], font = font, fill = 0)
                change_display = True
                
            if (ros_master != m):
                ros_master = m
                drawblack.text((8, 108), ros_master[7:-6], font = font, fill = 0)
                change_display = True
                
            if change_display:
                epd.display(epd.getbuffer(blackimage),epd.getbuffer(redimage))
                change_display = False
                
            s.close()
            rate.sleep()
            
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        
        logging.info("Clear...")
        epd.Clear()
        
        logging.info("Goto Sleep...")
        epd.sleep()
        epd1in54b_V2.epdconfig.module_exit()
        exit()

if __name__ == '__main__':
	try:
		display_ip()
	except rospy.ROSInterruptException:
		pass
