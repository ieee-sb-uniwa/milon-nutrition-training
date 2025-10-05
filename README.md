# MILON Nutrition Training

Model training pipeline for food recognition and nutritional analysis.

## Project Structure

```
milon-nutrition-training/
├── data/
│   ├── raw/              # Original datasets (Food-101, FoodX-251)
│   ├── processed/        # Preprocessed and augmented images
│   └── annotations/      # Labels, bounding boxes, nutritional data
├── notebooks/
│   ├── 01_eda.ipynb           # Exploratory data analysis
│   ├── 02_preprocessing.ipynb # Data preprocessing experiments
│   └── 03_experiments.ipynb   # Model experiments and analysis
├── src/
│   ├── data/
│   │   ├── dataset.py         # PyTorch Dataset classes
│   │   └── transforms.py      # Augmentation pipelines
│   ├── models/
│   │   ├── yolo.py            # YOLOv8 detection model
│   │   ├── classifier.py      # Food classification models
│   │   └── nutrition_estimator.py # Calorie/nutrient prediction
│   ├── training/
│   │   ├── train.py           # Training scripts
│   │   └── evaluate.py        # Evaluation and metrics
│   └── utils/
│       ├── metrics.py         # Custom metrics (mAP, calorie error)
│       └── config.py          # Configuration management
├── configs/
│   └── yolov8_food.yaml      # Model hyperparameters
├── experiments/              # Training logs, checkpoints, results
├── requirements.txt
└── README.md
```

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Train food detection model
python src/training/train.py --config configs/yolov8_food.yaml

# Evaluate model
python src/training/evaluate.py --checkpoint experiments/best.pt
```

## Related

- Trained models available in [Releases](https://github.com/your-org/milon-nutrition-training/releases)
- **Dataset Info**: [Food-101](https://data.vision.ee.ethz.ch/cvl/datasets_extra/food-101/) and [FoodX-251](https://www.kaggle.com/competitions/ifood-2019-fgvc6/data)
