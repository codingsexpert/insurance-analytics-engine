"""
Pydantic API request & response schemas for General Insurance API.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class QuoteRatingRequest(BaseModel):
    driver_age: int = Field(..., ge=18, le=90, description="Driver age in years")
    driving_experience: int = Field(..., ge=0, le=70, description="Years of driving experience")
    vehicle_type: str = Field(..., description="Sedan, SUV, Hatchback, Luxury, Sports")
    vehicle_age: int = Field(..., ge=0, le=30, description="Vehicle age in years")
    vehicle_value: float = Field(..., ge=1000, description="Vehicle insured value in INR (₹)")
    annual_mileage: int = Field(..., ge=1000, description="Estimated annual mileage in km")
    territory: str = Field(..., description="Urban_HighRisk, Urban_Standard, Suburban, Rural")
    bonus_malus: int = Field(..., ge=0, le=5, description="No Claim Bonus discount tier (0-5)")
    policy_tenure: int = Field(0, ge=0, description="Years with current insurer")
    deductible: float = Field(2500.0, ge=100.0, description="Policy deductible in INR (₹)")
    exposure: float = Field(1.0, ge=0.01, le=1.0, description="Policy exposure duration (fraction of year)")

class ClaimTriageRequest(BaseModel):
    days_to_report: int = Field(..., ge=0, description="Days elapsed between incident and reporting")
    paid_amount: float = Field(..., ge=0, description="Claim amount / estimate in INR (₹)")
    claim_type: str = Field(..., description="Collision, Comprehensive, Theft, Third_Party")
    driver_age: int = Field(..., ge=18, le=90)
    vehicle_age: int = Field(..., ge=0, le=30)
    vehicle_value: float = Field(..., ge=1000)
    bonus_malus: int = Field(..., ge=0, le=5)
    policy_tenure: int = Field(..., ge=0)
    deductible: float = Field(..., ge=100)
    territory: str = Field(...)

class SQLQueryRequest(BaseModel):
    query: str = Field(..., description="SELECT query to run against SQLite database")
