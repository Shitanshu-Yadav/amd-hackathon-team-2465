import pandas as pd
import re

from PIL import Image
import pytesseract

from models.schemas import OCRResult


def ocr_agent(customer_id):

    # ==========================
    # LOAD GROUND TRUTH
    # ==========================

    df = pd.read_csv(
        "data/pan_ground_truth.csv"
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
    # FIND RECORD
    # ==========================

    row = df[
        df["customer_id"]
        ==
        customer_id
    ]

    if row.empty:

        raise ValueError(
            f"customer_id {customer_id} not found"
        )

    row = row.iloc[0]

    image_path = str(
        row["image_path"]
    ).strip()

    # ==========================
    # LOAD IMAGE
    # ==========================

    try:

        image = Image.open(
            image_path
        )

    except Exception as e:

        raise FileNotFoundError(
            f"Unable to load image: {image_path}"
        ) from e

    # ==========================
    # OCR
    # ==========================

    text = pytesseract.image_to_string(
        image
    )

    print("\nIMAGE PATH\n")
    print(image_path)

    print("\nOCR TEXT\n")
    print(text)

    # ==========================
    # EXTRACT
    # ==========================

    name_match = re.search(
        r"Name[:\s]*(.+)",
        text,
        re.I
    )

    dob_match = re.search(
        r"DOB[:\-\s]*(.+)",
        text,
        re.I
    )

    pan_match = re.search(
        r"PAN[:\-\s]*([A-Z0-9]+)",
        text,
        re.I
    )

    name = (
        name_match.group(1)
        .strip()
        if name_match
        else ""
    )

    dob = (
        dob_match.group(1)
        .strip()
        if dob_match
        else ""
    )

    pan = (
        pan_match.group(1)
        .strip()
        .upper()
        if pan_match
        else ""
    )

    # ==========================
    # RETURN
    # ==========================

    return OCRResult(
        name=name,
        dob=dob,
        pan=pan
    )