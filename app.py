import streamlit as st
import pandas as pd

from graph.kyc_graph import graph
from models.schemas import RiskResult


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="KYC Intelligence Dashboard",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 KYC Intelligence Dashboard")

st.caption(
    "OCR → Validation → Identity → Transaction → Profile → Risk → Human Review"
)

st.divider()


# ==========================================
# INPUT
# ==========================================

customer_id = st.number_input(
    "Enter Customer ID",
    min_value=100001,
    step=1
)

run = st.button(
    "🚀 Run Analysis",
    use_container_width=True
)


# ==========================================
# RUN
# ==========================================

if run:

    with st.spinner("Running KYC Pipeline..."):

        try:

            result = graph.invoke(
                {
                    "customer_id": customer_id
                }
            )

        except Exception as e:

            st.error(str(e))
            st.stop()

    # =============================

    risk = RiskResult(
        **result["risk_result"]
    )

    review = result["review_result"]

    identity = result["identity_result"]

    txn = result["transaction_features"]

    profile = result["profile_result"]

    ocr = result["ocr_result"]

    document = result["document_result"]


    # ==========================================
    # FINAL DECISION
    # ==========================================

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
            "🟢 FINAL DECISION → AUTO APPROVED"
        )


    # ==========================================
    # TOP KPI
    # ==========================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Customer ID",
        identity["customer_id"]
    )

    c2.metric(
        "Risk Score",
        f"{risk.risk_score}/100"
    )

    c3.metric(
        "Risk Level",
        risk.risk_level
    )

    c4.metric(
        "Review Queue",
        review["review_queue"]
    )


    st.divider()


    # ==========================================
    # TABS
    # ==========================================

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📊 Overview",
            "📈 Transactions",
            "🧾 Verification",
            "🧑 Human Review"
        ]
    )


    # ==========================================
    # TAB 1
    # ==========================================

    with tab1:

        left, right = st.columns([2, 1])

        with left:

            st.subheader("Customer Profile")

            st.markdown(
                f"""
### {profile["profile"]}

{profile["ai_analysis"]}
"""
            )

            st.subheader(
                "Risk Indicators"
            )

            for item in profile["risk_indicators"]:

                st.success(
                    item
                )

        with right:

            st.subheader(
                "Risk Meter"
            )

            st.progress(
                int(
                    min(
                        risk.risk_score,
                        100
                    )
                )
            )

            st.metric(
                "Risk %",
                f"{risk.risk_score}%"
            )

            st.error(
                risk.explanation
            )


    # ==========================================
    # TAB 2
    # ==========================================

    with tab2:

        st.subheader(
            "Transaction Analytics"
        )

        a, b, c, d = st.columns(4)

        a.metric(
            "Credit",
            f"₹{txn['total_credit']:,.0f}"
        )

        b.metric(
            "Debit",
            f"₹{txn['total_debit']:,.0f}"
        )

        c.metric(
            "Cash Ratio",
            f"{txn['cash_ratio']*100:.1f}%"
        )

        d.metric(
            "Avg Balance",
            f"₹{txn['avg_account_balance']:,.0f}"
        )

        chart = pd.DataFrame(
            {
                "Metric": [
                    "Credit",
                    "Debit"
                ],

                "Amount": [
                    txn["total_credit"],
                    txn["total_debit"]
                ]
            }
        )

        st.bar_chart(
            chart.set_index(
                "Metric"
            )
        )

        st.subheader(
            "Transaction Summary"
        )

        txn_df = pd.DataFrame(
            [
                txn
            ]
        )

        st.dataframe(
            txn_df,
            use_container_width=True
        )


    # ==========================================
    # TAB 3
    # ==========================================

    with tab3:

        l, r = st.columns(2)

        with l:

            st.subheader(
                "OCR Information"
            )

            st.info(
                f"""
Name:
{ocr['name']}

DOB:
{ocr['dob']}

PAN:
{ocr['pan']}
"""
            )

            st.subheader(
                "Document Verification"
            )

            st.metric(
                "Document Score",
                document["document_score"]
            )

            st.success(
                document["status"]
            )

        with r:

            st.subheader(
                "Identity Verification"
            )

            st.metric(
                "Match Score",
                identity["match_score"]
            )

            st.write(
                identity["match_status"]
            )

            st.success(
                identity["reasoning"]
            )


    # ==========================================
    # TAB 4
    # ==========================================

    with tab4:

        st.subheader(
            "Human Review"
        )

        st.write(
            f"""
Queue:
{review['review_queue']}
"""
        )

        if review["escalate"]:

            comment = st.text_area(
                "Reviewer Notes",
                height=150
            )

            c1, c2 = st.columns(2)

            with c1:

                if st.button(
                    "✅ Approve"
                ):

                    st.success(
                        "Customer Approved"
                    )

                    st.write(
                        comment
                    )

            with c2:

                if st.button(
                    "❌ Reject"
                ):

                    st.error(
                        "Customer Rejected"
                    )

                    st.write(
                        comment
                    )

        else:

            st.success(
                "No human review required"
            )
