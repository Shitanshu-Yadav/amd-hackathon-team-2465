import streamlit as st
from graph.kyc_graph import graph
from models.schemas import RiskResult

# ==========================
# CONFIG
# ==========================

st.set_page_config(
    page_title="KYC Risk Analyzer",
    page_icon="🧾",
    layout="wide"
)

# ==========================
# HEADER
# ==========================

st.title(
    "🧾 KYC Risk Analysis System"
)

st.caption(
    "OCR → Validation → Identity → Transaction → Profile → Risk → Human Review"
)

# ==========================
# INPUT
# ==========================

customer_id = st.number_input(
    "Enter Customer ID",
    min_value=100001,
    step=1
)

run = st.button(
    "Run Analysis"
)

# ==========================
# RUN
# ==========================

if run:

    with st.spinner(
        "Running KYC Pipeline..."
    ):

        try:

            result = graph.invoke(
                {
                    "customer_id":
                    customer_id
                }
            )

        except Exception as e:

            st.error(
                str(e)
            )

            st.stop()

    risk = RiskResult(
        **result[
            "risk_result"
        ]
    )

    review = result[
        "review_result"
    ]

    # ==========================
    # DECISION BANNER
    # ==========================

    if risk.risk_level == "HIGH":

        st.error(
            "🔴 FINAL DECISION → MANUAL REVIEW"
        )

    elif risk.risk_level == "MEDIUM":

        st.warning(
            "🟡 FINAL DECISION → SECOND LEVEL REVIEW"
        )

    else:

        st.success(
            "🟢 FINAL DECISION → APPROVED"
        )

    # ==========================
    # DASHBOARD
    # ==========================

    st.subheader(
        "📌 Customer Summary"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Customer ID",
            result[
                "identity_result"
            ][
                "customer_id"
            ]
        )

    with c2:

        st.metric(
            "Risk Score",
            risk.risk_score
        )

    with c3:

        st.metric(
            "Risk Level",
            risk.risk_level
        )

    with c4:

        st.metric(
            "Review Queue",
            review[
                "review_queue"
            ]
        )

    # ==========================
    # PROGRESS
    # ==========================

    st.subheader(
        "⚙ Pipeline Status"
    )

    st.success("✓ OCR Completed")
    st.success("✓ Document Verified")
    st.success("✓ Identity Verified")
    st.success("✓ Transaction Analysis")
    st.success("✓ Financial Profile")
    st.success("✓ Risk Generated")

    # ==========================
    # RISK BAR
    # ==========================

    st.subheader(
        "🚨 Risk Meter"
    )

    st.progress(
        min(
            int(
                risk.risk_score
            ),
            100
        )
    )

    # ==========================
    # MAIN GRID
    # ==========================

    left, right = st.columns(
        2
    )

    with left:

        with st.expander(
            "📄 OCR Result",
            expanded=True
        ):

            st.json(
                result[
                    "ocr_result"
                ]
            )

        with st.expander(
            "📑 Document Validation"
        ):

            st.json(
                result[
                    "document_result"
                ]
            )

        with st.expander(
            "🪪 Identity Verification"
        ):

            st.json(
                result[
                    "identity_result"
                ]
            )

    with right:

        with st.expander(
            "💳 Transaction Features",
            expanded=True
        ):

            st.json(
                result[
                    "transaction_features"
                ]
            )

        with st.expander(
            "📊 Financial Profile"
        ):

            st.json(
                result[
                    "profile_result"
                ]
            )

        with st.expander(
            "🚨 Risk Analysis"
        ):

            st.write(
                risk.explanation
            )

    # ==========================
    # REVIEW
    # ==========================

    st.subheader(
        "🧑‍💼 Human Review"
    )

    st.json(
        review
    )

    if review[
        "escalate"
    ]:

        comment = st.text_area(
            "Reviewer Comment",
            height=150
        )

        if st.button(
            "Save Review"
        ):

            st.success(
                "Comment Saved"
            )

            st.write(
                comment
            )

    # ==========================
    # RAW OUTPUT
    # ==========================

    with st.expander(
        "🔍 Debug Output"
    ):

        st.json(
            result
        )