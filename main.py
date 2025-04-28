import os
import tkinter as tk
from tkinter import filedialog, ttk, colorchooser
from pygame import mixer
from PIL import Image, ImageTk, ImageSequence

class MusicPlayer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("MP3 Player")
        self.geometry("800x600")
        self.configure(bg="#FFE1FF")  # Default background color

        self.playlist = []
        self.current_track_index = 0
        self.paused = False

        mixer.init()

        self.setup_ui()

    def setup_ui(self):
        
        self.label_title = tk.Label(self, text="MP3 Player", font=("Ink Free Regular", 24), bg="#FFE1FF", fg="black")
        self.label_title.pack(pady=10)

        # Display GIF in the center
        self.load_gif()

        taskbar_frame = tk.Frame(self, bg="black")  # Black background for the taskbar

        # Load Songs Button
        self.load_button = tk.Button(taskbar_frame, text="📁", command=self.load_songs, bd=0, bg="black", font=("Arial", 16), fg="white")
        self.load_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Previous Button
        self.prev_button = tk.Button(taskbar_frame, text="⏮️", command=self.prev_track, bd=0, bg="black", font=("Arial", 16), fg="white")
        self.prev_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Play/Pause Button
        self.play_pause_button = tk.Button(taskbar_frame, text="▶️", command=self.play_track, bd=0, bg="black", font=("Arial", 16), fg="white")
        self.play_pause_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Next Button
        self.next_button = tk.Button(taskbar_frame, text="⏭", command=self.next_track, bd=0, bg="black", font=("Arial", 16), fg="white")
        self.next_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Stop Button
        self.stop_button = tk.Button(taskbar_frame, text="⏹️", command=self.stop, bd=0, bg="black", font=("Arial", 16), fg="white")
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Fast Forward Button (15 seconds)
        self.fast_forward_button = tk.Button(taskbar_frame, text="⏩", command=self.fast_forward, bd=0, bg="black", font=("Arial", 16), fg="white")
        self.fast_forward_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Rewind Button (15 seconds)
        self.rewind_button = tk.Button(taskbar_frame, text="⏪", command=self.rewind, bd=0, bg="black", font=("Arial", 16), fg="white")
        self.rewind_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Volume Label
        self.volume_label = tk.Label(taskbar_frame, text="Volume", bg="black", fg="white")
        self.volume_label.pack(side=tk.LEFT, padx=5, pady=5)

        # Volume Scale
        self.volume_scale = ttk.Scale(taskbar_frame, from_=0, to=100, orient="horizontal", command=self.set_volume, style="Horizontal.TScale")
        self.volume_scale.set(50)
        self.volume_scale.pack(side=tk.LEFT, padx=5, pady=5)

        # Playlist Dropdown
        self.playlist_combobox = ttk.Combobox(taskbar_frame, values=[], state="readonly", font=("Arial", 12))
        self.playlist_combobox.bind("<<ComboboxSelected>>", self.play_selected_track)
        self.playlist_combobox.pack(side=tk.LEFT, padx=10, pady=5)

        # Change gif button
        self.change_gif_button = tk.Button(taskbar_frame, text="Change GIF", command=self.change_gif, bd=0, bg="black", font=("Arial", 16), fg="white")
        self.change_gif_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Background Color Dropdown
        self.bg_color_label = tk.Label(taskbar_frame, text="Background Color", bg="black", fg="white")
        self.bg_color_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.bg_color_var = tk.StringVar()
        self.bg_color_var.set("#FFE1FF")  # Default color

        self.bg_color_dropdown = ttk.Combobox(taskbar_frame, textvariable=self.bg_color_var, values=["#FFE1FF", "Red", "Blue", "Green", "Custom"])
        self.bg_color_dropdown.bind("<<ComboboxSelected>>", self.change_bg_color)
        self.bg_color_dropdown.pack(side=tk.LEFT, padx=5, pady=5)

        self.style = ttk.Style()
        self.style.configure("Horizontal.TScale", troughcolor="black", slidercolor="black")

        taskbar_frame.pack(side=tk.BOTTOM, fill=tk.X)

    def change_gif(self):
        # Open file dialog to choose a new GIF
        gif_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])

        if gif_path:
            # Load the new GIF
            gif_image = Image.open(gif_path)
            gif_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif_image)]

            # Update the GIF label and frames
            self.gif_Label.configure(image=gif_frames[0])
            self.gif_frames = gif_frames
            self.current_frame = 0
            self.animate_gif()

    def load_gif(self):
        gif_path = "D:\downloads\giphy.gif"  # Replace with the path to your GIF file
        gif_image = Image.open(gif_path)
        gif_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif_image)]
        self.gif_Label = tk.Label(self, image=gif_frames[0])
        self.gif_Label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.gif_frames = gif_frames
        self.current_frame = 0
        self.animate_gif()

    def animate_gif(self):
        self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
        self.gif_Label.configure(image=self.gif_frames[self.current_frame])
        self.after(50, self.animate_gif)

    def load_songs(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.playlist = [os.path.join(folder_selected, file) for file in os.listdir(folder_selected) if file.lower().endswith(('.mp3', '.wav'))]
            self.update_playlist()
    
    def update_playlist(self):
        self.playlist_combobox["values"] = [os.path.basename(song) for song in self.playlist]

    def play_selected_track(self, event):
        selected_track = self.playlist_combobox.get()
        if selected_track:
            self.current_track_index = [os.path.basename(song) for song in self.playlist].index(selected_track) 
            self.play_track()

    def play_track(self):
        mixer.music.load(self.playlist[self.current_track_index])
        mixer.music.set_volume(self.volume_scale.get() / 100.0)
        mixer.music.play()
        self.paused = False
        self.label_title.config(text=f"Now Playing: {os.path.basename(self.playlist[self.current_track_index])}")

    def set_volume(self, value):
        mixer.music.set_volume(float(value) / 100.0)

    def fast_forward(self):
        self.adjust_track_position(15)

    def rewind(self):
        self.adjust_track_position(-15)

    def adjust_track_position(self, seconds):
        if not self.playlist or not mixer.music.get_busy():
            return

        current_position = mixer.music.get_pos() / 1000  # Convert milliseconds to seconds
        new_position = current_position + seconds

        # Ensure the new position is within the bounds of the track
        new_position = max(0, new_position)

        if new_position <= mixer.Sound(self.playlist[self.current_track_index]).get_length():
            mixer.music.set_pos(new_position)
        else:
            # If the new position is beyond the end of the track, stop the playback
            self.stop()


    def stop(self):
        mixer.music.stop()

    def next_track(self):
        if not self.playlist:
            return

        self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
        self.play_track()

    def prev_track(self):
        if not self.playlist:
            return

        self.current_track_index = (self.current_track_index - 1) % len(self.playlist)
        self.play_track()

    def change_bg_color(self, event):
        selected_color = self.bg_color_var.get()

        if selected_color == "Custom":
            color = colorchooser.askcolor()[1]
            if color:
                self.configure(bg=color)
                self.label_title.configure(bg=color)
        else:
            self.configure(bg=selected_color)
            self.label_title.configure(bg=selected_color)

if __name__ == "__main__":
    app = MusicPlayer()
    app.mainloop()
