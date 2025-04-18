import os
import yt_dlp

__all__ = [
    'download_mp3_from_youtube_urls',
]

def download_mp3_from_youtube_urls(input_dir):
    if os.path.isfile("urls.txt"):
        with open("urls.txt", "r") as file:
            lines = set(file.readlines())
            for line in lines:
                youtube_url = line.replace(" ", "").replace("\n", "")
                download_youtube_as_mp3(youtube_url, input_dir)


def download_youtube_as_mp3(youtube_url, input_dir):
    try:
        # Get video info first to get the title
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            video_title = info.get('title', 'video')
            # Clean the title for filename use
            video_title = "".join(c for c in video_title if c.isalnum() or c in [' ', '-', '_']).strip()

        print(f"[Processing]: {video_title}")

        # Download MP3
        mp3_filename = os.path.join(input_dir, f"{video_title}")
        mp3_options = {
            'format': 'bestaudio',
            'outtmpl': mp3_filename,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': False,
        }

        with yt_dlp.YoutubeDL(mp3_options) as ydl:
            ydl.download([youtube_url])

        return {
            "audio_file": mp3_filename
        }

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
