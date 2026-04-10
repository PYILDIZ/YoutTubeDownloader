import streamlit as st
import yt_dlp
import os

st.title("🚀 Pro High-Res Downloader")

# Load your cookies from Secrets for the ultimate bypass
if "YOUTUBE_COOKIES" in st.secrets:
    with open("cookies.txt", "w") as f:
        f.write(st.secrets["YOUTUBE_COOKIES"])

url = st.text_input("YouTube URL:")

if url:
    try:
        # Use Chrome impersonation to avoid 403 Forbidden
        ydl_opts_info = {
            'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
            'impersonate': 'chrome', 
            'quiet': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url, download=False)
            st.success(f"✅ Found: {info.get('title')}")

        if st.button("Download 1080p+ (MKV/WAV)"):
            with st.spinner("Processing..."):
                ydl_opts = {
                    'format': 'bestvideo[height<=1080]+bestaudio/best', # Safer for RAM limits
                    'outtmpl': 'temp_video.%(ext)s',
                    'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
                    'impersonate': 'chrome',
                    'merge_output_format': 'mkv',
                    'postprocessor_args': ['-c:a', 'pcm_s16le'], # WAV quality
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                if os.path.exists("temp_video.mkv"):
                    with open("temp_video.mkv", "rb") as f:
                        st.download_button("💾 Save Video", f, file_name=f"{info.get('title')}.mkv")
                    os.remove("temp_video.mkv")

    except Exception as e:
        st.error(f"Error: {e}")
