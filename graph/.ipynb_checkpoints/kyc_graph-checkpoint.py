from langgraph.graph import StateGraph
from typing import TypedDict

from agents.ocr_agent import ocr_agent
from agents.identity_agent import identity_agent
from agents.transaction_agent import transaction_agent
from agents.compliance_agent import compliance_agent
from agents.risk_agent import risk_agent


# =========================
# STATE DEFINITION
# =========================
class KYCState(TypedDict):
    ocr_text: str
    name: str
    matched_name: str
    transactions: list
    pep_flag: int
    sanctions_flag: int


# =========================
# MAIN PIPELINE NODE
# =========================
def run_kyc_pipeline(state: KYCState):

    # STEP 1: OCR
    ocr_result = ocr_agent(state["ocr_text"])

    # STEP 2: Identity Verification
    identity_result = identity_agent(
        state["name"],
        state["matched_name"]
    )

    # STEP 3: Transaction Analysis
    transaction_result = transaction_agent(state["transactions"])

    # STEP 4: Compliance Check
    compliance_result = compliance_agent(
        state["pep_flag"],
        state["sanctions_flag"]
    )

    # STEP 5: Risk Scoring
    risk_result = risk_agent(
        identity_result,
        transaction_result,
        compliance_result
    )

    # =========================
    # FINAL OUTPUT (IMPORTANT)
    # =========================
    return {
        "ocr": ocr_result.model_dump(),
        "identity": identity_result.model_dump(),
        "transaction": transaction_result.model_dump(),
        "compliance": compliance_result.model_dump(),
        "risk": risk_result.model_dump()
    }


# =========================
# BUILD GRAPH
# =========================
def build_graph():
    graph = StateGraph(KYCState)

    # single node pipeline (simple hackathon version)
    graph.add_node("kyc_pipeline", run_kyc_pipeline)

    graph.set_entry_point("kyc_pipeline")
    graph.set_finish_point("kyc_pipeline")

    return graph.compile()