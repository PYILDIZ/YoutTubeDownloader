from pytubefix import YouTube
import tkinter as tk
from tkinter import filedialog

def download_video(url, save_path):
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(only_video=True, file_extension="mp4").order_by('resolution').desc().first()        
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        video_stream = yt.streams.filter(only_video=True, file_extension="mp4").order_by('resolution').desc().first()
        video_stream.download(output_path=save_path, filename="video.mp4")
        audio_stream.download(output_path=save_path, filename="audio.mp3")
        print("Downloaded video and audio segments. You now need to merge them with FFmpeg.")

    except Exception as e:
        print(e)

url = "https://www.youtube.com/watch?v=zT7niRUOs9o"
save_path = r"C:\Users\polat\OneDrive\Masaüstü\code"
download_video(url, save_path)
