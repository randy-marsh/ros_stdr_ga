#!/usr/bin/env python

import rospy
import numpy

from geometry_msgs.msg import Twist

def controlLoop():
	rate = rospy.Rate(10)

	while not rospy.is_shutdown():
		vel.linear.x = 1
		vel.angular.z = 0
		velTopic.publish(vel)
		rate.sleep()

if __name__ == '__main__':
	rospy.init_node('controller')
	velTopic = rospy.Publisher("/robot0/cmd_vel", Twist, queue_size=10)
	vel = Twist()

	try:
		controlLoop()
	except rospy.ROSInterruptException:
		pass
