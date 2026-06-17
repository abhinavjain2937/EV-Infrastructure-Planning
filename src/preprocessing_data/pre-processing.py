import pandas as pd
import numpy as np
import sys
import os

def load_and_clean_data(filepath):
    """
    Loads data from CSV, strips whitespace from columns,
    and removes empty locations (ocean/wilderness).
    """
    print("Loading Data...")
    try:
        df = pd.read_csv(filepath, encoding='ISO-8859-1')
        df.columns = df.columns.str.strip()
        print(f"   -> Total Raw Locations: {len(df):,}")
    except FileNotFoundError:
        print(f"ERROR: File not found at {filepath}")
        sys.exit(1)

    print("Cleaning Data (Removing Ocean/Empty Zones)...")
    before_count = len(df)

    # Filter: Must have either roads, commercial activity, or residential activity
    valid_mask = (
        (df.get('road_density_total', 0) > 0.01) | 
        (df.get('poi_density_commercial', 0) > 0) | 
        (df.get('poi_density_residential', 0) > 0)
    )
    df_clean = df[valid_mask].copy()
    
    # Fill remaining NaNs with 0 for density columns
    df_clean = df_clean.fillna(0)

    after_count = len(df_clean)
    print(f"   -> Removed: {before_count - after_count:,} empty locations.")
    print(f"   -> Remaining Valid Land Points: {after_count:,}")
    
    return df_clean

if __name__ == "__main__":
    # For testing independently
    data = load_and_clean_data("data/raw/HERO_dataset.csv")
