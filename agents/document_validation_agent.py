import pandas as pd
from difflib import SequenceMatcher

from models.schemas import (
    DocumentValidationResult
)


def document_validation_agent(
    customer_id,
    ocr_result
):

    # ==========================
    # LOAD DATA
    # ==========================

    df = pd.read_csv(
        "data/pan_ground_truth.csv"
    )

    # ==========================
    # NORMALIZE
    # ==========================

    df["customer_id"] = (
        df["customer_id"]
        .astype(str)
        .str.strip()
    )

    customer_id = str(
        customer_id
    ).strip()

    # ==========================
    # FIND CUSTOMER
    # ==========================

    customer = df[
        df["customer_id"]
        ==
        customer_id
    ]

    if customer.empty:

        return DocumentValidationResult(
            document_score=0,
            status="CUSTOMER_NOT_FOUND",
            proceed=False
        )

    customer = customer.iloc[0]

    # ==========================
    # NAME SCORE
    # ==========================

    name_score = SequenceMatcher(
        None,
        str(
            ocr_result.name
        ).upper(),
        str(
            customer["name"]
        ).upper()
    ).ratio()

    # ==========================
    # DOB
    # ==========================

    dob_match = (
        str(
            ocr_result.dob
        ).strip()
        ==
        str(
            customer["dob"]
        ).strip()
    )

    # ==========================
    # PAN
    # ==========================

    pan_match = (
        str(
            ocr_result.pan
        ).upper()
        ==
        str(
            customer["pan"]
        ).upper()
    )

    # ==========================
    # SCORE
    # ==========================

    final_score = (
        0.4
        * name_score
        +
        0.3
        * int(
            dob_match
        )
        +
        0.3
        * int(
            pan_match
        )
    )

    # ==========================
    # RESULT
    # ==========================

    status = (
        "DOCUMENT_VERIFIED"
        if final_score >= 0.90
        else
        "DOCUMENT_REJECTED"
    )

    return DocumentValidationResult(
        document_score=round(
            final_score,
            2
        ),
        status=status,
        proceed=(
            final_score >= 0.90
        )
    )