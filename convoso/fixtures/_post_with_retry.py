import requests
import time


def _post_with_retry(url, data, max_retries, delay, timeout=15):
    for attempt in range(max_retries):
        try:
            response = requests.post(url, data=data, timeout=timeout)
            return response.json()
        except requests.exceptions.ConnectionError:
            time.sleep(delay)
    return None
