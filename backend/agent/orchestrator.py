from __future__ import annotations

from typing import Any, Dict, Optional

from .config import DEFAULT_USER_ID
from .intent import detect_intent, extract_entities
from .models import AgentResponse
from .skills import build_plan, execute_intent


def route_intent(user_input: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Routes the user's intent to the appropriate skill and returns a structured response.
    """
    context = context or {}
    user_id = context.get("user_id") or DEFAULT_USER_ID

    detection = detect_intent(user_input)
    entities = extract_entities(user_input)
    entities = _merge_context(entities, context)

    plan = build_plan(detection["intent"])
    actions, message, warnings = execute_intent(detection["intent"], entities, user_id)

    status = _resolve_status(detection["intent"], actions)
    if detection["confidence"] < 0.4 and detection["intent"] != "unknown":
        warnings.append("low_confidence_intent")

    response = AgentResponse(
        status=status,
        intent=detection["intent"],
        confidence=detection["confidence"],
        entities=entities,
        plan=plan,
        actions=actions,
        message=message,
        warnings=warnings,
    )
    return response.model_dump()


def _resolve_status(intent_name: str, actions) -> str:
    if intent_name == "unknown" or not actions:
        return "failed"
    return "success" if all(action.success for action in actions) else "failed"


def _merge_context(entities: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    for key in ("location", "budget"):
        if key not in entities and context.get(key) is not None:
            entities[key] = context[key]
    return entities
