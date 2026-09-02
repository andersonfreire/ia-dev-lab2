from typing import List, Optional, Literal, Any
from pydantic import BaseModel, Field, model_validator

class ConfidenceScoreValidator(BaseModel):
    confidence_score: float = Field(
        ..., 
        ge=0.0, 
        le=1.0, 
        description="O valor de confidence_score deve estar no intervalo [0.0, 1.0]"
    )

class AuditPayload(ConfidenceScoreValidator):
    risk_classification: Literal["Baixo", "Médio", "Crítico"] = Field(
        ..., 
        description="Classificação de risco da predição"
    )
    explanations: Optional[List[Any]] = Field(
        default=None, 
        description="Objeto de explicabilidade (e.g. SHAP/LIME)"
    )

    @model_validator(mode='after')
    def validate_critical_risk(self):
        if self.risk_classification == "Crítico":
            if not self.explanations or len(self.explanations) == 0:
                raise ValueError('O array de explicabilidade não pode ser nulo ou vazio quando o risco for "Crítico".')
        return self
