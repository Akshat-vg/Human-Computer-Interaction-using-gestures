from PIL import Image, ImageTk
import customtkinter

class GestureAnimation:
    def __init__(self, root, anchor, gif_path):
        self.root = root
        self.gif_path = gif_path
        self.anchor = anchor

        # Load the GIF
        self.gif = Image.open(gif_path)
        self.frames = []
        self.load_frames()
        self.runFlag = True

        # Create a label to display the GIF
        self.label = customtkinter.CTkLabel(root, text="")
        if anchor == 'left':
            self.label.grid(row=1, column=0, padx=30)
        else:
            self.label.grid(row=1, column=1)

        # Display the GIF
        self.display_frames()

    def update_gif(self, gif_path):
        try:
            # Remove old frames
            self.runFlag = False
            self.frames.clear()

            # Load the new GIF
            self.gif = Image.open(gif_path)
            self.load_frames()
            self.runFlag = True
            self.display_frames()
        except Exception as e:
            pass

    def load_frames(self):
        try:
            while True:
                self.frames.append(ImageTk.PhotoImage(self.gif.copy()))
                self.gif.seek(len(self.frames))
        except EOFError:
            pass

    def display_frames(self):
        try:
            def update_frame(idx):
                if self.runFlag:
                    try:
                        frame = self.frames[idx]
                        self.label.configure(image=frame)
                        self.root.after(50, update_frame, (idx + 1) % len(self.frames))
                    except Exception as e:
                        pass
            update_frame(0)
        except Exception as e:
            pass
