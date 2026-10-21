"""
FastAPI Server & Real-time Serving Engine for General Insurance Analytics.
Serves Actuarial KPIs, SQLite queries, Real-time Rating Engine, Claims Triage,
Actuarial Reserving (Triangles & IBNR), Retention Simulator,
and Regulatory Explainability & Fair Lending Audits.
"""

import sys
import os
from pathlib import Path

# Ensure workspace root is always in sys.path
_ROOT = str(Path(__file__).resolve().parent.parent.parent)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import json
import sqlite3
import numpy as np
import pandas as pd
import joblib
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from src.api.schemas import QuoteRatingRequest, ClaimTriageRequest, SQLQueryRequest
from src.data.db import DB_PATH, run_query
from src.data.ingestion import ingest_custom_file, get_sample_template_csv
from src.models.retention import PriceElasticitySimulator
from src.evaluation.explainability import (
    extract_rating_relativities,
    compute_feature_importance,
    compute_fair_lending_audit
)
from src.evaluation.report_generator import generate_actuarial_report
from src.analytics.scenario_stress_test import ActuarialStressTester
from src.analytics.geo_risk import compute_geo_concentration_analysis
from src.analytics.batch_scoring import run_batch_portfolio_scoring

app = FastAPI(
    title="General Insurance Analytics & Modeling Platform",
    description="End-to-end Actuarial Rating Engine, SQLite Lakehouse, Reserving & Retention API",
    version="2.5.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODELS = {}
elasticity_sim = PriceElasticitySimulator()

def load_models():
    """Loads trained actuarial and ML models into memory."""
    models_dir = "models_saved"
    try:
        if os.path.exists(os.path.join(models_dir, "freq_glm.joblib")):
            MODELS['freq_glm'] = joblib.load(os.path.join(models_dir, "freq_glm.joblib"))
        if os.path.exists(os.path.join(models_dir, "freq_booster.joblib")):
            MODELS['freq_booster'] = joblib.load(os.path.join(models_dir, "freq_booster.joblib"))
        if os.path.exists(os.path.join(models_dir, "sev_glm.joblib")):
            MODELS['sev_glm'] = joblib.load(os.path.join(models_dir, "sev_glm.joblib"))
        if os.path.exists(os.path.join(models_dir, "sev_booster.joblib")):
            MODELS['sev_booster'] = joblib.load(os.path.join(models_dir, "sev_booster.joblib"))
        if os.path.exists(os.path.join(models_dir, "tweedie_pipeline.joblib")):
            MODELS['tweedie'] = joblib.load(os.path.join(models_dir, "tweedie_pipeline.joblib"))
        if os.path.exists(os.path.join(models_dir, "fraud_model.joblib")):
            MODELS['fraud'] = joblib.load(os.path.join(models_dir, "fraud_model.joblib"))
        print("Models successfully loaded into memory.")
    except Exception as e:
        print(f"Warning loading models: {e}")

@app.on_event("startup")
def startup_event():
    load_models()

@app.get("/api/summary")
def get_portfolio_summary():
    """Returns top-level portfolio actuarial metrics from SQLite."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*), SUM(exposure), SUM(claim_count), SUM(total_claim_amount) FROM silver_policies;")
        pol_count, tot_exp, tot_claims, tot_losses = cur.fetchone()
        
        cur.execute("SELECT COUNT(*), SUM(is_fraud) FROM bronze_claims;")
        total_claims_recorded, total_fraud_claims = cur.fetchone()
        
        cur.execute("SELECT SUM(estimated_ibnr_reserve), SUM(projected_ultimate_loss) FROM gold_reserves_summary;")
        row_res = cur.fetchone()
        tot_ibnr = row_res[0] if row_res else 0.0
        tot_ultimate = row_res[1] if row_res else 0.0
        
        conn.close()
        
        freq = (tot_claims / tot_exp) if tot_exp else 0
        sev = (tot_losses / tot_claims) if tot_claims else 0
        pure_prem = (tot_losses / tot_exp) if tot_exp else 0
        
        metrics = {}
        if os.path.exists("reports/model_summary.json"):
            with open("reports/model_summary.json") as f:
                metrics = json.load(f).get("metrics", {})
                
        return {
            "portfolio_size": pol_count,
            "total_exposure_years": round(tot_exp or 0, 1),
            "total_claims": tot_claims,
            "total_incurred_loss": round(tot_losses or 0, 2),
            "empirical_frequency": round(freq, 4),
            "empirical_severity": round(sev, 2),
            "empirical_pure_premium": round(pure_prem, 2),
            "fraud_claims_count": total_fraud_claims,
            "total_estimated_ibnr": round(tot_ibnr or 0, 2),
            "total_projected_ultimate_loss": round(tot_ultimate or 0, 2),
            "model_metrics": metrics
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/gold_marts")
def get_gold_rating_cells():
    """Returns aggregated rating cell table from Gold layer in SQLite."""
    try:
        df = run_query("SELECT * FROM gold_rating_cells ORDER BY territory, driver_age_band LIMIT 100;")
        df = df.replace({np.nan: None})
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/rate_quote")
def rate_quote(req: QuoteRatingRequest):
    """Real-time actuarial quote rating engine."""
    if 'tweedie' not in MODELS or 'freq_booster' not in MODELS:
        load_models()
        if 'tweedie' not in MODELS:
            raise HTTPException(status_code=503, detail="Models are initializing. Please wait a moment.")
            
    row = pd.DataFrame([{
        'driver_age': req.driver_age,
        'driving_experience': req.driving_experience,
        'vehicle_age': req.vehicle_age,
        'vehicle_value': req.vehicle_value,
        'annual_mileage': req.annual_mileage,
        'bonus_malus': req.bonus_malus,
        'policy_tenure': req.policy_tenure,
        'deductible': req.deductible,
        'vehicle_type': req.vehicle_type,
        'territory': req.territory,
        'exposure': req.exposure
    }])
    
    tweedie_pipe = MODELS['tweedie']
    tweedie_rate = float(tweedie_pipe.predict(row)[0])
    pure_premium = tweedie_rate * req.exposure
    
    fb = MODELS['freq_booster']
    X_freq = row[fb['features']].copy()
    X_freq[['vehicle_type', 'territory']] = fb['encoder'].transform(X_freq[['vehicle_type', 'territory']])
    expected_freq = float(fb['model'].predict(X_freq)[0] * req.exposure)
    
    sb = MODELS['sev_booster']
    X_sev = row[sb['features']].copy()
    X_sev[['vehicle_type', 'territory']] = sb['encoder'].transform(X_sev[['vehicle_type', 'territory']])
    expected_sev = float(sb['model'].predict(X_sev)[0])
    
    gross_tariff_premium = pure_premium / 0.75
    
    if tweedie_rate < 150:
        tier = "Tier A (Preferred)"
    elif tweedie_rate < 300:
        tier = "Tier B (Standard Plus)"
    elif tweedie_rate < 550:
        tier = "Tier C (Standard)"
    elif tweedie_rate < 900:
        tier = "Tier D (Non-Standard)"
    else:
        tier = "Tier E (High Risk)"
        
    return {
        "pure_premium": round(pure_premium, 2),
        "annual_pure_premium_rate": round(tweedie_rate, 2),
        "expected_claim_frequency": round(expected_freq, 4),
        "expected_claim_severity": round(expected_sev, 2),
        "two_part_pure_premium": round(expected_freq * expected_sev, 2),
        "recommended_gross_premium": round(gross_tariff_premium, 2),
        "risk_tier": tier,
        "expense_loading_pct": 20,
        "profit_margin_pct": 5
    }

@app.post("/api/triage_claim")
def triage_claim(req: ClaimTriageRequest):
    """Evaluates claim for fraud risk and assigns triage route."""
    if 'fraud' not in MODELS:
        load_models()
        if 'fraud' not in MODELS:
            raise HTTPException(status_code=503, detail="Fraud model is initializing.")
            
    fraud_bundle = MODELS['fraud']
    model = fraud_bundle['model']
    train_cols = fraud_bundle['train_columns']
    
    row_dict = {
        'days_to_report': req.days_to_report,
        'paid_amount': req.paid_amount,
        'driver_age': req.driver_age,
        'vehicle_age': req.vehicle_age,
        'vehicle_value': req.vehicle_value,
        'bonus_malus': req.bonus_malus,
        'policy_tenure': req.policy_tenure,
        'deductible': req.deductible,
        'claim_type': req.claim_type,
        'territory': req.territory
    }
    df = pd.DataFrame([row_dict])
    X = pd.get_dummies(df, drop_first=True)
    for col in train_cols:
        if col not in X:
            X[col] = 0
    X = X[train_cols]
    
    fraud_prob = float(model.predict_proba(X)[:, 1][0])
    
    if fraud_prob > 0.38:
        recommendation = "SIU Escalation (High Fraud Probability)"
        status = "FLAGGED_FOR_INVESTIGATION"
        badge_color = "red"
    elif req.paid_amount < 2500 and req.days_to_report <= 7 and fraud_prob < 0.12:
        recommendation = "Fast-Track STP (Immediate Digital Approval)"
        status = "APPROVED_FAST_TRACK"
        badge_color = "green"
    else:
        recommendation = "Standard Desk Adjuster Review"
        status = "STANDARD_REVIEW"
        badge_color = "blue"
        
    return {
        "fraud_probability": round(fraud_prob, 4),
        "fraud_risk_score_100": round(fraud_prob * 100, 1),
        "status": status,
        "recommendation": recommendation,
        "badge_color": badge_color
    }

@app.get("/api/reserving/triangles")
def get_loss_triangles():
    """Returns accident-year cumulative loss development triangle from SQLite."""
    try:
        df = run_query("SELECT * FROM gold_loss_triangles ORDER BY accident_year, development_year;")
        pivoted = df.pivot(index='accident_year', columns='development_year', values='cumulative_paid')
        
        records = []
        for ay in pivoted.index:
            row = {"accident_year": int(ay)}
            for dev in range(5):
                val = pivoted.loc[ay, dev] if dev in pivoted.columns else None
                row[f"dev_{dev}"] = float(val) if pd.notnull(val) else None
            records.append(row)
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reserving/ibnr")
def get_ibnr_summary():
    """Returns IBNR Reserve estimates by accident year from SQLite."""
    try:
        df = run_query("SELECT * FROM gold_reserves_summary ORDER BY accident_year;")
        df = df.replace({np.nan: None})
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class RenewalQuoteRequest(BaseModel):
    current_premium: float = Field(..., ge=50.0)
    proposed_price_change_pct: float = Field(..., ge=-30.0, le=50.0)
    policy_tenure: int = Field(..., ge=0)
    bonus_malus: int = Field(..., ge=0, le=5)
    had_claim: int = Field(0, ge=0, le=1)

@app.post("/api/retention/quote_renewal")
def quote_renewal_retention(req: RenewalQuoteRequest):
    """Evaluates renewal probability and customer price elasticity for a renewal offer."""
    prob = elasticity_sim.predict_renewal_probability(
        price_change_pct=req.proposed_price_change_pct,
        tenure=req.policy_tenure,
        ncb=req.bonus_malus,
        had_claim=req.had_claim
    )
    new_premium = req.current_premium * (1.0 + (req.proposed_price_change_pct / 100.0))
    expected_value = new_premium * prob
    
    return {
        "renewal_probability": round(prob, 4),
        "renewal_likelihood_pct": round(prob * 100, 1),
        "proposed_premium": round(new_premium, 2),
        "expected_realized_premium": round(expected_value, 2),
        "price_sensitivity_status": "High Churn Risk" if prob < 0.65 else ("Moderate Retention" if prob < 0.85 else "Strong Retention")
    }

@app.get("/api/retention/simulate")
def simulate_retention_curve():
    """Simulates portfolio-wide renewal elasticity curve across rate adjustments."""
    try:
        df_sample = run_query("SELECT * FROM silver_policies LIMIT 15000;")
        results = elasticity_sim.simulate_portfolio_renewal(df_sample)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- EXPLAINABILITY & REGULATORY AUDIT ENDPOINTS ---
@app.get("/api/explainability/relativities")
def get_rate_relativities():
    """Returns published pure premium relativities and base rate for tariff filing."""
    return extract_rating_relativities()

@app.get("/api/explainability/feature_importance")
def get_feature_importance():
    """Returns normalized feature importance rankings."""
    return compute_feature_importance()

@app.get("/api/explainability/fairness_audit")
def get_fairness_audit():
    """Returns Disparate Impact Ratio (DIR) compliance analysis under Four-Fifths Rule."""
    return compute_fair_lending_audit()

class StressTestRequest(BaseModel):
    severity_inflation_pct: float = Field(10.0, ge=-20.0, le=50.0)
    frequency_surge_pct: float = Field(15.0, ge=-20.0, le=100.0)
    reinsurance_retention_limit: float = Field(25000.0, ge=5000.0)
    expense_ratio_pct: float = Field(22.0, ge=10.0, le=40.0)

stress_tester = ActuarialStressTester()

@app.post("/api/analytics/stress_test")
def run_scenario_stress_test(req: StressTestRequest):
    """Simulates inflation, catastrophe shocks, and reinsurance outcomes."""
    try:
        res = stress_tester.run_stress_test(
            severity_inflation_pct=req.severity_inflation_pct,
            frequency_surge_pct=req.frequency_surge_pct,
            reinsurance_retention_limit=req.reinsurance_retention_limit,
            expense_ratio_pct=req.expense_ratio_pct
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/geo_risk")
def get_geo_risk_analytics():
    """Returns territorial exposure concentration and Probable Maximum Loss (PML)."""
    try:
        return compute_geo_concentration_analysis()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/batch_score")
def execute_batch_score(sample_size: int = 2500):
    """Executes batch portfolio pure premium rating on active book."""
    try:
        return run_batch_portfolio_scoring(sample_size=sample_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/report/markdown", response_class=PlainTextResponse)
def get_report_markdown():
    """Generates and returns full executive valuation report in Markdown."""
    report_text = generate_actuarial_report()
    return report_text

@app.post("/api/sql")
def execute_sql(req: SQLQueryRequest):
    """Executes read queries against SQLite database."""
    query = req.query.strip()
    if not (query.upper().startswith("SELECT") or query.upper().startswith("PRAGMA") or query.upper().startswith("EXPLAIN")):
        raise HTTPException(status_code=400, detail="Only SELECT or PRAGMA queries are permitted.")
    try:
        df = run_query(query)
        df = df.replace({np.nan: None})
        return {
            "columns": list(df.columns),
            "rows": df.to_dict(orient="records"),
            "row_count": len(df)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/double_lift")
def get_double_lift():
    path = "reports/double_lift_chart.csv"
    if os.path.exists(path):
        df = pd.read_csv(path)
        return df.to_dict(orient="records")
    return []

# Alias routes for flexible API compatibility
@app.post("/api/quote")
def quote_alias(req: QuoteRatingRequest):
    return rate_quote(req)

@app.post("/api/stress_test")
def stress_test_alias(req: StressTestRequest):
    return run_scenario_stress_test(req)

@app.post("/api/quote_renewal")
def quote_renewal_alias(req: RenewalQuoteRequest):
    return quote_renewal_retention(req)

@app.get("/api/geo_risk")
def geo_risk_alias():
    return get_geo_risk_analytics()

@app.get("/api/loss_triangles")
def loss_triangles_alias():
    return get_loss_triangles()

@app.get("/api/reserves_summary")
def reserves_summary_alias():
    return get_ibnr_summary()

@app.get("/api/retention_curve")
def retention_curve_alias():
    return simulate_retention_curve()

@app.get("/api/governance")
def governance_alias():
    return {
        "relativities": extract_rating_relativities(),
        "fairness_audit": compute_fair_lending_audit(),
        "feature_importance": compute_feature_importance()
    }

@app.post("/api/upload/dataset")
async def upload_custom_dataset(
    file: UploadFile = File(...),
    dataset_type: str = Form("policies"),
    mode: str = Form("append")
):
    """
    Accepts CSV / Excel / JSON custom files, cleans & ingests into Bronze,
    and automatically rebuilds Silver & Gold layers in SQLite.
    """
    try:
        content = await file.read()
        result = ingest_custom_file(
            file_bytes=content,
            filename=file.filename,
            dataset_type=dataset_type,
            mode=mode
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/template/{dataset_type}", response_class=PlainTextResponse)
def download_sample_template(dataset_type: str):
    """Generates and returns sample CSV template for policies or claims."""
    if dataset_type not in ("policies", "claims"):
        raise HTTPException(status_code=400, detail="Invalid dataset type. Choose 'policies' or 'claims'.")
    csv_str = get_sample_template_csv(dataset_type)
    return Response(
        content=csv_str,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=sample_{dataset_type}_template.csv"}
    )

@app.api_route("/static/chart.umd.min.js", methods=["GET", "HEAD"])
def serve_chartjs():
    chart_path = "src/api/chart.umd.min.js"
    if os.path.exists(chart_path):
        with open(chart_path, "r", encoding="utf-8") as f:
            return Response(content=f.read(), media_type="application/javascript")
    raise HTTPException(status_code=404, detail="Chart.js file not found")

@app.api_route("/", methods=["GET", "HEAD"], response_class=HTMLResponse)
def serve_dashboard():
    with open("src/api/index.html", "r") as f:
        return f.read()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.main:app", host="127.0.0.1", port=8000, reload=True)

