"""
Automated Actuarial & Platform Test Suite.
Verifies database integrity, model predictions, reserving formulas,
and reinsurance stress testing logic.
"""

import unittest
import numpy as np
import pandas as pd
import sqlite3
import joblib

from src.data.db import DB_PATH, run_query
from src.analytics.scenario_stress_test import ActuarialStressTester
from src.analytics.geo_risk import compute_geo_concentration_analysis
from src.evaluation.explainability import extract_rating_relativities, compute_fair_lending_audit

class TestActuarialPlatform(unittest.TestCase):
    
    def test_sqlite_tables_exist(self):
        """Verify all Medallion layers and Gold marts exist in SQLite."""
        tables_df = run_query("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = set(tables_df['name'].tolist())
        
        expected_tables = {
            'bronze_policies', 'bronze_claims',
            'silver_policies', 'gold_rating_cells',
            'gold_loss_triangles', 'gold_reserves_summary'
        }
        for t in expected_tables:
            self.assertIn(t, table_names, f"Missing expected table: {t}")

    def test_silver_exposure_validity(self):
        """Ensure all policies have valid positive exposures <= 1.0."""
        df = run_query("SELECT MIN(exposure), MAX(exposure) FROM silver_policies;")
        min_exp, max_exp = df.iloc[0]
        self.assertGreater(min_exp, 0.0)
        self.assertLessEqual(max_exp, 1.0)

    def test_reserving_chain_ladder_consistency(self):
        """Ensure Projected Ultimate Loss is >= Latest Cumulative Paid."""
        df = run_query("SELECT projected_ultimate_loss, latest_cumulative_paid, estimated_ibnr_reserve FROM gold_reserves_summary;")
        for _, row in df.iterrows():
            self.assertGreaterEqual(row['projected_ultimate_loss'], row['latest_cumulative_paid'])
            self.assertGreaterEqual(row['estimated_ibnr_reserve'], 0.0)

    def test_rate_relativities_structure(self):
        """Ensure rate relativities contain base rate and all rating factors."""
        rel = extract_rating_relativities()
        self.assertIn("base_rate_annual_pure_premium", rel)
        self.assertIn("territory", rel["factors"])
        self.assertIn("vehicle_type", rel["factors"])
        self.assertIn("driver_age_band", rel["factors"])

    def test_stress_test_reinsurance_effect(self):
        """Ensure Reinsurance Ceded Losses reduce net incurred loss under severe shock."""
        tester = ActuarialStressTester()
        res = tester.run_stress_test(
            severity_inflation_pct=25.0,
            frequency_surge_pct=30.0,
            reinsurance_retention_limit=15000.0
        )
        outcome = res["stressed_outcome"]
        self.assertGreater(outcome["total_stressed_gross_loss"], outcome["total_retained_net_loss"])
        self.assertGreater(outcome["total_ceded_to_reinsurer"], 0.0)
        self.assertLess(outcome["net_loss_ratio_pct"], outcome["gross_loss_ratio_pct"])

    def test_geo_risk_pml(self):
        """Ensure PML 250-year is strictly greater than PML 100-year."""
        geo_results = compute_geo_concentration_analysis()
        self.assertGreater(len(geo_results), 0)
        for r in geo_results:
            self.assertGreater(r["pml_250_year"], r["pml_100_year"])
            self.assertGreater(r["total_insured_value"], 0.0)

    def test_custom_dataset_ingestion(self):
        """Ensure custom CSV ingestion successfully parses and transforms."""
        from src.data.ingestion import ingest_custom_file, get_sample_template_csv
        template_csv = get_sample_template_csv("policies")
        self.assertTrue("policy_id" in template_csv)
        
        result = ingest_custom_file(
            file_bytes=template_csv.encode('utf-8'),
            filename="unit_test_policies.csv",
            dataset_type="policies",
            mode="append"
        )
        self.assertEqual(result["status"], "SUCCESS")
        self.assertGreaterEqual(result["ingested_rows"], 3)
        self.assertIn("total_policies", result["portfolio_summary"])

if __name__ == "__main__":
    unittest.main()

