import asyncio
import websockets
import sounddevice as sd
import numpy as np

sd.default.device = (12, None)  # tu micrófono bueno

SAMPLERATE = 48000
CHUNK = 1024


async def audio_stream():
    uri = "ws://localhost:3000/audio"
    async with websockets.connect(uri) as websocket:
        print("🎤 Conectado a WebSocket con 2 canales, 48000 Hz")

        async def enviar_audio():
            with sd.InputStream(
                samplerate=SAMPLERATE, channels=2, dtype="int16"
            ) as stream:
                while True:
                    data = stream.read(CHUNK)[0].tobytes()
                    await websocket.send(data)

        async def recibir_audio():
            with sd.OutputStream(
                samplerate=SAMPLERATE, channels=1, dtype="int16"
            ) as stream:
                buffer = bytearray()  # Acumulador de audio

                while True:
                    data = await websocket.recv()
                    buffer.extend(data)  # Añadir nuevo fragmento

                    # 🧠 Si hay al menos 2 bytes disponibles
                    if len(buffer) >= 2:
                        # ⚖️ Alineamos a múltiplos de 2
                        usable_length = len(buffer) - (len(buffer) % 2)
                        audio_bytes = buffer[:usable_length]
                        buffer = buffer[
                            usable_length:
                        ]  # lo que queda para el siguiente ciclo

                        array = np.frombuffer(audio_bytes, dtype="int16").reshape(-1, 1)
                        stream.write(array)

        await asyncio.gather(enviar_audio(), recibir_audio())


if __name__ == "__main__":
    asyncio.run(audio_stream())
