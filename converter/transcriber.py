import assemblyai as aai
import os
import pprint
import config.settings
import concurrent.futures

__all__ = [
    'transcribe_audio',
]

_AUDIO_FILE_EXTENSION = ".mp3"
_OUTPUT_FILE_EXTENSION = ".txt"
aai.settings.api_key = config.settings.cfg.API_KEY
config = aai.TranscriptionConfig(speaker_labels=True, language_detection=True)
transcriber = aai.Transcriber()

def transcribe_audio(files, input_dir, output_dir, max_workers=None):

    print(f"[Transcribing] {len(files)} files to {output_dir} using parallel processing...")

    os.makedirs(output_dir, exist_ok=True)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {
            executor.submit(
                transcribe_single_file,
                file,
                input_dir,
                output_dir,
            ): file for file in files
        }

        completed_files = []
        for future in concurrent.futures.as_completed(future_to_file):
            file = future_to_file[future]
            try:
                result = future.result()
                if result:
                    completed_files.append(result)
            except Exception as e:
                print(f"Exception processing {file}: {str(e)}")

    print(f"Completed transcription of {len(completed_files)} files.")
    return completed_files

def transcribe_single_file(file, input_dir, output_dir):
    if not file.endswith(_AUDIO_FILE_EXTENSION):
        return

    try:
        transcript = transcriber.transcribe(file, config)
        if transcript.status == aai.TranscriptStatus.error:
            print(f"Transcription failed: {transcript.error}")
            return

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

        print(f"Transcribed: {file}")
        return output_file_name
    except Exception as e:
        print(f"Error processing {file}: {str(e)}")
        return None