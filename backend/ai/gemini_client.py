
import base64
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from google import genai


# Load backend/.env
load_dotenv(Path(__file__).resolve().parents[1] / ".env")


def get_gemini_client() -> genai.Client:
    """
    Returns an initialized Google Gen AI client using GEMINI_API_KEY.
    """
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or not api_key.strip():
        raise ValueError(
            "GEMINI_API_KEY environment variable is missing"
        )

    return genai.Client(
        api_key=api_key.strip()
    )


def generate_structured_content(
    prompt_text: str,
    image_bytes: Optional[bytes] = None,
    mime_type: Optional[str] = None,
    client: Optional[genai.Client] = None
) -> str:
    """
    Generates content using the Gemini Interactions API.

    Supports:
    - Text input
    - Multimodal image input

    Returns the generated response as text.
    """

    if client is None:
        client = get_gemini_client()

    # ---------------------------------------------------------
    # MULTIMODAL INPUT
    # ---------------------------------------------------------
    if image_bytes and mime_type:

        # Gemini Interactions API expects inline image data
        # as a Base64-encoded UTF-8 string, not raw bytes.
        image_base64 = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        input_content = [
            {
                "type": "text",
                "text": prompt_text
            },
            {
                "type": "image",
                "data": image_base64,
                "mime_type": mime_type
            }
        ]

    # ---------------------------------------------------------
    # TEXT INPUT
    # ---------------------------------------------------------
    else:
        input_content = prompt_text

    # ---------------------------------------------------------
    # GEMINI INTERACTION
    # ---------------------------------------------------------
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=input_content
    )

    if not interaction or not interaction.output_text:
        raise ValueError(
            "Empty response received from Gemini API"
        )

    return interaction.output_text

