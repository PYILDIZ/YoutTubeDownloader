import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Pro YT Downloader", page_icon="🚀")
st.title("🚀 Pro High-Res Downloader")

# Load cookies from Streamlit Secrets (for private bypass)
if "YOUTUBE_COOKIES" in st.secrets:
    with open("cookies.txt", "w") as f:
        f.write(st.secrets["YOUTUBE_COOKIES"])

url = st.text_input("Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    try:
        # 1. Fetch info only first
        ydl_opts_info = {
            'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url, download=False)
            st.success(f"✅ Found: {info.get('title')}")

        if st.button("Download 1080p+ (MKV with WAV Audio)"):
            with st.spinner("🚀 Processing... High-quality files take a minute to merge."):
                
                # 2. Main Download & Merge Logic
                # temp_file will be the base name for the process
                final_filename = "downloaded_video.mkv"
                
                ydl_opts = {
                    'format': 'bestvideo+bestaudio/best',
                    'outtmpl': 'temp_video.%(ext)s',
                    'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
                    'merge_output_format': 'mkv',
                    # This converts the audio stream to high-quality PCM (WAV) during the merge
                    'postprocessor_args': [
                        '-c:a', 'pcm_s16le', 
                    ],
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # yt-dlp automatically merges into an .mkv based on our format choice
                # We need to find the merged file (it usually renames it to temp_video.mkv)
                if os.path.exists("temp_video.mkv"):
                    with open("temp_video.mkv", "rb") as f:
                        st.download_button(
                            label="💾 Save Final Video",
                            data=f,
                            file_name=f"{info.get('title')}.mkv",
                            mime="video/x-matroska"
                        )
                    # Cleanup
                    os.remove("temp_video.mkv")
                else:
                    st.error("Merging failed. Please check the logs.")

    except Exception as e:
        st.error(f"Error: {e}")
