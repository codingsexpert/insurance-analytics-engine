"""
Python Client & Integration SDK for General Insurance Platform.
Demonstrates how external Core PAS (Policy Administration Systems),
Broker quote engines, and Claims FNOL systems interact with the platform API.
"""

import urllib.request
import json
from typing import Dict, Any

class GeneralInsuranceClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url.rstrip("/")

    def _post(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))

    def _get(self, endpoint: str) -> Any:
        url = f"{self.base_url}{endpoint}"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))

    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Fetches top-level portfolio actuarial metrics."""
        return self._get("/api/summary")

    def rate_policy_quote(
        self,
        driver_age: int,
        driving_experience: int,
        vehicle_type: str,
        vehicle_age: int,
        vehicle_value: float,
        annual_mileage: int,
        territory: str,
        bonus_malus: int = 2,
        deductible: float = 500.0,
        exposure: float = 1.0
    ) -> Dict[str, Any]:
        """Calculates expected frequency, severity, pure premium, and commercial tariff."""
        payload = {
            "driver_age": driver_age,
            "driving_experience": driving_experience,
            "vehicle_type": vehicle_type,
            "vehicle_age": vehicle_age,
            "vehicle_value": vehicle_value,
            "annual_mileage": annual_mileage,
            "territory": territory,
            "bonus_malus": bonus_malus,
            "deductible": deductible,
            "exposure": exposure
        }
        return self._post("/api/rate_quote", payload)

    def triage_new_claim(
        self,
        claim_type: str,
        paid_amount: float,
        days_to_report: int,
        policy_tenure: int,
        driver_age: int,
        vehicle_value: float,
        vehicle_age: int,
        territory: str,
        bonus_malus: int = 1,
        deductible: float = 500.0
    ) -> Dict[str, Any]:
        """Scores claim for fraud risk and assigns Fast-Track vs SIU routing."""
        payload = {
            "claim_type": claim_type,
            "paid_amount": paid_amount,
            "days_to_report": days_to_report,
            "policy_tenure": policy_tenure,
            "driver_age": driver_age,
            "vehicle_value": vehicle_value,
            "vehicle_age": vehicle_age,
            "territory": territory,
            "bonus_malus": bonus_malus,
            "deductible": deductible
        }
        return self._post("/api/triage_claim", payload)

    def get_ibnr_reserves(self) -> Any:
        """Retrieves Chain Ladder IBNR reserves by accident year."""
        return self._get("/api/reserving/ibnr")

    def run_stress_test(
        self,
        severity_inflation_pct: float = 10.0,
        frequency_surge_pct: float = 15.0,
        reinsurance_retention: float = 25000.0
    ) -> Dict[str, Any]:
        """Simulates macroeconomic and catastrophe shock impact on combined ratio."""
        payload = {
            "severity_inflation_pct": severity_inflation_pct,
            "frequency_surge_pct": frequency_surge_pct,
            "reinsurance_retention_limit": reinsurance_retention,
            "expense_ratio_pct": 22.0
        }
        return self._post("/api/analytics/stress_test", payload)

if __name__ == "__main__":
    print("Connecting to local General Insurance API...")
    client = GeneralInsuranceClient()
    
    # 1. Summary
    summary = client.get_portfolio_summary()
    print(f"\n[1] Portfolio Policies: {summary.get('portfolio_size', 0):,} | Empirical Frequency: {summary.get('empirical_frequency', 0)*100:.2f}%")
    
    # 2. Real-time Quote Rating
    print("\n[2] Rating a New Motor Policy Quote:")
    quote = client.rate_policy_quote(
        driver_age=22,
        driving_experience=3,
        vehicle_type="Sports",
        vehicle_age=1,
        vehicle_value=42000.0,
        annual_mileage=18000,
        territory="Urban_HighRisk",
        bonus_malus=0, # No discount
        deductible=500.0
    )
    print(f"  Risk Tier: {quote['risk_tier']}")
    print(f"  Expected Annual Claim Frequency: {quote['expected_claim_frequency']*100:.2f}%")
    print(f"  Expected Claim Severity: ${quote['expected_claim_severity']:.2f}")
    print(f"  Actuarial Pure Premium: ${quote['pure_premium']:.2f}")
    print(f"  Commercial Gross Tariff: ${quote['recommended_gross_premium']:.2f}")
    
    # 3. Claims Triage
    print("\n[3] Triaging a Suspicious FNOL Claim:")
    clm = client.triage_new_claim(
        claim_type="Collision",
        paid_amount=24500.0,
        days_to_report=45, # Late reporting
        policy_tenure=0,   # Brand new policy
        driver_age=23,
        vehicle_value=45000.0,
        vehicle_age=1,
        territory="Urban_HighRisk",
        bonus_malus=0
    )
    print(f"  Fraud Risk Score: {clm['fraud_risk_score_100']}/100")
    print(f"  Triage Status: {clm['status']}")
    print(f"  Recommendation: {clm['recommendation']}")
    
    # 4. Stress Test
    print("\n[4] Running Catastrophe Stress Test (+20% Severity Inflation, +25% Storm Surge):")
    stress = client.run_stress_test(severity_inflation_pct=20.0, frequency_surge_pct=25.0)
    out = stress["stressed_outcome"]
    print(f"  Stressed Gross Loss: ${out['total_stressed_gross_loss']:,.2f}")
    print(f"  Ceded to Reinsurance: ${out['total_ceded_to_reinsurer']:,.2f}")
    print(f"  Net Combined Ratio: {out['net_combined_ratio_pct']:.1f}% -> {out['financial_health']}")
