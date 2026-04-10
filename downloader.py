import streamlit as st
import yt_dlp
import os

st.title("🚀 Pro High-Res Downloader")

# Load cookies from Secrets
if "YOUTUBE_COOKIES" in st.secrets:
    with open("cookies.txt", "w") as f:
        f.write(st.secrets["YOUTUBE_COOKIES"])

url = st.text_input("YouTube URL:")

if url:
    try:
        # These extractor-args are the key to bypassing 403 errors in April 2026
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best',
            'outtmpl': 'temp_video.%(ext)s',
            'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
            
            # --- THE BYPASS SETTINGS ---
            'impersonate': 'chrome', 
            'extractor_args': {'youtube': {'player_client': ['default', '-android_sdkless']}},
            # ---------------------------
            
            'merge_output_format': 'mkv',
            'postprocessor_args': ['-c:a', 'pcm_s16le'],
        }

        if st.button("Download & Merge"):
            with st.spinner("🚀 Bypassing YouTube security..."):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    
                if os.path.exists("temp_video.mkv"):
                    with open("temp_video.mkv", "rb") as f:
                        st.download_button("💾 Save Video", f, file_name=f"{info.get('title')}.mkv")
                    os.remove("temp_video.mkv")

    except Exception as e:
        st.error(f"Error: {e}")
