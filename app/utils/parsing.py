import fitz

def pdf_bytes_to_text(pdf_bytes:bytes)->str:
    """
    Converts PDF bytes into a single string of text.
    """
    try:
        text = ""
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text("text",sort=True) + " "
        return text.strip()
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return ""