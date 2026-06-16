from models.schemas import (
    FinancialProfile
)

from utils.llm_loader import llm


def financial_profile_agent(
    features
):

    # ==========================
    # PROMPT
    # ==========================

    prompt = f"""
You are a banking analyst.

Return ONLY:

Customer Profile: <one line>

Risk Summary: <one line>

Data:

Total Credit:
{features.total_credit}

Total Debit:
{features.total_debit}

Cash Ratio:
{features.cash_ratio}

Average Transaction:
{features.avg_transaction}

High Value Transactions:
{features.high_value_txn_count}

International Ratio:
{features.international_ratio}

Average Balance:
{features.avg_account_balance}
"""

    # ==========================
    # LLM
    # ==========================

    ai_analysis = ""

    try:

        response = llm(
            prompt,
            max_new_tokens=80
        )[0][
            "generated_text"
        ]

        ai_analysis = (
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

    if len(ai_analysis) < 10:

        ai_analysis = (
            "Customer Profile: Stable banking behaviour.\n"
            "Risk Summary: Low transaction concern."
        )

    # ==========================
    # PROFILE
    # ==========================

    if features.cash_ratio > 0.60:

        profile = (
            "Cash Intensive Customer"
        )

    elif features.total_credit > 150000:

        profile = (
            "High Income Customer"
        )

    else:

        profile = (
            "Salary Based Customer"
        )

    # ==========================
    # RISK FLAGS
    # ==========================

    risks = []

    if features.cash_ratio > 0.50:

        risks.append(
            "High Cash Usage"
        )

    if features.high_value_txn_count > 3:

        risks.append(
            "Frequent High Value Transactions"
        )

    if features.international_ratio > 0.30:

        risks.append(
            "International Exposure"
        )

    if not risks:

        risks.append(
            "Low Transaction Risk"
        )

    # ==========================
    # RETURN
    # ==========================

    return FinancialProfile(

        profile=profile,

        risk_indicators=risks,

        ai_analysis=ai_analysis
    )