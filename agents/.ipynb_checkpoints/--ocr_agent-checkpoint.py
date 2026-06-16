import pandas as pd
import re

from PIL import Image
import pytesseract

from models.schemas import OCRResult


def ocr_agent(sno):

    # ==========================
    # READ CSV
    # ==========================

    df = pd.read_csv(
        "data/pan_ground_truth.csv"
    )


    # ==========================
    # FIND IMAGE
    # ==========================

    row = df.loc[
        df["sno"] == sno
    ]


    if len(row) == 0:

        raise ValueError(
            f"sno {sno} not found"
        )


    image_path = row.iloc[0][
        "image_path"
    ]


    print("\nIMAGE PATH\n")
    print(image_path)


    # ==========================
    # OPEN IMAGE
    # ==========================

    image = Image.open(
        str(image_path)
    )


    # ==========================
    # OCR
    # ==========================

    text = pytesseract.image_to_string(
        image
    )


    print("\nOCR TEXT\n")
    print(text)


    # ==========================
    # EXTRACT FIELDS
    # ==========================

    name = re.search(
        r"Name[:\s]*(.+)",
        text,
        re.I
    )


    dob = re.search(
        r"DOB[:\-\s]*(.+)",
        text,
        re.I
    )


    pan = re.search(
        r"PAN[:\-\s]*([A-Z0-9]+)",
        text,
        re.I
    )


    return OCRResult(

        name=
        (
            name.group(1).strip()
            if name
            else ""
        ),

        dob=
        (
            dob.group(1).strip()
            if dob
            else ""
        ),

        pan=
        (
            pan.group(1).strip()
            if pan
            else ""
        )

    )