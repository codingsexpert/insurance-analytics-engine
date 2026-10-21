"""
Customer Renewal & Dynamic Price Elasticity Modeling.
Evaluates portfolio retention, churn sensitivity to premium increases,
and simulates optimal renewal price elasticity curves.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List
from sklearn.linear_model import LogisticRegression
import joblib
import os

from src.data.db import DB_PATH, run_query

class PriceElasticitySimulator:
    def __init__(self):
        # Logistic elasticity parameters calibrated to industry general insurance renewals
        self.beta_0 = 1.95             # Baseline ~87.5% renewal with 0% price change
        self.beta_price = 4.20         # Price sensitivity: 10% price hike reduces renewal log-odds by 0.42
        self.beta_tenure = 0.12        # Loyal customers have higher retention
        self.beta_ncb = 0.08           # High NCB customers are more sticky
        self.beta_prior_claim = -0.35  # Customers with claims may shop around if premium jumps

    def predict_renewal_probability(
        self,
        price_change_pct: float,
        tenure: int,
        ncb: int,
        had_claim: int
    ) -> float:
        """Computes individual probability of policy renewal under a given price change."""
        z = (
            self.beta_0 
            - self.beta_price * (price_change_pct / 100.0)
            + self.beta_tenure * min(tenure, 8)
            + self.beta_ncb * ncb
            + self.beta_prior_claim * had_claim
        )
        return float(1.0 / (1.0 + np.exp(-z)))

    def simulate_portfolio_renewal(
        self,
        policies_df: pd.DataFrame,
        price_change_pct_range: List[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Simulates renewal conversion rate, expected gross written premium,
        expected claim losses, and combined loss ratio across different price change scenarios.
        """
        if price_change_pct_range is None:
            price_change_pct_range = [-15.0, -10.0, -5.0, 0.0, 5.0, 10.0, 15.0, 20.0, 25.0]

        # Base commercial premium per policy
        # Assume base premium = loss_cost / 0.75 or minimum $200
        base_prem = np.maximum(policies_df['loss_cost'] / 0.75, 180.0)
        tenure = policies_df['policy_tenure'].values
        ncb = policies_df['bonus_malus'].values
        had_claim = (policies_df['claim_count'] > 0).astype(int).values
        expected_claims_cost = policies_df['total_claim_amount'].values

        results = []
        for delta_p in price_change_pct_range:
            multiplier = 1.0 + (delta_p / 100.0)
            offered_premium = base_prem * multiplier

            # Renewal probability vector
            z = (
                self.beta_0
                - self.beta_price * (delta_p / 100.0)
                + self.beta_tenure * np.minimum(tenure, 8)
                + self.beta_ncb * ncb
                + self.beta_prior_claim * had_claim
            )
            renewal_probs = 1.0 / (1.0 + np.exp(-z))

            expected_renewed_policies = float(np.sum(renewal_probs))
            conversion_rate = (expected_renewed_policies / len(policies_df)) * 100.0

            # Expected Gross Written Premium (GWP) from renewed cohort
            expected_gwp = float(np.sum(renewal_probs * offered_premium))

            # Expected losses incurred by renewing cohort
            expected_losses = float(np.sum(renewal_probs * expected_claims_cost))

            # Loss Ratio (%)
            loss_ratio = (expected_losses / expected_gwp * 100.0) if expected_gwp > 0 else 0.0

            results.append({
                'price_change_pct': round(delta_p, 1),
                'offered_rate_multiplier': round(multiplier, 3),
                'conversion_rate_pct': round(conversion_rate, 2),
                'expected_renewed_count': int(expected_renewed_policies),
                'projected_gwp_revenue': round(expected_gwp, 2),
                'projected_incurred_loss': round(expected_losses, 2),
                'projected_loss_ratio_pct': round(loss_ratio, 2)
            })

        return results

if __name__ == "__main__":
    df_sample = run_query("SELECT * FROM silver_policies LIMIT 10000;")
    sim = PriceElasticitySimulator()
    res = sim.simulate_portfolio_renewal(df_sample)
    df_res = pd.DataFrame(res)
    print("\n--- PRICE ELASTICITY & RENEWAL SIMULATION ---")
    print(df_res.to_string(index=False))
