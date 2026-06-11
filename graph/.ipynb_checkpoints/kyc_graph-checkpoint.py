from typing import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph import END

from models.schemas import (
    OCRResult,
    IdentityResult,
    TransactionFeatures,
    RiskResult
)

from agents.ocr_agent import ocr_agent
from agents.identity_agent import identity_agent
from agents.transaction_agent import transaction_feature_agent
from agents.profile_agent import financial_profile_agent
from agents.risk_agent import risk_agent
from agents.review_agent import human_review_agent

from utils.customer_data import (
    customer_master_df,
    transactions_df
)


# =====================================
# STATE
# =====================================

class KYCState(TypedDict):

    customer_id: int

    document_text: str

    ocr_result: dict

    identity_result: dict

    transaction_features: dict

    profile_result: dict

    risk_result: dict

    review_result: dict


# =====================================
# OCR NODE
# =====================================

def ocr_node(state):

    result = ocr_agent(
        state["document_text"]
    )

    return {
        "ocr_result":
        result.model_dump()
    }


# =====================================
# IDENTITY NODE
# =====================================

def identity_node(state):

    customer_record = customer_master_df[
        customer_master_df["customer_id"]
        ==
        state["customer_id"]
    ].iloc[0]

    result = identity_agent(
        OCRResult(
            **state["ocr_result"]
        ),
        customer_record
    )

    return {
        "identity_result":
        result.model_dump()
    }


# =====================================
# TRANSACTION NODE
# =====================================

def transaction_node(state):

    txns = transactions_df[
        transactions_df["customer_id"]
        ==
        state["customer_id"]
    ].to_dict(
        orient="records"
    )

    result = transaction_feature_agent(
        txns
    )

    return {
        "transaction_features":
        result.model_dump()
    }


# =====================================
# PROFILE NODE
# =====================================

def profile_node(state):

    result = financial_profile_agent(
        TransactionFeatures(
            **state["transaction_features"]
        )
    )

    return {
        "profile_result":
        result
    }


# =====================================
# RISK NODE
# =====================================

def risk_node(state):

    result = risk_agent(

        IdentityResult(
            **state["identity_result"]
        ),

        TransactionFeatures(
            **state["transaction_features"]
        ),

        state["profile_result"]

    )

    return {
        "risk_result":
        result.model_dump()
    }


# =====================================
# REVIEW NODE
# =====================================

def review_node(state):

    result = human_review_agent(

        RiskResult(
            **state["risk_result"]
        )

    )

    return {
        "review_result":
        result.model_dump()
    }


# =====================================
# BUILD GRAPH
# =====================================

builder = StateGraph(KYCState)

builder.add_node(
    "ocr",
    ocr_node
)

builder.add_node(
    "identity",
    identity_node
)

builder.add_node(
    "transaction",
    transaction_node
)

builder.add_node(
    "profile",
    profile_node
)

builder.add_node(
    "risk",
    risk_node
)

builder.add_node(
    "review",
    review_node
)


builder.set_entry_point(
    "ocr"
)

builder.add_edge(
    "ocr",
    "identity"
)

builder.add_edge(
    "identity",
    "transaction"
)

builder.add_edge(
    "transaction",
    "profile"
)

builder.add_edge(
    "profile",
    "risk"
)

builder.add_edge(
    "risk",
    "review"
)

builder.add_edge(
    "review",
    END
)

graph = builder.compile()