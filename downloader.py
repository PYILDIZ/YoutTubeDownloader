ydl_opts = {
    # 'format' logic: try 1080p+, fallback to anything available
    'format': 'bestvideo[height<=1080]+bestaudio/best',
    'outtmpl': 'temp_video.%(ext)s',
    'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
    
    # NEW: Tell YouTube we are a real Chrome browser
    'impersonate': 'chrome', 
    'quiet': False, # Set to False so you can see logs in Streamlit 'Manage App'
    
    'merge_output_format': 'mkv',
    'postprocessor_args': [
        '-c:a', 'pcm_s16le', # Your high-quality WAV audio
    ],
}
