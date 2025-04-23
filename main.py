import os
from utils.fileutils import clear_directory_files
from converter.youtube import download_mp3_from_youtube_urls
from converter.transcriber import transcribe_audio

def main():
    input_dir = "input"
    output_dir = "output"

    download_mp3_from_youtube_urls(input_dir)
    files_to_process = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if
                      os.path.isfile(os.path.join(input_dir, f))]

    transcribe_audio(files_to_process, input_dir, output_dir)
    clear_directory_files(input_dir)


if __name__ == '__main__':
    main()
