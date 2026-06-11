from models.schemas import HumanReviewResult


def human_review_agent(risk_result):

    if risk_result.risk_level == "HIGH":

        return HumanReviewResult(
            escalate=True,
            review_queue="MANUAL_REVIEW"
        )

    return HumanReviewResult(
        escalate=False,
        review_queue="AUTO_APPROVED"
    )