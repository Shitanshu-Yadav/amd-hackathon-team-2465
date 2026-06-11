import json
import re

from models.schemas import OCRResult
from utils.llm_loader import llm


def extract_json(text):

    matches = re.findall(
        r'\{.*?\}',
        text,
        re.DOTALL
    )

    for item in matches:

        try:
            return json.loads(item)

        except:
            pass

    return None


def ocr_agent(document_text):

    prompt = f"""
Extract customer details from the document.

Document:

{document_text}

Return JSON only.
"""

    response = llm(
        prompt,
        max_new_tokens=100,
        do_sample=False
    )[0]["generated_text"]

    print(response)

    # fallback extraction

    name = re.search(
        r"Name:\s*(.*)",
        document_text
    )

    dob = re.search(
        r"DOB:\s*(.*)",
        document_text
    )

    pan = re.search(
        r"PAN:\s*(.*)",
        document_text
    )

    return OCRResult(
        name=name.group(1).strip(),
        dob=dob.group(1).strip(),
        pan=pan.group(1).strip()
    )