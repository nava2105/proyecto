from programacion_lineal import simplex_paso_a_paso

def main():
    # Datos de prueba para el método Simplex
    c = [3, 2]  # Coeficientes de la función objetivo
    A = [
        [1, 2],
        [1, 1]
    ]  # Coeficientes de las restricciones
    b = [4, 3]  # Lados derechos de las restricciones

    # Llamada a la función simplex_paso_a_paso
    resultado = simplex_paso_a_paso(c, A, b)

    # Mostrar los resultados
    print("\nResultado del Método Simplex:")
    print(f"Estado: {resultado['estado']}")
    if resultado['valores_óptimos'] is not None:
        print(f"Valores óptimos: {resultado['valores_óptimos']}")
        print(f"Valor de la función objetivo: {resultado['valor_funcion_objetivo']}")

    print("\nPasos detallados:")
    for paso in resultado['pasos_detallados']:
        print(paso)

if __name__ == "__main__":
    main()