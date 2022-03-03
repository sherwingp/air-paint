from tkinter import *
from PIL import Image, ImageTk
from hand_tracker import MyVideoCapture
import cv2

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

        # Create canvas
        self.canvas = Canvas(self.window, width=self.vid.width, height = self.vid.height)
        self.image = self.canvas.create_image(0, 0, anchor="nw")
        self.canvas.pack()

        self.delay = 15
        self.update()
        
        self.window.mainloop()

    def paint(self):
        if self.mode == "Paint":
            # Check if co-ordinates are valid
            if self.x_pos is not None and self.y_pos is not None:
                # Check if line is continuing
                if self.old_x_pos is None and self.old_y_pos is None:
                    # Start new line
                    self.canvas.create_line(self.x_pos, self.y_pos, self.x_pos, self.y_pos, width=5,fill='red',capstyle=ROUND,smooth=True)
                    self.old_x_pos = self.x_pos
                    self.old_y_pos = self.y_pos
                else:
                    # Continue old line
                    self.canvas.create_line(self.old_x_pos, self.old_y_pos, self.x_pos, self.y_pos, width=5,fill='red',capstyle=ROUND,smooth=True)
                    self.old_x_pos = self.x_pos
                    self.old_y_pos = self.y_pos

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        # Add hand tracking
        frame, cursor_pos, self.mode = self.vid.track_hands(cv2.flip(frame, 1))
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

root = Tk()
paint_app = PaintApp(root, "Air Paint")