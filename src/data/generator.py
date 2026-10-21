"""
General Insurance Synthetic Actuarial Data Generator.
Generates realistic Motor/P&C insurance portfolio data conforming to
actuarial distributions (Poisson frequency with exposure offset and Gamma severity).
"""

import numpy as np
import pandas as pd
from typing import Tuple, Dict
import os

def generate_insurance_portfolio(
    n_policies: int = 50000,
    seed: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generates two conformed relational tables:
    1. policies_df: Policy-level exposures, driver risk factors, and coverage details.
    2. claims_df: Granular claim-level records linked by policy_id.
    """
    np.random.seed(seed)
    
    # 1. Driver and Policy Demographics
    policy_ids = [f"POL-{i+100000:06d}" for i in range(n_policies)]
    
    # Driver Age: Bimodal mix of young drivers and mature drivers
    driver_age = np.clip(
        np.concatenate([
            np.random.normal(loc=23, scale=3, size=int(n_policies * 0.18)),
            np.random.normal(loc=44, scale=12, size=int(n_policies * 0.82))
        ]),
        18, 82
    ).astype(int)
    np.random.shuffle(driver_age)
    
    # Driver Experience (correlated with age)
    driving_experience = np.clip(driver_age - 18 - np.random.poisson(lam=1.5, size=n_policies), 0, 60)
    
    # Vehicle characteristics
    vehicle_types = ['Hatchback', 'Sedan', 'SUV', 'Luxury', 'Sports']
    vehicle_probs = [0.35, 0.30, 0.22, 0.08, 0.05]
    vehicle_type = np.random.choice(vehicle_types, size=n_policies, p=vehicle_probs)
    
    vehicle_age = np.clip(np.random.exponential(scale=4.5, size=n_policies), 0, 20).astype(int)
    
    # Base vehicle value depending on type
    base_values = {'Hatchback': 14000, 'Sedan': 24000, 'SUV': 35000, 'Luxury': 65000, 'Sports': 55000}
    depreciation = (1 - 0.08) ** vehicle_age
    vehicle_value = np.array([base_values[v] for v in vehicle_type]) * depreciation * np.random.uniform(0.85, 1.25, size=n_policies)
    vehicle_value = np.round(vehicle_value, 2)
    
    # Annual mileage (km)
    annual_mileage = np.clip(np.random.lognormal(mean=9.4, sigma=0.45, size=n_policies), 3000, 50000).astype(int)
    
    # Geographical rating territory
    territories = ['Urban_HighRisk', 'Urban_Standard', 'Suburban', 'Rural']
    territory_probs = [0.25, 0.35, 0.25, 0.15]
    territory = np.random.choice(territories, size=n_policies, p=territory_probs)
    
    # Bonus-Malus / No-Claim-Bonus level (0: 0% discount to 5: 50% discount)
    bonus_malus = np.random.choice([0, 1, 2, 3, 4, 5], size=n_policies, p=[0.20, 0.15, 0.15, 0.20, 0.15, 0.15])
    
    # Policy tenure (years with this insurer)
    policy_tenure = np.clip(np.random.geometric(p=0.35, size=n_policies) - 1, 0, 12)
    
    # Policy Exposure (fraction of year in force, e.g. 0.05 to 1.0)
    # Most policies are full-year (1.0), others mid-term inception or cancellations
    full_year_mask = np.random.binomial(n=1, p=0.75, size=n_policies)
    partial_exposure = np.random.uniform(0.08, 0.98, size=n_policies)
    exposure = np.where(full_year_mask == 1, 1.0, partial_exposure).round(3)
    
    # Deductible option ($)
    deductible = np.random.choice([250, 500, 1000, 2000], size=n_policies, p=[0.25, 0.45, 0.20, 0.10])
    
    # 2. Actuarial Claim Frequency Process (Poisson / Negative Binomial)
    # Young drivers, sports cars, high mileage, urban zones increase baseline frequency
    beta_0 = -2.35 # Baseline annual frequency around ~9.5%
    
    # Non-linear age penalty (U-shaped: young high, seniors slight increase)
    age_effect = np.where(driver_age < 25, (25 - driver_age) * 0.065, 0.0) + \
                 np.where(driver_age > 68, (driver_age - 68) * 0.025, 0.0)
                 
    type_effect = np.array([{'Hatchback': 0.0, 'Sedan': 0.05, 'SUV': 0.12, 'Luxury': 0.18, 'Sports': 0.38}[v] for v in vehicle_type])
    geo_effect = np.array([{'Rural': -0.25, 'Suburban': -0.05, 'Urban_Standard': 0.10, 'Urban_HighRisk': 0.32}[t] for t in territory])
    mileage_effect = np.log(annual_mileage / 12000) * 0.30
    ncb_effect = -0.14 * bonus_malus
    veh_age_effect = -0.02 * np.minimum(vehicle_age, 10)
    
    # Log-lambda linear predictor
    log_lambda = beta_0 + age_effect + type_effect + geo_effect + mileage_effect + ncb_effect + veh_age_effect
    
    # Expected claim count given exposure: lambda_i = exposure_i * exp(log_lambda)
    expected_claims = exposure * np.exp(log_lambda)
    
    # Generate actual observed claim counts: Poisson distribution
    claim_count = np.random.poisson(lam=expected_claims)
    
    # Assemble Policy Table
    policies_df = pd.DataFrame({
        'policy_id': policy_ids,
        'driver_age': driver_age,
        'driving_experience': driving_experience,
        'vehicle_type': vehicle_type,
        'vehicle_age': vehicle_age,
        'vehicle_value': vehicle_value,
        'annual_mileage': annual_mileage,
        'territory': territory,
        'bonus_malus': bonus_malus,
        'policy_tenure': policy_tenure,
        'deductible': deductible,
        'exposure': exposure,
        'claim_count': claim_count
    })
    
    # 3. Actuarial Claim Severity Process (Gamma distribution)
    # Generate individual claims
    claims_list = []
    claim_counter = 1000000
    
    for idx, row in policies_df[policies_df['claim_count'] > 0].iterrows():
        p_id = row['policy_id']
        n_c = int(row['claim_count'])
        v_val = row['vehicle_value']
        v_type = row['vehicle_type']
        
        # Mean severity increases with vehicle value, luxury/sports, and decreases with deductible
        sev_alpha_0 = 7.6 # ~ $2,000 baseline
        val_factor = 0.28 * np.log(max(v_val, 3000) / 20000)
        type_sev_factor = {'Hatchback': -0.15, 'Sedan': 0.0, 'SUV': 0.15, 'Sports': 0.35, 'Luxury': 0.50}[v_type]
        
        mean_sev = np.exp(sev_alpha_0 + val_factor + type_sev_factor)
        gamma_shape = 2.2 # Actuarial standard shape parameter for P&C auto
        gamma_scale = mean_sev / gamma_shape
        
        for c_idx in range(n_c):
            claim_id = f"CLM-{claim_counter}"
            claim_counter += 1
            
            # Simulated raw loss amount before deductible
            raw_loss = np.random.gamma(shape=gamma_shape, scale=gamma_scale)
            
            # Apply deductible
            paid_amount = max(0.0, raw_loss - row['deductible'])
            if paid_amount == 0.0:
                paid_amount = round(np.random.uniform(50, 200), 2) # Minor reporting/admin costs
            else:
                paid_amount = round(paid_amount, 2)
                
            # Claims metadata
            claim_types = ['Collision', 'Comprehensive', 'Theft', 'Third_Party']
            c_type = np.random.choice(claim_types, p=[0.55, 0.22, 0.08, 0.15])
            
            days_to_report = int(np.clip(np.random.exponential(scale=5.0), 0, 90))
            
            # Fraud indicators (staged collision, late reporting, new policy inception)
            fraud_latent = (
                0.03 +
                (0.06 if days_to_report > 30 else 0) +
                (0.05 if row['policy_tenure'] == 0 else 0) +
                (0.08 if paid_amount > 20000 else 0) +
                (0.04 if row['bonus_malus'] == 0 else 0)
            )
            is_fraud = int(np.random.binomial(n=1, p=min(fraud_latent, 0.45)))
            
            # Settlement status
            is_settled = 1 if days_to_report < 60 else np.random.binomial(n=1, p=0.85)
            
            claims_list.append({
                'claim_id': claim_id,
                'policy_id': p_id,
                'claim_type': c_type,
                'days_to_report': days_to_report,
                'paid_amount': paid_amount,
                'is_fraud': is_fraud,
                'is_settled': is_settled
            })
            
    claims_df = pd.DataFrame(claims_list)
    
    return policies_df, claims_df

if __name__ == "__main__":
    raw_dir = "data/raw"
    os.makedirs(raw_dir, exist_ok=True)
    print("Generating actuarial portfolio...")
    pol_df, clm_df = generate_insurance_portfolio(n_policies=50000, seed=42)
    
    pol_path = os.path.join(raw_dir, "policies_raw.csv")
    clm_path = os.path.join(raw_dir, "claims_raw.csv")
    pol_df.to_csv(pol_path, index=False)
    clm_df.to_csv(clm_path, index=False)
    
    print(f"Generated {len(pol_df)} policies -> {pol_path}")
    print(f"Generated {len(clm_df)} claims -> {clm_path}")
    print(f"Overall frequency: {pol_df['claim_count'].sum() / pol_df['exposure'].sum():.4f} claims per exposure year")
    print(f"Average claim severity: ${clm_df['paid_amount'].mean():.2f}")
