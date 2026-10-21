"""
End-to-End Orchestrator:
Runs Medallion Lakehouse ETL in SQLite, trains all models,
evaluates on held-out test data, and exports metrics.
"""

import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from src.data.generator import generate_insurance_portfolio
from src.data.db import init_db, load_bronze_data, build_silver_layer, build_gold_actuarial_marts, run_query
from src.models.frequency import FrequencyModel
from src.models.severity import SeverityModel
from src.models.tweedie import TweedieModel
from src.models.fraud import FraudModel
from src.evaluation.actuarial_metrics import (
    poisson_deviance, gamma_deviance, calculate_gini, compute_double_lift_chart
)

def run_full_pipeline():
    print("=== STEP 1: INITIALIZING SQLITE DATABASE ===")
    os.makedirs("models_saved", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    init_db()
    
    print("=== STEP 2: GENERATING SYNTHETIC PORTFOLIO DATA ===")
    policies_raw, claims_raw = generate_insurance_portfolio(n_policies=50000, seed=42)
    load_bronze_data(policies_raw, claims_raw)
    
    print("=== STEP 3: RUNNING MEDALLION ETL (SILVER & GOLD) IN SQLITE ===")
    build_silver_layer()
    build_gold_actuarial_marts()
    
    print("=== STEP 4: PREPARING DATA SPLITS FOR MODELING ===")
    silver_df = run_query("SELECT * FROM silver_policies;")
    
    # Train / Val / Test (70% / 15% / 15%)
    train_df, test_df = train_test_split(silver_df, test_size=0.15, random_state=42)
    train_df, val_df = train_test_split(train_df, test_size=0.1765, random_state=42) # ~15% of total
    
    print(f"Train size: {len(train_df)} | Val size: {len(val_df)} | Test size: {len(test_df)}")
    
    print("=== STEP 5: TRAINING ACTUARIAL FREQUENCY MODELS ===")
    freq_model = FrequencyModel()
    freq_model.train_glm(train_df)
    freq_model.train_booster(train_df, val_df)
    freq_model.save()
    
    # Evaluate Frequency on Test
    test_actual_freq = test_df['claim_count'].values
    pred_freq_glm = freq_model.predict(test_df, model_type='glm')
    pred_freq_bst = freq_model.predict(test_df, model_type='booster')
    
    dev_freq_glm = poisson_deviance(test_actual_freq, pred_freq_glm, weights=test_df['exposure'].values)
    dev_freq_bst = poisson_deviance(test_actual_freq, pred_freq_bst, weights=test_df['exposure'].values)
    print(f"Frequency Test Poisson Deviance -> GLM: {dev_freq_glm:.4f} | Booster: {dev_freq_bst:.4f}")
    
    print("=== STEP 6: TRAINING ACTUARIAL SEVERITY MODELS ===")
    sev_model = SeverityModel()
    sev_model.train_glm(train_df)
    sev_model.train_booster(train_df, val_df)
    sev_model.save()
    
    # Evaluate Severity on Test (positive claims only)
    test_pos = test_df[test_df['claim_count'] > 0].copy()
    test_actual_sev = (test_pos['total_claim_amount'] / test_pos['claim_count']).values
    pred_sev_glm = sev_model.predict(test_pos, model_type='glm')
    pred_sev_bst = sev_model.predict(test_pos, model_type='booster')
    
    dev_sev_glm = gamma_deviance(test_actual_sev, pred_sev_glm, weights=test_pos['claim_count'].values)
    dev_sev_bst = gamma_deviance(test_actual_sev, pred_sev_bst, weights=test_pos['claim_count'].values)
    print(f"Severity Test Gamma Deviance -> GLM: {dev_sev_glm:.4f} | Booster: {dev_sev_bst:.4f}")
    
    print("=== STEP 7: TRAINING TWEEDIE COMPOUND PURE PREMIUM MODEL ===")
    tweedie_model = TweedieModel(tweedie_variance_power=1.5)
    tweedie_model.train(train_df, val_df)
    tweedie_model.save()
    
    # Pure premium predictions on full test set
    pred_rate_tweedie = tweedie_model.predict(test_df) # annual rate
    pred_pure_premium_tweedie = pred_rate_tweedie * test_df['exposure'].values
    
    # Two-part Frequency x Severity Pure Premium
    pred_freq_full = freq_model.predict(test_df, model_type='booster')
    pred_sev_full = sev_model.predict(test_df, model_type='booster')
    pred_pure_premium_2part = pred_freq_full * pred_sev_full
    
    actual_test_losses = test_df['total_claim_amount'].values
    gini_tweedie = calculate_gini(actual_test_losses, pred_pure_premium_tweedie, test_df['exposure'].values)
    gini_2part = calculate_gini(actual_test_losses, pred_pure_premium_2part, test_df['exposure'].values)
    print(f"Test Gini Coefficient -> Tweedie: {gini_tweedie:.4f} | Two-Part (Freq x Sev): {gini_2part:.4f}")
    
    print("=== STEP 8: DOUBLE LIFT CHARTS (DECILE RISK DISCRIMINATION) ===")
    lift_df = compute_double_lift_chart(
        y_true=actual_test_losses,
        y_pred=pred_pure_premium_tweedie,
        exposure=test_df['exposure'].values,
        n_buckets=10
    )
    print(lift_df.to_string(index=False))
    lift_df.to_csv("reports/double_lift_chart.csv", index=False)
    
    print("=== STEP 9: TRAINING CLAIMS FRAUD & TRIAGE CLASSIFIER ===")
    claims_sql = """
    SELECT 
        c.claim_id, c.policy_id, c.claim_type, c.days_to_report, 
        c.paid_amount, c.is_fraud, c.is_settled,
        p.driver_age, p.vehicle_age, p.vehicle_value, p.bonus_malus, 
        p.policy_tenure, p.deductible, p.territory
    FROM bronze_claims c
    JOIN bronze_policies p ON c.policy_id = p.policy_id;
    """
    claims_joined = run_query(claims_sql)
    fraud_model = FraudModel()
    fraud_metrics = fraud_model.train(claims_joined)
    fraud_model.save()
    print(f"Fraud Classifier Metrics: PR-AUC={fraud_metrics['pr_auc']}, ROC-AUC={fraud_metrics['roc_auc']}")
    
    summary = {
        'portfolio_size': 50000,
        'claims_count': len(claims_joined),
        'metrics': {
            'frequency_deviance_glm': round(dev_freq_glm, 4),
            'frequency_deviance_booster': round(dev_freq_bst, 4),
            'severity_deviance_glm': round(dev_sev_glm, 4),
            'severity_deviance_booster': round(dev_sev_bst, 4),
            'gini_tweedie': gini_tweedie,
            'gini_two_part': gini_2part,
            'fraud_pr_auc': fraud_metrics['pr_auc'],
            'fraud_roc_auc': fraud_metrics['roc_auc']
        }
    }
    with open("reports/model_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print("=== PIPELINE AND MODEL TRAINING SUCCESSFULLY COMPLETED! ===")

if __name__ == "__main__":
    run_full_pipeline()
