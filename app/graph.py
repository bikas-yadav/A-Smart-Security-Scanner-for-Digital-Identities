from typing import List
from neo4j import GraphDatabase, Driver
from .config import settings

# Simple Neo4j client

class GraphClient:
    def __init__(self):
        self._driver: Driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )

    def close(self):
        self._driver.close()

    def upsert_entity_node(self, entity_id: int, entity_type: str, value: str):
        with self._driver.session() as session:
            session.run(
                """
                MERGE (e:Entity {id: $id})
                SET e.type = $type, e.value = $value
                """,
                id=str(entity_id),
                type=entity_type,
                value=value,
            )

    def create_relation(self, source_id: int, target_id: int, rel_type: str):
        with self._driver.session() as session:
            session.run(
                """
                MATCH (s:Entity {id: $source_id})
                MATCH (t:Entity {id: $target_id})
                MERGE (s)-[r:%s]->(t)
                """ % rel_type,
                source_id=str(source_id),
                target_id=str(target_id),
            )

    def get_neighbors(self, entity_id: int):
        with self._driver.session() as session:
            result = session.run(
                """
                MATCH (center:Entity {id: $id})-[r]-(neighbor:Entity)
                RETURN center, r, neighbor
                """,
                id=str(entity_id),
            )
            nodes = {}
            edges = []
            for record in result:
                center = record["center"]
                neighbor = record["neighbor"]
                rel = record["r"]

                nodes[center["id"]] = {
                    "id": center["id"],
                    "label": center.get("type", "Entity"),
                    "value": center.get("value", ""),
                }
                nodes[neighbor["id"]] = {
                    "id": neighbor["id"],
                    "label": neighbor.get("type", "Entity"),
                    "value": neighbor.get("value", ""),
                }
                edges.append(
                    {
                        "source": center["id"],
                        "target": neighbor["id"],
                        "type": type(rel).__name__,
                    }
                )
            return list(nodes.values()), edges

graph_client = GraphClient()
