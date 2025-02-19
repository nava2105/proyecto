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


def gran_m(c, A, b, restricciones, M=1e6):
    pasos_detallados = []
    try:
        num_variables = len(c)
        num_restricciones = len(A)

        # Contar el número de variables artificiales y de exceso
        num_artificiales = sum(1 for r in restricciones if r in ('>=', '='))
        num_variables_exceso = sum(1 for r in restricciones if r == '>=')
        num_variables_holgura = sum(1 for r in restricciones if r == '<=')

        # Crear la tabla inicial
        total_variables = num_variables + num_variables_holgura + num_variables_exceso + num_artificiales
        tabla = np.zeros((num_restricciones + 1, total_variables + 1))
        col_actual = num_variables

        # Inicializar c_ampliado con ceros para todas las columnas adicionales
        c_ampliado = list(c) + [0] * (num_variables_holgura + num_variables_exceso) + [M] * num_artificiales

        # Añadir variables de holgura, exceso y artificiales
        for i, restriccion in enumerate(restricciones):
            if restriccion == '<=':
                tabla[i, col_actual] = 1  # Holgura positiva
                col_actual += 1
            elif restriccion == '>=':
                tabla[i, col_actual] = -1  # Exceso negativa
                col_actual += 1
                tabla[i, col_actual] = 1   # Artificial positiva
                col_actual += 1
            elif restriccion == '=':
                tabla[i, col_actual] = 1   # Solo artificial
                col_actual += 1

        # Insertar restricciones en la tabla
        tabla[:-1, :num_variables] = A
        tabla[:-1, -1] = b

        # Configurar la función objetivo
        tabla[-1, :-1] = -np.array(c_ampliado, dtype=float)

        # Ajustar la fila Z restando M veces cada fila con variable artificial
        for i, restriccion in enumerate(restricciones):
            if restriccion in ('>=', '='):
                tabla[-1, :] -= M * tabla[i, :]

        # Continuar con el método Simplex
        iteracion = 0
        iteraciones = []

        while np.any(tabla[-1, :-1] < 0):
            iteracion += 1
            pasos_detallados.append(f"\n🔄 **Iteración {iteracion}:**")
            pasos_detallados.append("Tabla actual:")
            pasos_detallados.append(pd.DataFrame(tabla).to_string(index=False))

            # Selección de la columna pivote
            columna_pivote = np.argmin(tabla[-1, :-1])
            pasos_detallados.append(f"Selección de la columna pivote (variable entrante): Columna {columna_pivote}")

            # Ratios para seleccionar la fila pivote
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
            pasos_detallados.append(
                f"Normalización de la fila pivote: Dividiendo la fila {fila_pivote} por {tabla[fila_pivote, columna_pivote]}")
            tabla[fila_pivote, :] /= tabla[fila_pivote, columna_pivote]

            # Actualización de las demás filas
            for i in range(len(tabla)):
                if i != fila_pivote:
                    pasos_detallados.append(
                        f"Actualizando la fila {i}: Restando {tabla[i, columna_pivote]} veces la fila pivote")
                    tabla[i, :] -= tabla[i, columna_pivote] * tabla[fila_pivote, :]

            iteraciones.append(tabla.tolist())
            pasos_detallados.append("Tabla actualizada:")
            pasos_detallados.append(pd.DataFrame(tabla).to_string(index=False))

        # Extraer los valores óptimos
        solucion = np.zeros(num_variables)
        for i in range(num_restricciones):
            columna_variable_basica = -1
            for j in range(num_variables):
                if tabla[i, j] == 1 and np.all(tabla[:i, j] == 0) and np.all(tabla[i + 1:, j] == 0):
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


if __name__ == "__main__":
    # Prueba del método de la Gran M
    c = [3, 5]
    A = [[1, 1], [2, 3]]
    b = [10, 20]
    restricciones = ['<=', '=']

    resultado = gran_m(c, A, b, restricciones)

    print("\nResultado de la prueba:")
    print(resultado["estado"])
    if resultado["valores_óptimos"]:
        print("Valores óptimos:", resultado["valores_óptimos"])
        print("Valor de la función objetivo:", resultado["valor_funcion_objetivo"])

    print("\nPasos detallados:")
    for paso in resultado["pasos_detallados"]:
        print(paso)

    resultado = simplex_paso_a_paso(c, A, b)

    print("\nResultado de la prueba:")
    print(resultado["estado"])
    if resultado["valores_óptimos"]:
        print("Valores óptimos:", resultado["valores_óptimos"])
        print("Valor de la función objetivo:", resultado["valor_funcion_objetivo"])

    print("\nPasos detallados:")
    for paso in resultado["pasos_detallados"]:
        print(paso)