import numpy as np

def metodo_costo_minimo(costos, oferta, demanda):
    """
    Implementa el Método del Costo Mínimo para resolver problemas de transporte.

    :param costos: Matriz de costos de transporte.
    :param oferta: Lista con la cantidad de producto disponible en cada origen.
    :param demanda: Lista con la cantidad requerida en cada destino.
    :return: Diccionario con la asignación óptima y el costo total.
    """
    try:
        costos = np.array(costos, dtype=float)
        oferta = np.array(oferta, dtype=float)
        demanda = np.array(demanda, dtype=float)

        # 📌 **Balancear el problema de transporte**
        total_oferta = np.sum(oferta)
        total_demanda = np.sum(demanda)

        if total_oferta > total_demanda:
            # Agregar un destino ficticio con demanda extra
            diferencia = total_oferta - total_demanda
            demanda = np.append(demanda, diferencia)
            costos = np.column_stack((costos, np.zeros(len(oferta))))
        elif total_demanda > total_oferta:
            # Agregar un origen ficticio con oferta extra
            diferencia = total_demanda - total_oferta
            oferta = np.append(oferta, diferencia)
            costos = np.vstack((costos, np.zeros(len(demanda))))

        filas, columnas = costos.shape
        asignacion = np.zeros((filas, columnas))

        while np.any(oferta > 0) and np.any(demanda > 0):
            # 📌 **Seleccionar la celda con menor costo**
            indices = np.where(costos == np.min(costos[costos > 0]))
            fila, columna = indices[0][0], indices[1][0]

            # 📌 **Asignar la cantidad mínima posible**
            cantidad = min(oferta[fila], demanda[columna])
            asignacion[fila, columna] = cantidad

            # 📌 **Actualizar oferta y demanda**
            oferta[fila] -= cantidad
            demanda[columna] -= cantidad

            # 📌 **Marcar fila o columna como agotada**
            if oferta[fila] == 0:
                costos[fila, :] = np.inf
            if demanda[columna] == 0:
                costos[:, columna] = np.inf

        costos = np.nan_to_num(costos, nan=0.0, posinf=0.0, neginf=0.0)  # Convertir inf/NaN a 0
        costo_total = np.sum(asignacion * costos)  # Multiplicación válida


        return {
            "estado": "Optimización completada exitosamente",
            "asignaciones": asignacion.tolist(),
            "costo_total": costo_total
        }

    except Exception as e:
        return {
            "estado": f"Error en el cálculo: {str(e)}",
            "asignaciones": None,
            "costo_total": None
        }
