from typing import List
from .config import settings
from .models import Entity
from .schemas import RiskSummary

import os

try:
    from openai import OpenAI
    _openai_available = True
except ImportError:
    _openai_available = False

def _rule_based_risk(entity: Entity) -> float:
    """
    Very simple rule-based risk score just for demo.
    """
    base = 0.3
    if entity.type.value in ("email", "username"):
        base += 0.2
    if entity.description and "breach" in entity.description.lower():
        base += 0.3
    return min(base, 1.0)

def generate_risk_summary(entity: Entity, related_entities: List[Entity]) -> RiskSummary:
    # If OpenAI key and library available: use LLM
    if settings.OPENAI_API_KEY and _openai_available:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        related_text = "\n".join(
            [f"- {e.type.value}: {e.value} ({e.description or 'no description'})"
             for e in related_entities]
        )
        prompt = f"""
You are an analyst in a cyber intelligence team.

Entity:
    type: {entity.type.value}
    value: {entity.value}
    description: {entity.description or 'N/A'}

Related entities:
{related_text or 'None'}

Task:
1. Rate overall risk as Low, Medium or High.
2. Give a short 3–4 line summary.
3. List 3 key signals justifying your assessment.
"""
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        text = completion.choices[0].message.content

        # For simplicity: just wrap whole output, not parsing deeply.
        return RiskSummary(
            risk_level="Unknown (LLM)",
            summary=text,
            key_signals=["LLM generated – see summary."]
        )

    # Fallback: simple rule-based summary
    risk_score = _rule_based_risk(entity)
    if risk_score < 0.4:
        level = "Low"
    elif risk_score < 0.7:
        level = "Medium"
    else:
        level = "High"

    summary = (
        f"This {entity.type.value} '{entity.value}' has an estimated {level} risk level "
        f"based on basic heuristic signals and its relationships."
    )
    signals = [
        f"Type is {entity.type.value}",
        f"Description mentions possible breach" if entity.description and "breach" in entity.description.lower() else "No explicit breach in description",
        f"{len(related_entities)} related entities detected in graph"
    ]

    return RiskSummary(
        risk_level=level,
        summary=summary,
        key_signals=signals,
    )
