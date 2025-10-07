# 🥗 Nutrition Facts Dataset

## 📘 Overview
This dataset provides detailed **nutritional information** for various food items.  
Each row represents a unique food entry categorized by type (e.g., Fruit, Meat, Dairy, etc.) and includes macronutrients, micronutrients, vitamins, and minerals.

---

## 📂 File Information

- **Filename:** `nutrition_facts.csv`
- **Format:** CSV (Comma-Separated Values)
- **Rows:** (depends on file)
- **Columns:** 37

---

## 📊 Columns Description

| Column Name | Description |
|--------------|-------------|
| `Category` | Main food group (e.g., Fruits, Vegetables, Meats, Grains). |
| `Description` | Detailed name or description of the food item. |
| `Nutrient Data Bank Number` | Unique identifier (USDA reference number). |

### 🔸 Macronutrients

| Column | Description |
|--------|-------------|
| `Data.Carbohydrate` | Carbohydrates in grams per 100g. |
| `Data.Protein` | Protein content in grams per 100g. |
| `Data.Fat.Total Lipid` | Total fat content in grams per 100g. |
| `Data.Fat.Saturated Fat` | Saturated fat content in grams per 100g. |
| `Data.Fat.Monosaturated Fat` | Monounsaturated fat content in grams per 100g. |
| `Data.Fat.Polysaturated Fat` | Polyunsaturated fat content in grams per 100g. |
| `Data.Sugar Total` | Total sugar content in grams per 100g. |
| `Data.Fiber` | Dietary fiber in grams per 100g. |
| `Data.Water` | Water content in grams per 100g. |
| `Data.Cholesterol` | Cholesterol content in milligrams per 100g. |

---

### 🔸 Vitamins

| Column | Description |
|--------|-------------|
| `Data.Vitamins.Vitamin A - RAE` | Vitamin A (Retinol Activity Equivalent) in µg. |
| `Data.Vitamins.Vitamin B12` | Vitamin B12 in µg. |
| `Data.Vitamins.Vitamin B6` | Vitamin B6 in mg. |
| `Data.Vitamins.Vitamin C` | Vitamin C (ascorbic acid) in mg. |
| `Data.Vitamins.Vitamin E` | Vitamin E in mg. |
| `Data.Vitamins.Vitamin K` | Vitamin K in µg. |
| `Data.Niacin` | Niacin (Vitamin B3) in mg. |
| `Data.Riboflavin` | Riboflavin (Vitamin B2) in mg. |
| `Data.Thiamin` | Thiamin (Vitamin B1) in mg. |
| `Data.Retinol` | Retinol (Vitamin A1) in µg. |

---

### 🔸 Carotenoids & Phytochemicals

| Column | Description |
|--------|-------------|
| `Data.Alpha Carotene` | Alpha-carotene in µg. |
| `Data.Beta Carotene` | Beta-carotene in µg. |
| `Data.Beta Cryptoxanthin` | Beta-cryptoxanthin in µg. |
| `Data.Lutein and Zeaxanthin` | Lutein + Zeaxanthin in µg. |
| `Data.Lycopene` | Lycopene in µg. |

---

### 🔸 Minerals

| Column | Description |
|--------|-------------|
| `Data.Major Minerals.Calcium` | Calcium in mg. |
| `Data.Major Minerals.Copper` | Copper in mg. |
| `Data.Major Minerals.Iron` | Iron in mg. |
| `Data.Major Minerals.Magnesium` | Magnesium in mg. |
| `Data.Major Minerals.Phosphorus` | Phosphorus in mg. |
| `Data.Major Minerals.Potassium` | Potassium in mg. |
| `Data.Major Minerals.Sodium` | Sodium in mg. |
| `Data.Major Minerals.Zinc` | Zinc in mg. |
| `Data.Selenium` | Selenium in µg. |

---

### 🔸 Other Compounds

| Column | Description |
|--------|-------------|
| `Data.Choline` | Choline in mg (important for liver and brain function). |

---

## ⚙️ Example Row

| Category | Description | Protein | Carbohydrate | Fat.Total Lipid | Vitamin C |
|-----------|--------------|----------|---------------|------------------|-----------|
| Fruit | Orange, raw | 0.9 | 11.8 | 0.1 | 53.2 |

---

## 💡 Possible Use Cases

- Nutritional analysis and diet optimization  
- Food classification and nutrient prediction models  
- Calorie and macronutrient estimation systems  
- Health tracking and personalized meal recommendation systems  
- Data visualization (e.g., vitamin vs. mineral density charts)

---
## Problems

The dataset doesn't contain a calories columns so we are going to approximate the values by doing 
Calories = 4*protein + 4*carbohydrates + 9*fats