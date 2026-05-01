from __future__ import annotations

import json
from datetime import datetime, timezone
from threading import Lock
from typing import Any, Dict, Optional

from .config import DEFAULT_PROFILE, STORE_PATH

_STORE_LOCK = Lock()


def _read_store() -> Dict[str, Any]:
    if not STORE_PATH.exists():
        return {"users": {}}
    with STORE_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def _write_store(store: Dict[str, Any]) -> None:
    STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with STORE_PATH.open("w", encoding="utf-8") as file:
        json.dump(store, file, indent=2, ensure_ascii=True)


def _get_or_create_user(store: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    users = store.setdefault("users", {})
    if user_id not in users:
        users[user_id] = {
            "profile": DEFAULT_PROFILE.copy(),
            "orders": [],
        }
    return users[user_id]


def get_user_profile(user_id: str) -> Dict[str, Any]:
    with _STORE_LOCK:
        store = _read_store()
        user = _get_or_create_user(store, user_id)
        _write_store(store)
        return user.get("profile", DEFAULT_PROFILE.copy())


def update_user_profile(user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    with _STORE_LOCK:
        store = _read_store()
        user = _get_or_create_user(store, user_id)
        profile = user.get("profile", {})
        profile.update(updates)
        user["profile"] = profile
        _write_store(store)
        return profile


def add_order(user_id: str, order: Dict[str, Any]) -> Dict[str, Any]:
    with _STORE_LOCK:
        store = _read_store()
        user = _get_or_create_user(store, user_id)
        timestamp = datetime.now(timezone.utc).isoformat()
        order_entry = {"timestamp": timestamp, **order}
        user.setdefault("orders", []).append(order_entry)
        _write_store(store)
        return order_entry


def get_last_order(user_id: str, intent: Optional[str] = None) -> Optional[Dict[str, Any]]:
    with _STORE_LOCK:
        store = _read_store()
        user = _get_or_create_user(store, user_id)
        orders = list(user.get("orders", []))
        if intent:
            orders = [order for order in orders if order.get("intent") == intent]
        return orders[-1] if orders else None
