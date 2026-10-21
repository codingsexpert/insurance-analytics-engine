"""
SQLite Database Engine & Medallion Pipeline for General Insurance.
Stores Bronze (raw), Silver (cleaned & aggregated), and Gold (actuarial marts)
in local SQLite: insurance.db
"""

import sqlite3
import pandas as pd
import numpy as np
import os
from typing import Optional, List, Dict, Any

DB_PATH = "insurance.db"

def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path: str = DB_PATH):
    """Initializes tables and indexes in SQLite."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    # 1. Bronze (Raw Tables)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bronze_policies (
        policy_id TEXT PRIMARY KEY,
        driver_age INTEGER,
        driving_experience INTEGER,
        vehicle_type TEXT,
        vehicle_age INTEGER,
        vehicle_value REAL,
        annual_mileage INTEGER,
        territory TEXT,
        bonus_malus INTEGER,
        policy_tenure INTEGER,
        deductible REAL,
        exposure REAL,
        claim_count INTEGER
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bronze_claims (
        claim_id TEXT PRIMARY KEY,
        policy_id TEXT,
        claim_type TEXT,
        days_to_report INTEGER,
        paid_amount REAL,
        is_fraud INTEGER,
        is_settled INTEGER,
        FOREIGN KEY (policy_id) REFERENCES bronze_policies(policy_id)
    );
    """)
    
    # Indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_claims_policy ON bronze_claims(policy_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_policies_territory ON bronze_policies(territory);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_policies_vehicle_type ON bronze_policies(vehicle_type);")
    
    conn.commit()
    conn.close()

def load_bronze_data(policies_df: pd.DataFrame, claims_df: pd.DataFrame, db_path: str = DB_PATH):
    """Loads raw simulated policies and claims into Bronze SQLite tables."""
    conn = get_connection(db_path)
    policies_df.to_sql('bronze_policies', conn, if_exists='replace', index=False)
    claims_df.to_sql('bronze_claims', conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()
    print("Bronze tables loaded successfully into SQLite.")

def build_silver_layer(db_path: str = DB_PATH):
    """
    Transforms Bronze -> Silver.
    Cleans data, validates exposures, and creates an enriched policy-level
    analytical view joining aggregated claim losses and fraud signals.
    """
    conn = get_connection(db_path)
    
    # Execute SQL transformation
    silver_query = """
    CREATE TABLE IF NOT EXISTS silver_policies AS
    SELECT 
        p.policy_id,
        p.driver_age,
        CASE 
            WHEN p.driver_age < 25 THEN '18-24'
            WHEN p.driver_age BETWEEN 25 AND 35 THEN '25-35'
            WHEN p.driver_age BETWEEN 36 AND 55 THEN '36-55'
            WHEN p.driver_age BETWEEN 56 AND 70 THEN '56-70'
            ELSE '71+'
        END AS driver_age_band,
        p.driving_experience,
        p.vehicle_type,
        p.vehicle_age,
        p.vehicle_value,
        p.annual_mileage,
        p.territory,
        p.bonus_malus,
        p.policy_tenure,
        p.deductible,
        p.exposure,
        p.claim_count,
        COALESCE(c.total_claim_amount, 0.0) AS total_claim_amount,
        COALESCE(c.max_claim_amount, 0.0) AS max_claim_amount,
        COALESCE(c.fraud_claim_count, 0) AS fraud_claim_count,
        CASE 
            WHEN p.exposure > 0 THEN COALESCE(c.total_claim_amount, 0.0) / p.exposure 
            ELSE 0.0 
        END AS loss_cost
    FROM bronze_policies p
    LEFT JOIN (
        SELECT 
            policy_id,
            SUM(paid_amount) AS total_claim_amount,
            MAX(paid_amount) AS max_claim_amount,
            SUM(is_fraud) AS fraud_claim_count
        FROM bronze_claims
        GROUP BY policy_id
    ) c ON p.policy_id = c.policy_id;
    """
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS silver_policies;")
    cursor.execute(silver_query)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_silver_pol_id ON silver_policies(policy_id);")
    
    conn.commit()
    conn.close()
    print("Silver layer constructed successfully in SQLite.")

def build_gold_actuarial_marts(db_path: str = DB_PATH):
    """
    Transforms Silver -> Gold.
    Creates Actuarial Rating Cell Mart aggregating exposure, claims,
    empirical frequency, mean severity, and empirical pure premium.
    """
    conn = get_connection(db_path)
    
    gold_query = """
    CREATE TABLE IF NOT EXISTS gold_rating_cells AS
    SELECT 
        territory,
        driver_age_band,
        vehicle_type,
        COUNT(policy_id) AS policy_count,
        ROUND(SUM(exposure), 2) AS total_exposure,
        SUM(claim_count) AS total_claims,
        ROUND(SUM(total_claim_amount), 2) AS total_incurred_loss,
        ROUND(CAST(SUM(claim_count) AS REAL) / NULLIF(SUM(exposure), 0), 4) AS empirical_frequency,
        ROUND(CAST(SUM(total_claim_amount) AS REAL) / NULLIF(SUM(claim_count), 0), 2) AS empirical_severity,
        ROUND(CAST(SUM(total_claim_amount) AS REAL) / NULLIF(SUM(exposure), 0), 2) AS empirical_pure_premium
    FROM silver_policies
    GROUP BY territory, driver_age_band, vehicle_type;
    """
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS gold_rating_cells;")
    cursor.execute(gold_query)
    
    conn.commit()
    conn.close()
    print("Gold Actuarial Marts constructed successfully in SQLite.")

def run_query(query: str, db_path: str = DB_PATH) -> pd.DataFrame:
    """Executes any read SQL query against SQLite and returns a DataFrame."""
    conn = get_connection(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
