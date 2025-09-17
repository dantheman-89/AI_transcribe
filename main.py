#!/usr/bin/env python3
"""
AI Transcribing Service using faster-whisper

This script transcribes audio files using the faster-whisper library.
It supports .m4a files and outputs transcribed text with paragraph separation.
"""

import os
import sys
from pathlib import Path
from faster_whisper import WhisperModel

# Configuration
AUDIO_FILE_PATH = "input/sample.m4a"  # Hard-coded audio file path
OUTPUT_DIR = "output"  # Hard-coded output directory
MODEL_SIZE = "base"  # Whisper model size (tiny, base, small, medium, large)


def setup_model():
    """Initialize the Whisper model."""
    print(f"Loading Whisper model: {MODEL_SIZE}")
    try:
        model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
        print("Model loaded successfully!")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)


def transcribe_audio(model, audio_path):
    """
    Transcribe audio file using faster-whisper.
    
    Args:
        model: WhisperModel instance
        audio_path: Path to the audio file
        
    Returns:
        tuple: (segments, info) containing transcription segments and metadata
    """
    print(f"Transcribing audio file: {audio_path}")
    
    try:
        segments, info = model.transcribe(
            audio_path,
            beam_size=5,
            language=None,  # Auto-detect language
            task="transcribe"
        )
        
        print(f"Detected language: {info.language} (probability: {info.language_probability:.2f})")
        print(f"Duration: {info.duration:.2f} seconds")
        
        return segments, info
    except Exception as e:
        print(f"Error during transcription: {e}")
        sys.exit(1)


def format_transcription(segments):
    """
    Format transcription segments into readable text with paragraph separation.
    
    Args:
        segments: Generator of transcription segments
        
    Returns:
        str: Formatted transcription text
    """
    print("Processing transcription segments...")
    
    formatted_text = []
    current_paragraph = []
    
    for segment in segments:
        text = segment.text.strip()
        
        # Add timestamp for reference (optional)
        timestamp = f"[{segment.start:.2f}s - {segment.end:.2f}s]"
        
        # Simple paragraph separation logic:
        # - Create new paragraph after silence longer than 2 seconds
        # - Or when sentence ends with period, question mark, or exclamation
        if current_paragraph and (
            segment.start - prev_end > 2.0 or  # 2+ second gap
            current_paragraph[-1].strip().endswith(('.', '!', '?'))
        ):
            # Join current paragraph and add to formatted text
            paragraph_text = ' '.join(current_paragraph)
            formatted_text.append(paragraph_text)
            current_paragraph = []
        
        current_paragraph.append(text)
        prev_end = segment.end
        
        # Print progress
        print(f"  {timestamp} {text}")
    
    # Add the last paragraph if it exists
    if current_paragraph:
        paragraph_text = ' '.join(current_paragraph)
        formatted_text.append(paragraph_text)
    
    # Join paragraphs with double newlines
    return '\n\n'.join(formatted_text)


def save_transcription(text, audio_path, output_dir):
    """
    Save transcription to a text file.
    
    Args:
        text: Transcribed text
        audio_path: Original audio file path (for naming)
        output_dir: Output directory path
    """
    # Generate output filename based on input filename
    audio_file = Path(audio_path)
    output_filename = f"{audio_file.stem}_transcription.txt"
    output_path = Path(output_dir) / output_filename
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"Transcription saved to: {output_path}")
        print(f"Total characters: {len(text)}")
        
    except Exception as e:
        print(f"Error saving transcription: {e}")
        sys.exit(1)


def main():
    """Main function to orchestrate the transcription process."""
    print("AI Transcribing Service Starting...")
    print("=" * 50)
    
    # Check if audio file exists
    if not os.path.exists(AUDIO_FILE_PATH):
        print(f"Error: Audio file not found at {AUDIO_FILE_PATH}")
        print(f"Please place your .m4a file at: {AUDIO_FILE_PATH}")
        sys.exit(1)
    
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Initialize model
    model = setup_model()
    
    # Transcribe audio
    segments, info = transcribe_audio(model, AUDIO_FILE_PATH)
    
    # Format transcription
    transcribed_text = format_transcription(segments)
    
    # Save transcription
    save_transcription(transcribed_text, AUDIO_FILE_PATH, OUTPUT_DIR)
    
    print("=" * 50)
    print("Transcription completed successfully!")


if __name__ == "__main__":
    main()