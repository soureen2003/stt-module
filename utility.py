import speech_recognition as sr
import threading
import time
import wave
from config import SAMPLE_RATE, FILENAME, THRESHOLD, SILENCE_TIMEOUT, MAX_RECORD_DURATION

recognizer = sr.Recognizer()
stop_flag = False  # Flag to stop recording manually

def listen_for_enter():
    """Waits for ENTER key to stop recording."""
    global stop_flag
    input()  # Blocks until ENTER is pressed
    stop_flag = True  # Set flag to stop recording

def record_audio():
    """Records audio until SILENCE_TIMEOUT (e.g., 5s) or ENTER key is pressed."""
    global stop_flag
    stop_flag = False  # Reset before recording
    silence_start = None  # Track when silence starts
    audio_data = bytearray()  # Store raw audio bytes

    with sr.Microphone(sample_rate=SAMPLE_RATE) as source:
        print("🎤 Speak something... (Press ENTER to stop, or {}s silence)".format(SILENCE_TIMEOUT))
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Auto noise reduction
        recognizer.energy_threshold = THRESHOLD  # Set sensitivity manually

        # Start a separate thread to listen for ENTER key
        enter_thread = threading.Thread(target=listen_for_enter, daemon=True)
        enter_thread.start()

        start_time = time.time()
        
        while not stop_flag:  # Continue recording until stopped
            try:
                audio = recognizer.listen(source, timeout=2)  # Capture short pauses
                audio_data.extend(audio.get_raw_data())  # Accumulate audio chunks
                silence_start = None  # Reset silence timer when speaking
            except sr.WaitTimeoutError:
                # First time detecting silence → Start the timer
                if silence_start is None:
                    silence_start = time.time()
                else:
                    elapsed_silence = time.time() - silence_start
                    print(f"⏳ Silence detected for {elapsed_silence:.2f} seconds...", end="\r")

                    if elapsed_silence >= SILENCE_TIMEOUT:  # Silence timeout reached
                        print("\n🛑 Silence detected. Stopping recording...")
                        break

            # Stop recording if max duration is reached
            elapsed_time = time.time() - start_time
            if elapsed_time >= MAX_RECORD_DURATION:
                print("\n⏳ Maximum recording duration reached. Stopping...")
                break

        # Save the recorded audio
        if not audio_data:
            print("⚠ No speech detected!")
            return None

        with wave.open(FILENAME, "wb") as f:
            f.setnchannels(1)
            f.setsampwidth(2)  # 16-bit PCM
            f.setframerate(SAMPLE_RATE)
            f.writeframes(audio_data)

        print(f"✅ Audio saved as {FILENAME}")
        return FILENAME