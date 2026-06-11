import pandas as pd

# ==========================
# OCR DOCUMENTS
# ==========================

ocr_documents_df = pd.DataFrame([
    {
        "customer_id": 1,
        "document_text": """
Name: Aarav Mehta
DOB: 12/06/1994
PAN: ABCDE1234F
"""
    }
])

# ==========================
# CUSTOMER MASTER
# ==========================

customer_master_df = pd.DataFrame([
    {
        "customer_id": 1,
        "name": "Aarav Mehta",
        "dob": "12/06/1994",
        "pan": "ABCDE1234F",
        "income": 1200000
    }
])

# ==========================
# TRANSACTIONS
# ==========================

transactions_df = pd.DataFrame([

    {
        "customer_id":1,
        "amount":50000,
        "type":"credit",
        "mode":"salary"
    },

    {
        "customer_id":1,
        "amount":25000,
        "type":"debit",
        "mode":"cash"
    },

    {
        "customer_id":1,
        "amount":15000,
        "type":"debit",
        "mode":"cash"
    },

    {
        "customer_id":1,
        "amount":12000,
        "type":"debit",
        "mode":"upi"
    },

    {
        "customer_id":1,
        "amount":100000,
        "type":"credit",
        "mode":"bonus"
    }

])