from typing import List, Tuple
from sqlalchemy.orm import Session
from .models import Entity, EntityType
from .graph import graph_client
from .vector_store import vector_store

def create_entity(
    db: Session,
    type_: EntityType,
    value: str,
    description: str | None = None,
    risk_score: float | None = None,
) -> Entity:
    entity = Entity(
        type=type_,
        value=value,
        description=description,
        risk_score=risk_score,
    )
    db.add(entity)
    db.commit()
    db.refresh(entity)

    # Sync with graph & vector
    graph_client.upsert_entity_node(entity.id, entity.type.value, entity.value)
    vector_store.add_or_update(entity)
    return entity

def fake_osint_enrichment(db: Session, base_entity: Entity) -> List[Tuple[Entity, str]]:
    """
    Fake OSINT: create a few deterministic related entities + relationship types.
    Returns list of (entity, relation_type)
    """
    related: List[Tuple[Entity, str]] = []

    if base_entity.type == EntityType.email:
        # username from local-part
        username_str = base_entity.value.split("@")[0]
        username_entity = create_entity(
            db,
            EntityType.username,
            username_str,
            description=f"Username derived from {base_entity.value}",
        )
        related.append((username_entity, "USES"))

        # domain
        domain_str = base_entity.value.split("@")[1]
        domain_entity = create_entity(
            db,
            EntityType.domain,
            domain_str,
            description=f"Domain extracted from {base_entity.value}",
        )
        related.append((domain_entity, "REGISTERED_AT"))

        # breach
        breach_entity = create_entity(
            db,
            EntityType.breach,
            f"{domain_str}-breach-2023",
            description=f"Simulated breach record involving {domain_str}",
        )
        related.append((breach_entity, "APPEARS_IN"))

    elif base_entity.type == EntityType.username:
        # Mock related domain and breach
        domain_entity = create_entity(
            db,
            EntityType.domain,
            "example.com",
            description="Default related domain for username",
        )
        related.append((domain_entity, "USES"))

    elif base_entity.type == EntityType.phone:
        breach_entity = create_entity(
            db,
            EntityType.breach,
            "phone-breach-collection",
            description="Simulated phone leak collection",
        )
        related.append((breach_entity, "APPEARS_IN"))

    # Create relationships in graph
    for ent, rel in related:
        graph_client.create_relation(base_entity.id, ent.id, rel)

    return related

def get_related_entities(db: Session, entity_ids: List[int]) -> List[Entity]:
    if not entity_ids:
        return []
    return db.query(Entity).filter(Entity.id.in__(entity_ids)).all()
