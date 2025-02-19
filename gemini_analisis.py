from google import genai
import json

class GeminiProcessor:
    def __init__(self, api_key):
        """
        Inicializa la conexión con la API de Gemini.

        :param api_key: Clave de la API de Google Gemini.
        """
        self.client = genai.Client(api_key=api_key)

    def analizar_sensibilidad(self, datos, tipo_problema):
        """
        Envía los datos a Gemini para analizar la sensibilidad de los resultados.

        :param datos: Diccionario con los datos del problema.
        :param tipo_problema: Tipo de optimización ("Programación Lineal", "Transporte", "Inventario", "Redes").
        :return: Respuesta del análisis de sensibilidad.
        """
        try:
            # Definir prompts detallados para cada tipo de problema
            prompts = {
                "Programación Lineal": (
                    f"Dado el siguiente problema de Programación Lineal:\n"
                    f"{json.dumps(datos, indent=2)}\n"
                    f"Analiza cómo cambian los resultados si los coeficientes de la función objetivo aumentan o disminuyen en un 10%. "
                    f"Explica cómo afecta la solución óptima y el valor de la función objetivo."
                ),
                "Transporte": (
                    f"Analiza el impacto en los costos de transporte y distribución para el siguiente problema:\n"
                    f"{json.dumps(datos, indent=2)}\n"
                    f"Considera un cambio del 15% en la oferta o demanda y evalúa cómo afecta la asignación de recursos y el costo total."
                ),
                "Inventario": (
                    f"Para este problema de gestión de inventarios:\n"
                    f"{json.dumps(datos, indent=2)}\n"
                    f"Evalúa cómo variaría el inventario de seguridad y la cantidad óptima de pedido si la demanda diaria cambia en un 20%."
                ),
                "Redes": (
                    f"Este problema optimiza rutas de distribución en una red de transporte:\n"
                    f"{json.dumps(datos, indent=2)}\n"
                    f"Analiza cómo cambiaría la ruta óptima si los costos de transporte aumentaran en un 5%. ¿Qué impacto tendría en la eficiencia?"
                ),
            }

            # Seleccionar el prompt correspondiente al tipo de problema
            prompt = prompts.get(tipo_problema, "Analiza la sensibilidad de estos datos.")

            # Enviar el prompt a Gemini
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            # Manejar y formatear la respuesta de Gemini
            if hasattr(response, "text"):
                return response.text.strip()
            else:
                return {"error": "Respuesta inesperada de Gemini."}

        except Exception as e:
            return {"error": f"Error en el análisis de sensibilidad: {str(e)}"}
