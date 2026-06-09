from models.schemas import TransactionOutput

def transaction_agent(transactions: list) -> TransactionOutput:

    credit = sum(t["amount"] for t in transactions if t["type"] == "credit")
    debit = sum(t["amount"] for t in transactions if t["type"] == "debit")

    cash_ratio = len([t for t in transactions if t["mode"] == "cash"]) / len(transactions)

    return TransactionOutput(
        credit=credit,
        debit=debit,
        cash_ratio=cash_ratio
    )