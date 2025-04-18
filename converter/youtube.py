import os
import yt_dlp
import concurrent.futures

__all__ = [
    'download_mp3_from_youtube_urls',
]

def download_mp3_from_youtube_urls(input_dir):
    """
        Download audio files from youtube in parallel using concurrent.futures.
        Args:
            input_dir: Input directory path
    """

    # Create the input directory if it doesn't exist
    os.makedirs(input_dir, exist_ok=True)

    if os.path.isfile("urls.txt"):
        with open("urls.txt", "r") as file:
            lines = set(file.readlines())
            urls = [line.replace(" ", "").replace("\n", "") for line in lines]

        # Using ThreadPoolExecutor for concurrent downloads
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Create a list of futures
            futures = [executor.submit(download_youtube_as_mp3, url, input_dir) for url in urls]

            # Wait for all futures to complete
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        print(f"Successfully downloaded: {os.path.basename(result['audio_file'])}")
                except Exception as exc:
                    print(f"A download generated an exception: {exc}")


def download_youtube_as_mp3(youtube_url, input_dir):
    """Helper function to download a single audio file."""
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
        print(f"An error occurred while downloading {youtube_url}: {str(e)}")
        return None
