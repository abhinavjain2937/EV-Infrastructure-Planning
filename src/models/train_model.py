import pandas as pd
import joblib
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.model_selection import train_test_split

def train_and_save(X, y, save_path="models/Final_Research_Ensemble_Model.pkl"):
    print("Training Ensemble AI Model...")

    # Create 3 Classes (Low, Med, High) based on Quantiles
    y_class = pd.qcut(y.fillna(0), q=3, labels=[0, 1, 2])

    # Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y_class, test_size=0.2, random_state=42)

    # Define Models
    clf1 = xgb.XGBClassifier(
        objective='multi:softmax', 
        num_class=3, 
        n_estimators=100, 
        max_depth=6, 
        n_jobs=-1, 
        random_state=42
    )
    clf2 = RandomForestClassifier(
        n_estimators=100, 
        max_depth=8, 
        n_jobs=-1, 
        random_state=42
    )

    # Voting Ensemble
    model = VotingClassifier(estimators=[('xgb', clf1), ('rf', clf2)], voting='soft')
    model.fit(X_train, y_train)

    # Validate
    acc = model.score(X_test, y_test)
    print(f"   -> Ensemble Validation Accuracy: {acc:.2%}")

    # Save
    joblib.dump(model, save_path)
    print(f"SUCCESS: Model saved to {save_path}")
    
    return model
