# hackathon-2025

# 🛒 AI-Powered Grocery Budget & Health Assistant
# Full Stack Alchemists -- 

Kalan Dsouza, Hikmatullah Hussain Zada, Sammak Ahmed, Hailey Dsouza

## 🚀 Overview
This project helps users **compare the cheapest vs. healthiest grocery options** using AI.  
Users input their grocery list and budget, and the AI finds:
- **Cheapest grocery options** (sorted by price and store).
- **Healthiest alternatives** (organic, low sugar, whole grain, etc.).

**✨ Why This Matters:**  
Many people struggle to buy **healthy groceries while staying on budget**. This AI-powered platform **simplifies decision-making** by providing a side-by-side comparison of affordability vs. nutrition.

---

## 🎯 **How It Works**
1️⃣ **User inputs grocery items & budget.**  
2️⃣ **Backend fetches data:**  
    - Finds **cheapest price per item** from different stores.  
    - Finds **healthiest alternative** using AI filtering.  
3️⃣ **Frontend displays a clear comparison table.**  
4️⃣ **User selects cheapest or healthiest option per item.**  
5️⃣ **Budget dynamically updates as selections are made.**  

---

## 🔥 **AI-Powered Features**
### 🧠 **Healthiest Grocery Selection (AI)**
- **Uses NLP & filtering logic** to find **organic, low-fat, low-sugar, whole-grain** items.
- **Avoids mismatches**.
- **Smart swap recommendations** for healthier alternatives if items are too expensive.

### 🏪 **Cheapest Grocery Price Finder**
- **Manually sourced prices for now** (scraper can be added later).
- **Matches user-inputted groceries with best-priced items per store.**

---

## 🏗️ **Tech Stack**
- **Frontend:** React, Tailwind CSS  
- **Backend:** Python (Flask), Nutritionix API  
- **AI Integration:** Custom filtering logic for healthiest food selection  
- **Data Storage:** JSON (for now)  

---

## 📷 **Screenshots**
| **Grocery Input Page** | **Comparison Table** | **Final Budget Selection** |
|-----------------|-----------------|-----------------|
| _User enters groceries & budget_ | _AI finds cheapest vs. healthiest options_ | _Users select options & budget updates_ |



---

## 📖 **Installation & Setup**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/ChammakA/hackathon-2025.git
cd hackathon-2025
