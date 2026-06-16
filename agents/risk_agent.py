from models.schemas import (
    RiskResult
)

from utils.llm_loader import llm


def risk_agent(
    identity_result,
    features,
    profile_result
):

    risk_score = 0

    # ==========================
    # IDENTITY
    # ==========================

    if (
        identity_result.match_score
        <
        0.80
    ):

        risk_score += 40

    # ==========================
    # CASH
    # ==========================

    if (
        features.cash_ratio
        >
        0.50
    ):

        risk_score += 25

    # ==========================
    # HIGH VALUE
    # ==========================

    if (
        features.high_value_txn_count
        >
        3
    ):

        risk_score += 15

    # ==========================
    # CREDIT
    # ==========================

    if (
        features.total_credit
        >
        500000
    ):

        risk_score += 10

    # ==========================
    # INTERNATIONAL
    # ==========================

    if (
        features.international_ratio
        >
        0.30
    ):

        risk_score += 10

    # ==========================
    # PROFILE SIGNAL
    # ==========================

    if (
        "High Cash Usage"
        in
        profile_result.risk_indicators
    ):

        risk_score += 10

    # ==========================
    # LEVEL
    # ==========================

    if risk_score >= 60:

        risk_level = "HIGH"

    elif risk_score >= 30:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"

    # ==========================
    # LLM
    # ==========================

    prompt = f"""
You are a Senior KYC Risk Officer.

Return ONLY:

Risk Reason: <one line>

Main Concern: <one line>

Recommendation: <one line>

Identity Status:
{identity_result.match_status}

Identity Score:
{identity_result.match_score}

Cash Ratio:
{features.cash_ratio}

High Value Count:
{features.high_value_txn_count}

International Ratio:
{features.international_ratio}

Customer Profile:
{profile_result.profile}

Risk Indicators:
{profile_result.risk_indicators}

Final Risk:
{risk_level}
"""

    explanation = ""

    try:

        response = llm(
            prompt,
            max_new_tokens=100
        )[0][
            "generated_text"
        ]

        explanation = (
            response
            .replace(
                prompt,
                ""
            )
            .strip()
        )

    except:
        pass

    # ==========================
    # FALLBACK
    # ==========================

    if len(explanation) < 10:

        explanation = f"""
Risk Reason:
Customer categorized as {risk_level} risk.

Main Concern:
Transaction and identity indicators.

Recommendation:
Proceed according to review workflow.
"""

    # ==========================
    # RETURN
    # ==========================

    return RiskResult(

        risk_score=float(
            risk_score
        ),

        risk_level=risk_level,

        explanation=(
            explanation.strip()
        )
    )