import pandas as pd

from models.schemas import (
    TransactionFeatures
)


def transaction_agent(
    customer_id
):

    # ==========================
    # LOAD DATA
    # ==========================

    df = pd.read_csv(
        "data/transactions.csv"
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
    # FILTER
    # ==========================

    df = df[
        df["customer_id"]
        ==
        customer_id
    ]

    # ==========================
    # EMPTY
    # ==========================

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

    # ==========================
    # CREDIT
    # ==========================

    total_credit = (
        df.loc[
            df["transaction_type"]
            .astype(str)
            .str.lower()
            ==
            "credit",
            "amount"
        ]
        .sum()
    )

    # ==========================
    # DEBIT
    # ==========================

    total_debit = (
        df.loc[
            df["transaction_type"]
            .astype(str)
            .str.lower()
            ==
            "debit",
            "amount"
        ]
        .sum()
    )

    # ==========================
    # CASH RATIO
    # ==========================

    cash_ratio = (
        df["mode"]
        .astype(str)
        .str.lower()
        .eq("cash")
        .mean()
    )

    # ==========================
    # AVG TRANSACTION
    # ==========================

    avg_transaction = (
        df["amount"]
        .mean()
    )

    # ==========================
    # HIGH VALUE TXN
    # ==========================

    high_value_txn_count = (
        df["amount"]
        >
        50000
    ).sum()

    # ==========================
    # INTERNATIONAL (FIXED)
    # ==========================

    df["is_international"] = (
        df["is_international"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    international_txn_count = (
        df["is_international"]
        .isin(["true", "1", "yes", "y"])
        .sum()
    )

    international_ratio = (
        international_txn_count
        /
        len(df)
    )

    # ==========================
    # BALANCES
    # ==========================

    balances = (
        df["account_balance"]
        .dropna()
    )

    avg_balance = (
        balances.mean()
        if not balances.empty
        else 0
    )

    min_balance = (
        balances.min()
        if not balances.empty
        else 0
    )

    max_balance = (
        balances.max()
        if not balances.empty
        else 0
    )

    # ==========================
    # RETURN
    # ==========================

    return TransactionFeatures(

        total_credit=round(total_credit, 2),

        total_debit=round(total_debit, 2),

        cash_ratio=round(cash_ratio, 2),

        avg_transaction=round(avg_transaction, 2),

        high_value_txn_count=int(high_value_txn_count),

        international_txn_count=int(international_txn_count),

        international_ratio=round(international_ratio, 2),

        avg_account_balance=round(avg_balance, 2),

        min_account_balance=round(min_balance, 2),

        max_account_balance=round(max_balance, 2)
    )