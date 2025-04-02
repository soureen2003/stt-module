import wave
import json
import vosk
from faster_whisper import WhisperModel
from config import SAMPLE_RATE, WHISPER_MODEL_SIZE, VOSK_MODEL_PATH, DEVICE, FILENAME

def transcribe_with_whisper(file_path=FILENAME):
    """Transcribes audio file using Faster-Whisper with minimal auto-correction."""
    model = WhisperModel(WHISPER_MODEL_SIZE, device=DEVICE, compute_type="int8")

    print("📝 Transcribing with Faster-Whisper (minimal correction mode)...")
    segments, _ = model.transcribe(
        file_path, 
        beam_size=1,  # Reduce beam search optimization
        language="en", 
        word_timestamps=True,  # Force raw words
        temperature=0  # Reduce correction randomness
    )

    result_text = " ".join(segment.text for segment in segments)
    print("\n📝 Whisper (Minimal Correction) Captured Text:", result_text)
    return result_text

def transcribe_with_vosk(file_path=FILENAME):
    """Transcribes audio file using Vosk."""
    print("📝 Transcribing with Vosk...")

    # Load Vosk Model
    if not hasattr(transcribe_with_vosk, "vosk_model"):
        transcribe_with_vosk.vosk_model = vosk.Model(VOSK_MODEL_PATH)

    # Open the recorded audio file
    with wave.open(file_path, "rb") as wf:
        recognizer = vosk.KaldiRecognizer(transcribe_with_vosk.vosk_model, SAMPLE_RATE)
        
        while True:
            data = wf.readframes(4000)  # Process in chunks
            if len(data) == 0:
                break
            recognizer.AcceptWaveform(data)

        result_json = json.loads(recognizer.FinalResult())
        result_text = result_json.get("text", "")

    print("\n📝 Vosk Captured Text:", result_text)
    return result_text