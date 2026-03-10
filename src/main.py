import argparse
import os
from dotenv import load_dotenv
from langfuse import Langfuse

from image_parser import parse_contract_image
from agents.contextualization_agent import ContextualizationAgent
from agents.extraction_agent import ExtractionAgent


# Cargar variables de entorno
load_dotenv()

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY")
)


def main(original_image: str, amendment_image: str):
    """Función principal que orquesta el análisis de contratos."""
    
    with langfuse.start_as_current_span(# pylint: disable=not-context-manager
        name="contract-analysis",
        input={
            "original_image": original_image,
            "amendment_image": amendment_image
        }
        ) as root_span:

        print("\n--- INICIO DEL ANÁLISIS DE CONTRATOS ---\n")

        # Parse contrato original
        span1 = langfuse.start_span(
            name="parse_original_contract",
            input={"image_path": original_image}
        )

        original_text = parse_contract_image(original_image)

        span1.update(output={"extracted_text": original_text[:500]})
        span1.end()

        # Parse contrato enmendado
        span2 = langfuse.start_span(
            name="parse_amendment_contract",
            input={"image_path": amendment_image}
        )

        amendment_text = parse_contract_image(amendment_image)

        span2.update(output={"extracted_text": amendment_text[:500]})
        span2.end()

        # Contextualización
        context_agent = ContextualizationAgent()

        span3 = langfuse.start_span(
            name="contextualization_agent"
        )

        context_map = context_agent.run(
            original_text,
            amendment_text
        )

        span3.update(output={"context_map": context_map[:500]})
        span3.end()

        # Extracción de cambios
        extraction_agent = ExtractionAgent()

        span4 = langfuse.start_span(
            name="extraction_agent"
        )

        result = extraction_agent.run(
            context_map,
            original_text,
            amendment_text
        )

        span4.update(output=result.model_dump())
        span4.end()

        root_span.update_trace(
            output=result.model_dump()
        )

        print("\n--- RESULTADO FINAL ---\n")
        print(result.model_dump_json(indent=2))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--original",
        required=True,
        help="Path del contrato original"
    )

    parser.add_argument(
        "--amendment",
        required=True,
        help="Path de la enmienda"
    )

    args = parser.parse_args()

    main(args.original, args.amendment)
