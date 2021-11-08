import cv2
import numpy as np
import mediapide

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# For static images:
  IMAGE_FILES = [ ]
  print(IMAGE_FILES)
  BG_COLOR = (192, 192, 192) # gray
  keypoints_dict=[]

def mediapipe_images(IMAGE_FILES):

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
