import numpy as np
from gemini_analisis import GeminiProcessor  # Importamos la clase de análisis de Gemini

# API Key de Gemini (reemplázala con tu clave real)
API_KEY = "AIzaSyDzJAY51jcAxoNl3dHsvnVUdPwO8KEPD_I"
gemini = GeminiProcessor(API_KEY)

def resolver_programacion_dinamica(n, valores):
    """
    Implementa un modelo de Programación Dinámica para optimización secuencial y envía los datos a Gemini para análisis de sensibilidad.

    :param n: Número de etapas en la optimización.
    :param valores: Matriz con los valores de decisión por etapa.
    :return: Diccionario con la solución óptima, su valor y el análisis de sensibilidad.
    """
    try:
        # Validación de entrada
        if not valores or n != len(valores):
            return {
                "estado": "Error: La cantidad de etapas no coincide con los valores ingresados",
                "solucion": None,
                "valor_optimo": None
            }

        dp = np.zeros(n)

        # Aplicamos un enfoque secuencial para maximizar el resultado
        for i in range(n):
            dp[i] = max(valores[i])

        valor_optimo = sum(dp)

        # Enviar datos a la IA de Gemini para análisis de sensibilidad
        datos_problema = {
            "numero_etapas": n,
            "valores_decision": valores,
            "solucion": dp.tolist(),
            "valor_optimo": valor_optimo
        }
        analisis_ia = gemini.analizar_sensibilidad(datos_problema, "Programación Dinámica")

        return {
            "solucion": dp.tolist(),
            "valor_optimo": valor_optimo,
            "analisis_sensibilidad": analisis_ia  # Se devuelve el análisis de Gemini
        }

    except Exception as e:
        return {
            "estado": f"Error en el cálculo: {str(e)}",
            "solucion": None,
            "valor_optimo": None
        }
