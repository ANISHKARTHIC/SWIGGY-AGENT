from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .config import SWIGGY_API_BASE_URL, SWIGGY_MODE


class SwiggyClientBase:
    def place_food_order(
        self,
        *,
        restaurant: str,
        items: List[str],
        time: str,
        budget: Optional[int],
        address: str,
        instructions: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        raise NotImplementedError

    def place_grocery_order(
        self,
        *,
        items: List[str],
        time: str,
        budget: Optional[int],
        address: str,
    ) -> Dict[str, Any]:
        raise NotImplementedError

    def book_dining(
        self,
        *,
        restaurant: str,
        time: str,
        date: Optional[str],
        party_size: int,
        budget: Optional[int],
    ) -> Dict[str, Any]:
        raise NotImplementedError

    def track_order(self, order_id: str) -> Dict[str, Any]:
        raise NotImplementedError

    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        raise NotImplementedError


class MockSwiggyClient(SwiggyClientBase):
    def __init__(self) -> None:
        self.base_url = SWIGGY_API_BASE_URL

    def _new_id(self, prefix: str) -> str:
        return f"{prefix}-{uuid.uuid4().hex[:8].upper()}"

    def _is_scheduled(self, time_value: str) -> bool:
        normalized = (time_value or "").lower()
        return normalized not in {"now", "asap", ""}

    def place_food_order(
        self,
        *,
        restaurant: str,
        items: List[str],
        time: str,
        budget: Optional[int],
        address: str,
        instructions: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        scheduled = self._is_scheduled(time)
        return {
            "order_id": self._new_id("FOOD"),
            "status": "confirmed",
            "restaurant": restaurant,
            "items": items,
            "delivery_address": address,
            "budget": budget,
            "scheduled": scheduled,
            "scheduled_time": time if scheduled else "now",
            "eta_minutes": 30 if not scheduled else None,
            "instructions": instructions or [],
        }

    def place_grocery_order(
        self,
        *,
        items: List[str],
        time: str,
        budget: Optional[int],
        address: str,
    ) -> Dict[str, Any]:
        scheduled = self._is_scheduled(time)
        return {
            "order_id": self._new_id("GROC"),
            "status": "confirmed",
            "store": "Instamart",
            "items": items,
            "delivery_address": address,
            "budget": budget,
            "scheduled": scheduled,
            "scheduled_time": time if scheduled else "now",
            "eta_minutes": 20 if not scheduled else None,
        }

    def book_dining(
        self,
        *,
        restaurant: str,
        time: str,
        date: Optional[str],
        party_size: int,
        budget: Optional[int],
    ) -> Dict[str, Any]:
        return {
            "reservation_id": self._new_id("DINE"),
            "status": "confirmed",
            "restaurant": restaurant,
            "time": time,
            "date": date or "today",
            "party_size": party_size,
            "budget": budget,
        }

    def track_order(self, order_id: str) -> Dict[str, Any]:
        return {
            "order_id": order_id,
            "status": "out_for_delivery",
            "eta_minutes": 18,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        return {
            "order_id": order_id,
            "status": "canceled",
            "refunded": True,
        }


def get_swiggy_client() -> SwiggyClientBase:
    if SWIGGY_MODE == "live":
        raise RuntimeError(
            "Live Swiggy integration is not configured. Set SWIGGY_MODE=mock or implement a live client."
        )
    return MockSwiggyClient()
