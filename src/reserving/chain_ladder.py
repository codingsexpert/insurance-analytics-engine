"""
Actuarial Reserving Engine: Chain Ladder & IBNR Loss Development Triangles.
Computes Age-to-Age link ratios (LDF), Cumulative Development Factors (CDF),
Ultimate Losses, and Incurred But Not Reported (IBNR) reserves for P&C general insurance.
"""

import numpy as np
import pandas as pd
import sqlite3
from typing import Dict, Any, Tuple
import json
import os

from src.data.db import DB_PATH, get_connection

def generate_loss_triangles(db_path: str = DB_PATH) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Simulates and computes cumulative paid loss development triangles
    across 5 accident years (AY 2021-2025) and development periods (0 to 4).
    """
    accident_years = [2021, 2022, 2023, 2024, 2025]
    n_years = len(accident_years)
    
    # Base expected ultimate annual losses per accident year (growing portfolio)
    base_ultimates = {
        2021: 1850000.0,
        2022: 2120000.0,
        2023: 2450000.0,
        2024: 2800000.0,
        2025: 3250000.0
    }
    
    # Standard P&C empirical payment pattern (% of ultimate paid by dev year 0, 1, 2, 3, 4)
    # Typically: Dev 0 = 42%, Dev 1 = 72%, Dev 2 = 88%, Dev 3 = 96%, Dev 4 = 100%
    payment_pattern = [0.42, 0.72, 0.88, 0.96, 1.00]
    
    np.random.seed(101)
    
    triangle_records = []
    
    for i, ay in enumerate(accident_years):
        ult = base_ultimates[ay]
        for dev in range(n_years - i): # Only observe up to calendar year 2025
            expected_cum_pct = payment_pattern[dev]
            # Add stochastic claim volatility
            noise = np.random.normal(loc=0.0, scale=0.015)
            cum_pct = np.clip(expected_cum_pct + noise, 0.35, 1.00)
            cum_paid = round(ult * cum_pct, 2)
            
            triangle_records.append({
                'accident_year': ay,
                'development_year': dev,
                'calendar_year': ay + dev,
                'cumulative_paid': cum_paid
            })
            
    df_tri = pd.DataFrame(triangle_records)
    
    # Pivot into Triangle Grid
    triangle_grid = df_tri.pivot(index='accident_year', columns='development_year', values='cumulative_paid')
    
    # 2. Calculate Chain Ladder Link Ratios (Loss Development Factors: LDF)
    # LDF(d) = sum(CumPaid_{d+1}) / sum(CumPaid_{d}) across historical paired years
    link_ratios = []
    for d in range(n_years - 1):
        # find rows where both d and d+1 are observed
        valid_rows = triangle_grid.dropna(subset=[d, d + 1])
        sum_d = valid_rows[d].sum()
        sum_d1 = valid_rows[d + 1].sum()
        ldf = sum_d1 / sum_d
        link_ratios.append(ldf)
        
    # Cumulative Development Factors (CDF to Ultimate)
    cdf_factors = []
    for d in range(n_years - 1):
        cdf = np.prod(link_ratios[d:])
        cdf_factors.append(cdf)
    cdf_factors.append(1.0) # dev 4 is already ultimate
    
    # 3. Project Ultimate Losses and IBNR Reserve Estimation
    reserving_summary = []
    for i, ay in enumerate(accident_years):
        latest_dev = n_years - 1 - i
        latest_cum_paid = triangle_grid.loc[ay, latest_dev]
        cdf = cdf_factors[latest_dev]
        projected_ultimate = round(latest_cum_paid * cdf, 2)
        ibnr_reserve = round(projected_ultimate - latest_cum_paid, 2)
        
        reserving_summary.append({
            'accident_year': ay,
            'latest_development_year': latest_dev,
            'latest_cumulative_paid': latest_cum_paid,
            'cdf_to_ultimate': round(cdf, 4),
            'projected_ultimate_loss': projected_ultimate,
            'estimated_ibnr_reserve': ibnr_reserve
        })
        
    df_reserves = pd.DataFrame(reserving_summary)
    
    # Save into SQLite
    conn = get_connection(db_path)
    df_tri.to_sql('gold_loss_triangles', conn, if_exists='replace', index=False)
    df_reserves.to_sql('gold_reserves_summary', conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()
    
    # Format link ratios table
    ldf_records = []
    for d in range(n_years - 1):
        ldf_records.append({
            'development_step': f"Dev {d} -> {d+1}",
            'link_ratio_ldf': round(link_ratios[d], 4),
            'cdf_to_ultimate': round(cdf_factors[d], 4)
        })
    df_ldf = pd.DataFrame(ldf_records)
    
    print("Actuarial Reserving Loss Triangles & IBNR loaded to SQLite.")
    return df_tri, df_reserves, df_ldf

if __name__ == "__main__":
    tri, reserves, ldf = generate_loss_triangles()
    print("\n--- LINK RATIOS (LDF) ---")
    print(ldf.to_string(index=False))
    print("\n--- IBNR RESERVES SUMMARY ---")
    print(reserves.to_string(index=False))
