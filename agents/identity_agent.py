import pandas as pd
from difflib import SequenceMatcher

from models.schemas import (
    IdentityResult
)

from utils.llm_loader import llm


def identity_agent(
    ocr_result
):

    # ==========================
    # LOAD CUSTOMER MASTER
    # ==========================

    customer_master_df = pd.read_csv(
        "data/customer_master.csv"
    )

    # ==========================
    # NORMALIZE PAN
    # ==========================

    customer_master_df["pan"] = (
        customer_master_df["pan"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    pan = (
        str(
            ocr_result.pan
        )
        .strip()
        .upper()
    )

    # ==========================
    # FIND CUSTOMER
    # ==========================

    customer = customer_master_df[
        customer_master_df["pan"]
        ==
        pan
    ]

    if customer.empty:

        return IdentityResult(
            customer_id=0,
            name="UNKNOWN",
            pan=pan,
            match_score=0,
            match_status="CUSTOMER_NOT_FOUND",
            reasoning="PAN was not found in customer records."
        )

    customer = customer.iloc[0]

    # ==========================
    # NAME SCORE
    # ==========================

    name_score = SequenceMatcher(
        None,
        str(
            ocr_result.name
        )
        .lower()
        .strip(),
        str(
            customer["name"]
        )
        .lower()
        .strip()
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

    pan_match = True

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
    # LLM REASONING
    # ==========================

    prompt = f"""
Generate ONLY one sentence.

Name Match:
{name_score:.2f}

DOB Match:
{dob_match}

PAN Match:
{pan_match}

Reason:
"""

    reasoning = ""

    try:

        response = llm(
            prompt,
            max_new_tokens=40
        )[0][
            "generated_text"
        ]

        reasoning = (
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

    if len(reasoning) < 10:

        if final_score >= 0.90:

            reasoning = (
                "Customer identity verified using PAN, name and DOB consistency."
            )

        else:

            reasoning = (
                "Customer identity requires additional verification."
            )

    # ==========================
    # RETURN
    # ==========================

    return IdentityResult(

        customer_id=int(
            customer[
                "customer_id"
            ]
        ),

        name=str(
            customer[
                "name"
            ]
        ),

        pan=str(
            customer[
                "pan"
            ]
        ),

        match_score=round(
            final_score,
            2
        ),

        match_status=(
            "MATCH"
            if final_score >= 0.90
            else "MISMATCH"
        ),

        reasoning=reasoning
    )