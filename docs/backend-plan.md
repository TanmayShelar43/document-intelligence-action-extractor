# Document Intelligence & Action Extractor
# Backend Implementation Plan

> This document defines the complete backend responsibility for the backend developer.
>
> The locked architecture in `docs/architecture.md` is the source of truth.
> This document does NOT replace the architecture.
> It converts the architecture into an executable backend task plan.

---

# 1. Backend Ownership

The backend developer is responsible for the complete Python/FastAPI backend.

## Backend Technologies

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT
- bcrypt
- PyMuPDF
- python-docx
- OpenCV
- Gemini API
- Pydantic
- Firebase Admin SDK
- APScheduler

## Backend Responsibilities

The backend developer owns:

1. FastAPI application
2. REST APIs
3. Authentication
4. PostgreSQL database
5. SQLAlchemy models
6. Document upload/storage
7. Document parsing
8. Gemini integration
9. AI extraction
10. Pydantic validation
11. Confidence/safety rules
12. Task management APIs
13. Reminder APIs
14. FCM backend integration
15. Notification scheduler
16. Notification preferences
17. Backend security
18. API documentation/testing

---

# 2. Backend Folder Structure

The backend must follow the architecture:

backend/
│
├── main.py
│
├── api/
│   ├── auth.py
│   ├── documents.py
│   ├── analysis.py
│   ├── tasks.py
│   └── reminders.py
│
├── document_parser/
│   ├── pdf_parser.py
│   ├── docx_parser.py
│   ├── image_processor.py
│   └── validator.py
│
├── ai/
│   ├── gemini_client.py
│   ├── prompts.py
│   ├── extraction.py
│   └── schemas.py
│
├── database/
│   ├── models.py
│   └── database.py
│
├── services/
│   ├── document_service.py
│   ├── task_service.py
│   └── reminder_service.py
│
└── requirements.txt

Additional folders/files may be added only when required by implementation.

Do not unnecessarily redesign the architecture.

---

# 3. Git Branch

Backend development happens only on:

backend

Create it using:

git checkout -b backend

Push:

git push -u origin backend

Do not directly develop backend features on `main`.

---

# 4. Core Rule

The backend developer must follow this order:

M1 → M2 → M3 → M4 → M5 → M6 → M7 → M8 → M9 → M10

Do not implement future milestone functionality early unless explicitly required to unblock the current milestone.

Every milestone must:

1. Implement only its defined scope.
2. Run successfully.
3. Be tested.
4. Be committed.
5. Be pushed to the backend branch.

---

# 5. MILESTONE 1 — Backend Skeleton

## Goal

Create the minimal FastAPI backend.

## Tasks

Create:

backend/
├── main.py
└── requirements.txt

requirements.txt:

- fastapi
- uvicorn

main.py must expose:

GET /health

Expected response:

{
  "status": "ok"
}

## Run Test

Run the FastAPI server.

Verify:

GET /health

returns:

{
  "status": "ok"
}

## DO NOT IMPLEMENT

- PostgreSQL
- JWT
- Authentication
- Gemini
- Document upload
- AI
- Tasks
- Reminders
- FCM

## Completion Criteria

M1 backend is complete when:

- FastAPI starts successfully
- `/health` works
- No unnecessary dependencies are installed
- Code is committed
- Code is pushed to `backend`

Commit:

git add backend/
git commit -m "feat: add FastAPI backend skeleton"
git push

---

# 6. MILESTONE 2 — Database & Authentication

## Goal

Implement user authentication using PostgreSQL, SQLAlchemy, JWT and bcrypt.

## Install

Add:

- sqlalchemy
- psycopg2-binary
- python-jose[cryptography]
- passlib[bcrypt]
- python-multipart

## Create

database/database.py
database/models.py
api/auth.py

## Database

Create:

users

Fields:

- id
- name
- email
- password_hash
- created_at

## APIs

POST /auth/register

POST /auth/login

GET /auth/me

## Registration

Flow:

request
→ validate input
→ check email uniqueness
→ hash password
→ store user
→ generate JWT
→ return token

## Login

Flow:

request
→ find user
→ verify bcrypt password
→ generate JWT
→ return token

## JWT

Implement authentication dependency/middleware.

Protected endpoints must obtain:

user_id

from the JWT.

## Security

Never:

- store plaintext passwords
- hardcode JWT secret
- return password hash
- trust user_id sent from request body

## Completion Criteria

- Registration works
- Login works
- Wrong password rejected
- `/auth/me` works with JWT
- `/auth/me` rejects missing JWT
- PostgreSQL stores users
- Passwords are hashed

---

# 7. MILESTONE 3 — Document Upload & Storage

## Goal

Allow authenticated users to upload documents.

## Create

api/documents.py

services/document_service.py

Update:

database/models.py

## Database

Create:

documents

Fields:

- id
- user_id
- filename
- file_type
- file_size
- file_path
- processing_status
- uploaded_at

## Supported Types

- pdf
- doc
- docx
- jpg
- jpeg
- png
- webp
- heic

## APIs

POST /documents/upload

GET /documents

GET /documents/{id}

DELETE /documents/{id}

## Security

Every document query must belong to:

JWT user_id

A user must never access another user's document.

## Storage

Store uploaded files on backend filesystem.

Do not use cloud storage for MVP.

## Completion Criteria

- PDF upload works
- Image upload works
- Metadata saved
- File saved
- Document list works
- Document deletion works
- Unsupported file rejected
- Cross-user access blocked

---

# 8. MILESTONE 4 — Document Parsers

## Goal

Convert uploaded documents into content ready for Gemini.

## Install

- pymupdf
- python-docx
- opencv-python

## Create

document_parser/validator.py

document_parser/pdf_parser.py

document_parser/docx_parser.py

document_parser/image_processor.py

## PDF

Use PyMuPDF.

For every page:

1. Inspect text content.
2. If text exists:
   - extract text.
3. If page is scanned:
   - render page to image.
4. Mark scanned status.

## DOC/DOCX

Use python-docx.

Extract:

- paragraphs
- headings
- tables

## Images

Use OpenCV.

Perform:

- orientation correction
- quality preprocessing

Do NOT use:

- Tesseract
- ML Kit
- another OCR engine

## Database

Create:

document_pages

Fields:

- id
- document_id
- page_number
- content
- is_scanned

## Completion Criteria

- Text PDF parsed
- Scanned PDF detected
- Scanned pages rendered
- DOCX parsed
- Tables extracted
- Images preprocessed
- document_pages populated

---

# 9. MILESTONE 5 — Gemini Integration

## Goal

Connect Gemini to the backend and extract structured information.

## IMPORTANT

Before implementation:

Verify the current official Gemini Python SDK.

Do not blindly use:

google-generativeai

or any old package.

Use the currently appropriate official SDK.

## Create

ai/gemini_client.py

ai/prompts.py

ai/extraction.py

ai/schemas.py

## Gemini Responsibilities

Gemini extracts:

- summary
- actions
- deadlines
- fees
- required documents
- people
- risks
- confidence
- source page

## Input

Text:

document page text
→ Gemini text input

Scanned/image:

page image
→ Gemini Vision

## Output

Gemini must return structured JSON.

Never store raw Gemini output directly.

## Pydantic

Validate every Gemini response using Pydantic.

Create schemas:

- ExtractionResponse
- ActionSchema
- FeeSchema
- RiskSchema
- PersonSchema
- RequiredDocumentSchema

Enums:

- DeadlineType
- Priority
- Severity

## Confidence

>= 0.85

HIGH

0.60–0.84

MEDIUM

< 0.60

NEEDS VERIFICATION

## Database

Create:

actions
fees
risks

## APIs

POST /documents/{id}/analyze

GET /documents/{id}/analysis

## Safety

Gemini must never:

- invent exact dates
- fabricate missing information
- return uncontrolled prose for storage

## API Key

Gemini key must come from environment variable.

Never:

- hardcode API key
- put API key in Flutter
- commit `.env`

## Completion Criteria

- Text document analyzed
- Image/scanned document analyzed
- Structured JSON returned
- Pydantic validates output
- Invalid output rejected
- Actions stored
- Fees stored
- Risks stored
- Confidence stored
- Source page stored
- Partial failures handled

---

# 10. MILESTONE 6 — Analysis APIs

## Goal

Provide everything required by the Flutter analysis UI.

The Flutter developer owns the UI.

Backend developer owns the API.

## API

GET /documents/{id}/analysis

Response must provide:

- summary
- actions
- deadlines
- fees
- required documents
- people
- risks
- confidence
- source page
- processing status

## Important

Flutter must not call Gemini.

Flutter communicates only with FastAPI.

Backend communicates with Gemini.

Architecture:

Flutter
↓
FastAPI
↓
Gemini

## Completion Criteria

Flutter developer can consume the analysis API without needing direct Gemini access.

---

# 11. MILESTONE 7 — Task Management

## Goal

Implement task CRUD.

## Create

services/task_service.py

Update:

database/models.py

## Database

tasks:

- id
- user_id
- action_id nullable
- title
- description
- deadline
- priority
- status
- created_at

## APIs

POST /tasks

GET /tasks

PATCH /tasks/{id}

DELETE /tasks/{id}

## Task Types

1. Extracted task
2. Manual task

Manual task:

action_id = NULL

## Security

All task queries must filter by JWT user_id.

## NEEDS VERIFICATION

If source extraction has confidence < 0.60:

Task creation must be blocked unless user explicitly confirms the extraction.

## Completion Criteria

- Extracted task creation works
- Manual task creation works
- Task listing works
- Task update works
- Task deletion works
- Completion works
- Low-confidence gate works

---

# 12. MILESTONE 8 — Reminders

## Goal

Persist reminders for tasks.

## Create

services/reminder_service.py

Update:

database/models.py

## Database

reminders:

- id
- task_id
- reminder_time
- status

## APIs

POST /reminders

GET /reminders

DELETE /reminders/{id}

## Status

- pending
- sent
- cancelled

## Safety

If task originates from an unconfirmed NEEDS VERIFICATION extraction:

Reject reminder creation.

## IMPORTANT

M8 only stores reminders.

Actual FCM notification sending belongs to M9.

---

# 13. MILESTONE 9 — Push Notifications

## Goal

Send FCM notifications.

## Install

- firebase-admin
- apscheduler

## Firebase

Initialize Firebase Admin SDK.

Credentials must come from environment/config.

Never commit credentials.

## Database

Add to users:

fcm_token

## API

POST /auth/fcm-token

## Scheduler

APScheduler periodically checks:

pending reminders

where:

reminder_time <= now()

Then:

1. Get user's FCM token.
2. Send notification.
3. Mark reminder as sent.

## Notifications

Reminder:

"[Task Title] deadline is [date]."

Overdue task:

Daily notification for open overdue tasks.

Processing complete:

Notification after document analysis completes.

## Completion Criteria

- FCM token registered
- Token stored
- Reminder notification sent
- Reminder marked sent
- Overdue notification works
- Processing-complete notification works

---

# 14. MILESTONE 10 — Preferences & Backend Polish

## Goal

Implement notification preferences and backend edge cases.

## Database

Add:

notification_preferences

to users.

Store JSON preferences.

## API

PATCH /auth/preferences

## Notification Rules

Before sending notification:

1. Find user.
2. Read notification preferences.
3. Check notification type.
4. Send only if enabled.

## Types

- upcoming deadlines
- overdue tasks
- processing complete

## Backend Polish

Handle:

- invalid file
- oversized file
- malformed Gemini response
- Gemini timeout
- Gemini failure
- partial page failure
- database errors
- unauthorized access
- missing resources
- duplicate data
- invalid deadlines
- invalid confidence values

---

# 15. Backend API Summary

Authentication:

POST /auth/register
POST /auth/login
GET /auth/me
POST /auth/fcm-token
PATCH /auth/preferences

Documents:

POST /documents/upload
GET /documents
GET /documents/{id}
DELETE /documents/{id}

Analysis:

POST /documents/{id}/analyze
GET /documents/{id}/analysis

Tasks:

POST /tasks
GET /tasks
PATCH /tasks/{id}
DELETE /tasks/{id}

Reminders:

POST /reminders
GET /reminders
DELETE /reminders/{id}

Health:

GET /health

---

# 16. Backend Security Checklist

Before declaring backend complete:

[ ] JWT required on protected APIs

[ ] Every database query filters using authenticated user_id

[ ] Passwords are bcrypt hashed

[ ] JWT secret is environment-based

[ ] Gemini API key is environment-based

[ ] Firebase credentials are environment/config based

[ ] No secrets committed to Git

[ ] Users cannot access another user's documents

[ ] Users cannot access another user's tasks

[ ] Users cannot access another user's reminders

[ ] Low-confidence extraction cannot silently become a task

[ ] Raw Gemini output is never directly stored

---

# 17. Environment Variables

Use `.env` locally.

Example:

DATABASE_URL=...

JWT_SECRET=...

GEMINI_API_KEY=...

FIREBASE_CREDENTIALS=...

Never commit `.env`.

Add `.env` to `.gitignore`.

---

# 18. Testing Strategy

Every milestone must be tested before moving forward.

Backend testing should include:

- API tests
- authentication tests
- database tests
- file validation tests
- parser tests
- Gemini validation tests
- ownership/security tests
- task/reminder tests

Important security test:

User A must never access User B's data.

---

# 19. Git Workflow

Backend developer works on:

backend

Do not commit directly to main.

After completing a milestone:

git status

git add .

git commit -m "feat: complete Mx"

git push

Example:

git commit -m "feat: implement document upload APIs"

---

# 20. Coordination With Frontend Developer

The frontend developer does NOT need access to Gemini.

Frontend communicates with:

FastAPI REST APIs.

Backend must provide:

1. Endpoint
2. HTTP method
3. Request format
4. Response JSON
5. Error responses
6. Authentication requirement

Before frontend integration, backend developer should document API examples.

---

# 21. Backend Definition of Done

Backend is complete only when:

- All M1–M10 backend tasks are implemented.
- API endpoints work.
- Database models work.
- Authentication works.
- Document processing works.
- Gemini extraction works.
- Confidence safety rules work.
- Tasks work.
- Reminders work.
- FCM works.
- Notification preferences work.
- Security checks pass.
- No secrets are committed.
- Backend is pushed to the backend branch.

---

# 22. What Backend Developer Must NOT Do

Do not:

- redesign the Flutter architecture
- modify frontend UI unnecessarily
- call Gemini from Flutter
- add Tesseract
- add ML Kit backend OCR
- add Docker unless architecture changes
- add JWT refresh tokens
- add OAuth
- add unnecessary microservices
- add unnecessary queues
- replace PostgreSQL
- replace FastAPI
- replace Gemini
- bypass Pydantic validation
- store raw Gemini output
- bypass confidence confirmation rules

---

# 23. Working Principle

The backend developer should treat:

docs/architecture.md

as the technical source of truth.

This file:

docs/backend-plan.md

defines the backend execution order.

If there is a conflict:

architecture.md wins.

If implementation requires a new architectural decision:

STOP and discuss with the team before changing the architecture.

---

# 24. Final Backend Flow

The final system should work as:

User
↓
Flutter
↓
FastAPI
↓
Authentication
↓
Document Upload
↓
Document Parser
↓
Gemini
↓
Pydantic Validation
↓
Confidence/Safety Rules
↓
PostgreSQL
↓
Actions / Tasks
↓
Reminders
↓
FCM
↓
User Notification