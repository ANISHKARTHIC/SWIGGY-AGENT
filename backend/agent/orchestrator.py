from . import intent
from . import skills

def route_intent(user_input):
    """
    Routes the user's intent to the appropriate skill.
    """
    detected_intent = intent.detect_intent(user_input)
    entities = intent.extract_entities(user_input)
    
    # Skill mapping
    if detected_intent == "order_food":
        return skills.order_food(user_input, entities)
    elif detected_intent == "order_groceries":
        return skills.order_groceries(user_input, entities)
    elif detected_intent == "book_dining":
        return skills.book_dining(user_input, entities)
    elif detected_intent == "reorder_last_meal":
        return skills.reorder_last_meal(user_input, entities)
    else:
        return '{"status": "failed", "message": "Intent not understood."}'
