import numpy as np
import pandas as pd

def simplex_paso_a_paso(c, A, b):
    """
    Implementa el Método Simplex paso a paso y devuelve los pasos detallados.
    """
    pasos_detallados = []  # Lista para almacenar los pasos
    try:
        num_variables = len(c)
        num_restricciones = len(A)

        # Crear la tabla inicial del método Simplex
        tabla = np.zeros((num_restricciones + 1, num_variables + num_restricciones + 1))
        tabla[:-1, :-1] = np.hstack([A, np.eye(num_restricciones)])
        tabla[:-1, -1] = b
        tabla[-1, :-1] = np.concatenate([-np.array(c, dtype=float), np.zeros(num_restricciones)])

        iteracion = 0
        iteraciones = []

        while np.any(tabla[-1, :-1] < 0):
            iteracion += 1
            pasos_detallados.append(f"\n🔄 **Iteración {iteracion}:**")
            pasos_detallados.append("Tabla actual:")
            pasos_detallados.append(pd.DataFrame(tabla).to_string(index=False))

            # Selección de la columna pivote (variable entrante)
            columna_pivote = np.argmin(tabla[-1, :-1])
            pasos_detallados.append(f"Selección de la columna pivote (variable entrante): Columna {columna_pivote}")

            # Cálculo de los ratios para seleccionar la fila pivote (variable saliente)
            ratios = np.full(num_restricciones, np.inf)
            for i in range(num_restricciones):
                if tabla[i, columna_pivote] > 0:
                    ratios[i] = tabla[i, -1] / tabla[i, columna_pivote]

            if np.all(ratios == np.inf):
                pasos_detallados.append("El problema es ilimitado, no tiene solución óptima.")
                return {
                    "estado": "El problema es ilimitado, no tiene solución óptima.",
                    "valores_óptimos": None,
                    "valor_funcion_objetivo": None,
                    "iteraciones": iteraciones,
                    "pasos_detallados": pasos_detallados
                }

            fila_pivote = np.argmin(ratios)
            pasos_detallados.append(f"Selección de la fila pivote (variable saliente): Fila {fila_pivote}")

            # Normalización de la fila pivote
            pasos_detallados.append(f"Normalización de la fila pivote: Dividiendo la fila {fila_pivote} por {tabla[fila_pivote, columna_pivote]}")
            tabla[fila_pivote, :] /= tabla[fila_pivote, columna_pivote]

            # Actualización de las demás filas
            for i in range(len(tabla)):
                if i != fila_pivote:
                    pasos_detallados.append(f"Actualizando la fila {i}: Restando {tabla[i, columna_pivote]} veces la fila pivote")
                    tabla[i, :] -= tabla[i, columna_pivote] * tabla[fila_pivote, :]

            iteraciones.append(tabla.tolist())

            pasos_detallados.append("Tabla actualizada:")
            pasos_detallados.append(pd.DataFrame(tabla).to_string(index=False))

        # Extraer los valores óptimos
        solucion = np.zeros(num_variables)
        for i in range(num_restricciones):
            columna_variable_basica = -1
            for j in range(num_variables):
                if tabla[i, j] == 1 and np.all(tabla[:i, j] == 0) and np.all(tabla[i+1:, j] == 0):
                    columna_variable_basica = j
                    break

            if columna_variable_basica != -1:
                solucion[columna_variable_basica] = tabla[i, -1]

        pasos_detallados.append("\n✅ **Solución óptima encontrada:**")
        pasos_detallados.append(f"Valores óptimos de las variables: {solucion}")
        pasos_detallados.append(f"Valor de la función objetivo: {tabla[-1, -1]}")

        return {
            "estado": "Optimización completada exitosamente",
            "valores_óptimos": solucion.tolist(),
            "valor_funcion_objetivo": tabla[-1, -1],
            "iteraciones": iteraciones,
            "pasos_detallados": pasos_detallados
        }

    except Exception as e:
        return {"estado": f"Error en el cálculo: {str(e)}", "pasos_detallados": pasos_detallados}