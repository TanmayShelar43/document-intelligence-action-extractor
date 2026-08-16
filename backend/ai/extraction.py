import json
import logging
import os
from typing import List, Optional, Any

from backend.database.models import DocumentPage
from backend.ai.gemini_client import generate_structured_content
from backend.ai.prompts import build_text_extraction_prompt, build_vision_extraction_prompt
from backend.ai.schemas import ExtractionResponse

logger = logging.getLogger(__name__)


def get_image_mime_type(file_path: str) -> str:
    """Helper to detect image MIME type from extension."""
    ext = file_path.rsplit(".", 1)[-1].lower()
    mime_map = {
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "webp": "image/webp",
        "heic": "image/heic",
        "pdf": "application/pdf"
    }
    return mime_map.get(ext, "image/jpeg")


def extract_information_from_pages(
    pages: List[DocumentPage],
    file_path: str,
    client_mock: Optional[Any] = None
) -> ExtractionResponse:
    """
    Extracts structured document intelligence from M4 DocumentPage list using Gemini:
    - Text pages (is_scanned=False) -> Gemini Text model
    - Scanned pages (is_scanned=True) -> Gemini Vision model
    Validates output through ExtractionResponse Pydantic schema before returning.
    """
    if not pages:
        raise ValueError("No document pages provided for AI extraction")

    text_content_blocks = []
    scanned_pages = []

    for page in pages:
        if not page.is_scanned and page.content:
            text_content_blocks.append(f"--- Page {page.page_number} ---\n{page.content}")
        elif page.is_scanned:
            scanned_pages.append(page)

    raw_json_str = None

    # Process text pages if present
    if text_content_blocks:
        full_text = "\n\n".join(text_content_blocks)
        prompt = build_text_extraction_prompt(full_text)
        raw_json_str = generate_structured_content(prompt_text=prompt, client=client_mock)
    elif scanned_pages:
        # Process scanned pages using Gemini Vision
        first_scanned_page = scanned_pages[0]
        prompt = build_vision_extraction_prompt(first_scanned_page.page_number)

        image_bytes = None
        mime_type = get_image_mime_type(file_path)
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                image_bytes = f.read()

        raw_json_str = generate_structured_content(
            prompt_text=prompt,
            image_bytes=image_bytes,
            mime_type=mime_type,
            client=client_mock
        )

    if not raw_json_str:
        raise ValueError("No extractable content or images found in document pages")

    # Clean JSON response if wrapped in codeblocks
    cleaned_json = raw_json_str.strip()
    if cleaned_json.startswith("```json"):
        cleaned_json = cleaned_json[7:]
    if cleaned_json.startswith("```"):
        cleaned_json = cleaned_json[3:]
    if cleaned_json.endswith("```"):
        cleaned_json = cleaned_json[:-3]
    cleaned_json = cleaned_json.strip()

    try:
        parsed_dict = json.loads(cleaned_json)
    except json.JSONDecodeError as err:
        logger.error(f"Failed to parse Gemini output as JSON: {err}. Output was:\n{raw_json_str}")
        raise ValueError("Gemini response was not valid JSON") from err

    # Validate output using Pydantic schema
    try:
        validated_response = ExtractionResponse.model_validate(parsed_dict)
        return validated_response
    except Exception as err:
        logger.error(f"Pydantic schema validation failed for Gemini extraction: {err}")
        raise ValueError(f"Gemini output failed Pydantic schema validation: {str(err)}") from err
