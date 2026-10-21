"""
Actuarial Claim Frequency Modeling.
Provides:
1. Actuarial Poisson GLM (statsmodels) with exposure offset.
2. Histogram Gradient Boosted Poisson Regressor (scikit-learn).
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

class FrequencyModel:
    def __init__(self):
        self.glm_model = None
        self.hgb_model = None
        self.feature_names = [
            'driver_age', 'driving_experience', 'vehicle_age', 
            'vehicle_value', 'annual_mileage', 'bonus_malus', 
            'policy_tenure', 'deductible', 'vehicle_type', 'territory'
        ]
        self.cat_cols = ['vehicle_type', 'territory']
        self.encoder = OrdinalEncoder()

    def train_glm(self, train_df: pd.DataFrame):
        """Fits an interpretable actuarial Poisson GLM with log link and exposure offset."""
        formula = """
        claim_count ~ driver_age + driving_experience + vehicle_age + 
                      np.log(vehicle_value) + np.log(annual_mileage) + 
                      bonus_malus + policy_tenure + deductible + 
                      C(vehicle_type) + C(territory)
        """
        self.glm_model = smf.glm(
            formula=formula,
            data=train_df,
            family=sm.families.Poisson(link=sm.families.links.Log()),
            offset=np.log(train_df['exposure'])
        ).fit()
        return self.glm_model

    def train_booster(self, train_df: pd.DataFrame, val_df: pd.DataFrame):
        """Fits a Poisson Histogram Gradient Booster (no libomp dependency)."""
        X_train = train_df[self.feature_names].copy()
        X_train[self.cat_cols] = self.encoder.fit_transform(X_train[self.cat_cols])
        
        # Exposure rate: claim_count / exposure with sample_weight = exposure
        y_train = train_df['claim_count'] / train_df['exposure']
        weights = train_df['exposure'].values
        
        self.hgb_model = HistGradientBoostingRegressor(
            loss='poisson',
            learning_rate=0.06,
            max_iter=200,
            max_leaf_nodes=31,
            random_state=42
        )
        self.hgb_model.fit(X_train, y_train, sample_weight=weights)
        return self.hgb_model

    def predict(self, df: pd.DataFrame, model_type: str = 'booster') -> np.ndarray:
        """Predicts expected claim count for given policy exposures."""
        exposure = df['exposure'].values
        if model_type == 'glm':
            return self.glm_model.predict(df, offset=np.log(exposure)).values
        else:
            X = df[self.feature_names].copy()
            X[self.cat_cols] = self.encoder.transform(X[self.cat_cols])
            pred_rate = self.hgb_model.predict(X)
            return exposure * pred_rate

    def save(self, directory: str = "models_saved"):
        os.makedirs(directory, exist_ok=True)
        joblib.dump(self.glm_model, os.path.join(directory, "freq_glm.joblib"))
        joblib.dump({
            'model': self.hgb_model,
            'encoder': self.encoder,
            'features': self.feature_names
        }, os.path.join(directory, "freq_booster.joblib"))
