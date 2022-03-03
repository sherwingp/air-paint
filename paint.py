from tkinter import *
from PIL import Image, ImageTk
from hand_tracker import MyVideoCapture
import cv2

class PaintApp:
    def __init__(self, window, window_title, video_source=1):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source    
        self.vid = MyVideoCapture()

        self.canvas = Canvas(self.window, width=self.vid.width, height = self.vid.height)

        self.canvas.pack()

        self.delay = 15
        self.update()
        self.window.mainloop()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        # Add hand tracking
        frame = self.vid.track_hands(cv2.flip(frame, 1))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        if ret:
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = NW)

        self.window.after(self.delay, self.update)

    def draw(image, x_pos, y_pos, mode):
        drawing_tool = "draw"

PaintApp(Tk(), "Air Paint", 1)