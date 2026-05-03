import re

INTENT_PATTERNS = {
    "reorder_last_meal": [
        r"\breorder\b",
        r"\brepeat\b",
        r"\bsame as last\b",
        r"\bagain\b",
        r"\blast meal\b",
    ],
    "track_order": [
        r"\btrack\b",
        r"\bwhere is\b",
        r"\border status\b",
        r"\beta\b",
    ],
    "cancel_order": [
        r"\bcancel\b",
        r"\bstop\b",
        r"\bundo\b",
    ],
    "book_dining": [
        r"\bbook\b.*\btable\b",
        r"\btable for\b",
        r"\breserv(?:e|ation)\b",
        r"\bdineout\b",
        r"\brestaurant booking\b",
    ],
    "order_groceries": [
        r"\bgrocer(?:y|ies)\b",
        r"\binstamart\b",
        r"\bbuy\b.*\b(milk|bread|eggs|vegetables|fruits|rice|atta|oil)\b",
        r"\brestock\b",
    ],
    "order_food": [
        r"\b(order|get|deliver|send)\b.*\b(food|meal|lunch|dinner|breakfast)\b",
        r"\b(pizza|burger|biryani|dosa|sushi|noodles|pasta|thali|shawarma|tacos)\b",
        r"\bfood\b.*\bdeliver\b",
        r"\bswiggy\b.*\b(order|food)\b",
    ],
    "search_restaurants": [
        r"\bfind\b.*\brestaurant\b",
        r"\bsearch\b.*\brestaurant\b",
        r"\bnearby\b.*\brestaurant\b",
        r"\brestaurants? near\b",
        r"\brestaurants? in\b",
        r"\bbest\b.*\brestaurant\b",
    ],
    "apply_offer": [
        r"\bapply\b.*\b(code|coupon|offer)\b",
        r"\bdiscount\b",
        r"\bcoupon\b",
        r"\boffer code\b",
    ],
}

INTENT_PRIORITY = [
    "reorder_last_meal",
    "cancel_order",
    "track_order",
    "apply_offer",
    "book_dining",
    "order_groceries",
    "order_food",
    "search_restaurants",
]

ITEM_KEYWORDS = {
    "Pizza": ["pizza", "margherita", "farmhouse"],
    "Burger": ["burger", "cheeseburger"],
    "Biryani": ["biryani"],
    "Dosa": ["dosa"],
    "Idli": ["idli"],
    "Noodles": ["noodles"],
    "Pasta": ["pasta"],
    "Sushi": ["sushi"],
    "Thali": ["thali"],
    "Shawarma": ["shawarma"],
    "Tacos": ["tacos"],
    "Milk": ["milk"],
    "Bread": ["bread"],
    "Eggs": ["eggs", "egg"],
    "Rice": ["rice"],
    "Atta": ["atta", "flour"],
    "Cooking Oil": ["oil", "cooking oil"],
    "Sugar": ["sugar"],
    "Salt": ["salt"],
    "Vegetables": ["vegetables", "veggies", "vegetable"],
    "Fruits": ["fruits", "fruit"],
}

CUISINE_KEYWORDS = {
    "North Indian": ["north indian", "punjabi"],
    "South Indian": ["south indian"],
    "Chinese": ["chinese"],
    "Italian": ["italian"],
    "Mexican": ["mexican"],
    "Thai": ["thai"],
    "Japanese": ["japanese"],
    "American": ["american"],
}

MEAL_PERIODS = ["breakfast", "brunch", "lunch", "snack", "dinner"]


def detect_intent(user_input):
    """
    Detects the user's intent using rule-based scoring.
    Returns a dict with intent, confidence, and match details.
    """
    text = user_input.lower().strip()
    scores = []
    match_map = {}

    for intent_name, patterns in INTENT_PATTERNS.items():
        matches = [pattern for pattern in patterns if re.search(pattern, text)]
        match_map[intent_name] = matches
        score = len(matches)
        scores.append({"intent": intent_name, "score": score})

    scores.sort(key=lambda item: (-item["score"], INTENT_PRIORITY.index(item["intent"])))
    best = scores[0] if scores else {"intent": "unknown", "score": 0}
    best_intent = best["intent"] if best["score"] > 0 else "unknown"
    total_patterns = len(INTENT_PATTERNS.get(best_intent, [])) or 1
    confidence = min(1.0, best["score"] / total_patterns) if best_intent != "unknown" else 0.0

    return {
        "intent": best_intent,
        "confidence": round(confidence, 2),
        "matches": match_map.get(best_intent, []),
        "candidates": scores[:3],
    }


def extract_entities(user_input):
    """
    Extracts entities like time, items, budget, and location.
    """
    text = user_input.lower()
    entities = {}

    time_match = re.search(r"\b(?:at|by)\s*(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\b", text)
    if time_match:
        hour = time_match.group(1)
        minute = time_match.group(2) or "00"
        meridiem = time_match.group(3)
        time_value = f"{hour}:{minute}"
        if meridiem:
            time_value = f"{time_value} {meridiem}"
        entities["time"] = time_value

    if "tomorrow" in text:
        entities["day"] = "tomorrow"
    elif "today" in text:
        entities["day"] = "today"
    elif "tonight" in text:
        entities["day"] = "tonight"

    window_match = re.search(r"\bin\s*(\d{1,3})\s*(mins|minutes|hours|hrs)\b", text)
    if window_match:
        entities["delivery_window"] = f"{window_match.group(1)} {window_match.group(2)}"

    items = _find_keywords(text, ITEM_KEYWORDS)
    if items:
        entities["items"] = items

    cuisine = _find_keywords(text, CUISINE_KEYWORDS)
    if cuisine:
        entities["cuisine"] = cuisine[0]

    for meal_period in MEAL_PERIODS:
        if re.search(rf"\b{meal_period}\b", text):
            entities["meal_period"] = meal_period
            break

    party_match = re.search(r"\b(?:for|party of|table for)\s*(\d{1,2})\b", text)
    if party_match:
        entities["party_size"] = int(party_match.group(1))

    budget_match = re.search(r"\b(?:under|below|less than|max|budget)\s*(\d{2,5})\b", text)
    if budget_match:
        entities["budget"] = int(budget_match.group(1))

    location_match = re.search(r"\b(?:in|near|around)\s+([a-z][a-z\s\-]{2,})\b", text)
    if location_match:
        entities["location"] = location_match.group(1).strip()

    restaurant_match = re.search(
        r"\bfrom\s+([a-z0-9&'\.\-\s]{2,}?)(?=\s+(for|at|in|with|under|by|and|,|\.|$))",
        text,
    )
    if restaurant_match:
        entities["restaurant"] = restaurant_match.group(1).strip()

    if re.search(r"\b(veg|vegetarian|vegan)\b", text):
        entities["diet"] = "veg"
    elif re.search(r"\b(non-veg|non veg|chicken|mutton|fish)\b", text):
        entities["diet"] = "non_veg"

    if re.search(r"\b(pickup|takeaway)\b", text):
        entities["delivery_mode"] = "pickup"
    elif re.search(r"\bdeliver|delivery\b", text):
        entities["delivery_mode"] = "delivery"

    order_match = re.search(
        r"\b(?:order\s*id|order\s*#|#)\s*([a-z0-9-]{4,})\b", text
    )
    if order_match:
        entities["order_id"] = order_match.group(1).upper()

    offer_match = re.search(r"\b(?:code|coupon|offer)\s+([a-z0-9]{3,})\b", text)
    if offer_match:
        entities["offer_code"] = offer_match.group(1).upper()

    return entities


def _find_keywords(text, catalog):
    found = []
    for canonical, keywords in catalog.items():
        for keyword in keywords:
            if re.search(rf"\b{re.escape(keyword)}\b", text):
                found.append(canonical)
                break
    return found
