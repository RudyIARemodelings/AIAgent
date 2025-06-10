import time
import pandas as pd
import requests
from tqdm import tqdm
from datetime import datetime, date

#    values_list = [name,phone1,phone2,address,city,state,zip_code,job]


def create_lead(
    list_id, values_list, max_retries=5, delay=2
):  # values = [first_name, last_name, phone, email, address,job]
    insert_lead_url = "https://api.convoso.com/v1/leads/insert"
    for attempt in range(max_retries):
        try:
            first_name = values_list[0]
            phone = values_list[1]
            address = values_list[3]
            city = values_list[4]
            state = values_list[5]
            zip_code = values_list[6]
            job = values_list[7]
            post_lead_data = {
                "auth_token": "4fu4ldxttx3dzyx6x2f153y3yvwd7v81",
                "list_id": list_id,
                "first_name": first_name,
                #'last_name': last_name,
                "phone_code": 1,
                "phone_number": phone,
                "address1": address,
                "city": city,
                "state": state,
                "postal_code": zip_code,
                "job_group": job,
                "check_dup": 1,
            }

            response = requests.post(insert_lead_url, data=post_lead_data)
            break
        except requests.exceptions.ConnectionError as e:
            print(
                f"ConnectionError occurred: {e}. Retrying ({attempt + 1}/{max_retries})..."
            )
            time.sleep(delay)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break


#    values_list = [name,phone1,phone2,address,city,state,zip_code,job]


def update_lead(convoso_lead, values_list, list_id, max_retries=5, delay=2):
    update_lead_url = "https://api.convoso.com/v1/leads/update"
    for attempt in range(max_retries):
        try:
            first_name = values_list[0]
            phone = values_list[1]
            address = values_list[3]
            city = values_list[4]
            state = values_list[5]
            zip_code = values_list[6]
            job = values_list[7]
            update_lead_data = {
                "auth_token": "4fu4ldxttx3dzyx6x2f153y3yvwd7v81",
                "lead_id": convoso_lead,
                "list_id": list_id,
                "status": "A",
                "first_name": first_name,
                "last_name": "",
                "phone_number": phone,
                "address1": address,
                "city": city,
                "state": state,
                "postal_code": zip_code,
                "job_group": job,
            }
            response = requests.post(update_lead_url, data=update_lead_data)
            break
            # print(response.json())
        except requests.exceptions.ConnectionError as e:
            print(
                f"ConnectionError occurred: {e}. Retrying ({attempt + 1}/{max_retries})..."
            )
            time.sleep(delay)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break


def search_lead(phone, max_retries=5, delay=2):
    get_lead_url = "https://api.convoso.com/v1/leads/search"

    get_lead_data = {
        "auth_token": "4fu4ldxttx3dzyx6x2f153y3yvwd7v81",
        "phone_number": phone,
    }
    for attempt in range(max_retries):
        try:
            # Make the POST request
            response = requests.post(get_lead_url, data=get_lead_data, timeout=5)
            return response.json()
        except requests.exceptions.ConnectionError as e:
            print(
                f"ConnectionError occurred: {e}. Retrying ({attempt + 1}/{max_retries})..."
            )
            time.sleep(delay)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break


def process_leads(values_list, list_id, today):
    phone = values_list[1]
    convoso_data = search_lead(phone)
    try:
        if int(convoso_data["data"]["total"]) == 1:
            try:
                app_datetime = convoso_data["data"]["entries"][0]["field_81"]
                app_date = datetime.strptime(app_datetime, "%Y-%m-%d %H:%M:%S").date()
                status = convoso_data["data"]["entries"][0]["status"]
            except:
                app_date = date(1970, 1, 1)
                status = convoso_data["data"]["entries"][0]["status"]
            if today > app_date and status not in meeting_status:
                convoso_lead = convoso_data["data"]["entries"][0]["id"]
                update_lead(
                    convoso_lead, values_list, list_id
                )  # TOP PROS CONTRACTOR APPT OCT-N

        elif int(convoso_data["data"]["total"]) > 1:
            max_entry = max(
                convoso_data["data"]["entries"], key=lambda entry: entry["called_count"]
            )
            convoso_lead = max_entry["id"]
            try:
                app_datetime = max_entry["field_81"]
                app_date = datetime.strptime(app_datetime, "%Y-%m-%d %H:%M:%S").date()
                status = max_entry["status"]
            except:
                app_date = date(1970, 1, 1)
                status = max_entry["status"]
            if today > app_date and status not in meeting_status:
                update_lead(
                    convoso_lead, values_list, list_id
                )  # TOP PROS CONTRACTOR APPT OCT-N
        else:
            create_lead(list_id, values_list)
    except:
        print(phone, " - ", convoso_data)


df = pd.read_csv(
    r"C:\Users\IA\Documents\IARemodeling\Projects\1Convoso\files\1_estimate_guide_final.csv"
)
# Get today's date
today = datetime.today()

meeting_status = ["MTS", "MTC", "SCFU", "CCFU"]

for i in tqdm(range(len(df)), "Loading..."):
    name = df.loc[i, "name"]
    phone1 = int(df.loc[i, "phone1"])
    phone2 = df.loc[i, "phone2"]
    address = df.loc[i, "address"]
    city = df.loc[i, "city"]
    state = df.loc[i, "state"]
    zip_code = df.loc[i, "zip"]
    job = df.loc[i, "job"]

    values_list = [name, phone1, phone2, address, city, state, zip_code, job]

    process_leads(values_list, 9707, today.date())
