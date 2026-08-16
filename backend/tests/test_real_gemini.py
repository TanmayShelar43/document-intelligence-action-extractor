import os
import sys
import fitz  # PyMuPDF

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Helper to load .env if present without printing key
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("GEMINI_API_KEY="):
                key_val = line.split("=", 1)[1].strip("\"'")
                if key_val and "GEMINI_API_KEY" not in os.environ:
                    os.environ["GEMINI_API_KEY"] = key_val

from backend.database.database import SessionLocal
from backend.database.models import User, Document, DocumentPage, Action, Fee, Risk
from backend.services import parsing_service, analysis_service
from backend.ai.schemas import ExtractionResponse


def create_real_notice_pdf() -> str:
    """Generates a sample notice PDF for real Gemini extraction test."""
    notice_text = (
        "ABC UNIVERSITY ADMISSION & EXAMINATION NOTICE 2026\n\n"
        "1. All students must submit the completed registration form by 30 August 2026.\n"
        "2. An examination fee of 1500 INR must be paid at the finance office.\n"
        "3. Late submission after 30 August 2026 will incur a penalty of 500 INR.\n"
        "4. Required documents: Aadhaar Card, Previous Semester Marksheet.\n"
        "5. Contact Person: Dr. Rahul Sharma, Dean of Examinations.\n"
    )
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), notice_text)
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "real_notice_sample.pdf")
    doc.save(file_path)
    doc.close()
    return file_path


def run_real_gemini_test():
    print("==========================================")
    print("RUNNING REAL GEMINI API INTEGRATION TEST")
    print("==========================================")

    api_key_set = bool(os.getenv("GEMINI_API_KEY"))
    if not api_key_set:
        print("[ERROR] GEMINI_API_KEY is not set in environment or backend/.env!")
        sys.exit(1)

    print("[1/5] GEMINI_API_KEY configuration verified (Key is set in environment).")

    db = SessionLocal()
    pdf_path = create_real_notice_pdf()

    try:
        # Create test user in DB
        user = User(
            name="Real Gemini Tester",
            email=f"gemini_real_test_{os.getpid()}@example.com",
            password_hash="secret_pwd"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # Create Document in DB
        doc = Document(
            user_id=user.id,
            filename="notice_2026.pdf",
            file_type="pdf",
            file_size=os.path.getsize(pdf_path),
            file_path=pdf_path,
            processing_status="pending"
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)

        print("[2/5] Running M4 parsing service to extract page text...")
        pages = parsing_service.parse_document(db, doc)
        assert len(pages) > 0, "M4 Parsing failed to extract text"
        print(f" -> M4 parsed {len(pages)} page(s) into document_pages.")

        print("[3/5] Invoking REAL Gemini API model (gemini-2.5-flash)...")
        # Call real Gemini extraction via analysis_service
        analyzed_doc = analysis_service.analyze_document(db, doc)

        assert analyzed_doc.processing_status == "complete", f"Processing status expected 'complete', got {analyzed_doc.processing_status}"
        print(" -> Real Gemini API call succeeded! Returned processing status: 'complete'.")

        print("[4/5] Verifying Pydantic schema validation...")
        assert analyzed_doc.summary is not None and len(analyzed_doc.summary) > 0
        print(f" -> Summary extracted: \"{analyzed_doc.summary}\"")

        print("[5/5] Verifying PostgreSQL persistence of AI extractions...")
        actions = db.query(Action).filter(Action.document_id == doc.id).all()
        fees = db.query(Fee).filter(Fee.document_id == doc.id).all()
        risks = db.query(Risk).filter(Risk.document_id == doc.id).all()

        print(f" -> Actions persisted in DB: {len(actions)}")
        for act in actions:
            print(f"    * Action: {act.title} (Deadline: {act.deadline}, Priority: {act.priority}, Confidence: {act.confidence})")

        print(f" -> Fees persisted in DB: {len(fees)}")
        for f in fees:
            print(f"    * Fee: {f.amount} {f.currency} - {f.purpose} (Confidence: {f.confidence})")

        print(f" -> Risks persisted in DB: {len(risks)}")
        for r in risks:
            print(f"    * Risk: {r.description} (Severity: {r.severity}, Confidence: {r.confidence})")

        print(f" -> Required Documents in DB: {analyzed_doc.required_documents}")
        print(f" -> People in DB: {analyzed_doc.people}")

        assert len(actions) > 0 or len(fees) > 0 or len(risks) > 0, "At least one structured item should be extracted"
        print("\n==========================================")
        print("REAL GEMINI API INTEGRATION TEST PASSED SUCCESSFULLY!")
        print("==========================================")

    finally:
        db.close()
        if os.path.exists(pdf_path):
            try:
                os.remove(pdf_path)
            except OSError:
                pass


if __name__ == "__main__":
    run_real_gemini_test()
