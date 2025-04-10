import config.settings
import pathlib
import assemblyai as aai
import os
import pprint
import yt_dlp
from pathlib import Path
from typing import Union

def convert_audio(files):
    
    print(f"[Transcribing] files to {outputDir}...")
    for file in files:
        if file.endswith(AUDIO_FILE_EXTENSION):
            transcript = transcriber.transcribe(file, config)
            if transcript.status == aai.TranscriptStatus.error:
                print(f"Transcription failed: {transcript.error}")
                continue
            output_file_name = os.path.join(outputDir, file
                                      .replace(inputDir, outputDir)
                                      .replace(AUDIO_FILE_EXTENSION, OUTPUT_FILE_EXTENSION))
            with open(output_file_name, "w") as outputFile:
                pp = pprint.PrettyPrinter(indent=4, stream=outputFile)
                pp.pprint("Full Transcript:")
                pp.pprint(transcript.text)
                pp.pprint("Speaker Segmentation:")
                for utterance in transcript.utterances:
                    pp.pprint("Speaker " + utterance.speaker + ":" + utterance.text)
                outputFile.write("\nFull Transcript: \n\n")
                outputFile.write(transcript.text)
                outputFile.write("\nSpeaker Segmentation:\n")
                for utterance in transcript.utterances:
                    outputFile.write("Speaker " + utterance.speaker + ":" + utterance.text + "\n")

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


def clear_directory_files(
    directory_path: Union[str, Path],
    empty_subfolders: bool = False
) -> list:
    """Irreversibly removes all files inside the specified directory. Optionally
    clears subfolders from files too. Returns a list with paths Python lacks
    permission to delete."""
    if empty_subfolders:
        directory_items = Path(directory_path).rglob("*")
    else:
        directory_items = Path(directory_path).glob("*")

    erroneous_paths = []

    for file_path in (path_object for path_object in directory_items
                      if path_object.is_file()):
        try:
            file_path.unlink()
        except PermissionError:
            erroneous_paths.append(file_path)
    return erroneous_paths

if __name__ == '__main__':
    aai.settings.api_key = config.settings.cfg.API_KEY
    AUDIO_FILE_EXTENSION = ".mp3"
    OUTPUT_FILE_EXTENSION = ".txt"
    inputDir = "../input"
    outputDir = "../output"
    pathlib.Path(inputDir).mkdir(exist_ok=True)
    pathlib.Path(outputDir).mkdir(exist_ok=True)

    download_mp3_from_youtube_urls(inputDir)
    transcriber = aai.Transcriber()

    config = aai.TranscriptionConfig(speaker_labels=True, language_detection=True)

    filesToProcess = [os.path.join(inputDir, f) for f in os.listdir(inputDir) if
             os.path.isfile(os.path.join(inputDir, f))]

    convert_audio(filesToProcess)
    clear_directory_files(inputDir)
