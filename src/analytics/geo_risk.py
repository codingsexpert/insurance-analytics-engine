"""
Geo-Risk Concentration & Probable Maximum Loss (PML) Analytics Engine.
Calculates Total Insured Value (TIV), territory risk exposure density,
and 1-in-100 / 1-in-250 Year Probable Maximum Loss (PML) stress metrics.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List

from src.data.db import DB_PATH, run_query

def compute_geo_concentration_analysis() -> List[Dict[str, Any]]:
    """
    Computes spatial concentration, Total Insured Value (TIV),
    and catastrophe PML estimates across rating territories.
    """
    sql = """
    SELECT 
        p.territory,
        COUNT(p.policy_id) AS policy_count,
        ROUND(SUM(p.exposure), 2) AS total_exposure,
        ROUND(SUM(p.vehicle_value), 2) AS total_insured_value,
        SUM(p.claim_count) AS total_claims,
        ROUND(SUM(p.total_claim_amount), 2) AS total_incurred_loss,
        ROUND(AVG(p.vehicle_value), 2) AS avg_vehicle_value
    FROM silver_policies p
    GROUP BY p.territory
    ORDER BY total_insured_value DESC;
    """
    df = run_query(sql)
    
    total_tiv = df['total_insured_value'].sum()
    
    results = []
    # Territory PML vulnerability factors (percentage of TIV destroyed in 1-in-100 and 1-in-250 yr disaster)
    pml_100_factors = {
        'Urban_HighRisk': 0.045,  # 4.5% of TIV
        'Urban_Standard': 0.030,  # 3.0% of TIV
        'Suburban': 0.022,        # 2.2% of TIV
        'Rural': 0.015            # 1.5% of TIV
    }
    pml_250_factors = {
        'Urban_HighRisk': 0.075,  # 7.5% of TIV
        'Urban_Standard': 0.052,  # 5.2% of TIV
        'Suburban': 0.038,        # 3.8% of TIV
        'Rural': 0.028            # 2.8% of TIV
    }
    
    for _, row in df.iterrows():
        t = row['territory']
        tiv = row['total_insured_value']
        tiv_share = (tiv / total_tiv) * 100.0 if total_tiv else 0.0
        
        freq = (row['total_claims'] / row['total_exposure']) if row['total_exposure'] else 0.0
        sev = (row['total_incurred_loss'] / row['total_claims']) if row['total_claims'] else 0.0
        pure_prem = (row['total_incurred_loss'] / row['total_exposure']) if row['total_exposure'] else 0.0
        
        pml_100 = tiv * pml_100_factors.get(t, 0.025)
        pml_250 = tiv * pml_250_factors.get(t, 0.040)
        
        results.append({
            "territory": t,
            "policy_count": int(row['policy_count']),
            "total_exposure": float(row['total_exposure']),
            "total_insured_value": float(tiv),
            "tiv_concentration_pct": round(tiv_share, 2),
            "total_claims": int(row['total_claims']),
            "total_incurred_loss": float(row['total_incurred_loss']),
            "empirical_frequency_pct": round(freq * 100, 2),
            "mean_severity": round(sev, 2),
            "pure_premium": round(pure_prem, 2),
            "pml_100_year": round(pml_100, 2),
            "pml_250_year": round(pml_250, 2)
        })
        
    return results

if __name__ == "__main__":
    res = compute_geo_concentration_analysis()
    df_res = pd.DataFrame(res)
    print("GEO RISK CONCENTRATION & PML:")
    print(df_res.to_string(index=False))
