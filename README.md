# General Insurance Analytics & Actuarial Modeling Engine

An enterprise-grade, end-to-end Actuarial Analytics, Pure Premium Rating, and Claims Intelligence platform built on a local **SQLite Lakehouse (`insurance.db`)**, Python Actuarial stack (**statsmodels**, **scikit-learn**), and a real-time **FastAPI** web dashboard.

---

## Key Business Capabilities

1. **Actuarial Pure Premium Pricing (Tweedie & Compound Poisson-Gamma)**
   - **Claim Frequency**: Poisson GLM (with $\log(\text{exposure})$ offset) & Histogram Gradient Booster.
   - **Claim Severity**: Gamma GLM (log link) & Histogram Gradient Booster on positive claims.
   - **Tweedie Pure Premium ($p=1.5$)**: Test Gini Index = **0.3848** with monotonic 10-decile risk discrimination.
2. **Batch Portfolio Rating Engine**
   - Single-click automated scoring of books of business (e.g. 2,500+ policies at once).
   - Segregation into 5 risk tiers (Tier A Preferred to Tier E High Risk) and projection of Gross Written Premium (GWP).
3. **Actuarial Reserving & Loss Development Triangles (Chain Ladder)**
   - Run-off Cumulative Loss Development Triangles across Accident Years 2021–2025.
   - Age-to-age Link Ratios (LDF) & Cumulative Development Factors (CDF).
   - Solvency II / IFRS 17 compliant **Incurred But Not Reported (IBNR)** reserve calculation (~$2.59M).
4. **Dynamic Price Elasticity & Customer Renewal Simulator**
   - Logistic churn elasticity modeling ($\Delta P\%$ sensitivity, tenure, NCB).
   - Portfolio renewal scenario curves (-15% to +25%) balancing GWP volume vs. Combined Loss Ratio.
5. **Macroeconomic Stress Testing & Reinsurance (XoL)**
   - Social/repair cost inflation shock modeling (+0% to +50%).
   - Catastrophe frequency surge modeling (+0% to +100%).
   - Excess of Loss (XoL) reinsurance treaty retention limit impact on net combined ratio.
6. **Geo-Risk Concentration & Probable Maximum Loss (PML)**
   - Total Insured Value (TIV) by territory (Urban, Suburban, Rural).
   - 1-in-100 Year and 1-in-250 Year Catastrophe PML metrics.
7. **Model Governance & Regulatory Fair Lending Audit**
   - Published DOI Tariff Relativities & Multipliers.
   - Normalized Feature Importance breakdown.
   - Four-Fifths (80%) Rule Disparate Impact Ratio (DIR) compliance verification.
8. **Claims Fraud & FNOL Triage Engine**
   - Random Forest Classifier (PR-AUC: 0.9288, ROC-AUC: 0.9907).
   - Automated routing: Fast-Track STP, Standard Desk Review, and SIU Escalation.

---

## Architecture Overview (Medallion Lakehouse)

```
[Raw Simulation Ingestion]
        │
        ▼
[Bronze Layer (SQLite)]
  ├── bronze_policies  (50,000 raw policy extracts)
  └── bronze_claims    (granular claim occurrences)
        │
        ▼
[Silver Layer (SQLite)]
  └── silver_policies  (conformed exposures, matched losses, loss cost)
        │
        ▼
[Gold Layer (SQLite Actuarial Marts)]
  ├── gold_rating_cells          (empirical frequency, severity, pure premium)
  ├── gold_loss_triangles        (accident year x development year matrix)
  ├── gold_reserves_summary      (chain ladder IBNR reserves)
  └── gold_batch_scored_policies (batch inference risk tiers)
```

---

## Directory Structure

```
├── insurance.db                 # Local SQLite Lakehouse Database
├── requirements.txt             # Frozen Python Dependencies
├── train_and_evaluate.py        # Master pipeline training & evaluation script
├── reports/
│   ├── Actuarial_Portfolio_Valuation_Report.md
│   ├── double_lift_chart.csv
│   └── model_summary.json
├── src/
│   ├── data/
│   │   ├── generator.py         # Actuarial P&C data generator (Poisson/Gamma)
│   │   └── db.py                # SQLite Medallion Pipeline (Bronze/Silver/Gold)
│   ├── models/
│   │   ├── frequency.py         # Poisson GLM & Booster
│   │   ├── severity.py          # Gamma GLM & Booster
│   │   ├── tweedie.py           # Tweedie Pure Premium Model
│   │   ├── fraud.py             # Claim Fraud Classifier
│   │   └── retention.py         # Renewal Price Elasticity Simulator
│   ├── reserving/
│   │   └── chain_ladder.py      # Loss Development Triangles & IBNR
│   ├── analytics/
│   │   ├── scenario_stress_test.py # Macro shock & Reinsurance treaty engine
│   │   ├── geo_risk.py          # TIV Concentration & Catastrophe PML
│   │   └── batch_scoring.py     # Batch Portfolio Book Rating Engine
│   ├── evaluation/
│   │   ├── actuarial_metrics.py # Deviance, Gini, Double Lift deciles
│   │   ├── explainability.py    # Relativities & Fair Lending Audit
│   │   └── report_generator.py  # Markdown audit report generator
│   └── api/
│       ├── main.py              # FastAPI server
│       ├── schemas.py           # Pydantic validation schemas
│       └── index.html           # Enterprise Light-Mode Web Dashboard
└── tests/
    └── test_actuarial_platform.py # Automated test suite (6 tests passing)
```

---

## Quickstart & Local Execution

### 1. Run Automated Unit & Platform Tests
```bash
PYTHONPATH=. .venv/bin/python -m unittest tests/test_actuarial_platform.py
```

### 2. Run Full Data & Model Training Pipeline
```bash
PYTHONPATH=. .venv/bin/python train_and_evaluate.py
```

### 3. Launch Local Web Application & API
```bash
PYTHONPATH=. .venv/bin/uvicorn src.api.main:app --host 127.0.0.1 --port 8000
```
Open your browser at **[http://localhost:8000](http://localhost:8000)**.
