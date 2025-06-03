import os
import requests
from pathlib import Path
import pandas as pd


def download_recordings_from_df(df, folder_path=None):
    """
    Descarga archivos de audio desde enlaces contenidos en un DataFrame y los guarda con el nombre del lead_id.

    Parámetros:
        df (pd.DataFrame): Debe contener las columnas 'recording_link' y 'lead_id'.
        folder_path (str, opcional): Ruta donde se guardarán los audios.
                                     Si no se especifica, se creará una carpeta llamada 'audios' en el directorio actual.
    """
    if folder_path is None:
        folder_path = Path.cwd() / "audios"
    else:
        folder_path = Path(folder_path)

    folder_path.mkdir(parents=True, exist_ok=True)

    for _, row in df.iterrows():
        url = row.get("recording_link")
        lead_id = row.get("lead_id")

        if pd.isna(url) or pd.isna(lead_id):
            continue  # Saltar si falta alguno

        try:
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()
            file_path = folder_path / f"{lead_id}.mp3"

            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"✅ Guardado: {file_path}")

        except Exception as e:
            print(f"❌ Error al descargar {lead_id}: {e}")
