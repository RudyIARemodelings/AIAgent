def extract_fields(note):
    result = {
        "area": None,
        "schedule": None,
        "call_date": None,
        "name": None,
        "homeowner": None,
        "phone": None,
        "address": None,
        "job_title": None,
        "mortgage": None,
        "years_left": None,
        "credit_score": None,
        "project": None,
        "note_text": None,
        "agent": None,
        "confirmed_by": None,
        "lead_id": None,
        "lead_source": None,
    }

    lines = note.splitlines()
    notes_accumulator = []
    is_note_section = False

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("AREA:"):
            result["area"] = line.replace("AREA:", "").strip()
        elif line.startswith("SCHEDULE:"):
            result["schedule"] = line.replace("SCHEDULE:", "").strip()
        elif line.startswith("DATE OF THE CALL:"):
            result["call_date"] = line.replace("DATE OF THE CALL:", "").strip()
        elif line.startswith("NAME:"):
            result["name"] = line.replace("NAME:", "").strip()
        elif line.startswith("HOMEOWNER:"):
            result["homeowner"] = line.replace("HOMEOWNER:", "").strip()
        elif line.startswith("PHONE:"):
            result["phone"] = line.replace("PHONE:", "").strip()
        elif line.startswith("ADDRESS:"):
            result["address"] = line.replace("ADDRESS:", "").strip()
        elif line.startswith("JOB TITLE:"):
            result["job_title"] = line.replace("JOB TITLE:", "").strip()
        elif line.startswith("MORTGAGE:"):
            result["mortgage"] = line.replace("MORTGAGE:", "").strip()
        elif line.startswith("HOW MANY YEARS LEFT TO PAY:"):
            result["years_left"] = line.replace(
                "HOW MANY YEARS LEFT TO PAY:", ""
            ).strip()
        elif line.startswith("CREDIT SCORE OF HOMEOWNER:"):
            result["credit_score"] = line.replace(
                "CREDIT SCORE OF HOMEOWNER:", ""
            ).strip()
        elif line.startswith("PROJECT:"):
            result["project"] = line.replace("PROJECT:", "").strip()
        elif line.startswith("NOTES:"):
            is_note_section = True
            notes_accumulator.append(line.replace("NOTES:", "").strip())
        elif line.startswith("AGENT:"):
            is_note_section = False
            result["agent"] = line.replace("AGENT:", "").strip()
        elif line.startswith("CONFIRMED BY:"):
            result["confirmed_by"] = line.replace("CONFIRMED BY:", "").strip()
        elif line.startswith("LEAD ID:"):
            result["lead_id"] = line.replace("LEAD ID:", "").strip()
        elif line.startswith("LEAD SOURCE:"):
            result["lead_source"] = line.replace("LEAD SOURCE:", "").strip()
        elif is_note_section:
            notes_accumulator.append(line)

    if notes_accumulator:
        result["note_text"] = " ".join(notes_accumulator).strip()

    return result
