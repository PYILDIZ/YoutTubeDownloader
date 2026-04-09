import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Pro High-Res Downloader", page_icon="🚀")
st.title("🚀 Pro High-Res Downloader")

# Load cookies from Secrets
if "YOUTUBE_COOKIES" in st.secrets:
    with open("cookies.txt", "w") as f:
        f.write(st.secrets["YOUTUBE_COOKIES"])

url = st.text_input("YouTube URL:")

if url:
    try:
        # 1. Fetch info with cookies
        ydl_opts_info = {
            'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url, download=False)
            st.success(f"✅ Found: {info.get('title')}")

        if st.button("Download & Merge"):
            with st.spinner("🚀 Processing... This may take a minute."):
                
                # outtmpl: use a fixed name for processing
                output_name = "final_output.mkv"
                
                ydl_opts = {
                    # 'bestvideo+bestaudio/best' is the standard for 1080p+
                    # We add /best as a fallback in case + fails
                    'format': 'bestvideo+bestaudio/best',
                    'outtmpl': 'temp_video.%(ext)s',
                    'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
                    'merge_output_format': 'mkv',
                    # Post-processor to ensure WAV quality (PCM)
                    'postprocessors': [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mkv',
                    }],
                    'postprocessor_args': [
                        '-c:a', 'pcm_s16le', # Force high-quality WAV audio
                    ],
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # yt-dlp renames the file to temp_video.mkv after merging
                if os.path.exists("temp_video.mkv"):
                    with open("temp_video.mkv", "rb") as f:
                        st.download_button(
                            label="💾 Save Final Video",
                            data=f,
                            file_name=f"{info.get('title')}.mkv",
                            mime="video/x-matroska"
                        )
                    os.remove("temp_video.mkv")
                else:
                    # If temp_video.mkv doesn't exist, it might have kept the original extension
                    st.error("File not found after download. Check the logs.")

    except Exception as e:
        st.error(f"Error: {e}")
