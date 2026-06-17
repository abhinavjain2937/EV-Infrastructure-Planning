# Weekly Progress Report

* **Project:** Decision Support Tools for EV-Infrastructure Planning
* **Team Members:** Arpit Makkar, Sarvagya Sharma, Abhinav Jain, Shashwat Shukla
* **Goal:** To develop a data-driven framework for identifying optimal EV charging station locations using XGBoost and MCDM.

---

### Week 1 (Date: Oct 24, 2025)
**Phase: Project Scoping & Data Collection**

**Summary:**
The team initiated the project by defining the scope of the "Optimal Location Problem." We identified that placing EV stations requires balancing grid constraints, traffic flow, and demographic data. We set up the GitHub repository structure and began aggregating raw geospatial data.

**Detailed Progress:**
* **Arpit Makkar:** Initialized the Git repository with the cookiecutter data science structure. Set up the virtual environment (`ev_project_env`) and installed core dependencies (Pandas, GeoPandas). Researched potential data sources for traffic volume logs.
* **Sarvagya Sharma:** Downloaded and inspected the `HERO_dataset.csv`. Performed initial quality checks and identified that the dataset contained significant noise (ocean coordinates and uninhabited forestry zones).
* **Abhinav Jain:** Conducted a literature review on existing methods for EV infrastructure planning. Proposed moving away from simple proximity heuristics to a demand-prediction regression model.
* **Shashwat Shukla:** Started the collection of OpenStreetMap (OSM) data for road networks. Mapped the raw CSV coordinates to physical "grid cells" to standardize the spatial analysis.

**Challenges Faced:**
* Difficulty in aligning traffic sensor data with specific grid coordinates.
* Initial raw dataset was 600k+ rows, causing memory load times to be slow on local machines.

---

### Week 2 (Date: Oct 31, 2025)
**Phase: Data Preprocessing & Exploratory Data Analysis (EDA)**

**Summary:**
This week focused on cleaning the data and understanding the underlying distributions. We removed invalid geospatial points and dealt with missing values in the demographic columns.

**Detailed Progress:**
* **Arpit Makkar:** Developed the cleaning pipeline (`src/preprocessing_data/pre-processing.py`). Implemented a filter to remove grid cells with `road_density_total < 0.01`, effectively removing ocean/wilderness points.
* **Sarvagya Sharma:** Performed Univariate Analysis. Plotted histograms for `poi_density` features and discovered they followed a Power Law distribution (highly skewed), indicating that normalization/scaling would be necessary.
* **Abhinav Jain:** Handled missing values. Implemented Median Imputation for continuous variables like `traffic_volume` and Zero Imputation for POI counts where nulls implied absence of features.
* **Shashwat Shukla:** Created the Correlation Heatmap (`Figure 2.2`). Identified strong multicollinearity between `road_density_primary` and `poi_density_commercial`, noting that tree-based models would handle this better than linear models.

**Challenges Faced:**
* The dataset contained mixed data types in numeric columns, requiring strict type casting.
* Deciding whether to remove outliers (Central Business Districts); we decided to keep them as they represent high-value charging "hotspots."

---

### Week 3 (Date: Nov 7, 2025)
**Phase: Feature Engineering & Selection**

**Summary:**
We shifted focus to creating high-value predictors. We engineered a "Land Use Entropy" feature to measure the diversity of a location (mixed-use vs. single-use).

**Detailed Progress:**
* **Arpit Makkar:** Coded the `land_use_entropy` function using NumPy. This involved calculating the proportion of different POI types (Residential, Commercial, recreational) to quantify urban vibrancy.
* **Sarvagya Sharma:** Created the `urban_centrality_score` by aggregating betweenness centrality and closeness centrality metrics from the road network graph.
* **Abhinav Jain:** Ran Recursive Feature Elimination (RFE) to reduce dimensionality. We narrowed the input features from 40 down to the top 6 most impactful predictors to prevent the "Curse of Dimensionality."
* **Shashwat Shukla:** Documented the feature engineering process in the Quarto methodology section. Verified that the new features showed a stronger correlation with the target `demand_score` than raw columns.

**Challenges Faced:**
* Calculating Entropy involved division by zero errors for empty grid cells; resolved by adding a small epsilon constant ($1e-10$).
* Feature mismatch errors when trying to align the inference dataset with the training schema.

---

### Week 4 (Date: Nov 14, 2025)
**Phase: Model Development & Training**

**Summary:**
We built and compared multiple machine learning models. XGBoost was selected as the final champion model due to its superior performance on non-linear spatial data.

**Detailed Progress:**
* **Arpit Makkar:** Implemented the Training Pipeline (`src/models/train_model.py`). Set up the Stratified Train-Test split (80/20) based on traffic volume bins to ensure representative testing.
* **Sarvagya Sharma:** Trained the baseline Linear Regression model. It yielded a poor $R^2$ of 0.42, confirming that the relationship between urban features and charging demand is highly non-linear.
* **Abhinav Jain:** Implemented the Random Forest Regressor. Achieved decent accuracy ($R^2 \approx 0.76$) but training time was high (12.3s).
* **Shashwat Shukla:** Developed the XGBoost Regressor. Tuned hyperparameters (`max_depth=6`, `learning_rate=0.02`). Achieved the best performance with $R^2 \approx 0.88$ and RMSE of 42.1. Saved the model using `joblib`.

**Challenges Faced:**
* XGBoost initially threw errors regarding categorical column types; we fixed this by dropping non-informative object columns before training.
* Overfitting observed in early Random Forest runs; fixed by limiting tree depth.

---

### Week 5 (Date: Nov 21, 2025)
**Phase: Decision Support System (MCDM) & Optimization**

**Summary:**
Prediction alone was not enough; we needed to select *optimal* sites. We built a Multi-Criteria Decision Making (MCDM) layer to rank the predictions based on suitability constraints.

**Detailed Progress:**
* **Arpit Makkar:** Coded the MCDM scoring logic. We created a composite score: $0.4 \times Demand + 0.2 \times Access + 0.2 \times Centrality + 0.2 \times Entropy$.
* **Sarvagya Sharma:** Implemented DBSCAN clustering on the high-ranking points. This was crucial to prevent the recommendation of 10 stations on the same street corner (De-duplication).
* **Abhinav Jain:** Conducted Sensitivity Analysis. Artificially increased traffic volume by 10% in the test set to observe model behavior, confirming the model's robustness.
* **Shashwat Shukla:** Filtered the final list to the "Top 300" locations. Exported these coordinates for the mapping phase.

**Challenges Faced:**
* The raw model predicted high demand in some physically impossible locations (e.g., inside a dense intersection). The MCDM layer fixed this by weighing `road_density` into the final score.

---

### Week 6 (Date: Nov 28, 2025)
**Phase: Visualization, Reporting & Deployment**

**Summary:**
The final week was dedicated to visualizing results, compiling the Quarto report, and deploying the project to GitHub Pages.

**Detailed Progress:**
* **Arpit Makkar:** Generated the interactive Folium Heatmap (`Enhanced_EV_Map.html`). Added cluster markers with popups showing Demand Score and Rank. Configured the GitHub Actions workflow for deployment.
* **Sarvagya Sharma:** Compiled the "Results" and "Conclusion" chapters of the Quarto report. ensured all tables and figures were cross-referenced correctly.
* **Abhinav Jain:** Solved the "Large File" error during Git push. The HTML map files (>100MB) were blocking the upload. Implemented `git lfs` cleanup and optimized the Quarto `self-contained: false` setting to reduce file sizes.
* **Shashwat Shukla:** Finalized the `README.md`, `requirements.txt`, and project structure documentation. Verified that the deployed website links were working correctly on `sabudh.org` / GitHub Pages.

**Challenges Faced:**
* **Deployment Error:** "File chapters/references.html is 58.36 MB." We realized Quarto was embedding huge datasets into the HTML. Fixed by externalizing resources.
* **404 Errors:** The deployed site initially returned 404 errors due to incorrect `site-url` configuration in `_quarto.yml`. Fixed by updating the base URL to match the repo name.

---
