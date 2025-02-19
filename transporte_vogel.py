import numpy as np
import pandas as pd

def transporte_vogel(costos, oferta, demanda):
    """
    Resuelve el problema de transporte usando el Método de Vogel (VAM).
    Devuelve la solución y los pasos detallados.
    """
    pasos_detallados = []  # Lista para almacenar los pasos
    try:
        # Validar que la oferta total sea igual a la demanda total
        if sum(oferta) != sum(demanda):
            raise ValueError("La oferta total debe ser igual a la demanda total.")

        # Crear una copia de la matriz de costos, oferta y demanda
        costos = np.array(costos, dtype=float)
        oferta = np.array(oferta, dtype=float)
        demanda = np.array(demanda, dtype=float)

        # Inicializar la matriz de asignaciones
        asignaciones = np.zeros_like(costos)

        # Paso a paso del método de Vogel
        iteracion = 0
        while True:
            iteracion += 1
            paso = f"🔄 **Iteración {iteracion}:**\n"
            paso += f"- Oferta restante: {oferta}\n"
            paso += f"- Demanda restante: {demanda}\n"
            pasos_detallados.append(paso)

            # Verificar si la oferta y la demanda restantes son cero
            if np.all(oferta == 0) and np.all(demanda == 0):
                pasos_detallados.append("✅ Oferta y demanda restantes son cero. Terminando el bucle.\n")
                break

            # Calcular las penalizaciones para filas y columnas
            penalizaciones_filas = []
            for i in range(len(oferta)):
                if oferta[i] > 0:
                    fila = costos[i, :]
                    # Filtrar costos válidos (donde la demanda > 0)
                    fila_filtrada = fila[(fila > 0) & (demanda > 0)]
                    if len(fila_filtrada) >= 2:
                        fila_ordenada = np.sort(fila_filtrada)
                        penalizacion = fila_ordenada[1] - fila_ordenada[0]
                        penalizaciones_filas.append(penalizacion)
                        paso = f"- Penalización para fila {i}: {fila_ordenada[1]} - {fila_ordenada[0]} = {penalizacion}\n"
                        pasos_detallados.append(paso)
                    else:
                        penalizaciones_filas.append(0)
                else:
                    penalizaciones_filas.append(-1)

            penalizaciones_columnas = []
            for j in range(len(demanda)):
                if demanda[j] > 0:
                    columna = costos[:, j]
                    # Filtrar costos válidos (donde la oferta > 0)
                    columna_filtrada = columna[(columna > 0) & (oferta > 0)]
                    if len(columna_filtrada) >= 2:
                        columna_ordenada = np.sort(columna_filtrada)
                        penalizacion = columna_ordenada[1] - columna_ordenada[0]
                        penalizaciones_columnas.append(penalizacion)
                        paso = f"- Penalización para columna {j}: {columna_ordenada[1]} - {columna_ordenada[0]} = {penalizacion}\n"
                        pasos_detallados.append(paso)
                    else:
                        penalizaciones_columnas.append(0)
                else:
                    penalizaciones_columnas.append(-1)

            paso = f"- Penalizaciones de filas: {penalizaciones_filas}\n"
            paso += f"- Penalizaciones de columnas: {penalizaciones_columnas}\n"
            pasos_detallados.append(paso)

            # Encontrar la máxima penalización
            max_penalizacion_fila = max(penalizaciones_filas)
            max_penalizacion_columna = max(penalizaciones_columnas)

            if max_penalizacion_fila >= max_penalizacion_columna:
                fila_seleccionada = penalizaciones_filas.index(max_penalizacion_fila)
                # Seleccionar la columna con el menor costo en la fila seleccionada
                costos_fila = costos[fila_seleccionada, :].copy()
                costos_fila[demanda <= 0] = np.inf
                columna_seleccionada = np.argmin(costos_fila)
                paso = f"- Selección: Fila {fila_seleccionada} tiene la máxima penalización. Columna {columna_seleccionada} tiene el menor costo en esta fila.\n"
            else:
                columna_seleccionada = penalizaciones_columnas.index(max_penalizacion_columna)
                # Seleccionar la fila con el menor costo en la columna seleccionada
                costos_columna = costos[:, columna_seleccionada].copy()
                costos_columna[oferta <= 0] = np.inf
                fila_seleccionada = np.argmin(costos_columna)
                paso = f"- Selección: Columna {columna_seleccionada} tiene la máxima penalización. Fila {fila_seleccionada} tiene el menor costo en esta columna.\n"
            pasos_detallados.append(paso)

            # Asignar la cantidad máxima posible
            cantidad_asignada = min(oferta[fila_seleccionada], demanda[columna_seleccionada])
            if cantidad_asignada == 0:
                pasos_detallados.append("⚠ Cantidad asignada es cero. Buscando otra celda válida.\n")
                continue

            asignaciones[fila_seleccionada, columna_seleccionada] += cantidad_asignada

            # Actualizar oferta y demanda
            oferta[fila_seleccionada] -= cantidad_asignada
            demanda[columna_seleccionada] -= cantidad_asignada

            paso = f"- Asignación: {cantidad_asignada} unidades en ({fila_seleccionada}, {columna_seleccionada})\n"
            paso += f"- Oferta restante en fila {fila_seleccionada}: {oferta[fila_seleccionada]}\n"
            paso += f"- Demanda restante en columna {columna_seleccionada}: {demanda[columna_seleccionada]}\n"
            pasos_detallados.append(paso)

        # Calcular el costo total
        costo_total = np.sum(asignaciones * np.where(costos == np.inf, 0, costos))

        return {
            "estado": "Optimización completada exitosamente",
            "asignaciones": asignaciones.tolist(),
            "costo_total": costo_total,
            "pasos_detallados": pasos_detallados  # Devolver los pasos detallados
        }

    except Exception as e:
        return {
            "estado": f"Error en el cálculo: {str(e)}",
            "pasos_detallados": pasos_detallados
        }