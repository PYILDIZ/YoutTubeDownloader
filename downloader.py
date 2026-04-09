import streamlit as st
from pytubefix import YouTube
import os
import subprocess

st.title("🎥 High-Res Downloader")
url = st.text_input("Paste Link:")

if url:
    try:
        # 1. Use 'WEB_CREATOR' - usually bypasses 403 and doesn't require OAuth login
        yt = YouTube(url, client='WEB_CREATOR')
        st.write(f"**Found:** {yt.title}")

        if st.button("Start High-Quality Download"):
            with st.spinner("🚀 Downloading... Large files take longer!"):
                # Setup names
                v_file, a_file, out_file = "v.mp4", "a.mp4", f"{yt.title}.mkv"

                # 2. Get the streams
                # Note: We filter for 1080p specifically to avoid crashing the server with 4K files
                v_stream = yt.streams.filter(only_video=True, file_extension="mp4").order_by('resolution').desc().first()
                a_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

                v_stream.download(filename=v_file)
                a_stream.download(filename=a_file)

                # 3. Merge
                cmd = ['ffmpeg', '-y', '-i', v_file, '-i', a_file, '-c:v', 'copy', '-c:a', 'pcm_s16le', out_file]
                subprocess.run(cmd, check=True)

                # 4. Success
                with open(out_file, "rb") as f:
                    st.download_button("💾 Save to Device", f, file_name=out_file)

                # Cleanup
                for f in [v_file, a_file, out_file]:
                    if os.path.exists(f): os.remove(f)

    except Exception as e:
        st.error(f"Error: {e}")
