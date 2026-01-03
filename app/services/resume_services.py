
from app.services.pipeline import cleaning_pipeline,extraction_pipeline

# parsing,
def analyze_resume_bytes(pdf_bytes:bytes)->dict:
    clean_text = cleaning_pipeline(pdf_bytes)
    extracted_data = extraction_pipeline(clean_text)
    return extracted_data