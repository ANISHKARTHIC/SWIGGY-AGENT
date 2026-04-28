import json

# In-memory storage for the last order
last_order = None

def order_food(user_input, entities):
    """
    Simulates ordering food from a restaurant.
    """
    global last_order
    # Simulate API call to a food delivery service
    response = {
        "status": "success",
        "action": "food_order",
        "details": {
            "restaurant": "Domino's",
            "items": entities.get("items", ["Pizza"]),
            "delivery_time": "30 mins"
        }
    }
    last_order = response  # Save the order
    return json.dumps(response)

def order_groceries(user_input, entities):
    """
    Simulates ordering groceries.
    """
    # Simulate API call to a grocery delivery service
    return json.dumps({
        "status": "success",
        "action": "grocery_order",
        "details": {
            "store": "Instamart",
            "items": entities.get("items", ["Milk", "Bread"]),
            "delivery_time": "15 mins"
        }
    })

def book_dining(user_input, entities):
    """
    Simulates booking a table at a restaurant.
    """
    # Simulate API call to a reservation service
    return json.dumps({
        "status": "success",
        "action": "dining_booking",
        "details": {
            "restaurant": "The Great Indian BBQ",
            "time": entities.get("time", "8 PM"),
            "party_size": 2
        }
    })

def reorder_last_meal(user_input, entities):
    """
    Simulates reordering the last meal.
    """
    if last_order:
        return json.dumps(last_order)
    else:
        return json.dumps({
            "status": "failed",
            "action": "reorder_last_meal",
            "details": {
                "message": "No previous order found."
            }
        })
