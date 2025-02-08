from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("../../firebaseServiceKey.json") # Key is stored locally outside the repo, might change later
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

# Configure Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

def scrape_walmart(product_name):
    """Scrape Walmart for product prices using Selenium"""
    driver = webdriver.Chrome(service=Service('path/to/chromedriver'), options=chrome_options)
    try:
        driver.get(f"https://www.walmart.com/search?q={product_name}")
        time.sleep(5)  # Wait for the page to load

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        products = []

        # Extract product details
        for item in soup.find_all('div', class_='mb1 ph1 pa0-xl bb b--near-white w-25'):
            name = item.find('span', class_='w_Cs').text.strip() if item.find('span', class_='w_Cs') else "N/A"
            price = item.find('div', class_='w_cC').text.strip() if item.find('div', class_='w_cC') else "N/A"
            products.append({
                "name": name,
                "price": price,
                "store": "Walmart"
            })
        return products
    finally:
        driver.quit()

def store_prices(item, prices):
    """Store scraped prices in Firebase"""
    doc_ref = db.collection('prices').document(item)
    doc_ref.set({
        "item": item,
        "prices": prices,  # List of prices from different stores
        "timestamp": firestore.SERVER_TIMESTAMP
    })

@app.route('/scrape-prices', methods=['POST'])
def scrape_prices():
    # Get the grocery list and budget from the frontend
    data = request.json
    grocery_list = data.get("items", [])
    budget = data.get("budget", 0)
    
    # Scrape prices for each item
    results = []
    for item in grocery_list:
        scraped_data = scrape_walmart(item)
        store_prices(item, scraped_data)  # Store prices in Firebase
        results.append({
            "item": item,
            "prices": scraped_data
        })
    
    # Filter results based on budget
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
                "cheapest_option": cheapest_option
            })
    return filtered_results

if __name__ == '__main__':
    app.run(debug=True)