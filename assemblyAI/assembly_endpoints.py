from config import Config


class AssemblyEndpoints:
    ASSEMBLY_TOKEN = Config.ASSEMBLY_TOKEN
    BASE_URL = "https://api.assemblyai.com"
    UPLOAD_AUDIO_ENDPOINT = BASE_URL + "/v2/upload"
