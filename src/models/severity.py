"""
Actuarial Claim Severity Modeling.
Provides:
1. Actuarial Gamma GLM (statsmodels) with log link.
2. Histogram Gradient Boosted Gamma Regressor (scikit-learn).
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.preprocessing import OrdinalEncoder
from typing import Dict, Any
import joblib
import os

class SeverityModel:
    def __init__(self):
        self.glm_model = None
        self.hgb_model = None
        self.feature_names = [
            'vehicle_age', 'vehicle_value', 'vehicle_type', 
            'deductible', 'territory', 'annual_mileage'
        ]
        self.cat_cols = ['vehicle_type', 'territory']
        self.encoder = OrdinalEncoder()

    def train_glm(self, train_df: pd.DataFrame):
        """Fits an actuarial Gamma GLM with log link, weighted by claim count."""
        claims_df = train_df[train_df['claim_count'] > 0].copy()
        claims_df['avg_severity'] = claims_df['total_claim_amount'] / claims_df['claim_count']
        
        formula = """
        avg_severity ~ vehicle_age + np.log(vehicle_value) + deductible + 
                       np.log(annual_mileage) + C(vehicle_type) + C(territory)
        """
        self.glm_model = smf.glm(
            formula=formula,
            data=claims_df,
            family=sm.families.Gamma(link=sm.families.links.Log()),
            var_weights=claims_df['claim_count']
        ).fit()
        return self.glm_model

    def train_booster(self, train_df: pd.DataFrame, val_df: pd.DataFrame):
        """Fits a Gamma objective gradient booster on positive claims."""
        train_pos = train_df[train_df['claim_count'] > 0].copy()
        
        X_train = train_pos[self.feature_names].copy()
        X_train[self.cat_cols] = self.encoder.fit_transform(X_train[self.cat_cols])
        
        y_train = train_pos['total_claim_amount'] / train_pos['claim_count']
        weights = train_pos['claim_count'].values
        
        self.hgb_model = HistGradientBoostingRegressor(
            loss='gamma',
            learning_rate=0.05,
            max_iter=150,
            max_leaf_nodes=25,
            random_state=42
        )
        self.hgb_model.fit(X_train, y_train, sample_weight=weights)
        return self.hgb_model

    def predict(self, df: pd.DataFrame, model_type: str = 'booster') -> np.ndarray:
        """Predicts expected conditional claim severity ($)."""
        if model_type == 'glm':
            return self.glm_model.predict(df).values
        else:
            X = df[self.feature_names].copy()
            X[self.cat_cols] = self.encoder.transform(X[self.cat_cols])
            return self.hgb_model.predict(X)

    def save(self, directory: str = "models_saved"):
        os.makedirs(directory, exist_ok=True)
        joblib.dump(self.glm_model, os.path.join(directory, "sev_glm.joblib"))
        joblib.dump({
            'model': self.hgb_model,
            'encoder': self.encoder,
            'features': self.feature_names
        }, os.path.join(directory, "sev_booster.joblib"))
