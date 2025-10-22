# AI_transcribe
AI transcribing service using Python and faster-whisper package for converting audio files to text.

## Features
- Transcribes .m4a audio files to text
- Automatic language detection
- Paragraph separation based on silence gaps and sentence endings
- Timestamps for reference
- Easy-to-use command-line interface

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Place your .m4a audio file in the `input/` directory and name it `sample.m4a`

3. Run the transcription:
   ```bash
   python main.py
   ```

4. Find the transcribed text in the `output/` directory as `sample_transcription.txt`

## Configuration

You can modify the following settings in `main.py`:
- `AUDIO_FILE_PATH`: Path to your input audio file
- `OUTPUT_DIR`: Directory for output text files
- `MODEL_SIZE`: Whisper model size (`tiny`, `base`, `small`, `medium`, `large`)

## Requirements
- Python 3.7+
- faster-whisper package
- Audio file in .m4a format

## Directory Structure
```
AI_transcribe/
├── input/          # Place audio files here (.m4a)
├── output/         # Transcribed text files (.txt) appear here
├── main.py         # Main transcription script
├── requirements.txt
└── README.md
```

Note: The contents of `input/` and `output/` directories are ignored by git to avoid committing large audio files or transcription outputs.
