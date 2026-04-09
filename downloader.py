import streamlit as st
from pytubefix import YouTube
import os
import subprocess

# --- 1. Security: Load Cookies from Secrets ---
if "YOUTUBE_COOKIES" in st.secrets:
    with open("cookies.txt", "w") as f:
        f.write(st.secrets["YOUTUBE_COOKIES"])
else:
    st.error("Missing cookies in Streamlit Secrets!")

st.title("🎥 Private High-Res Downloader")
url = st.text_input("YouTube URL:")

if url:
    try:
        # --- 2. Authenticate with Cookies ---
        yt = YouTube(url, client='WEB', token_file="cookies.txt")
        st.write(f"✅ **Connected as User:** {yt.title}")

        if st.button("Download High Quality"):
            with st.spinner("Processing..."):
                v_file, a_file, out_file = "v.mp4", "a.mp4", f"{yt.title}.mkv"

                # Get best streams
                v_stream = yt.streams.filter(only_video=True, file_extension="mp4").order_by('resolution').desc().first()
                a_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

                v_stream.download(filename=v_file)
                a_stream.download(filename=a_file)

                # Merge using FFmpeg
                cmd = ['ffmpeg', '-y', '-i', v_file, '-i', a_file, '-c:v', 'copy', '-c:a', 'pcm_s16le', out_file]
                subprocess.run(cmd, check=True)

                with open(out_file, "rb") as f:
                    st.download_button("💾 Save to Device", f, file_name=out_file)

                # Cleanup server files
                for f_path in [v_file, a_file, out_file]:
                    if os.path.exists(f_path): os.remove(f_path)

    except Exception as e:
        st.error(f"Error: {e}")
