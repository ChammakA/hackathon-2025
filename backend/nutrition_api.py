import os
import re
import requests
import json
from dotenv import load_dotenv

load_dotenv()
NUTRITIONIX_APP_ID = os.getenv("NUTRITIONIX_APP_ID", "").strip()
NUTRITIONIX_APP_KEY = os.getenv("NUTRITIONIX_APP_KEY", "").strip()

def get_healthiest_option(food_item):
    """Fetch the healthiest alternative for a given grocery item from Nutritionix API."""
    url = "https://trackapi.nutritionix.com/v2/search/instant"
    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_APP_KEY
    }
    params = {"query": food_item}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return {"error": f"API request failed with status {response.status_code}"}
    
    data = response.json()

    health_keywords = [
        "organic", "grass-fed", "whole grain", "sugar-free", "low fat", "low sugar",
        "natural", "unsweetened", "non-GMO", "fortified", "plant-based", "high fiber",
        "raw", "fresh", "whole", "unprocessed", "no added sugar"
    ]

    exclusion_keywords = [
        "sauce", "juice", "shake", "drink", "candy", "snack", "bar", "processed",
        "canned", "jar", "bottle", "powder", "mix", "syrup", "sweetened", "beverage",
        "soda", "fried", "chocolate", "dessert", "pie", "pastry", "jam", "jelly",
        "preserves", "crisp", "cookie", "cake", "seasoning", "dressing", "dried"
    ]

    candidates = []

    for item in data.get("branded", []):
        name = item.get("food_name", "").lower()
        brand = item.get("brand_name", "Unknown Brand").lower()

        # Match whole word with optional plural 's'
        pattern = rf'\b{re.escape(food_item.lower())}s?\b'
        if not re.search(pattern, name):
            continue

        if any(excl in name for excl in exclusion_keywords):
            continue

        health_score = sum(1 for keyword in health_keywords if keyword in name)
        if health_score == 0:
            continue

        # Get nutritional values
        serving_qty = item.get("serving_qty", "")
        serving_unit = item.get("serving_unit", "")
        serving_size = f"{serving_qty} {serving_unit}".strip() if serving_qty else serving_unit

        candidates.append((
            health_score,
            -item.get("nf_calories", 0),
            -item.get("nf_sugars", 0),
            item.get("nf_protein", 0),
            item
        ))

    result = {
        "food_item": food_item,
        "healthiest_option": None
    }

    if candidates:
        candidates.sort(reverse=True)
        best_item = candidates[0][-1]
        
        serving_qty = best_item.get("serving_qty", "")
        serving_unit = best_item.get("serving_unit", "")
        serving_size = f"{serving_qty} {serving_unit}".strip() if serving_qty else serving_unit

        result["healthiest_option"] = {
            "food_name": best_item.get("food_name", "").title(),
            "brand": best_item.get("brand_name", "Unknown Brand").title(),
            "calories": best_item.get("nf_calories"),
            "serving_size": serving_size,
            "image": best_item.get("photo", {}).get("thumb", "")
        }

    return result

# Example Usage:
if __name__ == "__main__":
    food = "cheese"
    healthy_alternative = get_healthiest_option(food)
    print("\n--- SELECTED HEALTHY OPTION ---")
    print(json.dumps(healthy_alternative, indent=2))