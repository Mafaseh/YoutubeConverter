import os
import pytube
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from moviepy.video.io.VideoFileClip import VideoFileClip

class YouTubeConverter:
    def __init__(self, master):
        master.title("YouTube Converter")
        master.configure(bg="#303030")
        master.geometry("650x400")

        self.link_label = tk.Label(master, text="Add the YouTube link below:", fg="white", bg="#303030",
                                   font=("Arial", 14))
        self.link_label.place(relx=0.5, rely=0.1, anchor="center")

        self.link_entry = tk.Entry(master, width=50, fg="white", bg="#4D4D4D", font=("Arial", 12))
        self.link_entry.place(relx=0.5, rely=0.2, anchor="center")

        self.format_label = tk.Label(master, text="Choose MP3 or MP4:", fg="white", bg="#303030",
                                     font=("Arial", 14))
        self.format_label.place(relx=0.5, rely=0.35, anchor="center")

        self.format_var = tk.StringVar()
        self.mp3_button = tk.Button(master, text="MP3", command=lambda: self.format_var.set("mp3"),
                                    fg="white", bg="#FF4444", font=("Arial", 12))
        self.mp3_button.place(relx=0.4, rely=0.5, anchor="center")
        self.mp4_button = tk.Button(master, text="MP4", command=lambda: self.format_var.set("mp4"),
                                    fg="white", bg="#FF4444", font=("Arial", 12))
        self.mp4_button.place(relx=0.6, rely=0.5, anchor="center")

        self.convert_label = tk.Label(master, text="Converting...", fg="white", bg="#303030", font=("Arial", 14))
        self.progress_bar = ttk.Progressbar(master, orient="horizontal", mode="indeterminate")
        self.download_button = tk.Button(master, text="Download", command=self.download,
                                         fg="white", bg="#FF4444", font=("Arial", 16), state="disabled")

        self.update_download_button_state()

    def download(self):
        link = self.link_entry.get()
        format_choice = self.format_var.get()

        try:
            # Download YouTube video
            yt = pytube.YouTube(link)
            video = yt.streams.get_highest_resolution()
            video.download()

            # Convert to chosen format
            filename = video.default_filename
            if format_choice == "mp3":
                mp3_filename = self.convert_to_mp3(filename)
                messagebox.showinfo("Success!", f"Downloaded and converted to MP3: {mp3_filename}")
            elif format_choice == "mp4":
                mp4_filename = self.convert_to_mp4(filename)
                messagebox.showinfo("Success!", f"Downloaded and converted to MP4: {mp4_filename}")

            # Delete the video file that was downloaded
            os.remove(filename)

        except pytube.exceptions.RegexMatchError:
            messagebox.showerror("Error", "Invalid YouTube link.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.progress_bar.stop()
            self.convert_label.place_forget()

    def convert_to_mp3(self, filename):
        # Convert video to MP3 using moviepy
        self.convert_label.place(relx=0.5, rely=0.7, anchor="center")
        self.progress_bar.start()
        video = VideoFileClip(filename)
        mp3_filename = filename[:-3] + "mp3"
        audio = video.audio
        audio.write_audiofile(mp3_filename)
        video.close()
        return mp3_filename

    def convert_to_mp4(self, filename):
        # Convert video to MP4 using moviepy
        self.convert_label.place(relx=0.5, rely=0.7, anchor="center")
        self.progress_bar.start()
        video = VideoFileClip(filename)
        mp4_filename = filename[:-3] + "mp4"
        video.write_videofile(mp4_filename, codec="libx264")
        video.close()
        return mp4_filename

    def update_download_button_state(self):
        link = self.link_entry.get()
        format_choice = self.format_var.get()

        if link and format_choice:
            self.download_button.config(state="normal")
        else:
            self.download_button.config(state="disabled")

        self.download_button.place(relx=0.5, rely=0.85, anchor="center")
        self.progress_bar.place(relx=0.5, rely=0.7, anchor="center")

        self.link_entry.bind("<KeyRelease>", lambda e: self.update_download_button_state())
        self.format_var.trace("w", lambda name, index, mode: self.update_download_button_state())

if __name__ == "__main__":
    root = tk.Tk()
    converter = YouTubeConverter(root)
    root.mainloop()