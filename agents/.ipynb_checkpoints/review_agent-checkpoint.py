from models.schemas import (
    HumanReviewResult
)


def human_review_agent(
    risk_result,
    reviewer_comment=""
):

    # ==========================
    # HIGH
    # ==========================

    if (
        risk_result.risk_level
        ==
        "HIGH"
    ):

        return HumanReviewResult(

            escalate=True,

            review_queue=
            "MANUAL_REVIEW",

            reviewer_comment=
            reviewer_comment
        )

    # ==========================
    # MEDIUM
    # ==========================

    elif (
        risk_result.risk_level
        ==
        "MEDIUM"
    ):

        return HumanReviewResult(

            escalate=True,

            review_queue=
            "SECOND_LEVEL_REVIEW",

            reviewer_comment=
            reviewer_comment
        )

    # ==========================
    # LOW
    # ==========================

    return HumanReviewResult(

        escalate=False,

        review_queue=
        "AUTO_APPROVED",

        reviewer_comment=""
    )