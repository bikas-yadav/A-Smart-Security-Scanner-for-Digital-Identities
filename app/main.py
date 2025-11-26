from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .config import settings
from .database import Base, engine, get_db
from . import models
from .schemas import (
    EntityCreate,
    EntityResponse,
    GraphResponse,
    GraphNode,
    GraphEdge,
    SimilarResponse,
    SimilarEntity,
    RiskSummary,
)
from .services import create_entity, fake_osint_enrichment
from .graph import graph_client
from .vector_store import vector_store
from .ai_summary import generate_risk_summary

# Create DB tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
)

@app.get("/")
def root():
    return {"message": "Secure Entity Scanner API", "docs": "/docs"}

@app.post("/scan", response_model=EntityResponse)
def scan_entity(payload: EntityCreate, db: Session = Depends(get_db)):
    """
    Create an entity, perform fake OSINT enrichment,
    create relations in graph, and index in vector store.
    """
    # Create base entity
    base_entity = create_entity(
        db,
        payload.type,
        payload.value,
        description=f"Scanned {payload.type.value}: {payload.value}",
    )

    # Enrich
    _ = fake_osint_enrichment(db, base_entity)

    return base_entity

@app.get("/entities/{entity_id}", response_model=EntityResponse)
def get_entity(entity_id: int, db: Session = Depends(get_db)):
    entity = db.query(models.Entity).filter(models.Entity.id == entity_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    return entity

@app.get("/entities", response_model=List[EntityResponse])
def list_entities(db: Session = Depends(get_db)):
    return db.query(models.Entity).order_by(models.Entity.id.desc()).limit(50).all()

@app.get("/entities/{entity_id}/graph", response_model=GraphResponse)
def get_entity_graph(entity_id: int):
    nodes_raw, edges_raw = graph_client.get_neighbors(entity_id)
    nodes = [GraphNode(**n) for n in nodes_raw]
    edges = [GraphEdge(**e) for e in edges_raw]
    return GraphResponse(nodes=nodes, edges=edges)

@app.get("/search", response_model=SimilarResponse)
def search_similar(query: str, db: Session = Depends(get_db)):
    """
    Semantic search using in-memory vector store.
    """
    results = vector_store.search(query, k=5)
    entities: List[SimilarEntity] = []
    for entity_id, score in results:
        entity = db.query(models.Entity).filter(models.Entity.id == entity_id).first()
        if entity:
            entities.append(
                SimilarEntity(
                    entity=entity,
                    score=score
                )
            )
    return SimilarResponse(results=entities)

@app.get("/entities/{entity_id}/summary", response_model=RiskSummary)
def get_risk_summary(entity_id: int, db: Session = Depends(get_db)):
    entity = db.query(models.Entity).filter(models.Entity.id == entity_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    # Get neighbors from graph
    nodes_raw, _ = graph_client.get_neighbors(entity_id)
    neighbor_ids = [int(n["id"]) for n in nodes_raw if n["id"] != str(entity_id)]
    related_entities = (
        db.query(models.Entity)
        .filter(models.Entity.id.in_(neighbor_ids))
        .all()
    )

    summary = generate_risk_summary(entity, related_entities)
    return summary
