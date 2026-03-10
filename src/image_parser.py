import os
import base64
from openai import OpenAI
from dotenv import load_dotenv


# Carga las variables de entorno desde el archivo .env
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def encode_image(image_path: str) -> str:
    """Convierte una imagen a base64."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def parse_contract_image(image_path: str) -> str:
    """
    Extrae el texto de un contrato usando un modelo multimodal.
    """

    base64_img = encode_image(image_path)

    completion = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": """
                Eres un asistente especializado en lectura de contratos.

                Tu tarea es transcribir todo el texto del documento
                manteniendo la estructura de secciones y cláusulas.
                """
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extrae todo el texto del contrato en la imagen."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_img}",
                            "detail": "high"
                        }
                    }
                ]
            }
        ],
    )

    extracted_text = completion.choices[0].message.content

    return extracted_text
