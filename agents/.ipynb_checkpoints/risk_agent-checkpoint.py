from models.schemas import RiskOutput

def risk_agent(identity, transaction, compliance) -> RiskOutput:

    compliance_score = 0.2 if compliance.risk == "HIGH" else 0.7

    final_score = (
        0.3 * identity.match_score +
        0.4 * (1 - transaction.cash_ratio) +
        0.3 * compliance_score
    )

    label = "HIGH" if final_score > 0.7 else "MEDIUM" if final_score > 0.4 else "LOW"

    return RiskOutput(
        final_score=final_score,
        risk_label=label
    )