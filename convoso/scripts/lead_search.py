import json
import pandas as pd
import requests

from config import Config
from ..convoso_endpoints import ConvosoEndpoints
from .extract_field_notes import extract_fields
from ..fixtures import LEADS_BASIC_COLUMNS, LEAD_FIELD_MAPPING


def lead_search(
    auth_token="",
    columns_required=None,
    use_default_columns=True,
    limit=10,
    offset=0,
    timeout=15,
    **filters
):
    """
    Busca leads usando la API de Convoso con filtros dinámicos.

    Parámetros:
        columns_required (list): Lista personalizada de columnas a mantener.
        use_default_columns (bool): Si True, usa LEADS_BASIC_COLUMNS como filtro de columnas.
        limit(integer): Define cuantos elementos quieres obtener
        offset(integer): Define cuantos elementos quieres saltar
        timeout(integer): Tiempo maximo de espera
        **filters: Filtros dinámicos como lead_id, field_3 (solidity), list_id, etc.

    Retorna:
        pd.DataFrame con los leads encontrados.

    Example:
    from convoso import lead_search

    columns = [
        "lead_id",
        "status",
        "solidity",
    ]

    df_leads = lead_search(auth_token=auth_token, columns_required=columns,lead_id = call_log_lead_ids )
    """
    if not auth_token:
        print("⚠️ No existe un auth token.")
        return pd.DataFrame()

    url = ConvosoEndpoints.LEADS_SEARCH_ENDPOINT

    # Construcción del payload dinámico
    payload = {"auth_token": auth_token, "limit": limit, "offset": offset}
    for key, values in filters.items():
        if isinstance(values, list):
            payload[key] = ",".join(
                str(v) for v in values
            )  # convierte todos los elementos a str
        else:
            payload[key] = str(values)
    # print("🔍 Payload enviado:", payload)

    # Llamada a la API
    response = requests.post(
        url,
        data=payload,
        timeout=timeout,
    )
    result = response.json()

    lead_entries = result.get("data", {}).get("entries", [])
    if not lead_entries:
        print("⚠️ No se encontraron leads.")
        return pd.DataFrame()

    df = pd.DataFrame(lead_entries)

    # Renombrar columnas usando el mapping

    column_map = {v: k for k, v in LEAD_FIELD_MAPPING.items()}

    df.rename(columns=column_map, inplace=True)

    # Extraer campos desde la columna de notas
    if "notes" in df.columns:
        extracted_notes = df["notes"].apply(
            lambda x: extract_fields(x) if pd.notnull(x) else {}
        )
        df_notes = pd.DataFrame(extracted_notes.tolist())
        df = pd.concat([df, df_notes], axis=1)

    # Filtrar columnas si es necesario
    if use_default_columns:
        final_columns = columns_required if columns_required else LEADS_BASIC_COLUMNS
        print("FINAL COLUMNS__", final_columns)
        print("DF COLUMNS__", list(df.columns))
        columns_list = list(df.columns)
        with open("columns_snapshot.json", "w", encoding="utf-8") as f:
            json.dump(columns_list, f, ensure_ascii=False, indent=2)

        print("✅ Columnas guardadas en 'columns_snapshot.json'")

        df = df[[col for col in final_columns if col in df.columns]]

    return df
