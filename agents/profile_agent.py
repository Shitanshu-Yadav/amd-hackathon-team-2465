from models.schemas import FinancialProfile
from utils.llm_loader import llm


def financial_profile_agent(features):

    prompt = f"""
You are a senior banking analyst.

Customer Features:

Total Credit: {features.total_credit}
Total Debit: {features.total_debit}
Cash Ratio: {features.cash_ratio}
Average Transaction: {features.avg_transaction}
High Value Transactions: {features.high_value_txn_count}

Provide a short customer profile and risk observations.
"""

    response = llm(
        prompt,
        max_new_tokens=150
    )[0]["generated_text"]

    profile = "Salary Based Customer"

    risks = []

    if features.cash_ratio > 0.5:
        risks.append("High Cash Usage")

    if features.high_value_txn_count > 0:
        risks.append("High Value Transactions")

    if features.total_credit > 100000:
        risks.append("High Income Customer")

    return {
        "profile": profile,
        "risk_indicators": risks,
        "ai_analysis": response[-500:]
    }