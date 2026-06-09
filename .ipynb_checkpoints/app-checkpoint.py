from graph.kyc_graph import build_graph

graph = build_graph()

sample_input = {
    "ocr_text": "Name: Aarav Mehta\nDOB: 12/06/1994\nPAN: ABCDE1234F",
    "name": "Aarav Mehta",
    "matched_name": "Aarav Mehta",
    "transactions": [
        {"amount": 50000, "type": "credit", "mode": "salary"},
        {"amount": 20000, "type": "debit", "mode": "cash"}
    ],
    "pep_flag": 0,
    "sanctions_flag": 0
}

# IMPORTANT LINE
result = graph.invoke(sample_input)

print("\n===== FINAL KYC RESULT =====\n")
print(result)
































# # STEP 1: OCR AGENT ONLY (first test)

# def ocr_agent(text):
#     data = {
#         "name": "",
#         "dob": "",
#         "id_number": ""
#     }

#     for line in text.split("\n"):
#         if "Name" in line:
#             data["name"] = line.split(":")[-1].strip()
#         if "DOB" in line:
#             data["dob"] = line.split(":")[-1].strip()
#         if "PAN" in line or "Aadhaar" in line:
#             data["id_number"] = line.split(":")[-1].strip()

#     return data


# # SAMPLE INPUT
# ocr_text = """
# Name: Aarav Mehta
# DOB: 12/06/1994
# PAN: ABCDE1234F
# """

# # RUN AGENT
# result = ocr_agent(ocr_text)

# # PRINT OUTPUT
# print("OCR RESULT:")
# print(result)