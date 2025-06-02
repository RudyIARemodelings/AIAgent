from config import Config
from convoso.convoso_endpoints import ConvosoEndpoints
from datetime import datetime, timedelta
import json
import pandas as pd

import requests

def get_audio_files():

    auth_token = Config.CONVOSO_TOKEN

    call_logs_url = ConvosoEndpoints.CALL_LOGS_ENDPOINT
    timeout_seconds=5

    start_date = (datetime.today() - timedelta(days=4)).strftime('%Y-%m-%d')
    start_time = f"{start_date} 01:00:00"

    end_date = (datetime.today()).strftime('%Y-%m-%d')
    end_time = f"{end_date} 23:59:59"

    mts_status = 'MTS'
    mtc_status = 'MTC - Meeting Confirmed'

    filter = {
        'auth_token' : auth_token,
        'start_time' : start_time,
        'end_time': end_time,
        'limit': 10,
        'include_recordings': 1,
        'status': mts_status
    }

    print('FILTERR___',filter)

    

    response = requests.post(call_logs_url, data=filter, timeout=timeout_seconds)

    result = response.text

    batch_data = json.loads(result)

    print('RESPONSE___',result)
    print('batch_data___',batch_data)

    all_results = []

    if batch_data.get('success') and batch_data['data'].get('results'):
        all_results.extend(batch_data['data']['results'])
        total_found = int(batch_data['data']['total_found'])
        print('TOTAL FOUND__', total_found)
    call_log = pd.DataFrame(all_results)
    call_log.to_csv("call_logs.csv", index=False, encoding="utf-8")

    unique_leads = call_log["lead_id"].dropna().astype(int).unique()
    lead_details = []

    for lead_id in unique_leads:
        payload = {
            "auth_token": auth_token,
            "lead_id": lead_id
        }

        try:
            lead_url = ConvosoEndpoints.LEADS_SEARCH_ENDPOINT
            response = requests.post(lead_url, data=payload, timeout=10)
            response.raise_for_status()
            result = response.json()

            # Puedes ajustar esto según la estructura exacta de la respuesta
            lead_data = result.get("data", {})
            lead_data["lead_id"] = lead_id  # Para mantener la referencia
            lead_details.append(lead_data)

        except Exception as e:
            print(f"Error con lead_id {lead_id}: {e}")
            continue

        sleep(0.2)  # Pequeña pausa para evitar rate limiting

    # Guardar resultados a CSV
    df_leads = pd.DataFrame(lead_details)
    df_leads.to_csv("lead_details.csv", index=False, encoding="utf-8")

    print("✅ Datos de leads guardados en 'lead_details.csv'")

    print(call_log.head())
 
