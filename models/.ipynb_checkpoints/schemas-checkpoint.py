from pydantic import BaseModel
from typing import List

# ==========================
# OCR
# ==========================

class OCRResult(BaseModel):
    name: str
    dob: str
    pan: str


# ==========================
# DOCUMENT
# ==========================

class DocumentValidationResult(BaseModel):
    document_score: float
    status: str
    proceed: bool


# ==========================
# IDENTITY
# ==========================

class IdentityResult(BaseModel):
    customer_id: int
    name: str
    pan: str
    match_score: float
    match_status: str
    reasoning: str


# ==========================
# COMPLIANCE
# ==========================

class ComplianceResult(BaseModel):
    sanctions_match: bool
    pep_match: bool
    risk_level: str
    reasoning: str


# ==========================
# TRANSACTION
# ==========================

class TransactionFeatures(BaseModel):
    total_credit: float
    total_debit: float
    cash_ratio: float
    avg_transaction: float
    high_value_txn_count: int
    international_txn_count: int
    international_ratio: float
    avg_account_balance: float
    min_account_balance: float
    max_account_balance: float


# ==========================
# PROFILE
# ==========================

class FinancialProfile(BaseModel):
    profile: str
    risk_indicators: List[str]
    ai_analysis: str


# ==========================
# RISK
# ==========================

class RiskResult(BaseModel):
    risk_score: float
    risk_level: str
    explanation: str


# ==========================
# HUMAN REVIEW
# ==========================

class HumanReviewResult(BaseModel):
    escalate: bool
    review_queue: str
    reviewer_comment: str = ""