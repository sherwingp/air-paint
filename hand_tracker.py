import cv2
import mediapipe as mp
import finger_counter as fc

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,100)
fontScale              = 1
fontColor              = (0,0,0)
thickness              = 1
lineType               = 2

# For webcam input:
cap = cv2.VideoCapture(1)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue

    # Convert BGR image to RGB
    image = cv2.flip(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), 1)
    
    # Draw the hand annotations on the image.
    image.flags.writeable = True
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    annotated_image = image.copy()
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            annotated_image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

      annotated_image = fc.get_mode(annotated_image, results)

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', annotated_image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
