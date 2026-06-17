import os
import argparse
from src.preprocessing_data import pre_processing
from src.feature_engineering import build_features
from src.models import train_model, predict_model
from src.visualization import visualize

# CONFIG
DATA_PATH = "src/data/raw/HERO_dataset.csv"  # Update this path if needed
MODEL_PATH = "src/models/Final_Research_Ensemble_Model.pkl"

def main():
    # 1. Load & Clean
    df = pre_processing.load_and_clean_data(DATA_PATH)

    # 2. Engineer Features
    df = build_features.engineer_features(df)
    X, y = build_features.select_features(df)

    # 3. Train Model (Only if it doesn't exist or forced)
    if not os.path.exists(MODEL_PATH):
        print("Model not found. Retraining...")
        model = train_model.train_and_save(X, y, MODEL_PATH)
    else:
        print("Loading existing model...")
        model = predict_model.load_model(MODEL_PATH)

    # 4. Inference & Ranking
    # (In a real scenario, you might split X differently here, 
    # but we use the whole dataset for site searching as per notebook)
    top_sites = predict_model.predict_and_rank(model, df, X)

    # 5. Visualize
    visualize.generate_map(top_sites)
    
    print("\nPipeline Execution Complete!")

if __name__ == "__main__":
    main()
