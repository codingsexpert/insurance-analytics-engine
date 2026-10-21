"""
Batch Portfolio Rating & Risk Tiering Engine.
Scores large books of business in bulk, computing Pure Premium,
Risk Tiers, and Loss Cost distributions.
"""

import numpy as np
import pandas as pd
import sqlite3
import joblib
import os
from typing import Dict, Any, List

from src.data.db import DB_PATH, run_query

def run_batch_portfolio_scoring(sample_size: int = 5000, db_path: str = DB_PATH) -> Dict[str, Any]:
    """
    Pulls a sample of unrated/in-force policies from SQLite,
    runs the serialized Tweedie and Frequency/Severity pipeline,
    and returns aggregated portfolio risk tier distributions and metrics.
    """
    models_dir = "models_saved"
    tweedie_pipe = joblib.load(os.path.join(models_dir, "tweedie_pipeline.joblib"))
    fb = joblib.load(os.path.join(models_dir, "freq_booster.joblib"))
    sb = joblib.load(os.path.join(models_dir, "sev_booster.joblib"))
    
    # Query policies
    sql = f"""
    SELECT 
        policy_id, driver_age, driving_experience, vehicle_type, vehicle_age,
        vehicle_value, annual_mileage, territory, bonus_malus, policy_tenure,
        deductible, exposure, claim_count, total_claim_amount
    FROM silver_policies
    LIMIT {sample_size};
    """
    df = run_query(sql, db_path=db_path)
    
    # 1. Pure Premium Scoring
    pred_annual_rate = tweedie_pipe.predict(df)
    df['pred_pure_premium'] = np.round(pred_annual_rate * df['exposure'].values, 2)
    df['commercial_gross_premium'] = np.round(df['pred_pure_premium'] / 0.75, 2)
    
    # 2. Assign Risk Tiers
    conditions = [
        pred_annual_rate < 150,
        pred_annual_rate < 300,
        pred_annual_rate < 550,
        pred_annual_rate < 900
    ]
    choices = [
        "Tier A (Preferred)",
        "Tier B (Standard Plus)",
        "Tier C (Standard)",
        "Tier D (Non-Standard)"
    ]
    df['risk_tier'] = np.select(conditions, choices, default="Tier E (High Risk)")
    
    # 3. Aggregate Risk Tier Distribution
    tier_summary = df.groupby('risk_tier', observed=False).agg(
        policy_count=('policy_id', 'count'),
        total_exposure=('exposure', 'sum'),
        total_pure_premium=('pred_pure_premium', 'sum'),
        avg_pure_premium=('pred_pure_premium', 'mean'),
        total_gross_premium=('commercial_gross_premium', 'sum')
    ).reset_index()
    
    tier_summary['portfolio_share_pct'] = np.round((tier_summary['policy_count'] / len(df)) * 100.0, 1)
    tier_summary['avg_pure_premium'] = np.round(tier_summary['avg_pure_premium'], 2)
    tier_summary['total_pure_premium'] = np.round(tier_summary['total_pure_premium'], 2)
    tier_summary['total_gross_premium'] = np.round(tier_summary['total_gross_premium'], 2)
    
    # Top 5 highest risk policies
    top_risk_policies = df.sort_values(by='pred_pure_premium', ascending=False).head(10)[
        ['policy_id', 'driver_age', 'vehicle_type', 'vehicle_value', 'territory', 'risk_tier', 'pred_pure_premium', 'commercial_gross_premium']
    ].to_dict(orient='records')
    
    # Save scored policies to SQLite
    conn = sqlite3.connect(db_path)
    df[['policy_id', 'risk_tier', 'pred_pure_premium', 'commercial_gross_premium']].to_sql(
        'gold_batch_scored_policies', conn, if_exists='replace', index=False
    )
    conn.commit()
    conn.close()
    
    return {
        "batch_size": len(df),
        "total_portfolio_gwp": round(float(df['commercial_gross_premium'].sum()), 2),
        "total_pure_premium": round(float(df['pred_pure_premium'].sum()), 2),
        "avg_policy_pure_premium": round(float(df['pred_pure_premium'].mean()), 2),
        "tier_distribution": tier_summary.to_dict(orient='records'),
        "top_risk_samples": top_risk_policies
    }

if __name__ == "__main__":
    res = run_batch_portfolio_scoring(1000)
    print("BATCH SCORING COMPLETED:")
    print(f"Total Batch GWP: ${res['total_portfolio_gwp']:,.2f}")
    print(pd.DataFrame(res['tier_distribution']).to_string(index=False))
