from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
STORE_PATH = DATA_DIR / "store.json"

DEFAULT_USER_ID = "default"
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "Bengaluru")
DEFAULT_ADDRESS = os.getenv("DEFAULT_ADDRESS", "Home")
DEFAULT_FOOD_ITEMS = ["Chicken Biryani", "Raita"]
DEFAULT_GROCERY_ITEMS = ["Milk", "Bread", "Eggs"]
DEFAULT_DINE_TIME = os.getenv("DEFAULT_DINE_TIME", "8 PM")
DEFAULT_PARTY_SIZE = int(os.getenv("DEFAULT_PARTY_SIZE", "2"))
DEFAULT_BUDGET = int(os.getenv("DEFAULT_BUDGET", "300"))
DEFAULT_RESTAURANT = os.getenv("DEFAULT_RESTAURANT", "Meghana Foods")
DEFAULT_DINE_RESTAURANT = os.getenv("DEFAULT_DINE_RESTAURANT", "Barbeque Nation")
DEFAULT_CUISINE = os.getenv("DEFAULT_CUISINE", "Indian")

DEFAULT_PROFILE = {
    "city": DEFAULT_CITY,
    "default_address": DEFAULT_ADDRESS,
    "favorite_restaurant": DEFAULT_RESTAURANT,
    "favorite_items": DEFAULT_FOOD_ITEMS,
    "grocery_items": DEFAULT_GROCERY_ITEMS,
    "dine_restaurant": DEFAULT_DINE_RESTAURANT,
    "dine_time": DEFAULT_DINE_TIME,
    "party_size": DEFAULT_PARTY_SIZE,
    "budget": DEFAULT_BUDGET,
}

SWIGGY_MODE = os.getenv("SWIGGY_MODE", "mock")
SWIGGY_API_BASE_URL = os.getenv("SWIGGY_API_BASE_URL", "https://www.swiggy.com")
