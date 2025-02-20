import pandas as pd

def metodo_dos_fases(objetivo, restricciones, tipo_objetivo='max'):
    pasos_detallados = []
    try:
        df_fase1, variables_artificiales = crear_tabla_fase1(restricciones)
        df_fase1, iteraciones_fase1 = iterar_simplex(df_fase1, tipo_objetivo='min', fase=1)
        pasos_detallados.extend(iteraciones_fase1)

        if df_fase1.loc['Z', 'RHS'] != 0:
            return {
                "estado": "No hay solución factible",
                "valores_óptimos": None,
                "valor_funcion_objetivo": None,
                "iteraciones": pasos_detallados
            }

        df_fase2 = crear_tabla_fase2(df_fase1, objetivo, restricciones, tipo_objetivo, variables_artificiales)
        df_final, iteraciones_fase2 = iterar_simplex(df_fase2, tipo_objetivo)
        pasos_detallados.extend(iteraciones_fase2)

        resultado = mostrar_valores_finales(df_final)
        resultado['iteraciones'] = pasos_detallados

        return resultado

    except Exception as e:
        return {"estado": f"Error: {str(e)}"}


def crear_tabla_fase1(restricciones):
    variables_artificiales = []
    matriz = []

    for i, restriccion in enumerate(restricciones):
        fila = restriccion['coef'].copy()

        if restriccion['signo'] in ('=', '>='):
            var_artificial = f'a{i + 1}'
            fila[var_artificial] = 1
            variables_artificiales.append(var_artificial)

        fila['RHS'] = restriccion['rhs']
        matriz.append(fila)

    fila_objetivo = {var: 1 if var in variables_artificiales else 0 for var in matriz[0].keys()}
    fila_objetivo['Z'] = 1
    fila_objetivo['RHS'] = 0

    df = pd.DataFrame(matriz)
    df = df._append(pd.Series(fila_objetivo, name='Z'))

    return df, variables_artificiales


def crear_tabla_fase2(df_fase1, objetivo, restricciones, tipo_objetivo, variables_artificiales):
    df_fase2 = df_fase1.drop(columns=variables_artificiales)

    fila_objetivo = {var: -coef if tipo_objetivo == 'max' else coef for var, coef in objetivo.items()}
    for col in df_fase2.columns:
        fila_objetivo.setdefault(col, 0)
    fila_objetivo['Z'] = 1

    df_fase2.loc['Z'] = fila_objetivo

    return df_fase2


def iterar_simplex(df, tipo_objetivo='max', fase=2):
    iteracion = 1
    iteraciones = []

    while True:
        iteraciones.append(df.to_dict(orient='records'))

        col_entrante, fila_saliente = criterio_optimalidad(df, tipo_objetivo)
        if col_entrante is None or fila_saliente is None:
            break

        df = pivoteo(df, fila_saliente, col_entrante)
        iteracion += 1

    return df, iteraciones


def criterio_optimalidad(df, tipo_objetivo='max'):
    if tipo_objetivo == 'max':
        col_entrante = df.loc['Z'].drop(['RHS', 'Z']).idxmin()
        if df.loc['Z'][col_entrante] >= 0:
            return None, None
    else:
        col_entrante = df.loc['Z'].drop(['RHS', 'Z']).idxmax()
        if df.loc['Z'][col_entrante] <= 0:
            return None, None

    cocientes = []
    for index, row in df[:-1].iterrows():
        if row[col_entrante] > 0:
            cocientes.append((index, row['RHS'] / row[col_entrante]))
        else:
            cocientes.append((index, float('inf')))

    fila_saliente = min(cocientes, key=lambda x: x[1])[0]
    return col_entrante, fila_saliente


def pivoteo(df, fila_saliente, col_entrante):
    pivote = df.at[fila_saliente, col_entrante]
    df.loc[fila_saliente] = (df.loc[fila_saliente] / pivote).astype(float)

    for index, row in df.iterrows():
        if index != fila_saliente:
            factor = row[col_entrante]
            df.loc[index] = row - factor * df.loc[fila_saliente]

    return df


def mostrar_valores_finales(df):
    if any(df['RHS'][:-1] < 0):
        return {"estado": "No hay solución factible"}

    resultado = {}
    variables_decision = [col for col in df.columns if col.startswith('x')]

    for var in variables_decision:
        valor = 0
        for index, row in df[:-1].iterrows():
            if row[var] == 1 and all(row[v] == 0 for v in variables_decision if v != var):
                valor = row['RHS']
                break
        resultado[var] = valor

    resultado['Z'] = df.loc['Z', 'RHS']
    resultado['estado'] = "Optimización completada exitosamente"

    return resultado
