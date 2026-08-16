import os
import sys
import io
import time

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi.testclient import TestClient
from backend.main import app
from backend.database.database import SessionLocal
from backend.database.models import User, Document


client = TestClient(app)


def run_tests():
    print("==========================================")
    print("STARTING MILESTONE 3 VERIFICATION TESTS")
    print("==========================================")

    timestamp = int(time.time())

    # ----------------------------------------------------
    # 1. VERIFY M1 & M2 ENDPOINTS
    # ----------------------------------------------------
    print("\n[1/8] Verifying M1 Health Check...")
    resp = client.get("/health")
    assert resp.status_code == 200, f"Health check failed: {resp.text}"
    assert resp.json() == {"status": "ok"}
    print(" -> GET /health passed!")

    print("\n[2/8] Verifying M2 User Registration & Login (User A & User B)...")
    email_a = f"usera_{timestamp}@example.com"
    email_b = f"userb_{timestamp}@example.com"
    pwd = "SecurePassword123!"

    # Register User A
    resp_reg_a = client.post("/auth/register", json={
        "name": "User Alpha",
        "email": email_a,
        "password": pwd
    })
    assert resp_reg_a.status_code == 201, f"User A reg failed: {resp_reg_a.text}"
    token_a = resp_reg_a.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # Register User B
    resp_reg_b = client.post("/auth/register", json={
        "name": "User Beta",
        "email": email_b,
        "password": pwd
    })
    assert resp_reg_b.status_code == 201, f"User B reg failed: {resp_reg_b.text}"
    token_b = resp_reg_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # Test /auth/me for User A
    resp_me = client.get("/auth/me", headers=headers_a)
    assert resp_me.status_code == 200
    user_a_id = resp_me.json()["id"]
    print(f" -> Registration & Auth passed! User A ID: {user_a_id}")

    # ----------------------------------------------------
    # 2. VERIFY VALID DOCUMENT UPLOADS (M3)
    # ----------------------------------------------------
    print("\n[3/8] Verifying Valid Document Uploads (PDF & PNG)...")
    pdf_content = b"%PDF-1.4 sample pdf content for testing document intelligence"
    resp_upload_pdf = client.post(
        "/documents/upload",
        headers=headers_a,
        files={"file": ("sample_report.pdf", io.BytesIO(pdf_content), "application/pdf")}
    )
    assert resp_upload_pdf.status_code == 201, f"PDF upload failed: {resp_upload_pdf.text}"
    doc_a_pdf = resp_upload_pdf.json()
    assert doc_a_pdf["filename"] == "sample_report.pdf"
    assert doc_a_pdf["file_type"] == "pdf"
    assert doc_a_pdf["file_size"] == len(pdf_content)
    assert doc_a_pdf["processing_status"] == "pending"
    assert os.path.exists(doc_a_pdf["file_path"]), f"Physical file not found on disk at {doc_a_pdf['file_path']}"
    print(f" -> PDF Upload passed! Saved at: {doc_a_pdf['file_path']}")

    png_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR sample image data"
    resp_upload_png = client.post(
        "/documents/upload",
        headers=headers_a,
        files={"file": ("invoice_scan.png", io.BytesIO(png_content), "image/png")}
    )
    assert resp_upload_png.status_code == 201, f"PNG upload failed: {resp_upload_png.text}"
    doc_a_png = resp_upload_png.json()
    assert doc_a_png["file_type"] == "png"
    assert os.path.exists(doc_a_png["file_path"])
    print(f" -> PNG Upload passed! Saved at: {doc_a_png['file_path']}")

    # ----------------------------------------------------
    # 3. VERIFY INVALID FILE REJECTIONS (M3)
    # ----------------------------------------------------
    print("\n[4/8] Verifying Invalid File Extensions and Empty File Rejections...")
    # Unsupported extension (.exe)
    resp_bad_ext = client.post(
        "/documents/upload",
        headers=headers_a,
        files={"file": ("malicious.exe", io.BytesIO(b"binary data"), "application/octet-stream")}
    )
    assert resp_bad_ext.status_code == 400, f"Expected 400 for .exe upload, got {resp_bad_ext.status_code}"
    print(f" -> Unsupported extension (.exe) properly rejected: {resp_bad_ext.json()['detail']}")

    # Empty 0-byte file
    resp_empty = client.post(
        "/documents/upload",
        headers=headers_a,
        files={"file": ("empty.pdf", io.BytesIO(b""), "application/pdf")}
    )
    assert resp_empty.status_code == 400, f"Expected 400 for empty upload, got {resp_empty.status_code}"
    print(f" -> Empty file properly rejected: {resp_empty.json()['detail']}")

    # ----------------------------------------------------
    # 4. VERIFY DOCUMENT LISTING & RETRIEVAL (M3)
    # ----------------------------------------------------
    print("\n[5/8] Verifying Document Listing and Retrieval for User A...")
    resp_list = client.get("/documents", headers=headers_a)
    assert resp_list.status_code == 200
    docs_list = resp_list.json()
    assert len(docs_list) == 2, f"Expected 2 documents for User A, found {len(docs_list)}"
    print(f" -> List /documents passed! Found {len(docs_list)} documents.")

    doc_id_pdf = doc_a_pdf["id"]
    resp_get_pdf = client.get(f"/documents/{doc_id_pdf}", headers=headers_a)
    assert resp_get_pdf.status_code == 200
    assert resp_get_pdf.json()["id"] == doc_id_pdf
    print(f" -> Get /documents/{doc_id_pdf} passed!")

    # ----------------------------------------------------
    # 5. VERIFY USER A / USER B AUTHORIZATION ISOLATION (M3)
    # ----------------------------------------------------
    print("\n[6/8] Verifying Strict User Authorization & Cross-User Isolation...")
    # User B lists documents -> should be empty
    resp_list_b = client.get("/documents", headers=headers_b)
    assert resp_list_b.status_code == 200
    assert len(resp_list_b.json()) == 0, "User B should see 0 documents"

    # User B attempts to access User A's document -> 404 Not Found
    resp_b_get_a_doc = client.get(f"/documents/{doc_id_pdf}", headers=headers_b)
    assert resp_b_get_a_doc.status_code == 404, f"Expected 404 when User B accesses User A's doc, got {resp_b_get_a_doc.status_code}"

    # User B attempts to delete User A's document -> 404 Not Found
    resp_b_del_a_doc = client.delete(f"/documents/{doc_id_pdf}", headers=headers_b)
    assert resp_b_del_a_doc.status_code == 404, f"Expected 404 when User B deletes User A's doc, got {resp_b_del_a_doc.status_code}"
    print(" -> Strict User Isolation passed! User B cannot read or delete User A's documents.")

    # ----------------------------------------------------
    # 6. VERIFY DOCUMENT DELETION (DB + FILESYSTEM) (M3)
    # ----------------------------------------------------
    print("\n[7/8] Verifying Document Deletion (File System & Database cleanup)...")
    file_path_to_delete = doc_a_pdf["file_path"]
    assert os.path.exists(file_path_to_delete), "File must exist before deletion test"

    resp_del = client.delete(f"/documents/{doc_id_pdf}", headers=headers_a)
    assert resp_del.status_code == 200, f"Delete failed: {resp_del.text}"
    assert resp_del.json()["id"] == doc_id_pdf

    # Verify physical file on disk is removed
    assert not os.path.exists(file_path_to_delete), f"Physical file was NOT removed from disk! {file_path_to_delete}"

    # Verify DB record is removed
    resp_get_deleted = client.get(f"/documents/{doc_id_pdf}", headers=headers_a)
    assert resp_get_deleted.status_code == 404
    print(" -> Document Deletion passed! Physical file and database record successfully purged.")

    # ----------------------------------------------------
    # 7. UNAUTHENTICATED ACCESS BLOCKED
    # ----------------------------------------------------
    print("\n[8/8] Verifying Unauthenticated Requests block access...")
    assert client.get("/documents").status_code in (401, 403)
    assert client.post("/documents/upload").status_code in (401, 403)
    assert client.get(f"/documents/{doc_a_png['id']}").status_code in (401, 403)
    assert client.delete(f"/documents/{doc_a_png['id']}").status_code in (401, 403)
    print(" -> Unauthenticated requests properly rejected with 401/403!")


    print("\n==========================================")
    print("ALL MILESTONE 3 VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("==========================================")


if __name__ == "__main__":
    run_tests()
