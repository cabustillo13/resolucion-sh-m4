import os
from openai import OpenAI
from models import ContractChangeOutput

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class ExtractionAgent:
    """
    Agente encargado de identificar los cambios entre el contrato original
    y la enmienda utilizando el mapa contextual generado previamente.
    """

    def run(self, context_map: str, original_text: str, amendment_text: str) -> ContractChangeOutput:

        completion = client.beta.chat.completions.parse(
            model="gpt-4o",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": """
                    Eres un auditor legal especializado en análisis de contratos.

                    Debes identificar cambios entre un contrato original
                    y su enmienda.

                    Clasifica los cambios en:

                    - cláusulas agregadas
                    - cláusulas eliminadas
                    - cláusulas modificadas

                    Debes producir un análisis claro y preciso.
                    """
                },
                {
                    "role": "user",
                    "content": f"""
                    MAPA CONTEXTUAL DEL DOCUMENTO

                    {context_map}


                    CONTRATO ORIGINAL

                    {original_text}


                    CONTRATO ENMENDADO

                    {amendment_text}
                    """
                }
            ],
            response_format=ContractChangeOutput,
        )

        # Devuelve directamente el objeto Pydantic validado
        result = completion.choices[0].message.parsed

        return result
