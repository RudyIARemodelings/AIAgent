import json
import pandas as pd
import requests
from datetime import datetime, timedelta

from ..convoso_endpoints import ConvosoEndpoints
from ..fixtures import CALL_LOG_BASIC_COLUMNS


def extract_recording_url(recording_list):
    if isinstance(recording_list, list) and recording_list:
        return recording_list[0].get("public_url")
    return None


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
    Retrieve call logs from the Convoso API with dynamic filtering and optional recording extraction.

    Parameters:
        auth_token (str): Convoso authentication token.
        columns_required (list, optional): List of specific column names to keep in the final DataFrame.
        use_default_columns (bool): If True, filters the DataFrame to include only CALL_LOG_BASIC_COLUMNS.
        limit (int): Maximum number of records to retrieve per request.
        offset (int): Number of records to skip (for pagination).
        timeout (int): Maximum wait time in seconds for the API response.
        include_recordings (int): If 1, includes 'recording_link' extracted from JSON in results.
        days_back_start (int): Number of days before today to start the search window (e.g., 3 = 3 days ago).
        days_back_end (int): Number of days before today to end the search window (e.g., 1 = yesterday).
        start_time (str, optional): Override for search start datetime (format: "YYYY-MM-DD HH:MM:SS").
        end_time (str, optional): Override for search end datetime (format: "YYYY-MM-DD HH:MM:SS").
        **filters (dict): Additional Convoso API filters (e.g., status, campaign_id, etc.).

    Returns:
        pd.DataFrame: A DataFrame containing call log results, optionally filtered and enriched.

    Example:
        from scripts import call_log_search
        df = call_log_search(
            auth_token=Config.CONVOSO_TOKEN,
            days_back_start=4,
            days_back_end=1,
            limit=20,
            status="MTS"
        )
    """

    if not auth_token:
        print("⚠️ No existe un auth token.")
        return pd.DataFrame()

    url = ConvosoEndpoints.CALL_LOGS_SEARCH_ENDPOINT

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

    if include_recordings == 1:
        if "recording" in df.columns:
            df["recording_link"] = df["recording"].apply(
                lambda r: (
                    extract_recording_url(json.loads(r))
                    if isinstance(r, str)
                    else extract_recording_url(r)
                )
            )

    # Filtrar columnas si se requiere
    if use_default_columns:
        final_columns = columns_required if columns_required else CALL_LOG_BASIC_COLUMNS
        print("FINAL COLUMNS___", final_columns)

        if include_recordings == 1:
            final_columns.append("recording_link")

        df = df[[col for col in final_columns if col in df.columns]]

    return df
