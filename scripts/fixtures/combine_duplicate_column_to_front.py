def combine_duplicate_column_to_front(df, column_name):
    # Obtener las columnas que coinciden con el nombre base
    matching_cols = [col for col in df.columns if col.split(".")[0] == column_name]

    if len(matching_cols) <= 1:
        print(f"No hay columnas duplicadas de '{column_name}' para combinar.")
        return df

    # Extraer las columnas y combinarlas
    combined = df[matching_cols].bfill(axis=1).iloc[:, 0].tolist()

    # Eliminar todas las columnas repetidas
    df = df.drop(columns=matching_cols)

    # Insertar la columna combinada al inicio
    df.insert(0, column_name, combined)

    return df
