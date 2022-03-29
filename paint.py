from tkinter import *
from PIL import Image, ImageTk, ImageGrab
from hand_tracker import MyVideoCapture
import cv2
import numpy as np

class PaintApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.vid = MyVideoCapture()
        self.x_pos = None
        self.y_pos = None
        self.old_x_pos = None
        self.old_y_pos = None
        self.mode = None
        self.prev_mode = None
        self.history = []
        self.fill = (0, 255, 0)

        # Create canvas
        self.canvas = Canvas(self.window, width=self.vid.width, height = self.vid.height)
        self.image = self.canvas.create_image(0, 0, anchor="nw")
        self.canvas.pack()

        self.delay = 15
        self.update()
        
        self.window.mainloop()

    def rgb_hack(self, rgb):
        return "#%02x%02x%02x" % rgb 

    def paint(self):
        if self.mode == "Paint":
            # Check if co-ordinates are valid
            if self.x_pos is not None and self.y_pos is not None:
                # Check if line is continuing
                if self.old_x_pos is None and self.old_y_pos is None:
                    # Start new line
                    line = self.canvas.create_line(self.x_pos, self.y_pos, self.x_pos, self.y_pos, width=5,fill=self.rgb_hack(self.fill),capstyle=ROUND,smooth=True)
                    # Record drawings to history stack
                    self.history.append(line)
                    self.old_x_pos = self.x_pos
                    self.old_y_pos = self.y_pos
                else:
                    # Continue old line
                    self.canvas.create_line(self.old_x_pos, self.old_y_pos, self.x_pos, self.y_pos, width=5,fill=self.rgb_hack(self.fill),capstyle=ROUND,smooth=True)
                    self.old_x_pos = self.x_pos
                    self.old_y_pos = self.y_pos

    # Gets colour from gradient at Y relative to finger X position
    def get_pixel_colour(self):
        # Takes snapshot of canvas
        x = root.winfo_rootx() + self.canvas.winfo_x()
        y = root.winfo_rooty() + self.canvas.winfo_y()
        xx = x + self.canvas.winfo_width()
        yy = y + self.canvas.winfo_height()
        image = ImageGrab.grab(bbox=(x, y, xx, yy))

        # Returns colour of pixel at canvas
        return image.getpixel((self.x_pos, 450))

    def select_colour(self, frame):
        img = cv2.imread("colours.jpg")
        img_height, img_width, _ = img.shape
        img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)
        
        # Colour Selector Region of Interest (ROI)
        roi = frame[-img_height-10:-10, -img_width-10:-10]
        # Set an index of where the mask is
        roi[np.where(mask)] = 0
        roi += img

        # Set line colour to selected colour
        self.fill = self.get_pixel_colour()


    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        # Add hand tracking
        frame, cursor_pos, self.mode = self.vid.track_hands(cv2.flip(frame, 1), self.fill)

        if self.mode == "Select":
            self.select_colour(frame)

        # Get index finger position
        if cursor_pos:
            self.x_pos, self.y_pos = cursor_pos[0], cursor_pos[1]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Update canvas with opencv video frame
        if ret:
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
            self.canvas.itemconfig(self.image, image=self.photo)

        self.window.after(self.delay, self.update)

        # Reset old co-ordinates if not in paint mode
        if self.mode != "Paint":
            self.old_x_pos = None
            self.old_y_pos = None

        self.paint()

        # Record previous mode for undo function
        prev_mode = self.mode

root = Tk()
paint_app = PaintApp(root, "Air Paint")