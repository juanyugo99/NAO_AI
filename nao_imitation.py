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

def traduction(data): 
	trad_data = [
	round(data[1],1),
	round(data[0],1),
	round(data[9],1),
	round(data[8],1),
	round(data[7],1),
	round(data[10],1),
	round(data[2],1),
	round(data[3],1),
	round(data[21],1),
	round(data[20],1),
	round(data[19],1),
	round(data[22],1),
	round(data[14],1),
	round(data[15],1),
	round(data[11],1),
	round(data[12],1),
	round(data[5],1),
	round(data[4],1),
	round(data[13],1),
	round(data[6],1),
	round(data[23],1),
	round(data[24],1),
	round(data[17],1),
	round(data[16],1),
	round(data[25],1),
	round(data[18],1),
	0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]	

	return trad_data

def callback(data):
	global datos
	datos = data.data

def update_keypoints():
	global angles
	try: 	
		print ('reading poses')
		with open('/home/naoai/Documents/MediaPose/nao_angles.json') as f:
			angles = json.load(f)
			angles = angles["angles"][0]
	except Exception, e:
		print(e)

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

	while(True):
		current_posture = posture.getPostureFamily()

		if current_posture == "Standing":
			update_keypoints()
			#tts.say("Hi Jei, I'm going to move")
			motor_speed = 0.3
			motion.angleInterpolationWithSpeed(names, angles, motor_speed)
				#motion.angleInterpolationWithSpeed(JointNames, Pose0, pFractionMaxSpeed)
				#time.sleep(0.5)"""
			
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
