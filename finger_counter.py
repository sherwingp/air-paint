import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands

def get_mode(image, results):
    # Get the height and width of the input image.
    height, width, _ = image.shape
    
    # Create a copy of the input image to write the count of fingers on.
    output_image = image.copy()
    
    # Initialize a dictionary to store the count of fingers of both hands.
    count = {'RIGHT': 0, 'LEFT': 0}
    
    # Store the indexes of the tips landmarks of each finger of a hand in a list.
    fingers_tips_ids = [mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                        mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP]
    
    # Initialize a dictionary to store the status (i.e., True for open and False for close) of each finger of both hands.
    fingers_statuses = {'RIGHT_INDEX': False, 'RIGHT_MIDDLE': False, 'RIGHT_RING': False,
                        'RIGHT_PINKY': False, 'LEFT_INDEX': False, 'LEFT_MIDDLE': False,
                        'LEFT_RING': False, 'LEFT_PINKY': False}
    
    # Iterate over the found hands in the image.
    for hand_index, hand_info in enumerate(results.multi_handedness):
        
        # Retrieve the label of the found hand.
        hand_label = hand_info.classification[0].label
        
        # Retrieve the landmarks of the found hand.
        hand_landmarks =  results.multi_hand_landmarks[hand_index]

        # Track paint cursor position
        cursor_pos = [hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width, hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height]

        # Iterate over the indexes of the tips landmarks of each finger of the hand.
        for tip_index in fingers_tips_ids:
            
            # Retrieve the label (i.e., index, middle, etc.) of the finger on which we are iterating upon.
            finger_name = tip_index.name.split("_")[0]
            
            # Check if the finger is up by comparing the y-coordinates of the tip and pip landmarks.
            if (hand_landmarks.landmark[tip_index].y < hand_landmarks.landmark[tip_index - 2].y):
                
                # Update the status of the finger in the dictionary to true.
                fingers_statuses[hand_label.upper()+"_"+finger_name] = True
                
                # Increment the count of the fingers up of the hand by 1.
                count[hand_label.upper()] += 1

    # Write the mode   
    fs = fingers_statuses
    mode = 'None'
    if (fs['RIGHT_INDEX'] == True or fs['LEFT_INDEX'] == True) and count['RIGHT'] + count['LEFT'] == 1:
        mode = 'Paint'
    elif (fs['RIGHT_INDEX'] == True or fs['LEFT_INDEX'] == True) and (fs['RIGHT_MIDDLE'] == True or fs['LEFT_MIDDLE'] == True) and count['RIGHT'] + count['LEFT'] == 2:
        mode = 'Select'
    cv2.putText(output_image, f"Mode: {mode}", (10, 25),cv2.FONT_HERSHEY_COMPLEX, 1, (20,255,155), 2)

    # Return the output image and the index finger position
    return output_image, cursor_pos, mode