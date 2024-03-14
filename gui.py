# pip install imageio[ffmpeg] imageio[pyav]

import tkinter as tk
from tkinter import ttk, messagebox
import imageio
from PIL import Image, ImageTk


class GestureEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Gesture Editor")
        self.master.option_add("*tearOff", False)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        self.style = ttk.Style(self.master)
        self.master.tk.call("source", r"./forest-dark.tcl")
        self.style.theme_use("forest-dark")

        self.init_variables()
        self.create_widgets()
        self.load_videos()

    def init_variables(self):
        self.gestures = []
        self.selected_gesture = tk.StringVar(value="")
        self.key_bind_var = tk.StringVar()
        self.video_paths = {
            "Gesture 1": r"./toystory.mp4",
            "Gesture 2": r"./aa.mp4",
            "Gesture 3": r"./bb).mp4",
            "Gesture 4": r"./aa.mp4",
            "Gesture 5": r"./bb).mp4",
        }
        # self.video_player = None
        # self.preview_label = None

    def create_widgets(self):
        self.left_frame = ttk.Frame(self.master)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.right_frame = ttk.Frame(self.master)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Left Frame
        self.preview_label = ttk.Label(self.left_frame)
        self.preview_label.pack(padx=10, pady=10)

        # Right Frame
        self.radio_frame = ttk.LabelFrame(
            self.right_frame, text="Gestures", padding=(20, 10)
        )
        self.radio_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.radio_buttons = []
        for gesture in self.video_paths.keys():
            radio_button = ttk.Radiobutton(
                self.radio_frame,
                text=gesture,
                variable=self.selected_gesture,
                value=gesture,
                command=self.update_preview,
            )
            radio_button.pack(anchor="w", padx=5, pady=5)
            self.radio_buttons.append(radio_button)

        # Bottom Frame
        self.bottom_frame = ttk.Frame(self.master)
        self.bottom_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        ttk.Button(self.bottom_frame, text="New", command=self.add_new_gesture).pack(
            side="left", padx=5
        )
        ttk.Button(self.bottom_frame, text="Delete", command=self.delete_gesture).pack(
            side="left", padx=5
        )
        ttk.Button(self.bottom_frame, text="Save", command=self.save_gestures).pack(
            side="right", padx=5
        )
        ttk.Button(self.bottom_frame, text="Cancel", command=self.master.destroy).pack(
            side="right", padx=5
        )

    def load_videos(self):
        self.video_player = {}
        for gesture, video_path in self.video_paths.items():
            self.video_player[gesture] = imageio.get_reader(video_path)
        self.update_preview()

    def update_preview(self):
        selected_gesture = self.selected_gesture.get()
        if selected_gesture and selected_gesture in self.video_player:
            try:
                frame = self.video_player[selected_gesture].get_next_data()
                frame = Image.fromarray(frame)
                frame = ImageTk.PhotoImage(frame)
                self.preview_label.config(image=frame)
                self.preview_label.image = frame
                self.master.after(50, self.update_preview)
            except:
                self.video_player[selected_gesture].set_image_index(0)
                self.master.after(50, self.update_preview)

    def add_new_gesture(self):
        popup = tk.Toplevel(self.master)
        popup.title("Add New Gesture")

        label = ttk.Label(popup, text="Assign Key Bind:")
        label.pack(padx=20, pady=10)
        entry = ttk.Entry(popup, textvariable=self.key_bind_var)
        entry.pack(padx=20, pady=5)

        label = ttk.Label(popup, text="Select Video:")
        label.pack(padx=20, pady=10)
        video_dropdown = ttk.Combobox(popup, values=list(self.video_paths.keys()))
        video_dropdown.pack(padx=20, pady=5)

        save_button = ttk.Button(
            popup,
            text="Save",
            command=lambda: self.save_new_gesture(popup, video_dropdown.get()),
        )
        save_button.pack(pady=10)

    def save_new_gesture(self, popup, video_name):
        gesture_name = f"Gesture {len(self.video_paths) + 1}"
        selected_video_path = self.video_paths[video_name]
        self.video_paths[gesture_name] = selected_video_path
        self.selected_gesture.set(gesture_name)
        self.video_player[gesture_name] = imageio.get_reader(selected_video_path)
        radio_button = ttk.Radiobutton(
            self.radio_frame,
            text=gesture_name,
            variable=self.selected_gesture,
            value=gesture_name,
            command=self.update_preview,
        )
        radio_button.pack(anchor="w", padx=5, pady=5)
        self.radio_buttons.append(radio_button)
        popup.destroy()

    def delete_gesture(self):
        selected_gesture = self.selected_gesture.get()
        if selected_gesture:
            del self.video_paths[selected_gesture]
            del self.video_player[selected_gesture]
            self.selected_gesture.set("")
            for radio_button in self.radio_buttons:
                radio_button.destroy()
            self.radio_buttons.clear()
            for gesture in self.video_paths.keys():
                radio_button = ttk.Radiobutton(
                    self.radio_frame,
                    text=gesture,
                    variable=self.selected_gesture,
                    value=gesture,
                    command=self.update_preview,
                )
                radio_button.pack(anchor="w", padx=5, pady=5)
                self.radio_buttons.append(radio_button)

    def save_gestures(self):
        messagebox.showinfo("Save", "Gestures Saved Successfully")


if __name__ == "__main__":
    root = tk.Tk()
    app = GestureEditor(root)
    root.mainloop()
