import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

sd.default.device = (12, None)

samplerate = 48000
duration = 3  # segundos

print("🎙️ Grabando...")
audio = sd.rec(
    int(duration * samplerate), samplerate=samplerate, channels=2, dtype="int16"
)

sd.wait()
print(f"🔍 Shape: {audio.shape}, Max: {np.max(audio)}, Min: {np.min(audio)}")

write("test_grabacion.wav", samplerate, audio)
print("✅ Guardado como 'test_grabacion.wav'")
