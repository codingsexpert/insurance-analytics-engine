"""
Tweedie Compound Pure Premium Model.
Models Pure Premium = Total Loss / Exposure
using scikit-learn TweedieRegressor (variance power p = 1.5).
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import TweedieRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from typing import Dict, Any
import joblib
import os

class TweedieModel:
    def __init__(self, tweedie_variance_power: float = 1.5):
        self.tweedie_variance_power = tweedie_variance_power
        self.pipeline = None
        self.cat_cols = ['vehicle_type', 'territory']
        self.num_cols = [
            'driver_age', 'driving_experience', 'vehicle_age', 
            'vehicle_value', 'annual_mileage', 'bonus_malus', 
            'policy_tenure', 'deductible'
        ]

    def train(self, train_df: pd.DataFrame, val_df: pd.DataFrame = None):
        """Fits a Tweedie Generalized Linear Model with log link and exposure weights."""
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), self.num_cols),
                ('cat', OneHotEncoder(drop='first', sparse_output=False), self.cat_cols)
            ]
        )
        
        regressor = TweedieRegressor(
            power=self.tweedie_variance_power,
            link='log',
            max_iter=300,
            alpha=0.01
        )
        
        self.pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', regressor)
        ])
        
        X_train = train_df[self.num_cols + self.cat_cols]
        # Target: Loss rate per exposure
        y_train = train_df['total_claim_amount'] / train_df['exposure']
        weights = train_df['exposure'].values
        
        self.pipeline.fit(X_train, y_train, regressor__sample_weight=weights)
        return self.pipeline

    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """Predicts annual pure premium rate (per unit exposure)."""
        X = df[self.num_cols + self.cat_cols]
        return self.pipeline.predict(X)

    def save(self, directory: str = "models_saved"):
        os.makedirs(directory, exist_ok=True)
        joblib.dump(self.pipeline, os.path.join(directory, "tweedie_pipeline.joblib"))
