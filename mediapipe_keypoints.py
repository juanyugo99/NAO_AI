# Libraries 

import os
import sys
import glob
import cv2
import json
import time
import torch
import json
import numpy as np
import mediapipe as mp
from naonet_utils import import_net, Net
from sklearn.preprocessing import MinMaxScaler, StandardScaler, MaxAbsScaler, RobustScaler
from pickle import dump, load

def transpose(l1, l2):
  # to generate database from frames
  for i in range(len(l1[0])):
    row = []
    for item in l1:
      row.append(item[i])
    l2.append(row)
  return l2

# Joint names in order

names = ['HeadPitch', 'HeadYaw', 'LAnklePitch', 'LAnkleRoll', 'LElbowRoll', 'LElbowYaw', 'LHand', 'LHipPitch', 'LHipRoll', 'LHipYawPitch', 'LKneePitch', 'LShoulderPitch', 'LShoulderRoll', 'LWristYaw', 'RAnklePitch', 'RAnkleRoll', 'RElbowRoll', 'RElbowYaw', 'RHand', 'RHipPitch', 'RHipRoll', 'RHipYawPitch', 'RKneePitch', 'RShoulderPitch', 'RShoulderRoll','RWristYaw']

# utilities from mediapie

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# Network and Scaler Loading 

naonet = import_net("checkpoint.pth", features=99, outputs=26) # netwok
naonet.eval()
x_scaler = load(open('x_scaler.pkl', 'rb'))


if __name__ == '__main__':


  # For static images:
  IMAGE_FILES = [ ]
  print(IMAGE_FILES)
  BG_COLOR = (192, 192, 192) # gray
  keypoints_dict=[]

  with mp_pose.Pose(
      static_image_mode=True,
      model_complexity=2,
      enable_segmentation=True,
      min_detection_confidence=0.5) as pose:

    for idx, file in enumerate(IMAGE_FILES):
      image = cv2.imread(file)
      image_height, image_width, _ = image.shape
      # Convert the BGR image to RGB before processing.
      results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

      if not results.pose_landmarks:
        continue

      annotated_image = image.copy()
      # Draw segmentation on the image.
      # To improve segmentation around boundaries, consider applying a joint
      # bilateral filter to "results.segmentation_mask" with "image".
      condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
      bg_image = np.zeros(image.shape, dtype=np.uint8)
      bg_image[:] = BG_COLOR
      annotated_image = np.where(condition, annotated_image, bg_image)
      # Draw pose landmarks on the image.
      mp_drawing.draw_landmarks(
          annotated_image,
          results.pose_landmarks,
          mp_pose.POSE_CONNECTIONS,
          landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
      cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)
      # Plot pose world landmarks.


      keypoints = results.pose_landmarks.landmark
      keypoints_list = []
      for idlandmarks in mp_pose.PoseLandmark:
          x_landmrk = float(keypoints[idlandmarks].x)
          y_landmrk = float(keypoints[idlandmarks].y)
          z_landmrk = float(keypoints[idlandmarks].z)
          keypoints_list += [x_landmrk, y_landmrk, z_landmrk]

      #keypoints_dict.append({"image_id": str(file).split("\\")[1], "keypoints": keypoints_list})


      cv2.imshow("image", annotated_image)
      cv2.waitKey(0.2)

  with open('json_results.json', 'w') as f:
      json.dump(keypoints_dict, f)

  all_frames = []

  # For webcam input:
  #input = "/home/naoai/JP.mp4"
  input = 0
  cap = cv2.VideoCapture(input)

  frame_count = 0



  with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
      init_time = time.time()
      time.sleep(0.1)
      success, image = cap.read()
      if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue
        #break

      # To improve performance, optionally mark the image as not writeable to
      # pass by reference.
      image.flags.writeable = False
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      results = pose.process(image)

      # Draw the pose annotation on the image.
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      mp_drawing.draw_landmarks(
          image,
          results.pose_landmarks,
          mp_pose.POSE_CONNECTIONS,
          landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
      
      # Flip the image horizontally for a selfie-view display.
      cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
      if cv2.waitKey(5) & 0xFF == 27:
        break
      nao_out = []
      
      try:
        keypoints_list = []
        keypoints = results.pose_landmarks.landmark
        for idlandmarks in mp_pose.PoseLandmark:
            x_landmrk = float(keypoints[idlandmarks].x)
            y_landmrk = float(keypoints[idlandmarks].y)
            z_landmrk = float(keypoints[idlandmarks].z)
            keypoints_list += [x_landmrk, y_landmrk, z_landmrk] 

      except:
        pass

      try: 
      
        x_arr = x_scaler.transform(np.array(keypoints_list).reshape(1,-1))
        prediction = naonet(torch.Tensor(x_arr))
        nao_out = prediction.detach().numpy().tolist()

        times = np.ones((len(nao_out[0]),), dtype=int).tolist()

        #all_frames += [nao_out[0]]

        to_json = {
          "angles": nao_out, 
          "times":  times, 
          "joints": names }
        
        with open('nao_angles.json', 'w') as json_file:
          json.dump(to_json, json_file)

        print("time of execution: ", time.time() - init_time)
      except:
        pass
  

  cap.release()