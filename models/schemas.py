from pydantic import BaseModel
from typing import List


class OCRResult(BaseModel):
    name: str
    dob: str
    pan: str


class IdentityResult(BaseModel):
    match_score: float
    match_status: str
    reasoning: str


class ComplianceResult(BaseModel):
    sanctions_match: bool
    pep_match: bool
    risk_level: str
    reasoning: str


class TransactionFeatures(BaseModel):
    total_credit: float
    total_debit: float
    cash_ratio: float
    avg_transaction: float
    high_value_txn_count: int


class FinancialProfile(BaseModel):
    profile: str
    risk_indicators: List[str]


class RiskResult(BaseModel):
    risk_score: float
    risk_level: str
    explanation: str


class HumanReviewResult(BaseModel):
    escalate: bool
    review_queue: str