import speech_recognition as sr
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

# ⚙️ Parámetros de grabación
DURACION = 5  # segundos
FRECUENCIA_MUESTREO = 44100  # Hz


def grabar_audio(nombre_archivo="grabacion.wav"):
    print("🎙️ Grabando audio...")
    audio = sd.rec(
        int(DURACION * FRECUENCIA_MUESTREO),
        samplerate=FRECUENCIA_MUESTREO,
        channels=2,
        dtype="int16",
    )
    sd.wait()
    write(nombre_archivo, FRECUENCIA_MUESTREO, audio)
    print(f"✅ Audio guardado en '{nombre_archivo}'")


def accion_personalizada(texto):
    print(f"🔊 Se detectó: {texto}")
    if "hola" in texto.lower():
        print("👋 ¡Hola! ¿En qué te puedo ayudar?")
        grabar_audio()  # 🚨 Aquí se graba
    elif "adiós" in texto.lower():
        print("👋 Hasta luego!")
        return False  # Detiene la escucha
    return True  # Continúa escuchando


def iniciar_escucha():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("🎤 Escuchando... (di 'adiós' para salir)")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

        seguir_escuchando = True
        while seguir_escuchando:
            try:
                audio = recognizer.listen(source, timeout=5)
                texto = recognizer.recognize_google(audio, language="es-MX")
                seguir_escuchando = accion_personalizada(texto)
            except sr.WaitTimeoutError:
                print("⏳ No se detectó audio. Reintentando...")
            except sr.UnknownValueError:
                print("🤷 No entendí lo que dijiste.")
            except sr.RequestError as e:
                print(f"❌ Error al conectar con el servicio: {e}")
                seguir_escuchando = False


if __name__ == "__main__":
    iniciar_escucha()
