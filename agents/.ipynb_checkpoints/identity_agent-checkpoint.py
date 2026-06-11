from difflib import SequenceMatcher

from models.schemas import IdentityResult
from utils.llm_loader import llm


def identity_agent(
    ocr_result,
    customer_record
):

    name_score = SequenceMatcher(
        None,
        ocr_result.name.lower(),
        customer_record["name"].lower()
    ).ratio()

    dob_match = (
        ocr_result.dob ==
        customer_record["dob"]
    )

    pan_match = (
        ocr_result.pan ==
        customer_record["pan"]
    )

    final_score = (
        0.4 * name_score +
        0.3 * int(dob_match) +
        0.3 * int(pan_match)
    )

    prompt = f"""
You are a KYC analyst.

Name Similarity Score:
{name_score}

DOB Match:
{dob_match}

PAN Match:
{pan_match}

Explain the result in one sentence.
"""

    response = llm(
        prompt,
        max_new_tokens=80
    )[0]["generated_text"]

    return IdentityResult(
        match_score=round(final_score, 2),
        match_status=(
            "MATCH"
            if final_score > 0.9
            else "MISMATCH"
        ),
        reasoning=f"""
Name Similarity: {round(name_score,2)}
DOB Match: {dob_match}
PAN Match: {pan_match}
"""
    )