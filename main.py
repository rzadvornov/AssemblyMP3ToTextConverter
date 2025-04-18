import os
from utils.fileutils import clear_directory_files
from converter.youtube import download_mp3_from_youtube_urls
from converter.transcriber import transcribe_audio


if __name__ == '__main__':
    inputDir = "input"
    outputDir = "output"

    download_mp3_from_youtube_urls(inputDir)
    filesToProcess = [os.path.join(inputDir, f) for f in os.listdir(inputDir) if
             os.path.isfile(os.path.join(inputDir, f))]

    transcribe_audio(filesToProcess, inputDir, outputDir)
    clear_directory_files(inputDir)
