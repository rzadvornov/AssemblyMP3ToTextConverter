# Assembly MP3 to Text Converter

## Overview
Assembly MP3 to Text Converter is a powerful and intuitive application designed to convert spoken audio from MP3 files into accurate text transcriptions. Built with speech recognition technology optimized for multiple languages, this tool helps you quickly transcribe interviews, lectures, meetings, and other audio recordings.

## Features
- **Download MP3 from Youtube**: Downloads MP3 files from Youtube for transcription process
- **Fast Processing**: Convert audio to text using efficient speech recognition algorithms
- **Multi-language Support**: Transcribe audio in multiple languages including English, Ukrainian, Russian, German, French, and more
- **Speaker Identification**: Automatically differentiate between multiple speakers (when detectable)
- **Export Options**: Save transcriptions as TXT files
- **Batch Processing**: Convert multiple MP3 files simultaneously
- **Offline Mode**: Process transcriptions locally without internet connection

## Installation
**Works for Python `3.10+`. Previous python versions are not supported due to library dependencies.**
```
pip install betterconf
pip install assemblyai
pip install yt-dlp
```

You'll also need FFmpeg installed on your system:

- Windows: Download from https://ffmpeg.org/download.html and add it to your PATH
- macOS: brew install ffmpeg (using Homebrew)
- Linux: sudo apt install ffmpeg (Ubuntu/Debian) or sudo yum install ffmpeg (CentOS/RHEL)

## Usage
1. Put your Assembly API key from https://www.assemblyai.com/ into `config/settings.json`
2. Create `urls.txt` file with a list of youtube urls - one url per line at project directory. (Optional upload MP3 files into `input` directory)
3. Run main.py
4. After processing is finished check results at `output` directory 

## Troubleshooting
- **Slow Processing**: Try reducing the audio quality settings or splitting large files
- **File Not Recognized**: Ensure the MP3 is not corrupted
- **Application Not Responding**: Restart the application and try processing smaller audio segments

## Privacy
Assembly MP3 to Text Converter processes all audio locally on your machine. No audio data is sent to external servers unless you enable cloud processing for enhanced accuracy.

## Support and Feedback
For support issues, feature requests, or general feedback:

- Email: roman.zadvornov@gmail.com
- Submit bug reports on our GitHub repository

## License
Assembly MP3 to Text Converter is free software distributed under the MIT License. See the LICENSE file for details.
