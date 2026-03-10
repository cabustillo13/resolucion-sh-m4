from pydantic import BaseModel, Field
from typing import List


class ContractChangeOutput(BaseModel):
    """
    Modelo estructurado que describe los cambios detectados
    entre el contrato original y su enmienda.
    """

    sections_changed: List[str] = Field(
        description="Identificadores de las secciones del contrato que fueron modificadas"
    )

    topics_touched: List[str] = Field(
        description="Temas legales o comerciales afectados por la enmienda"
    )

    summary_of_the_change: str = Field(
        description="Descripción clara y precisa de los cambios introducidos"
    )
