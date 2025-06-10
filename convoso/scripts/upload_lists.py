import pandas as pd
from .lead_search import lead_search
from datetime import datetime, date
from convoso.fixtures.get_validate_field import get_validate_field
from ..fixtures.create_lead import create_lead
from ..fixtures.update_lead import update_lead


def upload_lists(
    df,
    date,
    meetings_status,
    list_id,
    auth_token,
    required_fields,
    optional_fields,
    skip_optional=True,
    check_dup_create=0,
    check_dup_update=0,
):
    """
    Sube leads a Convoso, creando o actualizando según estado de reunión.

    Parámetros:
    - df (DataFrame): Datos de leads.
    - today_date (date): Fecha actual.
    - meetings_status (list): Lista de estados con citas activas.
    - list_id (int): ID de la lista Convoso.
    - auth_token (str): Token de autenticación de Convoso.
    - skip_optional (bool): Si True, omite campos faltantes opcionales.
    """

    missing_required_columns = [col for col in required_fields if col not in df.columns]
    if missing_required_columns:
        raise ValueError(f"⛔ Faltan columnas requeridas: {missing_required_columns}")

    # 🧪 Validación de columnas opcionales
    missing_optional_columns = [col for col in optional_fields if col not in df.columns]
    if missing_optional_columns and not skip_optional:
        raise ValueError(
            f"⛔ Faltan columnas opcionales: {missing_optional_columns}. Usa skip_optional=True para ignorar."
        )

    for _, row in df.iterrows():

        missing_required = [
            field
            for field in required_fields
            if field not in row or pd.isnull(row[field])
        ]

        if missing_required:
            print(
                f"⛔ Faltan campos requeridos: {missing_required}. Se omite este lead."
            )
            continue

        lead = {
            "first_name": get_validate_field(
                row, "name", df, optional_fields, skip_optional
            ),
            "phone_number": int(
                get_validate_field(row, "phone1", df, optional_fields, skip_optional)
            ),
            "address1": get_validate_field(
                row, "address", df, optional_fields, skip_optional
            ),
            "city": get_validate_field(row, "city", df, optional_fields, skip_optional),
            "state": get_validate_field(
                row, "state", df, optional_fields, skip_optional
            ),
            "postal_code": get_validate_field(
                row, "zip", df, optional_fields, skip_optional
            ),
            "job_group": get_validate_field(
                row, "job", df, optional_fields, skip_optional
            ),
        }

        phone = int(row["phone1"])
        df_result = lead_search(
            auth_token=auth_token,
            columns_required=[
                "lead_id",
                "status",
                "appointment_date_and_time",
                "called_count",
                "notes",
            ],
            limit=10,
            use_default_columns=True,
            phone_number=phone,
        )

        if df_result.empty:
            create_lead(lead, list_id, check_dup=check_dup_create)
        else:
            df_result["called_count"] = pd.to_numeric(
                df_result["called_count"], errors="coerce"
            ).fillna(0)
            best = df_result.loc[df_result["called_count"].idxmax()]
            app_date_str = best.get("appointment_date_and_time")
            status = best.get("status")

            app_date = (
                datetime.strptime(app_date_str, "%Y-%m-%d %H:%M:%S").date()
                if pd.notnull(app_date_str)
                else datetime(1970, 1, 1).date()
            )

            if date > app_date and status not in meetings_status:
                update_lead(lead, list_id, best["lead_id"], check_dup=check_dup_update)
