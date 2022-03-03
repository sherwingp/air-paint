import cv2
import mediapipe as mp
import finger_counter as fc

class MyVideoCapture:
  def __init__(self, video_source=1):
    # Open video source
    self.cap = cv2.VideoCapture(1)
    self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

  def get_frame(self):
    if self.cap.isOpened():
        ret, frame = self.cap.read()
        if ret:
            # Return a boolean success flag and the current frame converted to BGR
            return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        else:
            return (ret, None)
    else:
        return (ret, None)

  def track_hands(self, image):
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands
    cursor_pos = None
    mode = None

    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

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

          annotated_image, cursor_pos, mode = fc.get_mode(annotated_image, results)
      
    return annotated_image, cursor_pos, mode

  def __del__(self):
    if self.cap.isOpened():
      self.cap.release()
      cv2.destroyAllWindows()