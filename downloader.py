import streamlit as st
import os
import yt_dlp

# --- NEW: Mandatory Import for 2026 Impersonation ---
from yt_dlp.networking.impersonate import ImpersonateTarget

st.title("🚀 Pro High-Res Downloader")

# Setup Cookies
if "YOUTUBE_COOKIES" in st.secrets:
    with open("cookies.txt", "w") as f:
        f.write(st.secrets["YOUTUBE_COOKIES"])

url = st.text_input("YouTube URL:")

if url:
    try:
        # --- NEW: Convert the string 'chrome' into a Target Object ---
        chrome_target = ImpersonateTarget.from_str("chrome")

        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best',
            'outtmpl': 'temp_video.%(ext)s',
            'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
            
            # Use the object instead of the string
            'impersonate': chrome_target, 
            
            'merge_output_format': 'mkv',
            'postprocessor_args': ['-c:a', 'pcm_s16le'],
        }

        if st.button("Download & Merge"):
            with st.spinner("🚀 Bypassing YouTube security..."):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    
                with open("temp_video.mkv", "rb") as f:
                    st.download_button("💾 Save Video", f, file_name=f"{info.get('title')}.mkv")
                os.remove("temp_video.mkv")

    except Exception as e:
        st.error(f"Error: {e}")
