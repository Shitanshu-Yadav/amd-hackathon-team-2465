import pandas as pd
from models.schemas import TransactionFeatures


def transaction_agent(customer_id):

    # Load transactions
    df = pd.read_csv("data/transactions.csv")

    # Filter customer
    df = df[df["customer_id"] == customer_id]

    if df.empty:
        return TransactionFeatures(
            total_credit=0,
            total_debit=0,
            cash_ratio=0,
            avg_transaction=0,
            high_value_txn_count=0,
            international_txn_count=0,
            international_ratio=0,
            avg_account_balance=0,
            min_account_balance=0,
            max_account_balance=0
        )

    # Credit / Debit
    total_credit = df.loc[
        df["transaction_type"].str.lower() == "credit",
        "amount"
    ].sum()

    total_debit = df.loc[
        df["transaction_type"].str.lower() == "debit",
        "amount"
    ].sum()

    # Cash ratio
    cash_ratio = (
        df["mode"]
        .astype(str)
        .str.lower()
        .eq("cash")
        .mean()
    )

    # Average transaction
    avg_transaction = df["amount"].mean()

    # High value transactions
    high_value_txn_count = (
        df["amount"] > 50000
    ).sum()

    # International transactions
    international_txn_count = (
        df["is_international"]
        .astype(str)
        .str.lower()
        .eq("true")
        .sum()
    )

    international_ratio = (
        international_txn_count / len(df)
    )

    # Balance metrics
    balances = (
        df["account_balance"]
        .dropna()
    )

    avg_account_balance = (
        balances.mean()
        if not balances.empty
        else 0
    )

    min_account_balance = (
        balances.min()
        if not balances.empty
        else 0
    )

    max_account_balance = (
        balances.max()
        if not balances.empty
        else 0
    )

    return TransactionFeatures(
        total_credit=round(total_credit, 2),
        total_debit=round(total_debit, 2),
        cash_ratio=round(cash_ratio, 2),
        avg_transaction=round(avg_transaction, 2),
        high_value_txn_count=int(high_value_txn_count),
        international_txn_count=int(international_txn_count),
        international_ratio=round(international_ratio, 2),
        avg_account_balance=round(avg_account_balance, 2),
        min_account_balance=round(min_account_balance, 2),
        max_account_balance=round(max_account_balance, 2)
    )