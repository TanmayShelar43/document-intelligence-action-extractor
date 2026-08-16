"""
Prompts for Gemini Document Intelligence extraction.
"""

EXTRACTION_SYSTEM_PROMPT = """
You are an expert Document Intelligence AI.
Analyze the provided document text/image and extract structured action items, deadlines, fees, risks, required documents, people, and a concise summary.

STRICT SAFETY RULES:
1. Do NOT invent exact dates or fabricate missing information. If a deadline is relative or conditional (e.g. "within 15 days of admission"), mark deadline_type as "relative" or "conditional".
2. Assign a floating-point confidence score between 0.00 and 1.00 for every extracted item based on clarity.
3. Return ONLY valid JSON matching this exact JSON schema:

{
  "summary": "Short useful summary of the document",
  "actions": [
    {
      "title": "Action title",
      "description": "Clear description",
      "deadline": "2026-08-23 or relative description",
      "deadline_type": "exact | range | relative | conditional",
      "priority": "HIGH | MEDIUM | LOW",
      "confidence": 0.95,
      "source_page": 1
    }
  ],
  "fees": [
    {
      "amount": 1250.0,
      "currency": "INR",
      "purpose": "Fee purpose",
      "confidence": 0.98,
      "source_page": 1
    }
  ],
  "risks": [
    {
      "description": "Risk or penalty description",
      "severity": "WARNING | CRITICAL",
      "confidence": 0.90,
      "source_page": 1
    }
  ],
  "required_documents": [
    "Aadhaar Card",
    "Income Certificate"
  ],
  "people": [
    {
      "name": "Dr. Rahul Sharma",
      "role": "Contact Person",
      "department": "Examination Department",
      "organization": "University",
      "source_page": 1
    }
  ]
}
"""


def build_text_extraction_prompt(document_text: str) -> str:
    """Builds prompt for text-based document analysis."""
    return f"{EXTRACTION_SYSTEM_PROMPT}\n\nDocument Text Content:\n\"\"\"\n{document_text}\n\"\"\""


def build_vision_extraction_prompt(page_number: int) -> str:
    """Builds prompt for image/scanned-based document analysis via Gemini Vision."""
    return f"{EXTRACTION_SYSTEM_PROMPT}\n\nAnalyze this scanned document page (Page {page_number}) and extract structured information."
