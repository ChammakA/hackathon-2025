from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json
import firebase_admin
from firebase_admin import credentials, firestore
import os
import re
import requests
from dotenv import load_dotenv

# Initialize Firebase
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(r"C:\Webdriver\chromedriver.exe"), options=chrome_options)
cred = credentials.Certificate("grocery-optimizer-40b48-firebase-adminsdk-fbsvc-b21ac7f0fc.json") # Update path
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
CORS(app)

# Load .env for Nutritionix API keys
load_dotenv()
NUTRITIONIX_APP_ID = os.getenv("NUTRITIONIX_APP_ID", "").strip()
NUTRITIONIX_APP_KEY = os.getenv("NUTRITIONIX_APP_KEY", "").strip()

# Configure Selenium for Walmart


def scrape_walmart(product_name):
    """Scrape Walmart for product prices using Selenium"""
    try:
        driver.get(f"https://www.walmart.com/search?q={product_name}")
        time.sleep(5)  # Wait for the page to load
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        products = []
        for item in soup.find_all('div', class_='mb1 ph1 pa0-xl bb b--near-white w-25'):
            name = item.find('span', class_='w_Cs').text.strip() if item.find('span', class_='w_Cs') else "N/A"
            price = item.find('div', class_='w_cC').text.strip() if item.find('div', class_='w_cC') else "N/A"
            products.append({"name": name, "price": price, "store": "Walmart"})
        return products
    finally:
        driver.quit()

def get_healthiest_option(food_item):
    """Fetch the healthiest alternative for a given grocery item from Nutritionix API."""
    url = "https://trackapi.nutritionix.com/v2/search/instant"
    headers = {"x-app-id": NUTRITIONIX_APP_ID, "x-app-key": NUTRITIONIX_APP_KEY}
    params = {"query": food_item}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return {"error": f"API request failed with status {response.status_code}"}
    data = response.json()
    health_keywords = ["organic", "whole grain", "low sugar", "sugar-free"]
    exclusion_keywords = ["sauce", "shake", "candy", "snack", "processed"]
    candidates = []
    for item in data.get("branded", []):
        name = item.get("food_name", "").lower()
        if not any(excl in name for excl in exclusion_keywords):
            health_score = sum(1 for keyword in health_keywords if keyword in name)
            if health_score > 0:
                candidates.append(item)
    if candidates:
        best_item = candidates[0]
        return {
            "food_name": best_item["food_name"],
            "brand": best_item.get("brand_name", "Unknown Brand"),
            "calories": best_item.get("nf_calories"),
            "serving_size": f"{best_item.get('serving_qty', '')} {best_item.get('serving_unit', '')}",
            "image": best_item.get("photo", {}).get("thumb", "")
        }
    return {"food_item": food_item, "healthiest_option": None}

@app.route('/scrape-prices', methods=['POST'])
def scrape_prices():
    data = request.json
    grocery_list = data.get("items", [])
    budget = data.get("budget", 0)
    
    # Scrape prices for each item
    results = []
    for item in grocery_list:
        walmart_prices = scrape_walmart(item)
        healthiest_option = get_healthiest_option(item)
        results.append({
            "item": item,
            "prices": walmart_prices,
            "healthiest_option": healthiest_option
        })
    
    # Filter based on budget
    filtered_results = filter_by_budget(results, budget)
    return jsonify(filtered_results)

def filter_by_budget(results, budget):
    """Filter and sort results based on the user's budget"""
    filtered_results = []
    for item in results:
        cheapest_option = min(item["prices"], key=lambda x: float(x["price"].replace('$', '')))
        if float(cheapest_option["price"].replace('$', '')) <= budget:
            filtered_results.append({
                "item": item["item"],
                "cheapest_option": cheapest_option,
                "healthiest_option": item["healthiest_option"]
            })
    return filtered_results

if __name__ == '__main__':
    app.run(debug=True)