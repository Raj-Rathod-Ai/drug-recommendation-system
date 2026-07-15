import os
import pickle
import pandas as pd
import numpy as np

# Column statistics derived from the dataset
DEFAULTS = {
    'Age': 45.0,
    'Sex': 'F',
    'BP': 'NORMAL',
    'Cholesterol': 'NORMAL',
    'Na_to_K': 13.94
}

VALIDATION_LIMITS = {
    'Age': {'min': 1.0, 'max': 120.0, 'step': 1.0},
    'Na_to_K': {'min': 5.0, 'max': 45.0, 'step': 0.1}
}

# Training mappings:
# Sex: F -> 0, M -> 1
SEX_MAPPING = {'F': 0, 'M': 1, 'Female': 0, 'Male': 1}

# BP: HIGH -> 0, LOW -> 1, NORMAL -> 2
BP_MAPPING = {'HIGH': 0, 'LOW': 1, 'NORMAL': 2, 'High': 0, 'Low': 1, 'Normal': 2}

# Cholesterol: HIGH -> 0, NORMAL -> 1
CHOLESTEROL_MAPPING = {'HIGH': 0, 'NORMAL': 1, 'High': 0, 'Normal': 1}

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'best_decision_tree_model.pkl')

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    return model

def predict_drug(age, sex, bp, cholesterol, na_to_k):
    """
    Predict recommended drug and prediction confidence percentage.
    Inputs are encoded automatically. Missing inputs default safely.
    """
    model = load_model()
    
    # Encode categorical features
    encoded_sex = SEX_MAPPING.get(sex, SEX_MAPPING[DEFAULTS['Sex']])
    encoded_bp = BP_MAPPING.get(bp, BP_MAPPING[DEFAULTS['BP']])
    encoded_chol = CHOLESTEROL_MAPPING.get(cholesterol, CHOLESTEROL_MAPPING[DEFAULTS['Cholesterol']])
    
    # Handle numeric fallbacks
    val_age = age if age is not None else DEFAULTS['Age']
    val_nak = na_to_k if na_to_k is not None else DEFAULTS['Na_to_K']
    
    # Create DataFrame matching model feature names
    # Features in model: ['Age' 'Sex' 'BP' 'Cholesterol' 'Na_to_K']
    features_df = pd.DataFrame([{
        'Age': float(val_age),
        'Sex': encoded_sex,
        'BP': encoded_bp,
        'Cholesterol': encoded_chol,
        'Na_to_K': float(val_nak)
    }])
    
    # Get class predictions and probabilities
    pred_class = model.predict(features_df)[0]
    probabilities = model.predict_proba(features_df)[0]
    
    # Find probability corresponding to predicted class
    class_idx = list(model.classes_).index(pred_class)
    confidence = float(probabilities[class_idx]) * 100.0
    
    return str(pred_class), confidence
