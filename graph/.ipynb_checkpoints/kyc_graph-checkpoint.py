from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    END
)

from models.schemas import (
    OCRResult,
    DocumentValidationResult,
    IdentityResult,
    TransactionFeatures,
    FinancialProfile,
    RiskResult
)

from agents.ocr_agent import (
    ocr_agent
)

from agents.document_validation_agent import (
    document_validation_agent
)

from agents.identity_agent import (
    identity_agent
)

from agents.transaction_agent import (
    transaction_agent
)

from agents.profile_agent import (
    financial_profile_agent
)

from agents.risk_agent import (
    risk_agent
)

from agents.review_agent import (
    human_review_agent
)


# ==========================
# SAFE DUMP
# ==========================

def safe_dump(x):

    if hasattr(
        x,
        "model_dump"
    ):

        return x.model_dump()

    return x


# ==========================
# STATE
# ==========================

class KYCState(TypedDict):

    customer_id: int

    ocr_result: dict

    document_result: dict

    identity_result: dict

    transaction_features: dict

    profile_result: dict

    risk_result: dict

    review_result: dict


# ==========================
# OCR
# ==========================

def ocr_node(
    state
):

    result = ocr_agent(

        state[
            "customer_id"
        ]

    )

    return {

        "ocr_result":

        safe_dump(
            result
        )

    }


# ==========================
# DOCUMENT
# ==========================

def document_node(
    state
):

    result = document_validation_agent(

        state[
            "customer_id"
        ],

        OCRResult(

            **state[
                "ocr_result"
            ]

        )

    )

    return {

        "document_result":

        safe_dump(
            result
        )

    }


# ==========================
# ROUTER
# ==========================

def validation_router(
    state
):

    if (

        state[
            "document_result"
        ][
            "proceed"
        ]

    ):

        return "identity"

    return END


# ==========================
# IDENTITY
# ==========================

def identity_node(
    state
):

    result = identity_agent(

        OCRResult(

            **state[
                "ocr_result"
            ]

        )

    )

    return {

        "identity_result":

        safe_dump(
            result
        )

    }


# ==========================
# TRANSACTION
# ==========================

def transaction_node(
    state
):

    customer_id = (

        state[
            "identity_result"
        ][
            "customer_id"
        ]

    )

    result = transaction_agent(

        customer_id

    )

    return {

        "transaction_features":

        safe_dump(
            result
        )

    }


# ==========================
# PROFILE
# ==========================

def profile_node(
    state
):

    result = financial_profile_agent(

        TransactionFeatures(

            **state[
                "transaction_features"
            ]

        )

    )

    return {

        "profile_result":

        safe_dump(
            result
        )

    }


# ==========================
# RISK
# ==========================

def risk_node(
    state
):

    result = risk_agent(

        IdentityResult(

            **state[
                "identity_result"
            ]

        ),

        TransactionFeatures(

            **state[
                "transaction_features"
            ]

        ),

        FinancialProfile(

            **state[
                "profile_result"
            ]

        )

    )

    return {

        "risk_result":

        safe_dump(
            result
        )

    }


# ==========================
# REVIEW
# ==========================

def review_node(
    state
):

    result = human_review_agent(

        RiskResult(

            **state[
                "risk_result"
            ]

        )

    )

    return {

        "review_result":

        safe_dump(
            result
        )

    }


# ==========================
# BUILD
# ==========================

builder = StateGraph(
    KYCState
)

builder.add_node(
    "ocr",
    ocr_node
)

builder.add_node(
    "document",
    document_node
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
    "document"
)

builder.add_conditional_edges(

    "document",

    validation_router,

    {

        "identity":
        "identity",

        END:
        END

    }

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