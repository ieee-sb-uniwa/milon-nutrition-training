# 🍽️ Food Datasets Overview

This document summarizes and compares **Food-101** and **Food-251**, two widely used datasets for *food image classification*, based on the analysis in *Food Recognition in the Wild* (Singla et al., 2019).

---

## **1. Food-101**
**Source:** [Bossard et al., 2014 – Food-101 Dataset](https://data.vision.ee.ethz.ch/cvl/datasets_extra/food-101/static/bossard_eccv14_food-101.pdf)

### **Dataset Summary**
| Attribute | Description |
|------------|--------------|
| **Classes** | 101 |
| **Total Images** | 101,000 |
| **Train Images per Class** | 750 |
| **Test Images per Class** | 250 |
| **Image Resolution** | 512 × 512 px (uniform) |
| **Image Variations** | Large variation in lighting, angle, and preparation style |
| **Food Type** | Western dishes (typically cooked) |
| **Category Type** | **Single-category** dataset (one dish per image) |

### **Dataset Characteristics**
- **Pros:**  
  ✅ Balanced class distribution  
  ✅ Covers diverse general food types  
  ✅ Common benchmark dataset for food recognition  

- **Cons / Issues:**  
  ❌ No calorie or portion information  
  ⚠️ Contains noisy data (mislabeled or over-saturated images)  
  ⚠️ Generalized labels (e.g., `pizza` instead of `pepperoni_pizza`)  

---

## **2. Food-251**
**Source:** [Singla et al., 2019 – Food Recognition in the Wild](https://ar5iv.labs.arxiv.org/html/1907.06167)

### **Dataset Summary**
| Attribute | Description |
|------------|--------------|
| **Classes** | 251 |
| **Total Images** | 158,846 |
| **Images per Class (avg.)** | ≈ 632 |
| **Train Set** | ≈ 118,000 images (≈ 470 per class) |
| **Test Set** | ≈ 28,000 images (≈ 112 per class) |
| **Derived From** | Food-101 (extended & re-labeled) |
| **Food Type** | Both Western and Asian cuisines (mostly cooked foods) |
| **Category Type** | **Multi-category** dataset (images can contain multiple food items) |

### **Dataset Characteristics**
- **Improvements over Food-101:**  
  ✅ More specific labels (e.g., `pepperoni_pizza`, `carbonara_pasta`)  
  ✅ ~40,000 human-verified labels for greater annotation quality  

- **Limitations:**  
  ⚠️ Inherits some noise from Food-101  
  ⚠️ Uneven visual conditions (lighting, plating styles, etc.)  

---

## **3. Comparative Observations**

| Aspect | **Food-101** | **Food-251** |
|--------|---------------|---------------|
| **Type** | Single-category | Multi-category |
| **Cuisine Focus** | Western | Global (Western + Asian) |
| **Cooked vs Raw Food** | Mostly cooked | Mostly cooked + some raw ingredients |
| **Label Specificity** | General labels (e.g., `pizza`) | Fine-grained labels (e.g., `pepperoni_pizza`) |
| **Use Case** | Baseline classification tasks | Advanced multi-label and contextual food recognition |
| **Metadata (Nutrition/Portion)** | Not available | Not available |

### **Research Considerations**
- Both datasets are excellent for **food recognition/classification** benchmarks.  
- Neither contains nutritional metadata (calories, portion size).  
- For **nutritional estimation**, you must combine them with complementary datasets (e.g., Nutrition5k, Food-Calorie-DB).

---

## **4. References**
1. Bossard, L., Guillaumin, M., & Van Gool, L. (2014).  
   *Food-101 – Mining Discriminative Components with Random Forests.* ECCV 2014.  
   [PDF](https://data.vision.ee.ethz.ch/cvl/datasets_extra/food-101/static/bossard_eccv14_food-101.pdf)  

2. Singla, A., Yuan, L., Ebrahimi, S. (2019).  
   *Food Recognition in the Wild.*  
   [arXiv Link](https://ar5iv.labs.arxiv.org/html/1907.06167)
