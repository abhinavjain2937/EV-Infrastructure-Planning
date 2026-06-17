import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import DBSCAN

def load_model(path="models/Final_Research_Ensemble_Model.pkl"):
    return joblib.load(path)

def predict_and_rank(model, df, X_features):
    print("Running MCDM Ranking & Optimization...")
    
    # 1. Predict Probabilities (AI Demand)
    probs = model.predict_proba(X_features)
    df['AI_Demand_Prob'] = probs[:, 2]  # Probability of High Demand Class

    # 2. Filter Candidates (The Ocean/Wilderness Filter)
    # Re-calculate local infrastructure sum for filtering
    df['Local_Road_Density'] = df.get('road_density_secondary', 0) + df.get('road_density_tertiary', 0)
    df['Inhabited_Activity'] = df.get('poi_density_commercial', 0) + df.get('poi_density_residential', 0)

    # Filter Logic
    candidates = df[
        (df['AI_Demand_Prob'] > 0.50) &
        (df['Local_Road_Density'] > 0.01) &
        (df['Inhabited_Activity'] > 0.05)
    ].copy()

    if len(candidates) == 0:
        print("WARNING: Strict filters returned 0 candidates. Using top 500 by demand.")
        candidates = df.sort_values(by='AI_Demand_Prob', ascending=False).head(500).copy()

    # 3. MCDM Scoring
    scaler = MinMaxScaler()
    
    # Normalize components for fair weighting
    c_norm = scaler.fit_transform(candidates[['urban_centrality_score']].fillna(0)).flatten()
    d_norm = scaler.fit_transform(candidates[['AI_Demand_Prob']]).flatten()
    e_norm = scaler.fit_transform(candidates[['land_use_entropy']].fillna(0)).flatten()
    
    # Weighted Formula
    candidates['MCDM_Score'] = (
        (0.40 * d_norm) +
        (0.20 * scaler.fit_transform(candidates[['Local_Road_Density']]).flatten()) +
        (0.20 * c_norm) +
        (0.20 * e_norm)
    )

    # 4. DBSCAN Clustering (De-duplication)
    print("   -> Clustering nearby points...")
    coords = candidates[['latitude_x', 'longitude_x']].values
    db = DBSCAN(eps=0.005, min_samples=1, metric='euclidean').fit(coords)
    candidates['Cluster_ID'] = db.labels_

    # 5. Pick Winners (Best Score per Cluster)
    final_sites = []
    for cluster_id, group in candidates.groupby('Cluster_ID'):
        winner = group.loc[group['MCDM_Score'].idxmax()]
        final_sites.append(winner)

    final_df = pd.DataFrame(final_sites).sort_values(by='MCDM_Score', ascending=False).head(300)
    print(f"   -> Selected Top {len(final_df)} Locations.")
    
    return final_df
