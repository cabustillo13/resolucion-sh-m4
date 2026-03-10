import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class ContextualizationAgent:
    """
    Agente encargado de comprender la estructura de ambos contratos
    antes de detectar los cambios.
    """

    def run(self, original_text: str, amendment_text: str) -> str:
        """
        Genera un mapa contextual que describe cómo se relacionan
        las secciones de ambos documentos.
        """

        completion = client.chat.completions.create(
            model="gpt-4o",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": """
                    Eres un analista legal senior especializado en revisión de contratos.

                    Tu tarea NO es detectar cambios todavía.

                    Primero debes analizar dos versiones de un contrato para
                    comprender su estructura y contexto.

                    Debes identificar:

                    - Qué secciones existen en ambos documentos
                    - Cómo se corresponden entre sí
                    - El propósito general de cada sección

                    Devuelve un análisis estructurado y claro que sirva
                    como mapa contextual para otro sistema que luego
                    detectará los cambios.
                    """
                },
                {
                    "role": "user",
                    "content": f"""
                    CONTRATO ORIGINAL

                    {original_text}


                    CONTRATO ENMENDADO / ADENDA

                    {amendment_text}
                    """
                }
            ],
        )

        return completion.choices[0].message.content
