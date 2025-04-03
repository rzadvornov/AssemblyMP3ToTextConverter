import config.settings
import pathlib
import assemblyai as aai
import os
from os import listdir
from os.path import isfile, join

def convert(files):

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
                outputFile.write("\nFull Transcript: \n\n")
                outputFile.write(transcript.text)
                outputFile.write("\nSpeaker Segmentation:\n")
                for utterance in transcript.utterances:
                    outputFile.write("Speaker " + utterance.speaker + ":" + utterance.text + "\n")

if __name__ == '__main__':
    aai.settings.api_key = config.settings.cfg.API_KEY

    AUDIO_FILE_EXTENSION = ".mp3"
    OUTPUT_FILE_EXTENSION = ".txt"
    inputDir = "../input"
    outputDir = "../output"
    pathlib.Path(inputDir).mkdir(exist_ok=True)
    pathlib.Path(outputDir).mkdir(exist_ok=True)
    transcriber = aai.Transcriber()

    config = aai.TranscriptionConfig(speaker_labels=True, language_detection=True)

    filesToProcess = [os.path.join(inputDir, f) for f in os.listdir(inputDir) if
             os.path.isfile(os.path.join(inputDir, f))]

    convert(filesToProcess)
