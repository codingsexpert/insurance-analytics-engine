"""
Actuarial Model Evaluation Metrics.
Includes Gini index (Lorenz curve), Poisson & Gamma deviance,
Double Lift decile charts, and Actual vs. Expected (A/E) ratios.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple

def poisson_deviance(y_true: np.ndarray, y_pred: np.ndarray, weights: np.ndarray = None) -> float:
    """Calculates weighted mean Poisson deviance."""
    eps = 1e-9
    y_pred = np.maximum(y_pred, eps)
    if weights is None:
        weights = np.ones_like(y_true)
        
    # deviance term: 2 * (y * log(y/mu) - (y - mu))
    # where y=0 -> 0 - (0 - mu) = mu
    dev = np.where(
        y_true > 0,
        2 * (y_true * np.log(np.maximum(y_true, eps) / y_pred) - (y_true - y_pred)),
        2 * y_pred
    )
    return float(np.sum(weights * dev) / np.sum(weights))

def gamma_deviance(y_true: np.ndarray, y_pred: np.ndarray, weights: np.ndarray = None) -> float:
    """Calculates weighted mean Gamma deviance for severity models."""
    eps = 1e-9
    y_pred = np.maximum(y_pred, eps)
    y_true = np.maximum(y_true, eps)
    if weights is None:
        weights = np.ones_like(y_true)
        
    dev = 2 * (-np.log(y_true / y_pred) + (y_true - y_pred) / y_pred)
    return float(np.sum(weights * dev) / np.sum(weights))

def calculate_gini(y_true_loss: np.ndarray, y_pred_loss: np.ndarray, exposures: np.ndarray) -> float:
    """
    Computes the Normalized Actuarial Gini Coefficient.
    Sorts policies by predicted risk relativities and computes the area between
    the Lorenz curve and the 45-degree diagonal.
    """
    df = pd.DataFrame({
        'actual': y_true_loss,
        'pred': y_pred_loss,
        'exposure': exposures
    })
    
    # Sort by predicted pure premium ascending
    df = df.sort_values(by='pred', ascending=True).reset_index(drop=True)
    
    cum_exposure = np.cumsum(df['exposure']) / np.sum(df['exposure'])
    cum_loss = np.cumsum(df['actual']) / np.sum(df['actual'])
    
    # Area under the model Lorenz curve (trapezoidal rule)
    trapz_fn = getattr(np, 'trapezoid', getattr(np, 'trapz', None))
    auc_model = trapz_fn(cum_loss, cum_exposure)
    gini = 1 - 2 * auc_model
    return float(round(gini, 4))

def compute_double_lift_chart(
    y_true: np.ndarray, 
    y_pred: np.ndarray, 
    exposure: np.ndarray, 
    n_buckets: int = 10
) -> pd.DataFrame:
    """
    Produces a 10-decile lift chart comparing Actual Pure Premium
    against Predicted Pure Premium across risk deciles.
    """
    df = pd.DataFrame({
        'actual_loss': y_true,
        'pred_loss': y_pred,
        'exposure': exposure
    })
    
    df['pred_rate'] = df['pred_loss'] / df['exposure']
    df['decile'] = pd.qcut(df['pred_rate'].rank(method='first'), q=n_buckets, labels=range(1, n_buckets + 1))
    
    lift_summary = df.groupby('decile', observed=False).agg(
        total_exposure=('exposure', 'sum'),
        total_actual_loss=('actual_loss', 'sum'),
        total_pred_loss=('pred_loss', 'sum')
    ).reset_index()
    
    lift_summary['actual_pure_premium'] = lift_summary['total_actual_loss'] / lift_summary['total_exposure']
    lift_summary['pred_pure_premium'] = lift_summary['total_pred_loss'] / lift_summary['total_exposure']
    lift_summary['ae_ratio'] = lift_summary['actual_pure_premium'] / lift_summary['pred_pure_premium']
    
    return lift_summary.round(3)
