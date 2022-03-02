import tkinter
from hand_tracker import MyVideoCapture

class PaintApp:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        self.vid = MyVideoCapture(self.video_source)

    def draw(image, x_pos, y_pos, mode):
        drawing_tool = "draw"

PaintApp(tkinter.Tk(), "Tkinter and OpenCV")