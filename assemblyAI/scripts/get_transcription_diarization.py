import requests
import time
from ..assembly_endpoints import AssemblyEndpoints
import json


def get_transcription_diarization(auth_token="", audio_file=""):
    headers = {"auth_token": auth_token}
    upload_endpoint = AssemblyEndpoints.UPLOAD_AUDIO_ENDPOINT

    print(audio_file)

    with open(audio_file, "rb") as f:
        response = requests.post(upload_endpoint, headers=headers, data=f)

    upload_url = response.json()["upload_url"]

    data = {
        "audio_url": upload_url,  # You can also use a URL to an audio or video file on the web
        "speaker_labels": True,
    }

    transcript_endpoint = AssemblyEndpoints.TRANSCRIPT_AUDIO_ENDPOINT
    response = requests.post(transcript_endpoint, json=data, headers=headers)

    transcript_id = response.json()["id"]
    polling_endpoint = transcript_endpoint + transcript_id

    while True:
        transcription_result = requests.get(polling_endpoint, headers=headers).json()

        if transcription_result["status"] == "completed":
            print(f"Transcript ID:", transcript_id)
            break

        elif transcription_result["status"] == "error":
            raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

        else:
            time.sleep(3)

    # Save json
    with open("transcripcion.json", "w", encoding="utf-8") as f:
        json.dump(transcription_result, f, ensure_ascii=False, indent=2)

    # TXT para lectura rápida
    with open("transcripcion.txt", "w", encoding="utf-8") as f:
        for utt in transcription_result["utterances"]:
            f.write(f"Speaker {utt['speaker']}: {utt['text']}\n")

    for utterance in transcription_result["utterances"]:
        print(f"Speaker {utterance['speaker']}: {utterance['text']}")
