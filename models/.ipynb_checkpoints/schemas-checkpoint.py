from pydantic import BaseModel

class OCROutput(BaseModel):
    name: str
    dob: str
    id_number: str


class IdentityOutput(BaseModel):
    match_score: float


class TransactionOutput(BaseModel):
    credit: float
    debit: float
    cash_ratio: float


class ComplianceOutput(BaseModel):
    risk: str


class RiskOutput(BaseModel):
    final_score: float
    risk_label: str


class FinalOutput(BaseModel):
    ocr: OCROutput
    identity: IdentityOutput
    transaction: TransactionOutput
    compliance: ComplianceOutput
    risk: RiskOutput