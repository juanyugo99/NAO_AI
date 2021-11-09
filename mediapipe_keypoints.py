# Libraries 

import os
import sys
import glob
import cv2
import json
import time
import torch
import json
import argparse
import numpy as np
import mediapipe as mp
from pickle import TRUE, dump, load
from naonet_utils import import_net, Net
from sklearn.preprocessing import StandardScaler

parser = argparse.ArgumentParser()

parser.add_argument("-m", "--mode",                   dest = "detection_mode", default = "camera" , help="mode of detection: from camera, video or image")
parser.add_argument("-in_dir", "--input_direction",   dest = "in_dir", default = 0 , help="source of detection: camera, video or image path")
parser.add_argument("-out_dir", "--output_direction", dest = "out_dir", default = "" , help= "destination of detection: path")
parser.add_argument("-sk", "--skip",                  dest = "skipped_frames", default = 10 , help= "frames to skip on video detection")
parser.add_argument("-save_img", "--save_images",     dest = "save_images", default = False , help= "save images")
parser.add_argument("-save_json", "--save_json",      dest = "save_json", default = False , help= "save json")

args = parser.parse_args()


def transpose(l1, l2):
  # to generate database from frames
  for i in range(len(l1[0])):
    row = []
    for item in l1:
      row.append(item[i])
    l2.append(row)
  return l2

# Joint names in order for robot imitation

names = ['HeadPitch', 'HeadYaw', 'LAnklePitch', 'LAnkleRoll', 'LElbowRoll', 'LElbowYaw', 'LHand', 'LHipPitch', 'LHipRoll', 'LHipYawPitch', 'LKneePitch', 'LShoulderPitch', 'LShoulderRoll', 'LWristYaw', 'RAnklePitch', 'RAnkleRoll', 'RElbowRoll', 'RElbowYaw', 'RHand', 'RHipPitch', 'RHipRoll', 'RHipYawPitch', 'RKneePitch', 'RShoulderPitch', 'RShoulderRoll','RWristYaw']

# utilities from mediapie & config

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

detection_mode =  str(args.detection_mode)
video_in =        args.in_dir if detection_mode == "camera" else str(args.in_dir)
skipped_frames =  int(args.skipped_frames)
save_img =        args.save_images
save_json =       args.save_json
out_dir =         str(args.out_dir)

# Network and Scaler Loading 

naonet = import_net("checkpoint_old.pth", features=99, outputs=26) # netwok
naonet.eval()
x_scaler = load(open('x_scaler.pkl', 'rb'))


if __name__ == '__main__':

  # -------------------------------------------------------- IMAGE DETECTION -------------------------------------------------------- #

  if detection_mode == "image":

    IMAGE_FILES = args.in_dir
    BG_COLOR = (192, 192, 192) # gray
    keypoints_dict=[]

    with mp_pose.Pose(
        static_image_mode=True,
        model_complexity=2,
        enable_segmentation=True,
        min_detection_confidence=0.5) as pose:

      for _, file in enumerate([IMAGE_FILES]):

        print("proccesing: ", file)

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

        keypoints = results.pose_landmarks.landmark
        keypoints_list = []
        for idlandmarks in mp_pose.PoseLandmark:
            x_landmrk = float(keypoints[idlandmarks].x)
            y_landmrk = float(keypoints[idlandmarks].y)
            z_landmrk = float(keypoints[idlandmarks].z)
            keypoints_list += [x_landmrk, y_landmrk, z_landmrk]

        x_arr = x_scaler.transform(np.array(keypoints_list).reshape(1,-1))
        prediction = naonet(torch.Tensor(x_arr))
        nao_out = prediction.detach().numpy().tolist()


        keypoints_dict.append({"image_id": str(file), "keypoints": keypoints_list, "prediction": nao_out})

        cv2.imshow("image", annotated_image)
        cv2.waitKey(100)

        if save_img:
          cv2.imwrite(out_dir+"{}.png".format(file), annotated_image)

      if save_json and keypoints_dict:
        with open(out_dir+'json_results.json', 'w') as f:
            json.dump(keypoints_dict, f)


  # -------------------------------------------------------- VIDEO DETECTION -------------------------------------------------------- #


  if detection_mode == ("video" or "camera"):

    cap = cv2.VideoCapture(video_in)

    keypoints_dict=[]

    frame_count = 0

    with mp_pose.Pose( 
      min_detection_confidence=0.5, 
      min_tracking_confidence=0.5) as pose:

      frame_num = 0

      while True:

        init_time = time.time()

        frame_count += 1
        
        success, image = cap.read()

        if not success:
          if save_json and keypoints_dict:
            with open(out_dir+'json_results.json', 'w') as f:
                print("exporting to json")
                json.dump(keypoints_dict, f)
          print("Ignoring empty camera frame.")
          cap.release()
          # If loading a video, use 'break' instead of 'continue'.
          break

        if frame_count % skipped_frames == 0:

          frame_num += 1

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
          cv2.waitkey(1)
          
          if cv2.waitKey(5) & 0xFF == 27:
            if save_json and keypoints_dict:
              with open(out_dir+'json_results.json', 'w') as f:
                  json.dump(keypoints_dict, f)
            break
          
          nao_out = []

          out = False
          
          try:
            keypoints_list = []
            keypoints = results.pose_landmarks.landmark
            for idlandmarks in mp_pose.PoseLandmark:
                x_landmrk = float(keypoints[idlandmarks].x)
                y_landmrk = float(keypoints[idlandmarks].y)
                z_landmrk = float(keypoints[idlandmarks].z)
                keypoints_list += [x_landmrk, y_landmrk, z_landmrk] 
            

            x_arr = x_scaler.transform(np.array(keypoints_list).reshape(1,-1))
            prediction = naonet(torch.Tensor(x_arr))
            nao_out = prediction.detach().numpy().tolist()

            if save_json:
              keypoints_dict.append({"image_id": "image_" + str(frame_count) , "keypoints": keypoints_list, "prediction": nao_out})

            times = np.ones((len(nao_out[0]),), dtype=int).tolist()

            print("detection complete\ntime of execution: ", time.time() - init_time)

            out = True

          except:
            out = False
            pass

          if out:
            to_json = {
              "angles": nao_out, 
              "times":  times, 
              "joints": names,
              "detection": True }
          if not out:
            to_json = {
              "angles": [], 
              "times":  [], 
              "joints": names,
              "detection": False }
            
          with open('nao_angles.json', 'w') as json_file:
            json.dump(to_json, json_file)

          if save_img:
            cv2.imwrite(out_dir + "image_{}.png".format(frame_num), cv2.flip(image, 1))