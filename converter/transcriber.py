import assemblyai as aai
import os
import pprint
import config.settings

__all__ = [
    'transcribe_audio',
]

_AUDIO_FILE_EXTENSION = ".mp3"
_OUTPUT_FILE_EXTENSION = ".txt"
aai.settings.api_key = config.settings.cfg.API_KEY
config = aai.TranscriptionConfig(speaker_labels=True, language_detection=True)

def transcribe_audio(files, input_dir, output_dir):
    transcriber = aai.Transcriber()

    print(f"[Transcribing] files to {output_dir}...")
    for file in files:
        if file.endswith(_AUDIO_FILE_EXTENSION):
            transcript = transcriber.transcribe(file, config)
            if transcript.status == aai.TranscriptStatus.error:
                print(f"Transcription failed: {transcript.error}")
                continue
            output_file_name = os.path.join(file.replace(input_dir, output_dir)
                                            .replace(_AUDIO_FILE_EXTENSION, _OUTPUT_FILE_EXTENSION))
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
