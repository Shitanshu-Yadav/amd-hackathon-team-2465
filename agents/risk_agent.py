from models.schemas import RiskResult
from utils.llm_loader import llm


def risk_agent(
    identity_result,
    features,
    profile_result
):

    risk_score = 0

    # Identity Risk

    if identity_result.match_score < 0.80:
        risk_score += 40

    # Cash Usage

    if features.cash_ratio > 0.50:
        risk_score += 25

    # High Value Transactions

    if features.high_value_txn_count > 0:
        risk_score += 15

    # Very High Credits

    if features.total_credit > 500000:
        risk_score += 10

    # Risk Level

    if risk_score >= 60:
        risk_level = "HIGH"

    elif risk_score >= 30:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    prompt = f"""
You are a Senior KYC Risk Officer.

Customer Identity Result:

{identity_result}

Customer Transaction Features:

{features}

Customer Financial Profile:

{profile_result}

Risk Score:
{risk_score}

Risk Level:
{risk_level}

Explain why the customer received this risk level in 3 lines.
"""

    response = llm(
        prompt,
        max_new_tokens=120
    )[0]["generated_text"]

    return RiskResult(
        risk_score=float(risk_score),
        risk_level=risk_level,
        explanation=response[-500:]
    )