from utility import record_audio
from transcript import transcribe_with_whisper, transcribe_with_vosk

if __name__ == "__main__":
    # Record Audio
    audio_file = record_audio()

    # Transcribe Using Faster-Whisper
    print("\n🔄 Using Faster-Whisper...")
    transcribed_text_whisper = transcribe_with_whisper(audio_file)

    # Transcribe Using Vosk
    # print("\n🔄 Using Vosk...")
    # transcribed_text_vosk = transcribe_with_vosk(audio_file)