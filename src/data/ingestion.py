"""
Custom Dataset Ingestion Engine for General Insurance Analytics.
Supports uploading CSV, Excel (.xlsx/.xls), and JSON files for Policies and Claims.
Performs actuarial schema validation, column mapping, data imputation,
and automatically refreshes the Medallion Silver & Gold Lakehouse marts.
"""

import io
import os
import sqlite3
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, Optional
from src.data.db import DB_PATH, get_connection, build_silver_layer, build_gold_actuarial_marts

# Canonical Column Mappings
POLICY_COLUMN_ALIASES = {
    'id': 'policy_id',
    'pol_id': 'policy_id',
    'policy_no': 'policy_id',
    'policyno': 'policy_id',
    'age': 'driver_age',
    'driverage': 'driver_age',
    'exp': 'driving_experience',
    'experience': 'driving_experience',
    'veh_type': 'vehicle_type',
    'vehtype': 'vehicle_type',
    'car_type': 'vehicle_type',
    'veh_age': 'vehicle_age',
    'car_age': 'vehicle_age',
    'idv': 'vehicle_value',
    'veh_val': 'vehicle_value',
    'car_value': 'vehicle_value',
    'mileage': 'annual_mileage',
    'annual_miles': 'annual_mileage',
    'zone': 'territory',
    'city': 'territory',
    'region': 'territory',
    'ncb': 'bonus_malus',
    'ncb_tier': 'bonus_malus',
    'tenure': 'policy_tenure',
    'ded': 'deductible',
    'exp_years': 'exposure',
    'claims': 'claim_count',
    'num_claims': 'claim_count'
}

CLAIM_COLUMN_ALIASES = {
    'id': 'claim_id',
    'clm_id': 'claim_id',
    'claim_no': 'claim_id',
    'policy_no': 'policy_id',
    'pol_id': 'policy_id',
    'type': 'claim_type',
    'clm_type': 'claim_type',
    'delay': 'days_to_report',
    'days_delay': 'days_to_report',
    'amount': 'paid_amount',
    'loss': 'paid_amount',
    'claim_amount': 'paid_amount',
    'incurred': 'paid_amount',
    'fraud': 'is_fraud',
    'fraud_flag': 'is_fraud',
    'settled': 'is_settled',
    'status': 'is_settled'
}

def clean_column_name(col: str) -> str:
    """Normalizes column names to lowercase snake_case."""
    return str(col).strip().lower().replace(' ', '_').replace('-', '_')

def validate_and_prepare_policies(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Validates, maps, and imputes missing fields for policies dataset."""
    df = df.copy()
    
    # 1. Rename columns by alias
    renamed = {}
    for col in df.columns:
        norm = clean_column_name(col)
        if norm in POLICY_COLUMN_ALIASES:
            renamed[col] = POLICY_COLUMN_ALIASES[norm]
        else:
            renamed[col] = norm
    df.rename(columns=renamed, inplace=True)
    
    stats = {
        'initial_rows': len(df),
        'imputations': {}
    }
    
    # 2. Ensure policy_id
    if 'policy_id' not in df.columns or df['policy_id'].isnull().all():
        df['policy_id'] = [f"POL_UP_{i+1:05d}" for i in range(len(df))]
        stats['imputations']['policy_id'] = f"Generated {len(df)} IDs"
    else:
        df['policy_id'] = df['policy_id'].astype(str)
        # Deduplicate
        df.drop_duplicates(subset=['policy_id'], keep='last', inplace=True)
    
    # 3. Impute / map driver_age
    if 'driver_age' not in df.columns:
        df['driver_age'] = 36
        stats['imputations']['driver_age'] = 'Default 36'
    else:
        df['driver_age'] = pd.to_numeric(df['driver_age'], errors='coerce').fillna(36).clip(18, 90).astype(int)
        
    # 4. Driving experience
    if 'driving_experience' not in df.columns:
        df['driving_experience'] = (df['driver_age'] - 18).clip(0, 50)
        stats['imputations']['driving_experience'] = 'Estimated from age'
    else:
        df['driving_experience'] = pd.to_numeric(df['driving_experience'], errors='coerce').fillna(5).clip(0, 65).astype(int)
        
    # 5. Vehicle type
    valid_types = {'Hatchback', 'Sedan', 'SUV', 'Sports', 'Luxury'}
    if 'vehicle_type' not in df.columns:
        df['vehicle_type'] = 'Sedan'
        stats['imputations']['vehicle_type'] = 'Default Sedan'
    else:
        df['vehicle_type'] = df['vehicle_type'].astype(str).str.capitalize()
        df['vehicle_type'] = df['vehicle_type'].apply(lambda x: x if x in valid_types else 'Sedan')
        
    # 6. Vehicle age
    if 'vehicle_age' not in df.columns:
        df['vehicle_age'] = 3
        stats['imputations']['vehicle_age'] = 'Default 3'
    else:
        df['vehicle_age'] = pd.to_numeric(df['vehicle_age'], errors='coerce').fillna(3).clip(0, 25).astype(int)
        
    # 7. Vehicle value (IDV ₹)
    if 'vehicle_value' not in df.columns:
        df['vehicle_value'] = 650000.0
        stats['imputations']['vehicle_value'] = 'Default ₹6,50,000'
    else:
        df['vehicle_value'] = pd.to_numeric(df['vehicle_value'], errors='coerce').fillna(650000.0).clip(50000, 10000000.0)
        
    # 8. Annual mileage
    if 'annual_mileage' not in df.columns:
        df['annual_mileage'] = 12000
    else:
        df['annual_mileage'] = pd.to_numeric(df['annual_mileage'], errors='coerce').fillna(12000).clip(1000, 100000).astype(int)
        
    # 9. Territory
    valid_terr = {'Urban_HighRisk', 'Urban_Standard', 'Suburban', 'Rural'}
    if 'territory' not in df.columns:
        df['territory'] = 'Urban_Standard'
    else:
        df['territory'] = df['territory'].astype(str)
        df['territory'] = df['territory'].apply(lambda x: x if x in valid_terr else 'Urban_Standard')
        
    # 10. Bonus malus (NCB 0-5)
    if 'bonus_malus' not in df.columns:
        df['bonus_malus'] = 2
    else:
        df['bonus_malus'] = pd.to_numeric(df['bonus_malus'], errors='coerce').fillna(2).clip(0, 5).astype(int)
        
    # 11. Policy tenure
    if 'policy_tenure' not in df.columns:
        df['policy_tenure'] = 3
    else:
        df['policy_tenure'] = pd.to_numeric(df['policy_tenure'], errors='coerce').fillna(3).clip(0, 25).astype(int)
        
    # 12. Deductible
    if 'deductible' not in df.columns:
        df['deductible'] = 2500.0
    else:
        df['deductible'] = pd.to_numeric(df['deductible'], errors='coerce').fillna(2500.0).clip(0, 50000.0)
        
    # 13. Exposure
    if 'exposure' not in df.columns:
        df['exposure'] = 1.0
    else:
        df['exposure'] = pd.to_numeric(df['exposure'], errors='coerce').fillna(1.0).clip(0.01, 1.0)
        
    # 14. Claim count
    if 'claim_count' not in df.columns:
        df['claim_count'] = 0
    else:
        df['claim_count'] = pd.to_numeric(df['claim_count'], errors='coerce').fillna(0).clip(0, 10).astype(int)
        
    canonical_cols = [
        'policy_id', 'driver_age', 'driving_experience', 'vehicle_type',
        'vehicle_age', 'vehicle_value', 'annual_mileage', 'territory',
        'bonus_malus', 'policy_tenure', 'deductible', 'exposure', 'claim_count'
    ]
    df = df[canonical_cols]
    stats['valid_rows'] = len(df)
    return df, stats

def validate_and_prepare_claims(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Validates, maps, and imputes missing fields for claims dataset."""
    df = df.copy()
    
    renamed = {}
    for col in df.columns:
        norm = clean_column_name(col)
        if norm in CLAIM_COLUMN_ALIASES:
            renamed[col] = CLAIM_COLUMN_ALIASES[norm]
        else:
            renamed[col] = norm
    df.rename(columns=renamed, inplace=True)
    
    stats = {
        'initial_rows': len(df),
        'imputations': {}
    }
    
    # 1. Claim ID
    if 'claim_id' not in df.columns:
        df['claim_id'] = [f"CLM_UP_{i+1:05d}" for i in range(len(df))]
    else:
        df['claim_id'] = df['claim_id'].astype(str)
        df.drop_duplicates(subset=['claim_id'], keep='last', inplace=True)
        
    # 2. Policy ID
    if 'policy_id' not in df.columns:
        df['policy_id'] = "UNKNOWN_POLICY"
        stats['imputations']['policy_id'] = 'Unknown reference'
    else:
        df['policy_id'] = df['policy_id'].astype(str)
        
    # 3. Claim type
    valid_types = {'Collision', 'Comprehensive', 'Theft', 'Third_Party'}
    if 'claim_type' not in df.columns:
        df['claim_type'] = 'Collision'
    else:
        df['claim_type'] = df['claim_type'].astype(str).str.capitalize()
        df['claim_type'] = df['claim_type'].apply(lambda x: x if x in valid_types else 'Collision')
        
    # 4. Days to report
    if 'days_to_report' not in df.columns:
        df['days_to_report'] = 3
    else:
        df['days_to_report'] = pd.to_numeric(df['days_to_report'], errors='coerce').fillna(3).clip(0, 180).astype(int)
        
    # 5. Paid amount (₹)
    if 'paid_amount' not in df.columns:
        df['paid_amount'] = 15000.0
    else:
        df['paid_amount'] = pd.to_numeric(df['paid_amount'], errors='coerce').fillna(0.0).clip(0.0, 10000000.0)
        
    # 6. Fraud flag
    if 'is_fraud' not in df.columns:
        df['is_fraud'] = 0
    else:
        df['is_fraud'] = pd.to_numeric(df['is_fraud'], errors='coerce').fillna(0).apply(lambda x: 1 if x > 0 else 0).astype(int)
        
    # 7. Settled flag
    if 'is_settled' not in df.columns:
        df['is_settled'] = 1
    else:
        df['is_settled'] = pd.to_numeric(df['is_settled'], errors='coerce').fillna(1).apply(lambda x: 1 if x > 0 else 0).astype(int)
        
    canonical_cols = [
        'claim_id', 'policy_id', 'claim_type', 'days_to_report',
        'paid_amount', 'is_fraud', 'is_settled'
    ]
    df = df[canonical_cols]
    stats['valid_rows'] = len(df)
    return df, stats

def ingest_custom_file(
    file_bytes: bytes,
    filename: str,
    dataset_type: str = "policies",
    mode: str = "append",
    db_path: str = DB_PATH
) -> Dict[str, Any]:
    """
    Parses file (CSV / Excel / JSON), validates schema, updates Bronze table in SQLite,
    and automatically rebuilds Silver & Gold layers.
    """
    filename_lower = filename.lower()
    
    # 1. Parse File
    try:
        if filename_lower.endswith('.csv') or filename_lower.endswith('.txt'):
            raw_df = pd.read_csv(io.BytesIO(file_bytes))
        elif filename_lower.endswith('.xlsx') or filename_lower.endswith('.xls'):
            raw_df = pd.read_excel(io.BytesIO(file_bytes))
        elif filename_lower.endswith('.json'):
            raw_df = pd.read_json(io.BytesIO(file_bytes))
        else:
            # Fallback to CSV parser
            raw_df = pd.read_csv(io.BytesIO(file_bytes))
    except Exception as e:
        raise ValueError(f"Could not parse uploaded file '{filename}': {str(e)}")
        
    if len(raw_df) == 0:
        raise ValueError("Uploaded file contains zero records.")

    conn = get_connection(db_path)
    cur = conn.cursor()
    
    # 2. Process according to dataset_type
    if dataset_type == "policies":
        clean_df, stats = validate_and_prepare_policies(raw_df)
        table_name = "bronze_policies"
        
        if mode == "replace":
            clean_df.to_sql(table_name, conn, if_exists='replace', index=False)
            stats['action'] = f"Replaced {table_name} with {len(clean_df)} policies"
        else: # append
            # To prevent primary key conflicts in SQLite, delete matching IDs then insert
            p_ids = tuple(clean_df['policy_id'].tolist()[:999])
            if len(p_ids) > 0:
                placeholders = ','.join(['?'] * len(p_ids))
                cur.execute(f"DELETE FROM bronze_policies WHERE policy_id IN ({placeholders});", p_ids)
            clean_df.to_sql(table_name, conn, if_exists='append', index=False)
            stats['action'] = f"Appended {len(clean_df)} policies to {table_name}"
            
    elif dataset_type == "claims":
        clean_df, stats = validate_and_prepare_claims(raw_df)
        table_name = "bronze_claims"
        
        if mode == "replace":
            clean_df.to_sql(table_name, conn, if_exists='replace', index=False)
            stats['action'] = f"Replaced {table_name} with {len(clean_df)} claims"
        else: # append
            c_ids = tuple(clean_df['claim_id'].tolist()[:999])
            if len(c_ids) > 0:
                placeholders = ','.join(['?'] * len(c_ids))
                cur.execute(f"DELETE FROM bronze_claims WHERE claim_id IN ({placeholders});", c_ids)
            clean_df.to_sql(table_name, conn, if_exists='append', index=False)
            stats['action'] = f"Appended {len(clean_df)} claims to {table_name}"
            
            # Update claim_count in bronze_policies if applicable
            cur.execute("""
            UPDATE bronze_policies 
            SET claim_count = (
                SELECT COUNT(*) FROM bronze_claims WHERE bronze_claims.policy_id = bronze_policies.policy_id
            );
            """)
    else:
        conn.close()
        raise ValueError(f"Unknown dataset_type: {dataset_type}. Expected 'policies' or 'claims'.")
        
    conn.commit()
    conn.close()
    
    # 3. Automatically Rebuild Silver & Gold Layers
    build_silver_layer(db_path)
    build_gold_actuarial_marts(db_path)
    
    # 4. Fetch updated portfolio metrics
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*), ROUND(SUM(exposure), 2), SUM(claim_count), ROUND(SUM(total_claim_amount), 2) FROM silver_policies;")
    tot_pols, tot_exp, tot_clms, tot_losses = cur.fetchone()
    conn.close()
    
    emp_freq = round((tot_clms / tot_exp), 4) if tot_exp and tot_exp > 0 else 0.0
    emp_sev = round((tot_losses / tot_clms), 2) if tot_clms and tot_clms > 0 else 0.0
    pure_prem = round((tot_losses / tot_exp), 2) if tot_exp and tot_exp > 0 else 0.0
    
    return {
        "status": "SUCCESS",
        "dataset_type": dataset_type,
        "mode": mode,
        "filename": filename,
        "ingested_rows": len(clean_df),
        "details": stats,
        "portfolio_summary": {
            "total_policies": tot_pols,
            "total_exposure_years": tot_exp,
            "total_claims": tot_clms,
            "total_incurred_losses": tot_losses,
            "empirical_frequency": emp_freq,
            "empirical_severity": emp_sev,
            "empirical_pure_premium": pure_prem
        }
    }

def get_sample_template_csv(dataset_type: str = "policies") -> str:
    """Returns sample CSV formatted string for users to download and populate."""
    if dataset_type == "policies":
        df = pd.DataFrame([
            {
                "policy_id": "POL_CUSTOM_001",
                "driver_age": 28,
                "driving_experience": 8,
                "vehicle_type": "Sedan",
                "vehicle_age": 2,
                "vehicle_value": 750000,
                "annual_mileage": 12000,
                "territory": "Urban_Standard",
                "bonus_malus": 3,
                "policy_tenure": 2,
                "deductible": 2500,
                "exposure": 1.0,
                "claim_count": 0
            },
            {
                "policy_id": "POL_CUSTOM_002",
                "driver_age": 45,
                "driving_experience": 22,
                "vehicle_type": "SUV",
                "vehicle_age": 4,
                "vehicle_value": 1400000,
                "annual_mileage": 15000,
                "territory": "Suburban",
                "bonus_malus": 4,
                "policy_tenure": 5,
                "deductible": 5000,
                "exposure": 1.0,
                "claim_count": 1
            },
            {
                "policy_id": "POL_CUSTOM_003",
                "driver_age": 22,
                "driving_experience": 2,
                "vehicle_type": "Hatchback",
                "vehicle_age": 1,
                "vehicle_value": 450000,
                "annual_mileage": 9000,
                "territory": "Urban_HighRisk",
                "bonus_malus": 1,
                "policy_tenure": 1,
                "deductible": 1000,
                "exposure": 0.5,
                "claim_count": 0
            }
        ])
    else: # claims
        df = pd.DataFrame([
            {
                "claim_id": "CLM_CUSTOM_001",
                "policy_id": "POL_CUSTOM_002",
                "claim_type": "Collision",
                "days_to_report": 2,
                "paid_amount": 28500.0,
                "is_fraud": 0,
                "is_settled": 1
            },
            {
                "claim_id": "CLM_CUSTOM_002",
                "policy_id": "POL_CUSTOM_001",
                "claim_type": "Comprehensive",
                "days_to_report": 4,
                "paid_amount": 12000.0,
                "is_fraud": 0,
                "is_settled": 1
            }
        ])
    return df.to_csv(index=False)
