# 🍽️ Food Datasets Overview

## **1. Food-101**
**Source:** [Food-101 Dataset (Bossard et al., 2014)](https://data.vision.ee.ethz.ch/cvl/datasets_extra/food-101/static/bossard_eccv14_food-101.pdf)

### **Dataset Summary**
| Attribute | Description |
|------------|--------------|
| **Classes** | 101 |
| **Total Images** | 101,000 |
| **Train Images per Class** | 750 |
| **Test Images per Class** | 250 |
| **Image Resolution** | 512 × 512 px (uniform) |
| **Image Variations** | Lighting, angle, and preparation style vary widely |

### **Dataset Characteristics**
- **Pros:**  
  - Balanced class distribution  
  - Covers a wide range of general food types  
  - Widely used for baseline benchmarking  

- **Cons / Issues:**  
  - ❌ **No calorie or portion information**  
  - ⚠️ **Contains noisy data** (some mislabeled or color-intense samples)  
  - ⚠️ **Generalized labels** (e.g., “pizza” instead of “pepperoni pizza”)  

---

## **2. Food-251**
**Source:** [Food-251 Dataset (Kawano et al., 2022)](https://ar5iv.labs.arxiv.org/html/1907.06167)  

### **Dataset Summary**
| Attribute | Description |
|------------|--------------|
| **Classes** | 251 |
| **Total Images** | 158,846 |
| **Images per Class (avg.)** | ~632 |
| **Train Set** | ~118,000 images → ~470 per class |
| **Test Set** | ~28,000 images → ~112 per class |
| **Derived From** | Food-101 (extended and relabeled) |

### **Dataset Characteristics**
- **Improvements over Food-101:**  
  - ✅ **More specific labels** (e.g., “pepperoni pizza”, “carbonara pasta”)  
  - ✅ **~40K human-verified labels** for improved annotation quality  

- **Limitations:**  
  - ⚠️ Still inherits noise from Food-101  
  - ⚠️ Uneven visual conditions (lighting, plating styles, etc.)  

---

## **3. Observations**
- **Label Hierarchy:**  
  Food-251 refines the general labels of Food-101 into more granular subclasses.  
  Example:  
  - *Food-101:* `pizza`  
  - *Food-251:* `pepperoni_pizza`, `margherita_pizza`, etc.

- **Research Considerations:**  
  - These datasets are ideal for **food recognition and classification** tasks.  
  - For **nutritional estimation (calories, portion size)**, additional metadata or complementary datasets are required.  

---

## **References**
1. Bossard, L., Guillaumin, M., & Van Gool, L. (2014). *Food-101 – Mining Discriminative Components with Random Forests*. ECCV 2014.[PDF](https://data.vision.ee.ethz.ch/cvl/datasets_extra/food-101/static/bossard_eccv14_food-101.pdf)  
2. Singla, A., Yuan, L., Ebrahimi, S. (2019). *Food Recognition in the Wild*. [Site](https://ar5iv.labs.arxiv.org/html/1907.06167) 