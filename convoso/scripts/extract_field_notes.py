def extract_fields(note):
    field_map = {
        "AREA:": "area",
        "SCHEDULE:": "schedule",
        "DATE OF THE CALL:": "call_date",
        "NAME:": "name",
        "HOMEOWNER:": "homeowner",
        "PHONE:": "phone",
        "ADDRESS:": "address",
        "JOB TITLE:": "job_title",
        "MORTGAGE:": "mortgage",
        "HOW MANY YEARS LEFT TO PAY:": "years_left",
        "CREDIT SCORE OF HOMEOWNER:": "credit_score",
        "PROJECT:": "project",
        "AGENT:": "agent",
        "CONFIRMED BY:": "confirmed_by",
        "LEAD ID:": "lead_id_notes",
        "LEAD SOURCE:": "lead_source",
        "NOTES:": "note_text",  # especial
    }

    result = {v: None for v in field_map.values()}
    notes_accumulator = []
    is_note_section = False

    for line in note.splitlines():
        line = line.strip()
        if not line:
            continue

        for prefix, key in field_map.items():
            if line.startswith(prefix):
                value = line[len(prefix) :].strip()
                if key == "note_text":
                    is_note_section = True
                    notes_accumulator.append(value)
                else:
                    result[key] = value
                break
        else:
            if is_note_section:
                notes_accumulator.append(line)

    if notes_accumulator:
        result["note_text"] = " ".join(notes_accumulator).strip()

    return result
