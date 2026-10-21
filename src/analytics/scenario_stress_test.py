"""
Actuarial Stress Testing & Catastrophe Scenario Simulation Engine.
Evaluates portfolio solvency and Combined Ratio under macro-economic stress:
- Claim Severity Inflation (Social & repair cost inflation: 0% to +30%)
- Frequency Surge / Catastrophe Shock (Severe weather / hail event: 0% to +50%)
- Excess of Loss (XoL) Reinsurance Treaty Modeling (Net vs. Ceded Losses)
"""

import numpy as np
import pandas as pd
import sqlite3
from typing import Dict, Any, List

from src.data.db import DB_PATH, run_query

class ActuarialStressTester:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        
    def run_stress_test(
        self,
        severity_inflation_pct: float = 0.0,
        frequency_surge_pct: float = 0.0,
        reinsurance_retention_limit: float = 25000.0,
        expense_ratio_pct: float = 22.0
    ) -> Dict[str, Any]:
        """
        Applies macroeconomic and catastrophe shocks to the portfolio
        and evaluates gross and net financial outcomes.
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        # Base numbers
        cur.execute("SELECT COUNT(*), SUM(exposure), SUM(claim_count), SUM(total_claim_amount) FROM silver_policies;")
        pol_count, tot_exp, base_claims, base_losses = cur.fetchone()
        
        # Query individual claims for XoL reinsurance simulation
        cur.execute("SELECT paid_amount FROM bronze_claims;")
        claims_rows = cur.fetchall()
        claim_amounts = np.array([r[0] for r in claims_rows])
        conn.close()
        
        # 1. Base Portfolio Performance
        # Baseline Earned Premium assuming $180/exposure unit
        base_rate_per_exposure = (base_losses / tot_exp) / 0.75 # Tariff calibrated to 75% target loss ratio
        earned_premium = tot_exp * base_rate_per_exposure
        
        base_loss_ratio = (base_losses / earned_premium) * 100.0
        base_combined_ratio = base_loss_ratio + expense_ratio_pct
        
        # 2. Apply Severity & Frequency Shocks
        sev_multiplier = 1.0 + (severity_inflation_pct / 100.0)
        freq_multiplier = 1.0 + (frequency_surge_pct / 100.0)
        
        stressed_claims_count = int(round(base_claims * freq_multiplier))
        
        # Shock individual claim amounts
        stressed_claim_amounts = claim_amounts * sev_multiplier
        # If frequency increased, resample additional claims to simulate catastrophe surge
        if freq_multiplier > 1.0 and len(stressed_claim_amounts) > 0:
            extra_n = stressed_claims_count - len(stressed_claim_amounts)
            if extra_n > 0:
                extra_samples = np.random.choice(stressed_claim_amounts, size=extra_n, replace=True)
                all_stressed_claims = np.concatenate([stressed_claim_amounts, extra_samples])
            else:
                all_stressed_claims = stressed_claim_amounts
        else:
            all_stressed_claims = stressed_claim_amounts
            
        total_stressed_gross_loss = float(np.sum(all_stressed_claims))
        
        # 3. Apply Excess of Loss (XoL) Reinsurance
        # Primary insurer pays min(claim, retention_limit)
        retained_net_claims = np.minimum(all_stressed_claims, reinsurance_retention_limit)
        total_retained_net_loss = float(np.sum(retained_net_claims))
        total_ceded_to_reinsurer = total_stressed_gross_loss - total_retained_net_loss
        
        # 4. Impacted Financial Ratios
        stressed_gross_loss_ratio = (total_stressed_gross_loss / earned_premium) * 100.0
        stressed_net_loss_ratio = (total_retained_net_loss / earned_premium) * 100.0
        
        stressed_net_combined_ratio = stressed_net_loss_ratio + expense_ratio_pct
        underwriting_profit_or_loss = earned_premium - (total_retained_net_loss + (earned_premium * (expense_ratio_pct / 100.0)))
        
        # Solvency capital assessment
        is_solvent = stressed_net_combined_ratio < 100.0
        if stressed_net_combined_ratio < 95.0:
            financial_health = "Strong Underwriting Profit"
            health_color = "green"
        elif stressed_net_combined_ratio <= 100.0:
            financial_health = "Marginal Profit / Break-even"
            health_color = "amber"
        else:
            financial_health = "Underwriting Loss (Capital Deficit)"
            health_color = "red"
            
        return {
            "scenario_inputs": {
                "severity_inflation_pct": severity_inflation_pct,
                "frequency_surge_pct": frequency_surge_pct,
                "reinsurance_retention_limit": reinsurance_retention_limit,
                "expense_ratio_pct": expense_ratio_pct
            },
            "baseline": {
                "earned_premium": round(earned_premium, 2),
                "incurred_loss": round(base_losses, 2),
                "loss_ratio_pct": round(base_loss_ratio, 2),
                "combined_ratio_pct": round(base_combined_ratio, 2)
            },
            "stressed_outcome": {
                "total_stressed_gross_loss": round(total_stressed_gross_loss, 2),
                "total_ceded_to_reinsurer": round(total_ceded_to_reinsurer, 2),
                "total_retained_net_loss": round(total_retained_net_loss, 2),
                "gross_loss_ratio_pct": round(stressed_gross_loss_ratio, 2),
                "net_loss_ratio_pct": round(stressed_net_loss_ratio, 2),
                "net_combined_ratio_pct": round(stressed_net_combined_ratio, 2),
                "net_underwriting_margin": round(underwriting_profit_or_loss, 2),
                "financial_health": financial_health,
                "health_color": health_color,
                "is_solvent": is_solvent
            }
        }

if __name__ == "__main__":
    tester = ActuarialStressTester()
    res = tester.run_stress_test(severity_inflation_pct=15.0, frequency_surge_pct=20.0, reinsurance_retention_limit=20000.0)
    print("STRESS TEST RESULTS:")
    print(res["stressed_outcome"])
