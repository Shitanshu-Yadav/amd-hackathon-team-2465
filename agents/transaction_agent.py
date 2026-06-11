from models.schemas import TransactionFeatures


def transaction_feature_agent(txns):

    total_credit = sum(
        x["amount"]
        for x in txns
        if x["type"] == "credit"
    )

    total_debit = sum(
        x["amount"]
        for x in txns
        if x["type"] == "debit"
    )

    cash_txns = [
        x for x in txns
        if x["mode"] == "cash"
    ]

    cash_ratio = (
        len(cash_txns)
        / len(txns)
    )

    avg_transaction = (
        sum(x["amount"] for x in txns)
        / len(txns)
    )

    high_value_txn_count = len([
        x for x in txns
        if x["amount"] > 50000
    ])

    return TransactionFeatures(
        total_credit=total_credit,
        total_debit=total_debit,
        cash_ratio=round(cash_ratio, 2),
        avg_transaction=round(avg_transaction, 2),
        high_value_txn_count=high_value_txn_count
    )