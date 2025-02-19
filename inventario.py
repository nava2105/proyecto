def inventario_programacion_dinamica(demanda, costo_pedido, costo_almacenamiento, capacidad_maxima, inventario_inicial):
    """
    Resuelve el problema de inventario usando programación dinámica.
    """
    num_semanas = len(demanda)
    costos = [[float('inf')] * (capacidad_maxima + 1) for _ in range(num_semanas + 1)]
    decisiones = [[0] * (capacidad_maxima + 1) for _ in range(num_semanas + 1)]

    # Inicialización
    costos[0][inventario_inicial] = 0

    # Programación dinámica
    for t in range(num_semanas):
        for I in range(capacidad_maxima + 1):
            if costos[t][I] != float('inf'):
                for x in range(max(0, demanda[t] - I), capacidad_maxima - I + demanda[t] + 1):
                    I_next = I + x - demanda[t]
                    if 0 <= I_next <= capacidad_maxima:
                        costo_total = costos[t][I] + (costo_pedido if x > 0 else 0) + costo_almacenamiento * I_next
                        if costo_total < costos[t + 1][I_next]:
                            costos[t + 1][I_next] = costo_total
                            decisiones[t + 1][I_next] = x

    # Recuperar la política óptima
    politica_optima = []
    I = 0
    for t in range(num_semanas, 0, -1):
        x = decisiones[t][I]
        politica_optima.append((t, x, I))
        I = I - x + demanda[t - 1]

    politica_optima.reverse()

    # Calcular el costo total mínimo
    costo_total_minimo = min(costos[num_semanas])

    # Preparar los pasos detallados
    pasos = [
        "1. Modelo matemático del problema de inventario:",
        "   Minimizar Z = ∑(C_p * δ(x_t) + C_a * I_t) para todas las semanas t.",
        "   Sujeto a:",
        "   - I_{t+1} = I_t + x_t - d_t.",
        "   - I_t ≥ 0.",
        "   - I_t ≤ capacidad máxima.",
        f"2. Política óptima de pedidos:",
    ]
    for t, x, I in politica_optima:
        pasos.append(f"   - Semana {t}: Pedir {x} unidades. Inventario final: {I}.")
    pasos.append(f"3. Costo total mínimo: {costo_total_minimo}.")

    return pasos