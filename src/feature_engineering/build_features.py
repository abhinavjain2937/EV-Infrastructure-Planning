import pandas as pd
import numpy as np
import re

# Define the final features selected in your notebook
FINAL_FEATURES = [
    'land_use_entropy', 
    'poi_density_commercial', 
    'poi_density_residential', 
    'road_density_primary', 
    'urban_centrality_score', 
    'mixed_use_index'
]

def engineer_features(df):
    """
    Calculates Land Use Entropy and prepares the feature matrix X.
    """
    print("Engineering Advanced Features...")
    
    # 1. Calculate Land Use Entropy
    poi_cols = ['poi_density_commercial', 'poi_density_residential', 'poi_density_industrial', 
                'poi_density_recreational', 'poi_density_transport_hub']
    
    existing_poi_cols = [c for c in poi_cols if c in df.columns]

    if existing_poi_cols:
        # Avoid division by zero
        df['total_poi'] = df[existing_poi_cols].sum(axis=1) + 1e-5 
        proportions = df[existing_poi_cols].div(df['total_poi'], axis=0)
        # Entropy formula
        df['land_use_entropy'] = - (proportions * np.log(proportions + 1e-10)).sum(axis=1)
        print("   -> Created 'land_use_entropy'")
    else:
        df['land_use_entropy'] = 0

    return df

def select_features(df):
    """
    Returns X (features) and y (target) based on final selection.
    """
    # Ensure all final features exist
    valid_feats = [f for f in FINAL_FEATURES if f in df.columns]
    
    X = df[valid_feats].copy()
    
    # Target variable (if training)
    y = None
    if 'demand_score_kwh_only' in df.columns:
        y = df['demand_score_kwh_only']
        
    return X, y
