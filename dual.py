import pandas as pd


def crear_tabla_simplex(objetivo, restricciones, tipo_objetivo='max'):
    variables = list(objetivo.keys())
    slack_surplus_count = 1
    var_basicas = []
    matriz = []

    for restriccion in restricciones:
        fila = {var: restriccion['coef'].get(var, 0) for var in variables}

        if restriccion['signo'] == '<=':
            var_slack = f's{slack_surplus_count}'
            fila[var_slack] = 1
            var_basicas.append(var_slack)
            slack_surplus_count += 1
        elif restriccion['signo'] == '>=':
            var_surplus = f'e{slack_surplus_count}'
            fila[var_surplus] = -1
            var_basicas.append(var_surplus)
            slack_surplus_count += 1
        else:
            var_basicas.append(None)

        fila['RHS'] = restriccion['rhs']
        matriz.append(fila)

    todas_las_vars = list(matriz[0].keys()) if matriz else []
    todas_las_vars = [var for var in todas_las_vars if var != 'RHS'] + ['RHS']

    for fila in matriz:
        for var in todas_las_vars:
            fila.setdefault(var, 0)

    fila_objetivo = {var: -coef if tipo_objetivo == 'max' else coef for var, coef in objetivo.items()}
    for var in todas_las_vars:
        fila_objetivo.setdefault(var, 0)
    fila_objetivo['Z'] = 1

    df = pd.DataFrame(matriz, dtype=float)
    df = df[todas_las_vars]
    df = df._append(pd.Series(fila_objetivo, name='Z'))

    return df


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


def iterar_simplex(df, tipo_objetivo='max'):
    iteraciones = []

    while True:
        iteraciones.append(df.to_dict(orient='records'))

        col_entrante, fila_saliente = criterio_optimalidad(df, tipo_objetivo)
        if col_entrante is None or fila_saliente is None:
            break

        df = pivoteo(df, fila_saliente, col_entrante)

    return df, iteraciones


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


def convertir_a_dual(objetivo, restricciones, tipo_objetivo='max'):
    dual_objetivo = {f'y{i+1}': restriccion['rhs'] for i, restriccion in enumerate(restricciones)}
    dual_restricciones = []

    for var in objetivo.keys():
        coeficientes = {f'y{i+1}': restriccion['coef'].get(var, 0) for i, restriccion in enumerate(restricciones)}
        dual_restricciones.append({
            'coef': coeficientes,
            'signo': '<=' if tipo_objetivo == 'max' else '>=',
            'rhs': objetivo[var]
        })

    dual_tipo_objetivo = 'min' if tipo_objetivo == 'max' else 'max'

    return dual_objetivo, dual_restricciones, dual_tipo_objetivo


def resolver_metodo_dual(objetivo, restricciones, tipo_objetivo='max'):
    resultado_json = {}
    pasos_detallados = []

    dual_objetivo, dual_restricciones, dual_tipo_objetivo = convertir_a_dual(objetivo, restricciones, tipo_objetivo)
    resultado_json['dual_objetivo'] = dual_objetivo
    resultado_json['dual_restricciones'] = dual_restricciones

    df = crear_tabla_simplex(dual_objetivo, dual_restricciones, dual_tipo_objetivo)
    df_final, iteraciones = iterar_simplex(df, dual_tipo_objetivo)
    pasos_detallados.extend(iteraciones)

    resultado_final = mostrar_valores_finales(df_final)
    resultado_final['iteraciones'] = pasos_detallados

    return resultado_final


# =================== Ejemplo de Uso del Dual ===================
if __name__ == "__main__":
    objetivo = {'x1': 5, 'x2': 2}
    tipo_objetivo = 'max'

    restricciones = [
        {'coef': {'x1': 1, 'x2': 0}, 'signo': '<=', 'rhs': 4},
        {'coef': {'x1': 0, 'x2': 2}, 'signo': '<=', 'rhs': 12},
        {'coef': {'x1': 3, 'x2': 2}, 'signo': '<=', 'rhs': 18}
    ]

    resultado = resolver_metodo_dual(objetivo, restricciones, tipo_objetivo)
    print(resultado)
