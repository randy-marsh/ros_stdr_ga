#!/usr/bin/env python

import rospy
import math

from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Pose2D
from sensor_msgs.msg import Range
from nav_msgs.msg import Odometry

from ros_stdr_ga.srv import *

from subprocess import call

# Parameters, do not touch it
N_SONAR = 4 # Number of sonars in the robot

LINEAR_MUL = 2 # Used to denormalize ANN output
ANGULAR_MUL = 2

ranges = [0] * N_SONAR
odom = [None] * 2
initX = 10
initY = 1.5

ann = None
distance = 0 

def callbackSonar(msg, arg):
	#rospy.loginfo("%f: [%f]"%(arg, msg.range))
	if msg.range == float("inf"):
		msg.range = msg.max_range

	ranges[arg] = msg.max_range / msg.range # Normalize ranges, needed to feed the ANN

def callbackOdom(msg):
	global distance
	global odom

	if (odom[0] is None): # Init odometry to properly compute distance
		odom[0] = msg.pose.pose.position.x
		odom[1] = msg.pose.pose.position.y
		
	distance = distance + math.sqrt(math.pow((odom[0]-msg.pose.pose.position.x),2) + math.pow((odom[1]-msg.pose.pose.position.y),2))
	odom[0] = msg.pose.pose.position.x
	odom[1] = msg.pose.pose.position.y
	#print ("Distance: " + str(distance))

def initANN():
	global ann

	rospy.loginfo("Building network")
	# ANN with  N_SONAR inputs and
	# two outputs for linear and angular velocities
	
	# TODO: Initialize network topology. Use the global variable ann to refer the network
	# The ANN *must* define N_SONAR input neurons and two output neurons

	rospy.loginfo("You must initialize your ANN, it will crash otherwise") # Your can remove this line safely

def controlLoop(weights):
	global ann
	global distance

	vel = Twist()
	iterations = 0

	# TODO: Set ANN weights with the array weights

	rate = rospy.Rate(10)
	while (not rospy.is_shutdown()) and iterations < 30: # 30 iterations seems enougth
		# TODO: Feed the ANN with global variable ranges and store its output as an array of two floats
		out = None

		# Move the robot according to the ANN output
		vel.linear.x = out[0] * LINEAR_MUL
		vel.angular.z = out[1] * ANGULAR_MUL
		velTopic.publish(vel)
		iterations = iterations + 1
		rate.sleep()

	# Stop robot motion
	vel.linear.x = 0
	vel.angular.z = 0
	velTopic.publish(vel)

	# Compute fitness
	fit = distance + math.sqrt(math.pow(odom[0]-initX, 2) + math.pow(odom[1]-initY,2))
	rospy.loginfo("Fitness: " + str(fit))
	return(fit)

def handle_computeFitness(req):
	# Stop robot motion
	# (Needed because of previous runs)
	vel = Twist()
	vel.linear.x = 0
	vel.angular.z = 0
	velTopic.publish(vel)

	# Reset distance
	global distance
	distance = 0

	rospy.loginfo("Init neurocontrol")
	weights = []
	for i in req.ann: weights.append(i)
	rospy.loginfo(weights)
	# Reset simulation
	try:
		call(["rosservice", "call", "/robot0/replace", "[10,1.5,0]"]) # I know, nasty code, fix it 
		fitness = controlLoop(weights)
	except rospy.ServiceException:
		print "Service call failed"

	return fitness

if __name__ == '__main__':
	global ann
	rospy.init_node('neurocontroller')
	
	# Stop robot motion
	# (Needed because of previous runs)
	velTopic = rospy.Publisher("/robot0/cmd_vel", Twist, queue_size=10)
	vel = Twist()
	vel.linear.x = 0
	vel.angular.z = 0
	velTopic.publish(vel)

	initANN()

	for i in range(N_SONAR):
		rospy.Subscriber("/robot0/sonar_"+str(i), Range, callbackSonar, i)

	rospy.Subscriber("/robot0/odom", Odometry, callbackOdom)

	rospy.Service('computeFitness', computeFitness, handle_computeFitness)
	rospy.loginfo("Waiting")
	rospy.spin()


