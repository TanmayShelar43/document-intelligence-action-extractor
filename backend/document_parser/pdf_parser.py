from typing import List, Dict, Any, Optional
import fitz  # PyMuPDF


def parse_pdf(file_path: str) -> List[Dict[str, Any]]:
    """
    Parses a PDF document using PyMuPDF (fitz).
    Inspects each page (1-indexed):
    - If text exists, extracts text, sets content=text, is_scanned=False.
    - If no text (scanned PDF page), sets content=None, is_scanned=True.
    Returns list of page result dictionaries.
    """
    doc = fitz.open(file_path)
    pages_data = []

    try:
        for page_idx in range(len(doc)):
            page_num = page_idx + 1
            page = doc[page_idx]
            extracted_text = page.get_text("text").strip()

            if extracted_text:
                content: Optional[str] = extracted_text
                is_scanned = False
            else:
                content = None
                is_scanned = True

            pages_data.append({
                "page_number": page_num,
                "content": content,
                "is_scanned": is_scanned
            })
    finally:
        doc.close()

    return pages_data
