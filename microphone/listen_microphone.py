import speech_recognition as sr
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

DURACION = 5
FRECUENCIA_MUESTREO = 44100


def detectar_dispositivo_entrada():
    print("🎛️ Buscando dispositivos de entrada...")
    dispositivos = sd.query_devices()
    indices_disponibles = [
        i for i, d in enumerate(dispositivos) if d["max_input_channels"] > 0
    ]

    if not indices_disponibles:
        raise RuntimeError("❌ No se encontraron dispositivos de entrada de audio.")

    default = sd.default.device[0]
    if default is None or default not in indices_disponibles:
        default = indices_disponibles[0]

    print(f"✅ Usando dispositivo {default}: {dispositivos[default]['name']}")
    return default


def grabar_audio(nombre_archivo="grabacion.wav", dispositivo=None):
    print("🎙️ Grabando audio...")
    sd.default.device = (dispositivo, None)  # (input, output)
    audio = sd.rec(
        int(DURACION * FRECUENCIA_MUESTREO),
        samplerate=FRECUENCIA_MUESTREO,
        channels=2,
        dtype="int16",
    )
    sd.wait()
    write(nombre_archivo, FRECUENCIA_MUESTREO, audio)
    print(f"✅ Audio guardado en '{nombre_archivo}'")


def accion_personalizada(texto, dispositivo):
    print(f"🔊 Se detectó: {texto}")
    if "hola" in texto.lower():
        print("👋 ¡Hola! ¿En qué te puedo ayudar?")
        grabar_audio(dispositivo=dispositivo)
    elif "adiós" in texto.lower():
        print("👋 Hasta luego!")
        return False
    return True


def iniciar_escucha():
    dispositivo_microfono = detectar_dispositivo_entrada()
    recognizer = sr.Recognizer()

    # Obtener el nombre del micrófono para usarlo con SpeechRecognition
    mic_name = sd.query_devices(dispositivo_microfono)["name"]
    mic_list = sr.Microphone.list_microphone_names()
    mic_index = next((i for i, name in enumerate(mic_list) if mic_name in name), None)

    if mic_index is None:
        raise RuntimeError(f"No se encontró un micrófono compatible para: {mic_name}")

    print("🎤 Escuchando... (di 'adiós' para salir)")
    with sr.Microphone(device_index=mic_index) as source:
        recognizer.adjust_for_ambient_noise(source)
        seguir_escuchando = True

        while seguir_escuchando:
            try:
                audio = recognizer.listen(source, timeout=5)
                texto = recognizer.recognize_google(audio, language="es-MX")
                seguir_escuchando = accion_personalizada(texto, dispositivo_microfono)
            except sr.WaitTimeoutError:
                print("⏳ No se detectó audio. Reintentando...")
            except sr.UnknownValueError:
                print("🤷 No entendí lo que dijiste.")
            except sr.RequestError as e:
                print(f"❌ Error al conectar con el servicio: {e}")
                seguir_escuchando = False


if __name__ == "__main__":
    iniciar_escucha()
