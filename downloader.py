import streamlit as st
from pytubefix import YouTube
import os
import subprocess

# 1. UI Setup (Replacing tkinter)
st.title("🎥 High-Res YouTube Downloader")
url = st.text_input("Paste YouTube Link:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    try:
        yt = YouTube(url, client='WEB')
        st.write(f"**Title:** {yt.title}")
        
        if st.button("Download & Merge (High Res + WAV)"):
            with st.spinner("Processing... This takes a moment."):
                # 2. Setup paths (Temporary files on the server)
                v_name = "temp_video.mp4"
                a_name = "temp_audio.mp4"
                final_name = f"{yt.title}.mkv".replace("/", "_")

                # 3. Get streams
                v_stream = yt.streams.filter(only_video=True, file_extension="mp4").order_by('resolution').desc().first()
                a_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

                v_stream.download(filename=v_name)
                a_stream.download(filename=a_name)

                # 4. Merge with FFmpeg (Converts audio to high-quality PCM/WAV)
                cmd = [
                    'ffmpeg', '-y', 
                    '-i', v_name, 
                    '-i', a_name, 
                    '-c:v', 'copy', 
                    '-c:a', 'pcm_s16le', 
                    final_name
                ]
                subprocess.run(cmd, check=True)

                # 5. Serve to user
                with open(final_name, "rb") as f:
                    st.download_button(
                        label="💾 Click to Save Video",
                        data=f,
                        file_name=final_name,
                        mime="video/x-matroska"
                    )

                # 6. Cleanup
                os.remove(v_name)
                os.remove(a_name)
                os.remove(final_name)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
