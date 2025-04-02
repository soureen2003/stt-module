import torch

# Global Configurations
SAMPLE_RATE = 16000
CHANNELS = 1
FILENAME = "recorded_audio.wav"
WHISPER_MODEL_SIZE = "base"  # Options: "tiny", "base", "medium", "large"
VOSK_MODEL_PATH = "vosk_model"  # Path to Vosk model
THRESHOLD = 0.01  # Noise threshold
SILENCE_TIMEOUT = 5  # Max silence duration in seconds
MAX_RECORD_DURATION = 60  # Safety limit for recording

# Detect if GPU is available
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"