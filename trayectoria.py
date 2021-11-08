#!/usr/bin/env python
import rospy
import os
import numpy
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
from std_msgs.msg import String
from std_msgs.msg import Float32MultiArray
import json 

node = os.popen("rosnode kill /joint_state_publisher").readlines()

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
			angles = traduction(angles["angles"][0])
		print(angles)
		return angles

	except Exception, e:
		print(e)
	

def update_init_position(new_value):
	return  new_value

def talker():

	global init_position
	init_position = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 2.0, 0.0, -1.8, 0.0, 2.0, 0.0, -2.0, 0.0, 1.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


	pub = rospy.Publisher('/joint_states', JointState, queue_size=10)
	rospy.init_node('Coronao', anonymous=False)
	rate = rospy.Rate(10)
	
	

	while not rospy.is_shutdown():

		update_keypoints()

		print ("starting movement")
		Joints = JointState()
		Joints.header = Header()
		Joints.header.stamp = rospy.Time.now()
		Joints.name = ['HeadYaw', 'HeadPitch', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll',
	  	'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'LShoulderPitch',
	  	'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll',
	  	'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand', 'RFinger23', 'RFinger13', 'RFinger12', 'LFinger21',
	  	'LFinger13', 'LFinger11', 'RFinger22', 'LFinger22', 'RFinger21', 'LFinger12', 'RFinger11', 'LFinger23',
	  	'LThumb1', 'RThumb1', 'RThumb2', 'LThumb2']		
		Joints.position = init_position
		Joints.velocity = []
		Joints.effort = []
		pub.publish(Joints)
		
		HeadYawVar = round(Joints.position[0],2)
		HeadPitchVar = round(Joints.position[1],2)
		LHipYawPitchVar = round(Joints.position[2],2)
		LHipRollVar= round(Joints.position[3],2)
		LHipPitchVar = round(Joints.position[4],2)
		LKneePitchVar = round(Joints.position[5],2)
		LAnklePitchVar = round(Joints.position[6],2)
		LAnkleRollVar = round(Joints.position[7],2)
		RHipYawPitchVar = round(Joints.position[8],2)
		RHipRollVar= round(Joints.position[9],2)
		RHipPitchVar = round(Joints.position[10],2)
		RKneePitchVar = round(Joints.position[11],2)
		RAnklePitchVar = round(Joints.position[12],2)
		RAnkleRollVar = round(Joints.position[13],2)
		LShoulderRollVar = round(Joints.position[15],2)
		RShoulderRollVar = round(Joints.position[21],2)
		LShoulderPitchVar = round(Joints.position[14],2)
		RShoulderPitchVar = round(Joints.position[20],2)
		LElbowYawVar = round(Joints.position[16],2)
		RElbowYawVar = round(Joints.position[22],2)
		LElbowRollVar = round(Joints.position[17],2)
		RElbowRollVar = round(Joints.position[23],2)
		LWristYawVar = round(Joints.position[18],2)
		RWristYawVar = round(Joints.position[24],2)
		LHandVar = round(Joints.position[19],2)
		RHandVar = round(Joints.position[25],2)

		HY = 0
		HP = 0
		LHYP = 0
		LHR = 0
		LHP = 0
		LKP = 0
		LAP = 0
		LAR = 0
		RHYP = 0
		RHR = 0
		RHP = 0
		RKP = 0
		RAP = 0
		RAR = 0
		LSR = 0
		RSR = 0
		LSP = 0
		RSP = 0
		LEY = 0
		REY = 0
		LER = 0
		RER = 0
		LWY = 0
		RWY = 0
		LH = 0
		RH = 0

		"""while((round(HeadYawVar,2) != round(angles[0],2) and HY == 0) or (round(HeadPitchVar,2) != round(angles[1],2) and HP == 0) or (round(LHipYawPitchVar,2) != round(angles[2],2) and LHYP == 0) or (round(LHipRollVar,2) != round(angles[3],2) and LHR == 0) or (round(LHipPitchVar,2) != round(angles[4],2) and LHP == 0) or (round(LKneePitchVar,2) != round(angles[5],2) and LKP == 0) or (round(LAnklePitchVar,2) != round(angles[6],2) and LKP == 0)or (round(LAnkleRollVar,2) != round(angles[7],2) and LAP == 0) or (round(RHipYawPitchVar,2) != round(angles[8],2) and RHYP == 0)  or (round(RHipRollVar,2) != round(angles[9],2) and RHR == 0) or (round(RHipPitchVar,2) != round(angles[10],2) and RHP == 0) or (round(RKneePitchVar,2) != round(angles[11],2) and RKP == 0) or (round(RAnklePitchVar,2) != round(angles[12],2) and RKP == 0)or (round(RAnkleRollVar,2) != round(angles[13],2) and RAP == 0) or (round(LShoulderRollVar,2) != round(angles[15],2) and LSR == 0) or (round(RShoulderRollVar,2) != round(angles[21],2) and RSR == 0) or (round(LShoulderPitchVar,2) != round(angles[14],2) and LSP == 0) or (round(RShoulderPitchVar,2) != round(angles[20],2) and RSP == 0) or (round(LElbowYawVar,2) != round(angles[16],2) and LEY == 0) or (round(RElbowYawVar,2) != round(angles[22],2) and REY == 0) or (round(LElbowRollVar,2) != round(angles[17],2) and LER == 0) or (round(RElbowRollVar,2) != round(angles[23],2) and RER == 0) or (round(LWristYawVar,2) != round(angles[18],2) and LWY == 0) or (round(RWristYawVar,2) != round(angles[24],2) and RWY == 0) or (round(LHandVar,2) != round(angles[19],2) and LH == 0)  or (round(RHandVar,2) != round(angles[25],2) and RH == 0)) :			
			print("starting interpolation")

			if (angles[0] >= -2.0 and angles[0] <=2.0):		# HeadYaw
				if HeadYawVar > round(angles[0],2) :
					HeadYawVar = round(HeadYawVar - 0.1 ,2)
				if HeadYawVar < round(angles[0],2) :
					HeadYawVar = round(HeadYawVar + 0.1 ,2)
			else :
				print("Error HeadYaw")
				HY = 1

			if (round(angles[1],2) >= -0.6 and angles[1] <=0.5):		# HeadPitch
				if HeadPitchVar > round(angles[1],2) :
					HeadPitchVar = round(HeadPitchVar - 0.1 ,2)
				if HeadPitchVar < round(angles[1],2) :
					HeadPitchVar = round(HeadPitchVar + 0.1 ,2)
			else :
				print("Error HeadPitch")
				HP = 1

			if (round(angles[2],2) >= -1.1 and angles[2] <=0.7):		# LHipYawPitch
				if LHipYawPitchVar > round(angles[2],2) :
					LHipYawPitchVar = round(LHipYawPitchVar - 0.1 ,2)
				if LHipYawPitchVar < round(angles[2],2) :
					LHipYawPitchVar = round(LHipYawPitchVar + 0.1 ,2)
			else :
				print("Error LHipYawPitch")
				LHYP = 1

			if (round(angles[3],2) >= -0.3 and angles[3] <=0.7):		# LHipRollVar
				if LHipRollVar > round(angles[3],2) :
					LHipRollVar = round(LHipRollVar - 0.1 ,2)
				if LHipRollVar < round(angles[3],2) :
					LHipRollVar = round(LHipRollVar + 0.1 ,2)
			else :
				print("Error LHipRoll")
				LHR = 1

			if (round(angles[4],2) >= -1.5 and round(angles[4],2) <=0.4):		# LHipPitch
				if LHipPitchVar > round(angles[4],2) :
					LHipPitchVar = round(LHipPitchVar - 0.1 ,2)
				if LHipPitchVar < round(angles[4],2) :
					LHipPitchVar = round(LHipPitchVar + 0.1 ,2)
			else :
				print("Error LHipPitch")
				LHP = 1

			if (round(angles[5],2) >= 0.0 and round(angles[5],2) <=2.1):		# LKneePitch
				if LKneePitchVar > round(angles[5],2) :
					LKneePitchVar = round(LKneePitchVar - 0.1 ,2)
				if LKneePitchVar < round(angles[5],2) :
					LKneePitchVar = round(LKneePitchVar + 0.1 ,2)
			else :
				print("Error LKneePitch")
				LKP = 1

			if (round(angles[6],2) >= -1.1 and round(angles[6],2) <=0.9):		# LAnklePitch
				if LAnklePitchVar > round(angles[6],2) :
					LAnklePitchVar = round(LAnklePitchVar - 0.1 ,2)
				if LAnklePitchVar < round(angles[6],2) :
					LAnklePitchVar = round(LAnklePitchVar + 0.1 ,2)
			else :
				print("Error LAnklePitch")
				LAP = 1

			if (round(angles[7],2) >= -0.3 and round(angles[7],2) <=0.7):		# LAnkleRoll
				if LAnkleRollVar > round(angles[7],2) :
					LAnkleRollVar = round(LAnkleRollVar - 0.1 ,2)
				if LAnkleRollVar < round(angles[7],2) :
					LAnkleRollVar = round(LAnkleRollVar + 0.1 ,2)
			else :
				print("Error LAnkleRoll")
				LAR = 1

			if (round(angles[8],2) >= -1.1 and angles[8] <=0.7):		# RHipYawPitch
				if RHipYawPitchVar > round(angles[8],2) :
					RHipYawPitchVar = round(RHipYawPitchVar - 0.1 ,2)
				if RHipYawPitchVar < round(angles[8],2) :
					RHipYawPitchVar = round(RHipYawPitchVar + 0.1 ,2)
			else :
				print("Error HeadPitch")
				RHYP = 1

			if (round(angles[9],2) >= -0.7 and angles[9] <=0.3):		# RHipRollVar
				if RHipRollVar > round(angles[9],2) :
					RHipRollVar = round(RHipRollVar - 0.1 ,2)
				if RHipRollVar < round(angles[9],2) :
					RHipRollVar = round(RHipRollVar + 0.1 ,2)
			else :
				print("Error RHipRoll")
				RHR = 1

			if (round(angles[10],2) >= -1.5 and round(angles[10],2) <=0.4):		# RHipPitch
				if RHipPitchVar > round(angles[10],2) :
					RHipPitchVar = round(RHipPitchVar - 0.1 ,2)
				if RHipPitchVar < round(angles[10],2) :
					RHipPitchVar = round(RHipPitchVar + 0.1 ,2)
			else :
				print("Error RHipPitch")
				RHP = 1

			if (round(angles[11],2) >= -0.1 and round(angles[11],2) <=2.1):		# RKneePitch
				if RKneePitchVar > round(angles[11],2) :
					RKneePitchVar = round(RKneePitchVar - 0.1 ,2)
				if RKneePitchVar < round(angles[11],2) :
					RKneePitchVar = round(RKneePitchVar + 0.1 ,2)
			else :
				print("Error RKneePitch")
				RKP = 1

			if (round(angles[12],2) >= -1.1 and round(angles[12],2) <=0.9):		# RAnklePitch
				if RAnklePitchVar > round(angles[12],2) :
					RAnklePitchVar = round(RAnklePitchVar - 0.1 ,2)
				if RAnklePitchVar < round(angles[12],2) :
					RAnklePitchVar = round(RAnklePitchVar + 0.1 ,2)
			else :
				print("Error RAnklePitch")
				RAP = 1

			if (round(angles[13],2) >= -0.7 and round(angles[13],2) <=0.3):		# RAnkleRoll
				if RAnkleRollVar > round(angles[13],2) :
					RAnkleRollVar = round(RAnkleRollVar - 0.1 ,2)
				if RAnkleRollVar < round(angles[13],2) :
					RAnkleRollVar = round(RAnkleRollVar + 0.1 ,2)
			else :
				print("Error RAnkleRoll")
				RAR = 1

			if (angles[15] >= -0.3 and angles[15] <=1.3):		# LShoulderRoll
				if LShoulderRollVar > round(angles[15],2) :
					LShoulderRollVar = round(LShoulderRollVar - 0.1 ,2)
				if LShoulderRollVar < round(angles[15],2) :
					LShoulderRollVar = round(LShoulderRollVar + 0.1 ,2)
			else :
				print("Error LShoulderRoll")
				LSR = 1
			if (angles[21] >= -1.3 and angles[21] <=0.3):	# RShoulderRoll	
				if RShoulderRollVar > round(angles[21],2) :
					RShoulderRollVar = round(RShoulderRollVar - 0.1 ,2)
				if RShoulderRollVar < round(angles[21],2) :
					RShoulderRollVar = round(RShoulderRollVar + 0.1 ,2)
			else :
				print("Error RShoulderRoll")
				RSR = 1
			if (angles[14] >= -2.0 and angles[14] <=2.0):		# LShoulderPitch
				if LShoulderPitchVar > round(angles[14],2) :
					LShoulderPitchVar = round(LShoulderPitchVar - 0.1 , 2)
				if LShoulderPitchVar < round(angles[14],2) :
					LShoulderPitchVar = round(LShoulderPitchVar + 0.1 , 2)
			else :
				print("Error LShoulderPitch")
				LSP = 1
			if (angles[20] >= -2.0 and angles[20] <=2.0):		# RShoulderPitch
				if RShoulderPitchVar > round(angles[20],2) :
					RShoulderPitchVar = round(RShoulderPitchVar - 0.1 , 2)
				if RShoulderPitchVar < round(angles[20],2) :
					RShoulderPitchVar = round(RShoulderPitchVar + 0.1 ,2)
			else :
				print("Error RShoulderPitch")
				RSP = 1
			if (angles[16] >= -2.0 and angles[16] <=2.0):		# LElbowYaw
				if LElbowYawVar > round(angles[16],2) :
					LElbowYawVar = round(LElbowYawVar - 0.1 ,2)
				if LElbowYawVar < round(angles[16],2) :
					LElbowYawVar = round(LElbowYawVar + 0.1 ,2)
			else :
				print("Error LElbowYaw")
				LEY = 1
			if (angles[22] >= -2.0 and angles[22] <=2.0):		# RElbowYaw
				if RElbowYawVar > round(angles[22],2) :
					RElbowYawVar = round(RElbowYawVar - 0.1 ,2)
				if RElbowYawVar < round(angles[22],2) :
					RElbowYawVar = round(RElbowYawVar + 0.1 ,2)
			else :
				print("Error RElbowYaw")
				REY = 1

			if (angles[17] >= -1.5 and angles[17] <=0.0):		# LElbowRoll
				if LElbowRollVar > round(angles[17],2) :
					LElbowRollVar = round(LElbowRollVar - 0.1 ,2)
				if LElbowRollVar < round(angles[17],2) :
					LElbowRollVar = round(LElbowRollVar + 0.1 ,2)
			else :
				print("Error LElbowRoll")
				LER = 1
			if (angles[23] >= 0.0 and angles[23] <=1.5):		# RElbowRoll
				if RElbowRollVar > round(angles[23],2) :
					RElbowRollVar = round(RElbowRollVar - 0.1 ,2)
				if RElbowRollVar < round(angles[23],2) :
					RElbowRollVar = round(RElbowRollVar + 0.1 ,2)
			else :
				print("Error RElbowRoll")
				RER = 1

			if (angles[18] >= -1.8 and angles[18] <=1.8):		# LWristYaw	
				if LWristYawVar > round(angles[18],2) :
					LWristYawVar = round(LWristYawVar - 0.1 ,2)
				if LWristYawVar < round(angles[18],2) :
					LWristYawVar = round(LWristYawVar + 0.1 ,2)
			else :
				print("Error LWristYaw")
				LWY = 1

			if (angles[24] >= -1.8 and angles[24] <=1.8):		# RWristYaw
				if RWristYawVar > round(angles[24],2) :
					RWristYawVar = round(RWristYawVar - 0.1 ,2)
				if RWristYawVar < round(angles[24],2) :
					RWristYawVar = round(RWristYawVar + 0.1 ,2)
			else :
				print("Error RWristYaw")
				RWY = 1

			if (angles[19] >= 0.0 and angles[19] <=1.0):		#LHand
				if LHandVar > round(angles[19],2) :
					LHandVar = round(LHandVar - 0.1 ,2)
				if LHandVar < round(angles[19],2) :
					LHandVar = round(LHandVar + 0.1 ,2)
			else:
				print("Error LHand")
				LH = 1

			if (angles[25] >= 0.0 and angles[25] <=1.0):		#RHand
				if RHandVar > round(angles[25],2) :
					RHandVar = round(RHandVar - 0.1 ,2)
				if RHandVar < round(angles[25],2) :
					RHandVar = round(RHandVar + 0.1 ,2)
			else:
				print("Error RHand")
				RH = 1	

			print("publishing angles")
	 	  	interpolated_position = JointState()
	   		interpolated_position.header = Header()
			interpolated_position.header.stamp = rospy.Time.now()
			interpolated_position.name = ['HeadYaw', 'HeadPitch', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll',
							'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'LShoulderPitch',
							'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll',
							'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand', 'RFinger23', 'RFinger13', 'RFinger12', 'LFinger21',
							'LFinger13', 'LFinger11', 'RFinger22', 'LFinger22', 'RFinger21', 'LFinger12', 'RFinger11', 'LFinger23',
							'LThumb1', 'RThumb1', 'RThumb2', 'LThumb2']
			interpolated_position.position = [HeadYawVar, HeadPitchVar, LHipYawPitchVar, LHipRollVar, LHipPitchVar, LKneePitchVar, LAnklePitchVar, LAnkleRollVar, RHipYawPitchVar,  RHipRollVar, RHipPitchVar, RKneePitchVar, RAnklePitchVar, RAnkleRollVar, LShoulderPitchVar, LShoulderRollVar, LElbowYawVar, LElbowRollVar, LWristYawVar, LHandVar, RShoulderPitchVar, RShoulderRollVar, RElbowYawVar, RElbowRollVar, RWristYawVar, RHandVar, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
			interpolated_position.velocity = []
			interpolated_position.effort = []
			pub.publish(interpolated_position)
			rate.sleep()"""

		print("movement finished")
		init_position = update_init_position(angles)

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass





