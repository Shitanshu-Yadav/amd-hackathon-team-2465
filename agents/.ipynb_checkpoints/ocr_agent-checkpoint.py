from models.schemas import OCROutput

def ocr_agent(text: str) -> OCROutput:
    data = {"name": "", "dob": "", "id_number": ""}

    for line in text.split("\n"):
        if "Name" in line:
            data["name"] = line.split(":")[-1].strip()
        elif "DOB" in line:
            data["dob"] = line.split(":")[-1].strip()
        elif "PAN" in line:
            data["id_number"] = line.split(":")[-1].strip()

    return OCROutput(**data)