from ._post_with_retry import _post_with_retry
from ..convoso_endpoints import ConvosoEndpoints


def create_lead(lead_data, list_id, max_retries=5, delay=2, check_dup=0):

    url = ConvosoEndpoints.INSERT_LEAD
    auth_token = ConvosoEndpoints.CONVOSO_TOKEN

    data = {
        "auth_token": auth_token,
        "list_id": list_id,
        "phone_code": 1,
        **lead_data,
    }

    if check_dup != 0:
        data["check_dup"] = check_dup

    print("Creating Lead...")
    print("url___", url)
    print("auth_token___", auth_token)
    print("data___", data)
    return _post_with_retry(url, data, max_retries, delay)
