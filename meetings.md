# Meeting Minutes

## Meeting Information

**Meeting Date/Time:** Oct 3rd

### Plan of the project:

#### **EV infrastructure planning tool, ROI and the importance of demand forecasting**

- **Purpose of planning tools** – EV‑charging infrastructure planning tools (e.g., NREL's **EVI‑Pro** and its web‑based **EVI‑Pro Lite**) help planners estimate the number and types of chargers needed. These tools utilize detailed data on typical daily travel patterns, EV characteristics, and charger types.
- **ROI analysis** – Because chargers are costly, planners must evaluate potential return on investment (ROI).
- **Demand forecasting as the first step** – Accurately forecasting EV charging demand is a **critical first step** in infrastructure planning. EVI-Pro works by analyzing travel-pattern data and user behaviour to forecast charging demand.

### Action Items

- Papers EV charging demand prediction (4 - 5) from IEEE, Elsevier, ScienceDirect.
- Identify datasets and features for modeling.

---

## Meeting Information

**Meeting Date/Time:** Oct 10th

### Work Updation:

- **Arpit Makkar:**
  - Initialized the Git repository using the standard cookiecutter data science structure.
  - Configured the virtual environment (`ev_project_env`) and resolved initial dependency conflicts for `geopandas` and `folium`.
  - Started searching for traffic sensor data APIs (focusing on localized urban data).

- **Sarvagya Sharma:**
  - Conducted deep-dive analysis into OpenStreetMap (OSM) data extraction tools (`osmnx`).
  - Identified key Points of Interest (POI) categories (Malls, Residential, Hospitals) required for demand correlation.

- **Abhinav & Shashwat:**
  - Reviewed literature on "Range Anxiety" and defined the project scope to focus on destination charging rather than highway charging.

---

## Meeting Information

**Meeting Date/Time:** Oct 17th

### Work Updation:

- **Arpit Makkar:**
  - Successfully loaded the raw `HERO_dataset.csv`.
  - Wrote scripts to clean column names (stripping whitespace) and identified encoding issues (`ISO-8859-1`).
  - Proposed a folder structure for raw vs. processed data to ensure reproducibility.

- **Sarvagya Sharma:**
  - Performed initial quality checks on the dataset.
  - Discovered a significant number of grid points located in oceans or uninhabited forestry.
  - Defined the logic for the "valid land mask" (must have roads OR commercial activity).

- **Team:**
  - Agreed to use a grid-based approach rather than point-based to normalize density.

---

## Meeting Information

**Meeting Date/Time:** Oct 24th

### Work Updation:

- **Arpit Makkar:**
  - Developed the `src/preprocessing_data/pre-processing.py` module.
  - Implemented the outlier removal logic: Dropped 250k+ rows where `road_density_total < 0.01`.
  - Integrated Median Imputation for missing traffic volume data.

- **Sarvagya Sharma:**
  - Conducted Univariate Analysis on the cleaned data.
  - Created histograms and boxplots showing that `poi_density` follows a Power Law distribution (highly skewed).
  - Recommended using non-linear models (Trees/Boosting) instead of simple regression due to data skewness.

---

## Meeting Information

**Meeting Date/Time:** Oct 31st

### Work Updation:

- **Arpit Makkar:**
  - Started Feature Engineering phase.
  - Researched "Land Use Entropy" formulas to quantify mixed-use developments (Diversity Index).
  - Wrote the NumPy implementation to calculate entropy based on residential vs. commercial proportions.

- **Sarvagya Sharma:**
  - Generated the Feature Correlation Matrix (`Figure 2.2`).
  - Identified high multicollinearity between `road_density_primary` and `poi_density_commercial`.
  - Proposed dropping redundant centrality measures (`betweenness`, `closeness`) to reduce noise.

---

## Meeting Information

**Meeting Date/Time:** Nov 7th

### Work Updation:

- **Arpit Makkar:**
  - Set up the Stratified Train-Test split (80/20) ensuring high-traffic zones were equally represented in both sets.
  - Defined the target variable: `demand_score_kwh_only`.

- **Sarvagya Sharma:**
  - Trained the baseline **Linear Regression** model.
  - Evaluation showed poor performance (R² ≈ 0.42), confirming that linear assumptions do not hold for complex urban data.
  - Suggested moving to Random Forest or XGBoost.

---

## Meeting Information

**Meeting Date/Time:** Nov 14th, 6:30 pm

### Work Updation:

- **Sarvagya Sharma:**
  - Discussed dataset exploration results, confirming the need for normalization.
  - Identified the target features and finalized the feature engineering list.
  - Discussed the future scope of the dataset (adding temporal data) and how to proceed with tree-based models.

- **Arpit Makkar:**
  - Conducted a feasibility analysis on the dataset structure to ensure compatibility with Scikit-Learn.
  - Collaborated on the dataset selection strategy by evaluating alternative sources.
  - Outlined necessary preprocessing steps for the preliminary model pipeline (One-Hot Encoding for grid types).

---

## Meeting Information

**Meeting Date/Time:** Nov 21st

### Work Updation:

- **Arpit Makkar:**
  - Implemented the **XGBoost Regressor** in `src/models/train_model.py`.
  - Handled the "Categorical Data" error in XGBoost by dropping non-informative object columns.
  - Tuned hyperparameters (`learning_rate=0.02`, `n_estimators=100`).

- **Sarvagya Sharma:**
  - Implemented and trained the **Random Forest Regressor** for comparison.
  - Analyzed feature importance: Found that Traffic Volume and Commercial POI density were top drivers.
  - Comparing results: XGBoost (R²=0.88) significantly outperformed Random Forest (R²=0.76).

---

## Meeting Information

**Meeting Date/Time:** Nov 28th

### Work Updation:

- **Arpit Makkar:**
  - Designed the **MCDM (Multi-Criteria Decision Making)** logic.
  - Created the weighted formula: Score = 0.4 · Demand + 0.2 · Access + 0.2 · Centrality + 0.2 · Entropy.
  - Coded the ranking system in `src/models/predict_model.py`.

- **Sarvagya Sharma:**
  - Solved the "Cluster Problem" (recommendations stacking on top of each other).
  - Implemented **DBSCAN Clustering** to group nearby high-score points and select only the best candidate per 500m radius.
  - Filtered the final output to the "Top 300" actionable sites.

---

## Meeting Information

**Meeting Date/Time:** Dec 5th

### Work Updation:

- **Arpit Makkar:**
  - Developed the visualization module (`src/visualization/visualize.py`).
  - Integrated **Folium** to generate the interactive Heatmap (`Enhanced_EV_Map.html`).
  - Added popup markers showing Rank, MCDM Score, and Demand Probability.

- **Sarvagya Sharma:**
  - Set up the **Quarto** reporting structure.
  - Wrote the "Methodology" and "Results" chapters, embedding the static plots generated by the pipeline.
  - Ensured references and citations were formatted correctly in `references.bib`.

---

## Meeting Information

**Meeting Date/Time:** Dec 12th

### Work Updation:

- **Arpit Makkar:**
  - Managed the deployment to **GitHub Pages**.
  - Debugged the "Large File Error" (HTML maps > 100MB) by configuring `git lfs` and optimizing Quarto's `self-contained: false` setting.
  - Fixed the 404 URL errors in `_quarto.yml` to ensure the site loaded correctly on the custom domain.

- **Sarvagya Sharma:**
  - Finalized the `README.md` with detailed project structure and installation instructions.
  - Compiled the `requirements.txt` to ensure reproducibility.
  - Conducted a final review of the "Conclusion" and "Future Work" sections in the report.
  - Verified the live deployment links.
