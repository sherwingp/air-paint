# Air Paint

A Python program that lets you draw on your webcam feed in different colours with your finger!

![ezgif com-gif-maker (1)](https://user-images.githubusercontent.com/67482908/156860062-4950b57e-d8dd-49f8-946c-2f2ce05aff81.gif)

## Features:
- Painting on webcam feed with fingers
- Change between paint, select and no mode by lifting the index, index and middle fingers, or no fingers 
- Select different colours by hovering over colour palette

## Todo:
- Add eraser

## Technologies used:
Python, Mediapipe, OpenCV, Tkinter

# Approach
- Uses Mediapipe's machine learning pipeline to perform hand and finger tracking
- Differentiates between modes by checking whether only the index finger is up or multiple, this is done by comparing the y-coordinates of the fingertip and knuckle of each finger
- The OpenCV frames are processed into Tkinter for a better UX and lines are drawn between the last finger position and the current in order to achieve smooth drawing
- When the user is in select mode, hovering over the colour palette takes the x-coordinate of the fingertip and the colour palette's y-coordinate to get the pixel of the desired colour, gets the colour from the pixel and changes the currently selected paint colour  

## How to Use

1. From the command line, clone this repository to your machine:

```
git clone https://github.com/sherwingp/air-paint.git
cd air-paint
```

2. Install dependencies:
```
pip install opencv-python
pip install mediapipe
```

3. Run
```
python paint.py
```
If there is no webcam feed:

Change the number in `self.cap = cv2.VideoCapture(1)` to `self.cap = cv2.VideoCapture(0)`
