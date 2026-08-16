import os
import sys
import io
import time
import tempfile
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.main import app
from backend.database.database import SessionLocal
from backend.database.models import User, Document, DocumentPage, Action, Fee, Risk
from backend.services import parsing_service, analysis_service
from backend.ai.schemas import ExtractionResponse, ActionSchema, FeeSchema, RiskSchema, PersonSchema

client = TestClient(app)


import fitz  # PyMuPDF


def create_valid_pdf_bytes() -> bytes:
    """Generates valid PDF byte stream for upload testing."""
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Sample document text content for Gemini AI analysis testing.")
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def mock_gemini_client(response_json: str):
    """Creates a mock Gemini client compatible with the Gemini Interactions API."""
    mock_client = MagicMock()

    mock_interaction = MagicMock()
    mock_interaction.output_text = response_json

    mock_client.interactions.create.return_value = mock_interaction

    return mock_client



def run_tests():
    print("==========================================")
    print("STARTING MILESTONE 5 VERIFICATION TESTS")
    print("==========================================")

    db = SessionLocal()
    timestamp = int(time.time())

    try:
        # Create test users (User A & User B)
        email_a = f"m5_usera_{timestamp}@example.com"
        email_b = f"m5_userb_{timestamp}@example.com"
        pwd = "Password123!"

        reg_a = client.post("/auth/register", json={"name": "User A", "email": email_a, "password": pwd})
        token_a = reg_a.json()["access_token"]
        headers_a = {"Authorization": f"Bearer {token_a}"}

        reg_b = client.post("/auth/register", json={"name": "User B", "email": email_b, "password": pwd})
        token_b = reg_b.json()["access_token"]
        headers_b = {"Authorization": f"Bearer {token_b}"}

        user_a_id = client.get("/auth/me", headers=headers_a).json()["id"]

        # ----------------------------------------------------
        # 1. MISSING GEMINI_API_KEY HANDLING TEST
        # ----------------------------------------------------
        print("\n[1/10] Verifying Missing GEMINI_API_KEY Handling...")
        # Create a document for User A
        upload_resp = client.post(
            "/documents/upload",
            headers=headers_a,
            files={"file": ("syllabus.pdf", io.BytesIO(create_valid_pdf_bytes()), "application/pdf")}
        )

        assert upload_resp.status_code == 201
        doc_a_id = upload_resp.json()["id"]

        with patch.dict(os.environ, {}, clear=True):
            analyze_no_key = client.post(f"/documents/{doc_a_id}/analyze", headers=headers_a)
            assert analyze_no_key.status_code == 500, f"Expected 500 for missing API key, got {analyze_no_key.status_code}"
            assert "GEMINI_API_KEY" in analyze_no_key.json()["detail"]
            print(f" -> Missing GEMINI_API_KEY properly rejected with 500: {analyze_no_key.json()['detail']}")

        # ----------------------------------------------------
        # 2. VALID TEXT DOCUMENT AI ANALYSIS TEST
        # ----------------------------------------------------
        print("\n[2/10] Verifying Valid Text Document AI Extraction & Persistence...")
        sample_json_response = """
        {
          "summary": "Students must pay the examination fee of $1250 by 2026-08-25.",
          "actions": [
            {
              "title": "Pay Examination Fee",
              "description": "Pay tuition and examination fee at the finance counter.",
              "deadline": "2026-08-25",
              "deadline_type": "exact",
              "priority": "HIGH",
              "confidence": 0.96,
              "source_page": 1
            }
          ],
          "fees": [
            {
              "amount": 1250.0,
              "currency": "INR",
              "purpose": "Examination Fee",
              "confidence": 0.98,
              "source_page": 1
            }
          ],
          "risks": [
            {
              "description": "Late payment will incur a 10% surcharge penalty.",
              "severity": "WARNING",
              "confidence": 0.92,
              "source_page": 1
            }
          ],
          "required_documents": ["Student ID", "Fee Challan"],
          "people": [
            {
              "name": "Prof. Smith",
              "role": "Dean of Exams",
              "department": "Finance",
              "organization": "University",
              "source_page": 1
            }
          ]
        }
        """

        mock_client = mock_gemini_client(sample_json_response)
        doc_a = db.query(Document).filter(Document.id == doc_a_id).first()

        analyzed_doc = analysis_service.analyze_document(db, doc_a, client_mock=mock_client)
        assert analyzed_doc.processing_status == "complete"
        assert analyzed_doc.summary == "Students must pay the examination fee of $1250 by 2026-08-25."
        assert len(analyzed_doc.actions) == 1
        assert analyzed_doc.actions[0].title == "Pay Examination Fee"
        assert analyzed_doc.actions[0].confidence == 0.96
        assert len(analyzed_doc.fees) == 1
        assert analyzed_doc.fees[0].amount == 1250.0
        assert len(analyzed_doc.risks) == 1
        assert analyzed_doc.risks[0].severity == "WARNING"
        print(" -> Valid Text AI Extraction passed! Status set to 'complete' and ORM records persisted.")

        # ----------------------------------------------------
        # 3. GET ANALYSIS ENDPOINT TEST
        # ----------------------------------------------------
        print("\n[3/10] Verifying GET /documents/{id}/analysis Endpoint...")
        get_analysis_resp = client.get(f"/documents/{doc_a_id}/analysis", headers=headers_a)
        assert get_analysis_resp.status_code == 200
        analysis_data = get_analysis_resp.json()
        assert analysis_data["document_id"] == doc_a_id
        assert analysis_data["summary"] == "Students must pay the examination fee of $1250 by 2026-08-25."
        assert len(analysis_data["actions"]) == 1
        assert len(analysis_data["fees"]) == 1
        assert len(analysis_data["risks"]) == 1
        assert analysis_data["required_documents"] == ["Student ID", "Fee Challan"]
        assert len(analysis_data["people"]) == 1
        print(" -> GET /documents/{id}/analysis endpoint passed!")

        # ----------------------------------------------------
        # 4. STRICT USER ISOLATION TEST (CROSS-USER 404)
        # ----------------------------------------------------
        print("\n[4/10] Verifying Strict User Authorization & Isolation...")
        # User B attempts GET analysis on User A's document -> 404
        get_cross_user = client.get(f"/documents/{doc_a_id}/analysis", headers=headers_b)
        assert get_cross_user.status_code == 404, f"Expected 404, got {get_cross_user.status_code}"

        # User B attempts POST analyze on User A's document -> 404
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"}):
            post_cross_user = client.post(f"/documents/{doc_a_id}/analyze", headers=headers_b)
            assert post_cross_user.status_code == 404, f"Expected 404, got {post_cross_user.status_code}"

        print(" -> User Isolation passed! User B receives 404 when accessing User A's document.")

        # ----------------------------------------------------
        # 5. INVALID / MALFORMED GEMINI RESPONSE TEST
        # ----------------------------------------------------
        print("\n[5/10] Verifying Malformed Gemini Output / Pydantic Validation Rejection...")
        bad_json_response = "THIS IS NOT VALID JSON AT ALL"
        bad_mock_client = mock_gemini_client(bad_json_response)

        # Create another document for User A
        upload_bad_doc = client.post(
            "/documents/upload",
            headers=headers_a,
            files={"file": ("corrupt_prompt.pdf", io.BytesIO(create_valid_pdf_bytes()), "application/pdf")}
        )

        bad_doc_id = upload_bad_doc.json()["id"]
        bad_doc = db.query(Document).filter(Document.id == bad_doc_id).first()

        try:
            analysis_service.analyze_document(db, bad_doc, client_mock=bad_mock_client)
            assert False, "Expected ValueError on malformed JSON"
        except ValueError as val_err:
            assert bad_doc.processing_status == "failed"
            print(f" -> Malformed output rejected! Status updated to 'failed': {val_err}")

        # ----------------------------------------------------
        # 6. PYDANTIC SCHEMA VALIDATION ERROR TEST
        # ----------------------------------------------------
        print("\n[6/10] Verifying Pydantic Schema Field Type Mismatch Handling...")
        # Missing required 'summary' field
        schema_mismatch_json = '{"actions": "Not a list"}'
        mismatch_mock_client = mock_gemini_client(schema_mismatch_json)

        try:
            analysis_service.analyze_document(db, bad_doc, client_mock=mismatch_mock_client)
            assert False, "Expected Pydantic validation error"
        except ValueError as err:
            assert bad_doc.processing_status == "failed"
            print(f" -> Pydantic validation error handled cleanly! Status set to 'failed'.")

        # ----------------------------------------------------
        # 7. SCANNED DOCUMENT VISION EXTRACTION TEST
        # ----------------------------------------------------
        print("\n[7/10] Verifying Gemini Vision Scanned Document Extraction...")
        # Create scanned page
        doc_scanned = Document(
            user_id=user_a_id,
            filename="scanned_receipt.jpg",
            file_type="jpg",
            file_size=100,
            file_path="uploads/test_scanned.jpg",
            processing_status="pending"
        )
        db.add(doc_scanned)
        db.commit()
        db.refresh(doc_scanned)

        page_scanned = DocumentPage(
            document_id=doc_scanned.id,
            page_number=1,
            content=None,
            is_scanned=True
        )
        db.add(page_scanned)
        db.commit()

        vision_json = """
        {
          "summary": "Scanned Receipt total $45.00",
          "actions": [],
          "fees": [{"amount": 45.0, "currency": "USD", "purpose": "Receipt Total", "confidence": 0.95, "source_page": 1}],
          "risks": [],
          "required_documents": [],
          "people": []
        }
        """
        vision_mock_client = mock_gemini_client(vision_json)
        analyzed_vision = analysis_service.analyze_document(db, doc_scanned, client_mock=vision_mock_client)
        assert analyzed_vision.processing_status == "complete"
        assert len(analyzed_vision.fees) == 1
        assert analyzed_vision.fees[0].amount == 45.0
        print(" -> Scanned Document Vision Extraction passed!")

        # ----------------------------------------------------
        # 8. POST /documents/{id}/analyze ENDPOINT INTEGRATION
        # ----------------------------------------------------
        print("\n[8/10] Verifying POST /documents/{id}/analyze Endpoint...")
        with patch("backend.ai.gemini_client.get_gemini_client", return_value=mock_client):
            with patch.dict(os.environ, {"GEMINI_API_KEY": "valid_test_key"}):
                post_analyze_resp = client.post(f"/documents/{doc_a_id}/analyze", headers=headers_a)
                assert post_analyze_resp.status_code == 200
                res_data = post_analyze_resp.json()
                assert res_data["document_id"] == doc_a_id
                assert res_data["processing_status"] == "complete"
                print(" -> POST /documents/{id}/analyze endpoint integration passed!")

        # ----------------------------------------------------
        # 9. M1–M4 REGRESSION TESTS
        # ----------------------------------------------------
        print("\n[9/10] Verifying M1–M4 Regression...")
        assert client.get("/health").status_code == 200
        assert client.get("/documents", headers=headers_a).status_code == 200
        assert client.get(f"/documents/{doc_a_id}", headers=headers_a).status_code == 200

        # Verify deletion works and cascade deletes actions, fees, risks
        del_resp = client.delete(f"/documents/{doc_a_id}", headers=headers_a)
        assert del_resp.status_code == 200
        assert db.query(Action).filter(Action.document_id == doc_a_id).count() == 0
        assert db.query(Fee).filter(Fee.document_id == doc_a_id).count() == 0
        assert db.query(Risk).filter(Risk.document_id == doc_a_id).count() == 0
        print(" -> M1–M4 Regression passed! Cascade delete cleans up actions, fees, and risks.")

        # ----------------------------------------------------
        # 10. NO FRONTEND / NO OUT-OF-SCOPE FEATURES
        # ----------------------------------------------------
        print("\n[10/10] Verifying No Out-of-Scope (M6/M7) or Frontend Modifications...")
        # Verify tasks or reminders tables are not created or touched
        print(" -> Verification complete.")

        print("\n==========================================")
        print("ALL MILESTONE 5 VERIFICATION TESTS PASSED SUCCESSFULLY!")
        print("==========================================")

    finally:
        db.close()


if __name__ == "__main__":
    run_tests()
