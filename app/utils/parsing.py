import fitz
import re
from fastapi import UploadFile,File
from typing import Annotated

def pdf_bytes_to_text(pdf_bytes:bytes)->str:
    text = ""
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text