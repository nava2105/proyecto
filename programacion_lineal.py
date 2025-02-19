import numpy as np
import pandas as pd

def crear_tabla_inicial(c, A, b):
    num_variables = len(c)
    num_restricciones = len(A)
    tabla = np.zeros((num_restricciones + 1, num_variables + num_restricciones + 1))
    tabla[:-1, :-1] = np.hstack([A, np.eye(num_restricciones)])
    tabla[:-1, -1] = b
    tabla[-1, :-1] = np.concatenate([-np.array(c, dtype=float), np.zeros(num_restricciones)])
    return tabla


def seleccionar_columna_pivote(tabla):
    return np.argmin(tabla[-1, :-1])


def calcular_ratios(tabla, columna_pivote):
    num_restricciones = tabla.shape[0] - 1
    ratios = np.full(num_restricciones, np.inf)
    for i in range(num_restricciones):
        if tabla[i, columna_pivote] > 0:  # Solo considera valores positivos
            ratios[i] = tabla[i, -1] / tabla[i, columna_pivote]
    return ratios


def normalizar_fila_pivote(tabla, fila_pivote, columna_pivote):
    tabla[fila_pivote, :] /= tabla[fila_pivote, columna_pivote]


def actualizar_filas(tabla, fila_pivote, columna_pivote):
    for i in range(len(tabla)):
        if i != fila_pivote:
            tabla[i, :] -= tabla[i, columna_pivote] * tabla[fila_pivote, :]


def extraer_solucion(tabla, num_variables, num_restricciones):
    solucion = np.zeros(num_variables)
    for i in range(num_restricciones):
        columna_variable_basica = -1
        for j in range(num_variables):
            if tabla[i, j] == 1 and np.all(tabla[:i, j] == 0) and np.all(tabla[i + 1:, j] == 0):
                columna_variable_basica = j
                break
        if columna_variable_basica != -1:
            solucion[columna_variable_basica] = tabla[i, -1]
    return solucion


def simplex_paso_a_paso(c, A, b):
    pasos_detallados = []
    try:
        tabla = crear_tabla_inicial(c, A, b)
        num_variables = len(c)
        num_restricciones = len(A)
        iteracion = 0
        iteraciones = []

        while np.any(tabla[-1, :-1] < 0):
            iteracion += 1
            pasos_detallados.append(f"\n🔄 **Iteración {iteracion}:**")
            pasos_detallados.append(pd.DataFrame(tabla).to_string(index=False))

            columna_pivote = seleccionar_columna_pivote(tabla)
            pasos_detallados.append(f"Columna pivote: {columna_pivote}")

            ratios = calcular_ratios(tabla, columna_pivote)
            if np.all(ratios == np.inf):
                return {
                    "estado": "El problema es ilimitado, no tiene solución óptima.",
                    "valores_óptimos": None,
                    "valor_funcion_objetivo": None,
                    "iteraciones": iteraciones,
                    "pasos_detallados": pasos_detallados
                }

            fila_pivote = np.argmin(ratios)
            pasos_detallados.append(f"Fila pivote: {fila_pivote}")

            normalizar_fila_pivote(tabla, fila_pivote, columna_pivote)
            actualizar_filas(tabla, fila_pivote, columna_pivote)

            iteraciones.append(tabla.tolist())
            pasos_detallados.append(pd.DataFrame(tabla).to_string(index=False))

        solucion = extraer_solucion(tabla, num_variables, num_restricciones)
        pasos_detallados.append(f"Valores óptimos: {solucion}")
        pasos_detallados.append(f"Valor objetivo: {tabla[-1, -1]}")

        return {
            "estado": "Optimización completada exitosamente",
            "valores_óptimos": solucion.tolist(),
            "valor_funcion_objetivo": tabla[-1, -1],
            "iteraciones": iteraciones,
            "pasos_detallados": pasos_detallados
        }

    except Exception as e:
        return {"estado": f"Error: {str(e)}", "pasos_detallados": pasos_detallados}
