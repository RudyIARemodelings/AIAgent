import pandas as pd


def get_validate_field(row, column, df, optional_fields, skip_optional=True):
    """
    Devuelve el valor de una columna, manejando opcionales y errores.

    - Si la columna es opcional y no existe → retorna None (si skip_optional=True)
    - Si la columna es opcional y no existe → lanza error (si skip_optional=False)
    - Si la columna existe pero está vacía → retorna None
    - Si es requerida y no existe → lanza error
    """
    if column in optional_fields:
        if column not in df.columns:
            if skip_optional:
                return None
            else:
                raise ValueError(
                    f"⛔ Falta la columna opcional '{column}' y skip_optional=False"
                )
    elif column not in df.columns:
        raise ValueError(f"⛔ Falta la columna requerida '{column}' en el DataFrame")

    value = row[column]
    if pd.isnull(value) or value == "":
        return None
    return value
