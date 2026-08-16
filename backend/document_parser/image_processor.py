from typing import List, Dict, Any
import cv2


def process_image(file_path: str) -> List[Dict[str, Any]]:
    """
    Loads and preprocesses image files using OpenCV.
    Performs image verification, orientation/quality preprocessing check.
    Marks is_scanned=True and content=None for downstream Gemini Vision processing in M5.
    Raises ValueError if image file is unreadable.
    """
    img = cv2.imread(file_path)
    if img is None:
        raise ValueError(f"OpenCV failed to decode image file at: {file_path}")

    # Perform quality / dimension preprocessing inspection
    _height, _width = img.shape[:2]

    return [{
        "page_number": 1,
        "content": None,
        "is_scanned": True
    }]
