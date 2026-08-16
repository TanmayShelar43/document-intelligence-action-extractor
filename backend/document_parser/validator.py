import os


def validate_document_file(file_path: str) -> None:
    """
    Validates physical document file existence and non-zero size.
    Raises FileNotFoundError or ValueError if invalid.
    """
    if not file_path or not os.path.exists(file_path):
        raise FileNotFoundError(f"Document file does not exist at path: {file_path}")

    if os.path.getsize(file_path) == 0:
        raise ValueError(f"Document file is empty (0 bytes): {file_path}")
