from app.utils import score_label
from app.pipeline import cleaning_pipeline,extraction_pipeline,scoring_pipeline

# parsing,
def analyze_resume_bytes(pdf_bytes:bytes)->dict:
    clean_text = cleaning_pipeline(pdf_bytes)
    extracted_data = extraction_pipeline(clean_text)
    overall_score = scoring_pipeline(extracted_data)
    score_labelling = score_label(overall_score)
    return {
        "score":overall_score,
        "label":score_labelling,
        "extracted_data":extracted_data
    }