from ._post_with_retry import _post_with_retry
from ..convoso_endpoints import ConvosoEndpoints


def update_lead(lead_data, list_id, lead_id, max_retries=5, delay=2, check_dup=0):

    url = ConvosoEndpoints.UPDATE_LEAD
    auth_token = ConvosoEndpoints.CONVOSO_TOKEN

    data = {
        "auth_token": auth_token,
        "lead_id": lead_id,
        "list_id": list_id,
        "phone_code": 1,
        **lead_data,
    }

    data["status"] = "RHSD"

    if check_dup != 0:
        data["check_dup"] = check_dup

    print("Updating Lead...")
    print("url___", url)
    print("auth_token___", auth_token)
    print("data___", data)

    return _post_with_retry(url, data, max_retries, delay)
