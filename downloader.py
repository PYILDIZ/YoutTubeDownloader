import streamlit as st
import os

# Wrap the imports to catch early failures
try:
    import yt_dlp
    from curl_cffi import requests
except ImportError as e:
    st.error(f"Installation failed: {e}. Please reboot the app.")

def run_app():
    st.title("🚀 Pro High-Res Downloader")
    
    # 1. Rebuild Cookies
    if "YOUTUBE_COOKIES" in st.secrets:
        with open("cookies.txt", "w") as f:
            f.write(st.secrets["YOUTUBE_COOKIES"])

    url = st.text_input("YouTube URL:")

    if url:
        try:
            # 2. Setup yt-dlp options
            ydl_opts = {
                'format': 'bestvideo[height<=1080]+bestaudio/best',
                'outtmpl': 'temp_video.%(ext)s',
                'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
                'impersonate': 'chrome',
                'merge_output_format': 'mkv',
                'postprocessor_args': ['-c:a', 'pcm_s16le'],
            }

            if st.button("Download Now"):
                with st.spinner("🚀 Bypassing YouTube security..."):
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        
                    with open("temp_video.mkv", "rb") as f:
                        st.download_button("💾 Save Video", f, file_name=f"{info.get('title')}.mkv")
                    os.remove("temp_video.mkv")

        except Exception as e:
            # This ensures NO error is empty
            st.error(f"❌ Detailed Error: {str(e)}")

# Run the app
if __name__ == "__main__":
    try:
        run_app()
    except Exception as fatal_e:
        st.write("A fatal error occurred before the app could start:")
        st.exception(fatal_e)
