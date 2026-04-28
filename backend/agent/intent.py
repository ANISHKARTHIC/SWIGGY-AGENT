import re

def detect_intent(user_input):
    """
    Detects the user's intent based on keywords in the input.
    """
    user_input = user_input.lower()
    
    # Rule-based intent detection
    if re.search(r'order food|pizza|burger|sushi', user_input):
        return "order_food"
    elif re.search(r'buy groceries|milk|bread|eggs', user_input):
        return "order_groceries"
    elif re.search(r'book dining|book a table|restaurant reservation', user_input):
        return "book_dining"
    elif re.search(r'reorder|last meal', user_input):
        return "reorder_last_meal"
    else:
        return "unknown"

def extract_entities(user_input):
    """
    Extracts basic entities like time, item, and budget from the user input.
    """
    user_input = user_input.lower()
    entities = {}
    
    # Extract time (e.g., "8 PM", "tomorrow")
    time_match = re.search(r'at (\d{1,2}(:\d{2})?\s?(am|pm)?)', user_input)
    if time_match:
        entities['time'] = time_match.group(1)
    
    # Extract items (simple keyword matching)
    items = []
    if "pizza" in user_input:
        items.append("Pizza")
    if "milk" in user_input:
        items.append("Milk")
    if "bread" in user_input:
        items.append("Bread")
    
    if items:
        entities['items'] = items
        
    return entities
