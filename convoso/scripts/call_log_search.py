import json
import pandas as pd
import requests
from datetime import datetime, timedelta

from config import Config
from ..convoso_endpoints import ConvosoEndpoints
from .extract_field_notes import extract_fields
from ..fixtures import CALL_LOG_BASIC_COLUMNS


def call_log_search(
    auth_token="",
    columns_required=None,
    use_default_columns=True,
    limit=10,
    offset=0,
    timeout=15,
    include_recordings=1,
    days_back_start=0,
    days_back_end=0,
    start_time=None,
    end_time=None,
    **filters,
):
    """
    Busca call logs desde la API de Convoso con parámetros dinámicos.

    Parámetros:
        auth_token (str): Token de autenticación.
        columns_required (list): Lista personalizada de columnas a mantener.
        use_default_columns (bool): Si True, usa LEADS_BASIC_COLUMNS como filtro.
        limit (int): Cuántos elementos obtener.
        offset (int): Cuántos elementos omitir.
        timeout (int): Tiempo de espera de la llamada.
        include_recordings (int): Si incluir grabaciones (1 = sí).
        days_back_start (int): Cuántos días atrás empezar la búsqueda.
        days_back_end (int): Cuántos días atrás terminar la búsqueda.
        **filters: Otros filtros dinámicos (status, campaign_id, etc).

    Retorna:
        pd.DataFrame con los call logs encontrados.
    """
    if not auth_token:
        print("⚠️ No existe un auth token.")
        return pd.DataFrame()

    url = ConvosoEndpoints.CALL_LOGS_ENDPOINT

    if not start_time:
        start_date = (datetime.today() - timedelta(days=days_back_start)).strftime(
            "%Y-%m-%d"
        )
        start_time = f"{start_date} 01:00:00"

    if not end_time:
        end_date = (datetime.today() - timedelta(days=days_back_end)).strftime(
            "%Y-%m-%d"
        )
        end_time = f"{end_date} 23:59:59"

    # Armar payload
    payload = {
        "auth_token": auth_token,
        "start_time": start_time,
        "end_time": end_time,
        "limit": limit,
        "offset": offset,
        "include_recordings": include_recordings,
    }

    for key, values in filters.items():
        payload[key] = (
            ",".join(str(v) for v in values)
            if isinstance(values, list)
            else str(values)
        )

    # Llamada a la API
    response = requests.post(url, data=payload, timeout=timeout)
    result = response.json()
    call_logs = result.get("data", {}).get("results", [])

    if not call_logs:
        print("⚠️ No se encontraron resultados de call log.")
        return pd.DataFrame()

    df = pd.DataFrame(call_logs)

    # Filtrar columnas si se requiere
    if use_default_columns:
        final_columns = columns_required if columns_required else CALL_LOG_BASIC_COLUMNS
        df = df[[col for col in final_columns if col in df.columns]]

    return df
