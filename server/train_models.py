import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import math
import os

def train_and_save_models():
    # Compute base directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
    MODELS_DIR = os.path.join(BASE_DIR, 'models')
    
    # Create models directory if it doesn't exist
    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR)

    # 1. Simple Home Price Model (Area, Bedrooms, Age)
    print("Training Simple Home Price Model...")
    df = pd.read_csv(os.path.join(DATA_DIR, "homeprices.csv"))
    
    # Pre-processing
    if 'bedrooms' in df.columns:
        median_bedroom = math.floor(df.bedrooms.median())
        df.bedrooms = df.bedrooms.fillna(median_bedroom)
    
    reg_simple = LinearRegression()
    # Features: area, bedrooms, age
    reg_simple.fit(df[['area', 'bedrooms', 'age']], df.price)
    joblib.dump(reg_simple, os.path.join(MODELS_DIR, 'model_simple.joblib'))
    print(f"Simple model saved to {MODELS_DIR}")

    # 2. Town Price Model (Town, Area)
    print("Training Town Price Model...")
    df_town = pd.read_csv(os.path.join(DATA_DIR, 'townprices.csv'))
    
    # Use only original columns if they exist
    df_town = df_town[['town', 'area', 'price']]
    
    dummies = pd.get_dummies(df_town.town)
    merged = pd.concat([df_town, dummies], axis='columns')
    final = merged.drop(['town', 'west windsor'], axis='columns')
    
    X = final.drop('price', axis='columns')
    y = final.price
    
    reg_town = LinearRegression()
    reg_town.fit(X.values, y)
    
    # Save the model and the columns (for dummy variable mapping)
    model_data = {
        'model': reg_town,
        'columns': X.columns.tolist()
    }
    joblib.dump(model_data, os.path.join(MODELS_DIR, 'model_town.joblib'))
    print("Town model saved successfully.")

if __name__ == "__main__":
    train_and_save_models()
