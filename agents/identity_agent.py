from models.schemas import IdentityOutput

def identity_agent(name: str, matched_name: str) -> IdentityOutput:
    score = 0.98 if name.lower() == matched_name.lower() else 0.75
    return IdentityOutput(match_score=score)