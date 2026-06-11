from pprint import pprint

from graph.kyc_graph import graph
from utils.customer_data import ocr_documents_df


def main():

    document_text = (
        ocr_documents_df.iloc[0]["document_text"]
    )

    result = graph.invoke(
        {
            "customer_id": 1,
            "document_text": document_text
        }
    )

    print("\n========== FINAL RESULT ==========\n")

    pprint(result)


if __name__ == "__main__":
    main()