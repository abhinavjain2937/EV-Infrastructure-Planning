# ⚡ EV Charging Infrastructure Optimization

### A Data-Driven Approach using XGBoost and MCDM

* **Deployed Project Report:** [Click here to view the Interactive Report](https://arpitmakkar12.github.io/Decision-Support-Tools-for-EV-Infrastructure-Planning/)  
* **Interactive Enhanced EV Heat Map:** [Click here to view the Interactive Map](https://arpitmakkar12.github.io/Decision-Support-Tools-for-EV-Infrastructure-Planning/chapters/Enhanced_EV_Map.html)

---

## 📖 Project Overview

The rapid adoption of Electric Vehicles (EVs) is hindered by "range anxiety" and the lack of accessible charging infrastructure. This project aims to solve the **Optimal Location Problem** for EV charging stations using a machine learning pipeline.

By integrating diverse geospatial datasets (traffic volume, population density, commercial/residential POIs, and road networks), we predict charging demand at a granular level and rank locations using a Multi-Criteria Decision Making (MCDM) system.

### 🔑 Key Features

* **Geospatial Feature Engineering:** Aggregated OpenStreetMap (OSM) data, demographic stats, and traffic sensor logs.
* **Predictive Modeling:** Trained an **XGBoost Regressor** to predict localized energy demand scores (R² ≈ 0.88).
* **Decision Support System:** Implemented an **MCDM Layer** to filter and rank the "Top 300" investment-ready sites.
* **Interactive Reporting:** Fully automated Quarto-based reporting with interactive geospatial visualizations.

---

## 📂 Project Organization

```
├── README.md          <- The top-level README for describing highlights for using this ML project.
│
├── notebooks          <- Jupyter notebooks. Naming convention: snake_case (e.g., final_last_model.ipynb).
│
├── reports            
│   ├── figures        <- Generated graphics and figures to be used in reporting.
│   ├── README.md      <- Youtube Video Link (Project Walkthrough).
│   ├── final_project_report <- Final report in .pdf/html format and supporting Quarto files.
│   └── presentation   <- Final PowerPoint presentation (.pptx).
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment.
│
├── src                <- Source code for use in this project.
│   ├── __init__.py    <- Makes src a Python module.
│   │
│   ├── data
│   │   ├── processed      <- The final, canonical data sets for modeling.
│   │   └── raw            <- The original, immutable data dump (OSM, Traffic, etc.).
│   │
│   ├── preprocessing_data           
│   │   └── pre-processing.py  <- Scripts to clean, merge, and impute missing data.
│   │
│   ├── feature_engineering       
│   │   └── build_features.py  <- Scripts to create density maps, centrality scores, and entropy indices.
│   │
│   ├── models         
│   │   ├── predict_model.py   <- Script to generate demand scores using the trained model.
│   │   └── train_model.py     <- Script to train XGBoost and save model artifacts.
│   │
│   ├── visualization  
│   │   └── visualize.py       <- Scripts to create static plots and interactive Folium maps.
│   │
│   └── main.py  <- Main orchestrator script to run the full pipeline.
│
├── LICENSE      <- MIT License terms.
```

---

## 🛠️ Installation & Setup

### 1. Prerequisites

* **Python Version:** `3.10` or higher is required.
* **Git LFS:** Required for handling large model files or HTML reports (if applicable).

### 2. Clone the Repository

```bash
git clone https://github.com/SabudhFoundation/batch-15-ev_infratructre_planning.git
cd batch-15-ev_infratructre_planning
```

### 3. Create a Virtual Environment

It is recommended to use a clean environment to avoid dependency conflicts.

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

You can run the entire pipeline using the master script, or execute individual modules manually.

### Option A: Run Full Pipeline

```bash
python src/main.py
```

*This will trigger preprocessing, feature engineering, model training, and result visualization in sequence.*

### Option B: Run Modules Individually

**1. Data Preprocessing:**

```bash
python src/preprocessing_data/pre-processing.py
```

**2. Feature Engineering:**

```bash
python src/feature_engineering/build_features.py
```

**3. Train Model:**

```bash
python src/models/train_model.py
```

**4. Generate Visualizations & Map:**

```bash
python src/visualization/visualize.py
```

---

## 📊 Results Summary

* **Best Model:** XGBoost Regressor
* **Accuracy:** RMSE: 42.1 | R²: 0.88
* **Top Predictors:** Traffic Volume, Commercial POI Density, Road Network Centrality.
* **Output:** A prioritized list of 300 optimal coordinates for charging stations, visualized in `reports/final_project_report`.

---

## 🤝 Contributors

* **Arpit Makkar**
* **Sarvagya Sharma**
* **Abhinav Jain**
* **Shashwat Shukla**

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
