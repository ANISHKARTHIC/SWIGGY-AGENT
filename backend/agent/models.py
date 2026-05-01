from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .config import DEFAULT_USER_ID


class AgentRequest(BaseModel):
    input: str = Field(..., min_length=1, max_length=1000)
    user_id: str = Field(default=DEFAULT_USER_ID)
    auto_execute: bool = True
    channel: Optional[str] = "web"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class PlanStep(BaseModel):
    step: str
    status: str = "pending"
    details: Optional[Dict[str, Any]] = None


class ActionResult(BaseModel):
    provider: str
    action: str
    success: bool
    details: Dict[str, Any]


class AgentResponse(BaseModel):
    status: str
    intent: str
    confidence: float
    entities: Dict[str, Any]
    plan: List[PlanStep]
    actions: List[ActionResult]
    message: str
    warnings: List[str] = Field(default_factory=list)
