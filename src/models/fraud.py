"""
Claim Fraud Detection & Triage Model.
Predicts likelihood of claim fraud based on claim details, timing, and policy tenure.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, average_precision_score, classification_report
import joblib
import os

class FraudModel:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=150,
            max_depth=8,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        )
        self.feature_names = [
            'days_to_report', 'paid_amount', 'driver_age', 
            'vehicle_age', 'vehicle_value', 'bonus_malus', 
            'policy_tenure', 'deductible'
        ]
        self.cat_cols = ['claim_type', 'territory']

    def train(self, claims_joined_df: pd.DataFrame):
        """Trains fraud model on joined claims and policy dataset."""
        df = claims_joined_df.copy()
        
        # One-hot encode categoricals
        X = pd.get_dummies(df[self.feature_names + self.cat_cols], drop_first=True)
        self.train_columns_ = X.columns.tolist()
        y = df['is_fraud']
        
        self.model.fit(X, y)
        train_probs = self.model.predict_proba(X)[:, 1]
        
        pr_auc = average_precision_score(y, train_probs)
        roc_auc = roc_auc_score(y, train_probs)
        
        return {
            'pr_auc': round(pr_auc, 4),
            'roc_auc': round(roc_auc, 4),
            'n_samples': len(df),
            'fraud_prevalence': round(y.mean(), 4)
        }

    def predict_proba(self, claims_df: pd.DataFrame) -> np.ndarray:
        """Returns fraud probability score [0.0 - 1.0]."""
        X = pd.get_dummies(claims_df[self.feature_names + self.cat_cols], drop_first=True)
        # Align columns
        for col in self.train_columns_:
            if col not in X:
                X[col] = 0
        X = X[self.train_columns_]
        return self.model.predict_proba(X)[:, 1]

    def save(self, directory: str = "models_saved"):
        os.makedirs(directory, exist_ok=True)
        joblib.dump({
            'model': self.model,
            'train_columns': self.train_columns_,
            'feature_names': self.feature_names
        }, os.path.join(directory, "fraud_model.joblib"))
