def create_lead(lead_data, list_id, max_retries=5, delay=2):
    url = "https://api.convoso.com/v1/leads/insert"
    data = {
        "auth_token": AUTH_TOKEN,
        "list_id": list_id,
        "phone_code": 1,
        "check_dup": 1,
        **lead_data,
    }
    return _post_with_retry(url, data, max_retries, delay)


def update_lead(lead_id, lead_data, list_id, max_retries=5, delay=2):
    url = "https://api.convoso.com/v1/leads/update"
    data = {
        "auth_token": AUTH_TOKEN,
        "lead_id": lead_id,
        "list_id": list_id,
        "status": "A",
        **lead_data,
    }
    return _post_with_retry(url, data, max_retries, delay)


def _post_with_retry(url, data, max_retries, delay):
    for attempt in range(max_retries):
        try:
            response = requests.post(url, data=data)
            return response.json()
        except requests.exceptions.ConnectionError:
            time.sleep(delay)
    return None
