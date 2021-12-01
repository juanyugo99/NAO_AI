#!/usr/bin/env python
import rospy
import sys
import motion
import time
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
from std_msgs.msg import String
from std_msgs.msg import Float32MultiArray
from naoqi import ALProxy
import json

# angles = []
old_angles = []

def callback(data):
	global datos
	datos = data.data

def update_keypoints():
	global angles
	try: 	
		print ('reading poses')
		with open('nao_angles.json') as f:
			angles = json.load(f)
			angles = angles["angles"][0]
		# print(angles)
	except Exception, e:
		print(e)

def comp_angles(angles, old_angles):
	grad = 0.069
	if ((old_angles[0] + grad >= angles[0]) and (old_angles[0] - grad <= angles[0])):	
		angles = old_angles

	if (old_angles[1] + grad >= angles[1] and old_angles[1] - grad <= angles[1]):	
		angles = old_angles

	if (old_angles[2] + grad >= angles[2] and old_angles[2] - grad <= angles[2]):	
		angles = old_angles

	if (old_angles[3] + grad >= angles[3] and old_angles[3] - grad <= angles[3]):	
		angles = old_angles

	if (old_angles[4] + grad >= angles[4] and old_angles[4] - grad <= angles[4]):	
		angles = old_angles

	if (old_angles[5] + grad >= angles[5] and old_angles[5] - grad <= angles[5]):	
		angles = old_angles

	if (old_angles[6] + grad >= angles[6] and old_angles[6] - grad <= angles[6]):	
		angles = old_angles

	if (old_angles[7] + grad >= angles[7] and old_angles[7] - grad <= angles[7]):	
		angles = old_angles

	if (old_angles[8] + grad >= angles[8] and old_angles[8] - grad <= angles[8]):	
		angles = old_angles

	if (old_angles[9] + grad >= angles[9] and old_angles[9] - grad <= angles[9]):	
		angles = old_angles

	if (old_angles[10] + grad >= angles[10] and old_angles[10] - grad <= angles[10]):	
		angles = old_angles

	if (old_angles[11] + grad >= angles[11] and old_angles[11] - grad <= angles[11]):	
		angles = old_angles

	if (old_angles[12] + grad >= angles[12] and old_angles[12] - grad <= angles[12]):	
		angles = old_angles

	if (old_angles[13] + grad >= angles[13] and old_angles[13] - grad <= angles[13]):	
		angles = old_angles

	if (old_angles[14] + grad >= angles[14] and old_angles[14] - grad <= angles[14]):	
		angles = old_angles

	if (old_angles[15] + grad >= angles[15] and old_angles[15] - grad <= angles[15]):	
		angles = old_angles

	if (old_angles[16] + grad >= angles[16] and old_angles[16] - grad <= angles[16]):	
		angles = old_angles

	if (old_angles[17] + grad >= angles[17] and old_angles[17] - grad <= angles[17]):	
		angles = old_angles

	if (old_angles[18] + grad >= angles[18] and old_angles[18] - grad <= angles[18]):	
		angles = old_angles

	if (old_angles[19] + grad >= angles[19] and old_angles[19] - grad <= angles[19]):	
		angles = old_angles

	if (old_angles[20] + grad >= angles[20] and old_angles[20] - grad <= angles[20]):	
		angles = old_angles

	if (old_angles[21] + grad >= angles[21] and old_angles[21] - grad <= angles[21]):	
		angles = old_angles

	if (old_angles[22] + grad >= angles[22] and old_angles[22] - grad <= angles[22]):	
		angles = old_angles

	if (old_angles[23] + grad >= angles[23] and old_angles[23] - grad <= angles[23]):	
		angles = old_angles

	if (old_angles[24] + grad >= angles[24] and old_angles[24] - grad <= angles[24]):	
		angles = old_angles

	if (old_angles[25] + grad >= angles[25] and old_angles[25] - grad <= angles[25]):	
		angles = old_angles


def update_init_position(new_value):
	return  new_value

def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

def main(nao_ip):

	try:
		motion = ALProxy("ALMotion", nao_ip, 9559)
		posture = ALProxy("ALRobotPosture", nao_ip, 9559)
		tts = ALProxy("ALTextToSpeech", nao_ip, 9559)
	except Exception, e:
		print(e)

	names = list()
	names = list()

	names.append("HeadPitch")
	names.append("HeadYaw")
	names.append("LAnklePitch")
	names.append("LAnkleRoll")
	names.append("LElbowRoll")
	names.append("LElbowYaw")
	names.append("LHand")
	names.append("LHipPitch")
	names.append("LHipRoll")
	names.append("LHipYawPitch")
	names.append("LKneePitch")
	names.append("LShoulderPitch")
	names.append("LShoulderRoll")
	names.append("LWristYaw")
	names.append("RAnklePitch")
	names.append("RAnkleRoll")
	names.append("RElbowRoll")
	names.append("RElbowYaw")
	names.append("RHand")
	names.append("RHipPitch")
	names.append("RHipRoll")
	names.append("RHipYawPitch")
	names.append("RKneePitch")
	names.append("RShoulderPitch")
	names.append("RShoulderRoll")
	names.append("RWristYaw")

	StiffnessOn(motion)
	tts.say("connection ready")

	posture.goToPosture("Stand", 1.0)

	entro = 1
	while(True):

		current_posture = posture.getPostureFamily()
		update_keypoints()
		if current_posture == "Standing":
			if entro == 1: 
				entro = 0
				print ("entro aki gg")
				old_angles = [-0.151908,
					  0.0137641,
					  0.095066,
					  -0.128814,
					  -0.391128,
					  -1.17662,
					  0.2896,
					  0.135034,
					  0.0966839,
					  -0.164096,
					  -0.0859461,
					  1.50635,
					  -0.01845,
					  0.033706,
					  0.0874801,
					  0.130432,
					  0.398881,
					  1.19955,
					  0.2944,
					  0.133416,
					  -0.0966001,
					  -0.164096,
					  -0.0843279,
					  1.50643,
					  0.0643861,
					  0.0720561]

				# print(angles)
				# print(old_angles)


			comp_angles(angles, old_angles)
			#tts.say("Hi, I'm going to move")
			try:
				motor_speed = 0.2
				motion.angleInterpolationWithSpeed(names, angles, motor_speed)
				#motion.angleInterpolationWithSpeed(JointNames, Pose0, pFractionMaxSpeed)
				#time.sleep(0.5)"""
				old_angles = angles 
			except Exception, e: 
				print(e)

		if current_posture != "Standing" :
			StiffnessOn(motion)
			tts.say("Give me one moment please")
			tts.post.say("This make take a while")
			posture.goToPosture("Stand", 1.0)
			motion.setWalkArmsEnabled(True, True)
			motion.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
			# Activate Whole Body Balancer.
			isEnabled = True
			motion.wbEnable(isEnabled)

			# Legs are constrained in a plane
			stateName = "Plane"
			supportLeg = "Legs"
			motion.wbFootState(stateName, supportLeg)
			tts.say("I'm ready again")




if __name__ == '__main__':
	
	nao_ip = "192.168.1.101"

	if len(sys.argv) <= 1:
		print "Usage python motion_walk.py robotIP (optional default: 127.0.0.1)"
	else:
		nao_ip = sys.argv[1]

	main(nao_ip)
