import requests
import time
import json
from ..assembly_endpoints import AssemblyEndpoints


def get_transcription_diarization(auth_token="", audio_file=""):
    headers = {
        "authorization": auth_token
    }  # AssemblyAI usa 'authorization', no 'auth_token'
    upload_endpoint = AssemblyEndpoints.UPLOAD_AUDIO_ENDPOINT

    print("📁 Subiendo archivo:", audio_file)

    # 1. Subir audio
    try:
        with open(audio_file, "rb") as f:
            response = requests.post(
                upload_endpoint, headers=headers, files={"file": f}
            )  # 'files' es lo correcto
    except Exception as e:
        print("❌ Error al abrir o subir el archivo:", e)
        return None

    # Validar respuesta del upload
    if response.status_code != 200:
        print(f"❌ Error al subir audio. Código {response.status_code}")
        print("🔍 Respuesta:", response.text)
        return None

    try:
        upload_url = response.json()["upload_url"]
    except (ValueError, KeyError) as e:
        print("❌ Error al obtener 'upload_url' del response:", e)
        print("🔍 Texto recibido:", response.text)
        return None

    print("✅ Audio subido. URL:", upload_url)

    # 2. Crear transcripción
    data = {
        "audio_url": upload_url,
        "speaker_labels": True,
    }

    transcript_endpoint = AssemblyEndpoints.TRANSCRIPT_AUDIO_ENDPOINT

    try:
        response = requests.post(transcript_endpoint, json=data, headers=headers)
    except Exception as e:
        print("❌ Error al solicitar transcripción:", e)
        return None

    if response.status_code != 200:
        print(f"❌ Error al iniciar transcripción. Código {response.status_code}")
        print("🔍 Respuesta:", response.text)
        return None

    try:
        transcript_id = response.json()["id"]
    except (ValueError, KeyError) as e:
        print("❌ Error al obtener 'id' de la transcripción:", e)
        print("🔍 Texto recibido:", response.text)
        return None

    polling_endpoint = transcript_endpoint + "/" + transcript_id
    print("📡 Transcripción iniciada. ID:", transcript_id)

    # 3. Esperar transcripción
    while True:
        try:
            transcription_response = requests.get(polling_endpoint, headers=headers)
            transcription_result = transcription_response.json()
        except Exception as e:
            print("❌ Error al hacer polling:", e)
            return None

        if transcription_result.get("status") == "completed":
            print("✅ Transcripción completada.")
            break
        elif transcription_result.get("status") == "error":
            print("❌ Falló la transcripción:", transcription_result.get("error"))
            return None
        else:
            print("⌛ Esperando transcripción...")
            time.sleep(3)

    # 4. Guardar archivos
    try:
        with open("transcripcion.json", "w", encoding="utf-8") as f:
            json.dump(transcription_result, f, ensure_ascii=False, indent=2)

        with open("transcripcion.txt", "w", encoding="utf-8") as f:
            for utt in transcription_result.get("utterances", []):
                f.write(f"Speaker {utt['speaker']}: {utt['text']}\n")
    except Exception as e:
        print("⚠️ Error al guardar archivos de salida:", e)

    # 5. Mostrar en consola
    for utterance in transcription_result.get("utterances", []):
        print(f"Speaker {utterance['speaker']}: {utterance['text']}")

    return transcription_result
