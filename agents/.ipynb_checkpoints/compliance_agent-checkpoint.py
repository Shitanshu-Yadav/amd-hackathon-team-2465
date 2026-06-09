from models.schemas import ComplianceOutput

def compliance_agent(pep_flag: int, sanctions_flag: int) -> ComplianceOutput:

    if sanctions_flag == 1:
        risk = "HIGH"
    elif pep_flag == 1:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return ComplianceOutput(risk=risk)