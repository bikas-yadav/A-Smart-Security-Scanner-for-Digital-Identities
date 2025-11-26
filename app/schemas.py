from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from .models import EntityType

class EntityCreate(BaseModel):
    type: EntityType
    value: str = Field(..., min_length=2, max_length=255)

class EntityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: EntityType
    value: str
    description: Optional[str]
    risk_score: Optional[float]
    created_at: datetime

class GraphNode(BaseModel):
    id: str
    label: str
    value: str

class GraphEdge(BaseModel):
    source: str
    target: str
    type: str

class GraphResponse(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]

class SimilarEntity(BaseModel):
    entity: EntityResponse
    score: float

class SimilarResponse(BaseModel):
    results: List[SimilarEntity]

class RiskSummary(BaseModel):
    risk_level: str
    summary: str
    key_signals: List[str]
