from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from .config import DEFAULT_PROFILE
from .integrations import get_swiggy_client
from .memory import add_order, get_last_order, get_user_profile
from .models import ActionResult, PlanStep


def build_plan(intent_name: str) -> List[PlanStep]:
    if intent_name == "unknown":
        return []

    steps = [
        PlanStep(
            step="Resolve user context",
            status="pending",
            details={"sources": ["input", "profile"]},
        ),
        PlanStep(
            step=_step_label(intent_name),
            status="pending",
            details={"intent": intent_name},
        ),
    ]
    return steps


def execute_intent(
    intent_name: str, entities: Dict[str, Any], user_id: str
) -> Tuple[List[ActionResult], str, List[str]]:
    if intent_name == "unknown":
        return [], "Intent not understood. Try a clearer request.", ["unknown_intent"]

    profile = get_user_profile(user_id)
    client = get_swiggy_client()

    handler_map = {
        "order_food": _handle_order_food,
        "order_groceries": _handle_order_groceries,
        "book_dining": _handle_book_dining,
        "reorder_last_meal": _handle_reorder_last_meal,
        "track_order": _handle_track_order,
        "cancel_order": _handle_cancel_order,
        "search_restaurants": _handle_search_restaurants,
        "apply_offer": _handle_apply_offer,
    }

    handler = handler_map.get(intent_name)
    if handler is None:
        return [], "Intent not supported yet.", ["unsupported_intent"]

    return handler(client, entities, profile, user_id)


def _handle_order_food(
    client, entities: Dict[str, Any], profile: Dict[str, Any], user_id: str
) -> Tuple[List[ActionResult], str, List[str]]:
    auto_resolved: List[str] = []
    items = _resolve_value(entities, profile, "items", "favorite_items", auto_resolved)
    restaurant = _resolve_value(
        entities, profile, "restaurant", "favorite_restaurant", auto_resolved
    )
    if _is_missing(items):
        items = DEFAULT_PROFILE["favorite_items"]
        auto_resolved.append("items")
    if _is_missing(restaurant):
        restaurant = DEFAULT_PROFILE["favorite_restaurant"]
        auto_resolved.append("restaurant")
    time_value = entities.get("time") or "now"
    budget = entities.get("budget") or profile.get("budget")
    address = profile.get("default_address", DEFAULT_PROFILE["default_address"])

    response = client.place_food_order(
        restaurant=restaurant,
        items=items,
        time=time_value,
        budget=budget,
        address=address,
        instructions=[],
    )

    add_order(
        user_id,
        {
            "intent": "order_food",
            "order_id": response["order_id"],
            "details": response,
        },
    )

    action = ActionResult(
        provider="swiggy",
        action="place_food_order",
        success=True,
        details={**response, "auto_resolved": auto_resolved},
    )
    return [action], "Food order placed.", _warnings_from_auto(auto_resolved)


def _handle_order_groceries(
    client, entities: Dict[str, Any], profile: Dict[str, Any], user_id: str
) -> Tuple[List[ActionResult], str, List[str]]:
    auto_resolved: List[str] = []
    items = _resolve_value(entities, profile, "items", "grocery_items", auto_resolved)
    if _is_missing(items):
        items = DEFAULT_PROFILE["grocery_items"]
        auto_resolved.append("items")
    time_value = entities.get("time") or "now"
    budget = entities.get("budget") or profile.get("budget")
    address = profile.get("default_address", DEFAULT_PROFILE["default_address"])

    response = client.place_grocery_order(
        items=items,
        time=time_value,
        budget=budget,
        address=address,
    )

    add_order(
        user_id,
        {
            "intent": "order_groceries",
            "order_id": response["order_id"],
            "details": response,
        },
    )

    action = ActionResult(
        provider="swiggy",
        action="place_grocery_order",
        success=True,
        details={**response, "auto_resolved": auto_resolved},
    )
    return [action], "Grocery order placed.", _warnings_from_auto(auto_resolved)


def _handle_book_dining(
    client, entities: Dict[str, Any], profile: Dict[str, Any], user_id: str
) -> Tuple[List[ActionResult], str, List[str]]:
    auto_resolved: List[str] = []
    restaurant = _resolve_value(
        entities, profile, "restaurant", "dine_restaurant", auto_resolved
    )
    time_value = _resolve_value(
        entities, profile, "time", "dine_time", auto_resolved
    )
    party_size = _resolve_value(
        entities, profile, "party_size", "party_size", auto_resolved
    )
    if _is_missing(restaurant):
        restaurant = DEFAULT_PROFILE["dine_restaurant"]
        auto_resolved.append("restaurant")
    if _is_missing(time_value):
        time_value = DEFAULT_PROFILE["dine_time"]
        auto_resolved.append("time")
    if _is_missing(party_size):
        party_size = DEFAULT_PROFILE["party_size"]
        auto_resolved.append("party_size")
    budget = entities.get("budget") or profile.get("budget")
    date_value = entities.get("day")

    response = client.book_dining(
        restaurant=restaurant,
        time=time_value,
        date=date_value,
        party_size=int(party_size),
        budget=budget,
    )

    add_order(
        user_id,
        {
            "intent": "book_dining",
            "order_id": response["reservation_id"],
            "details": response,
        },
    )

    action = ActionResult(
        provider="swiggy",
        action="book_dining",
        success=True,
        details={**response, "auto_resolved": auto_resolved},
    )
    return [action], "Dining reservation confirmed.", _warnings_from_auto(auto_resolved)


def _handle_reorder_last_meal(
    client, entities: Dict[str, Any], profile: Dict[str, Any], user_id: str
) -> Tuple[List[ActionResult], str, List[str]]:
    last_order = get_last_order(user_id, intent="order_food")
    if not last_order:
        action = ActionResult(
            provider="swiggy",
            action="reorder_last_meal",
            success=False,
            details={"message": "No previous food order found."},
        )
        return [action], "No previous food order found.", ["missing_history"]

    details = last_order.get("details", {})
    response = client.place_food_order(
        restaurant=details.get("restaurant") or profile.get("favorite_restaurant"),
        items=details.get("items") or profile.get("favorite_items"),
        time=entities.get("time") or "now",
        budget=details.get("budget") or profile.get("budget"),
        address=details.get("delivery_address") or profile.get("default_address"),
        instructions=details.get("instructions", []),
    )

    add_order(
        user_id,
        {
            "intent": "order_food",
            "order_id": response["order_id"],
            "details": response,
        },
    )

    action = ActionResult(
        provider="swiggy",
        action="reorder_last_meal",
        success=True,
        details={
            **response,
            "reordered_from": details.get("order_id"),
        },
    )
    return [action], "Reorder placed.", []


def _handle_track_order(
    client, entities: Dict[str, Any], profile: Dict[str, Any], user_id: str
) -> Tuple[List[ActionResult], str, List[str]]:
    order_id = entities.get("order_id")
    if not order_id:
        last_order = get_last_order(user_id, intent="order_food")
        if not last_order:
            last_order = get_last_order(user_id, intent="order_groceries")
        order_id = last_order.get("order_id") if last_order else None

    if not order_id:
        action = ActionResult(
            provider="swiggy",
            action="track_order",
            success=False,
            details={"message": "No order found to track."},
        )
        return [action], "No order found to track.", ["missing_order_id"]

    response = client.track_order(order_id)
    action = ActionResult(
        provider="swiggy",
        action="track_order",
        success=True,
        details=response,
    )
    return [action], "Order status retrieved.", []


def _handle_cancel_order(
    client, entities: Dict[str, Any], profile: Dict[str, Any], user_id: str
) -> Tuple[List[ActionResult], str, List[str]]:
    order_id = entities.get("order_id")
    if not order_id:
        last_order = get_last_order(user_id, intent="order_food")
        if not last_order:
            last_order = get_last_order(user_id, intent="order_groceries")
        order_id = last_order.get("order_id") if last_order else None

    if not order_id:
        action = ActionResult(
            provider="swiggy",
            action="cancel_order",
            success=False,
            details={"message": "No order found to cancel."},
        )
        return [action], "No order found to cancel.", ["missing_order_id"]

    response = client.cancel_order(order_id)
    action = ActionResult(
        provider="swiggy",
        action="cancel_order",
        success=True,
        details=response,
    )
    return [action], "Order canceled.", []


def _handle_search_restaurants(
    client, entities: Dict[str, Any], profile: Dict[str, Any], user_id: str
) -> Tuple[List[ActionResult], str, List[str]]:
    cuisine = (
        entities.get("cuisine")
        or profile.get("favorite_cuisine")
        or DEFAULT_PROFILE.get("favorite_cuisine")
        or "Popular"
    )
    location = entities.get("location") or profile.get("city") or DEFAULT_PROFILE.get("city")
    results = _suggest_restaurants(cuisine, location)
    action = ActionResult(
        provider="swiggy",
        action="search_restaurants",
        success=True,
        details={
            "cuisine": cuisine,
            "location": location,
            "results": results,
        },
    )
    return [action], "Restaurant options ready.", []


def _handle_apply_offer(
    client, entities: Dict[str, Any], profile: Dict[str, Any], user_id: str
) -> Tuple[List[ActionResult], str, List[str]]:
    order_id = entities.get("order_id")
    if not order_id:
        last_order = get_last_order(user_id, intent="order_food")
        if not last_order:
            last_order = get_last_order(user_id, intent="order_groceries")
        order_id = last_order.get("order_id") if last_order else None

    if not order_id:
        action = ActionResult(
            provider="swiggy",
            action="apply_offer",
            success=False,
            details={"message": "No order found to apply the offer."},
        )
        return [action], "No order found to apply the offer.", ["missing_order_id"]

    offer_code = entities.get("offer_code") or "SWIGGY50"
    action = ActionResult(
        provider="swiggy",
        action="apply_offer",
        success=True,
        details={
            "order_id": order_id,
            "offer_code": offer_code,
            "discount_percent": 20,
            "message": "Offer applied.",
        },
    )
    return [action], "Offer applied.", []


def _resolve_value(
    entities: Dict[str, Any],
    profile: Dict[str, Any],
    entity_key: str,
    profile_key: str,
    auto_resolved: List[str],
) -> Any:
    value = entities.get(entity_key)
    if _is_missing(value):
        profile_value = profile.get(profile_key)
        if profile_value is not None:
            auto_resolved.append(entity_key)
            value = profile_value
    return value


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, list):
        return len(value) == 0
    return False


def _warnings_from_auto(auto_resolved: List[str]) -> List[str]:
    if not auto_resolved:
        return []
    return [f"auto_resolved: {', '.join(auto_resolved)}"]


def _step_label(intent_name: str) -> str:
    labels = {
        "order_food": "Place food order",
        "order_groceries": "Place grocery order",
        "book_dining": "Book dining reservation",
        "reorder_last_meal": "Reorder last meal",
        "track_order": "Track order",
        "cancel_order": "Cancel order",
        "search_restaurants": "Search restaurants",
        "apply_offer": "Apply offer",
    }
    return labels.get(intent_name, "Execute action")


def _suggest_restaurants(cuisine: str, location: Optional[str]) -> List[Dict[str, Any]]:
    base = [
        {"name": "Spice Route", "rating": 4.5},
        {"name": "Urban Tadka", "rating": 4.4},
        {"name": "Green Bowl", "rating": 4.3},
        {"name": "Cloud Kitchen Co", "rating": 4.2},
        {"name": "Taste Atlas", "rating": 4.1},
    ]
    for entry in base:
        entry["cuisine"] = cuisine
        if location:
            entry["location"] = location
    return base
