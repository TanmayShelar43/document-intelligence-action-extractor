# Document Intelligence & Action Extractor


# FINAL LOCKED ARCHITECTURE


> **Status: LOCKED**
>
> This document supersedes all prior architectural notes and analysis.
> It incorporates every resolved decision listed in the architectural gap closure.
> No further architectural assumptions need to be made before M1 begins.


---


# A. Final Tech Stack


| Layer | Technology | Notes |
|---|---|---|
| Mobile Application | Flutter + Dart | Feature-based structure |
| State Management | **Riverpod** | Locked |
| Navigation | **go_router** | Locked |
| HTTP Client | **Dio** | Locked |
| Backend | Python + FastAPI | |
| AI / OCR / Document Understanding | Google Gemini API | Structured JSON output only |
| Gemini Python SDK | **Verify current official SDK before M5** | Do not assume outdated package name |
| PDF Processing | PyMuPDF | Text extraction + page-to-image rendering |
| DOC/DOCX Processing | python-docx | Paragraphs, headings, tables |
| Image Preprocessing | OpenCV | Orientation + quality — then Gemini Vision |
| AI Response Validation | Pydantic | All Gemini output passes through Pydantic before DB |
| Database | PostgreSQL | 8 core tables, normalized |
| Authentication | JWT access tokens (no refresh tokens in MVP) | |
| Push Notifications | Firebase Cloud Messaging (FCM) | |
| API Communication | REST API | |


> **Explicitly excluded:**
>
> - Tesseract OCR
> - Google ML Kit (backend)
> - Any separately installed OCR engine
> - Docker / deployment infrastructure (out of MVP scope)
> - JWT refresh tokens (out of MVP scope)


---


# B. Final Flutter Architecture


## Project Structure


```text
lib/
│
├── core/
│   ├── constants/          ← design tokens, app strings, enums
│   ├── network/            ← Dio client, interceptors, API base
│   ├── storage/            ← flutter_secure_storage wrapper
│   ├── theme/              ← AppTheme, colour tokens, typography
│   └── utils/              ← helpers, formatters, extensions
│
├── features/
│   ├── auth/               ← login, register screens + Riverpod providers
│   ├── home/               ← dashboard screen + providers
│   ├── documents/          ← document list screen + providers
│   ├── upload/             ← upload screen, file picker, camera + providers
│   ├── analysis/           ← document detail, extraction sections + providers
│   ├── tasks/              ← task list, task detail, task creation + providers
│   ├── reminders/          ← reminder picker screen + providers
│   └── notifications/      ← FCM setup, notification routing
│
├── models/                 ← Dart data models mirroring API responses
│
├── services/               ← shared services (auth service, document service, etc.)
│
├── router/                 ← go_router route definitions
│
└── main.dart               ← app entry point, ProviderScope, router init
State Management (Riverpod)
ProviderScope wraps the entire app at main.dart
Each feature contains its own providers (StateNotifierProvider, FutureProvider, etc.)
No global mutable state outside providers
Providers are feature-scoped; shared state (auth, user) lives in services/
Navigation (go_router)
Route definitions centralized in router/
Auth guard: redirect unauthenticated users to /login
Named routes for all 14 screens
Deep linking from FCM notification taps
HTTP (Dio)
Single Dio instance configured in core/network/
Interceptor adds Authorization: Bearer <token> from secure storage
Interceptor handles 401 responses (redirect to login)
Typed response parsing into Dart models
Key Flutter Rules
Gemini API key is never present in Flutter code or assets
JWT stored in flutter_secure_storage (never SharedPreferences)
All API calls go through the FastAPI backend — Flutter never calls Gemini directly
C. Final Backend Architecture
Project Structure
backend/
│
├── main.py                        ← FastAPI app entry, router registration
│
├── api/
│   ├── auth.py                    ← /auth/register, /auth/login, /auth/me
│   ├── documents.py               ← /documents CRUD
│   ├── analysis.py                ← /documents/{id}/analyze, /documents/{id}/analysis
│   ├── tasks.py                   ← /tasks CRUD
│   └── reminders.py               ← /reminders CRUD
│
├── document_parser/
│   ├── pdf_parser.py              ← PyMuPDF: text + scanned page detection
│   ├── docx_parser.py             ← python-docx: paragraphs, headings, tables
│   ├── image_processor.py         ← OpenCV: orientation, quality preprocessing
│   └── validator.py               ← file type + size validation
│
├── ai/
│   ├── gemini_client.py           ← Gemini SDK client (key from env var)
│   ├── prompts.py                 ← structured extraction prompts
│   ├── extraction.py              ← orchestrate Gemini call + parse response
│   └── schemas.py                 ← Pydantic schemas for all extraction types
│
├── database/
│   ├── models.py                  ← SQLAlchemy ORM models for all 8 tables
│   └── database.py                ← PostgreSQL connection, session factory
│
├── services/
│   ├── document_service.py        ← document lifecycle logic
│   ├── task_service.py            ← task CRUD logic
│   └── reminder_service.py        ← reminder CRUD + FCM scheduling
│
└── requirements.txt
Key Backend Rules
Gemini API key loaded from environment variable only — never hardcoded
Raw Gemini output never written directly to PostgreSQL
All Gemini JSON passes through Pydantic → business rules → confidence validation → DB
Every endpoint (except /auth/register and /auth/login) requires a valid JWT
Server-side: every query filters by user_id from the JWT — no cross-user data access
D. Final Document Processing / OCR Pipeline
Overall Flow
FILE RECEIVED BY FASTAPI
  ↓
File Validation (type, size, format)
  ↓
File Type Detection
  ↓
  ├── PDF ──────────────────────────────────────────────────→ PyMuPDF
  │                                                               ↓
  │                                          Inspect each page for text content
  │                                                               ↓
  │                              ┌──────────────────────────────────────────────┐
  │                              │                                              │
  │                       Text-based page                         Scanned / image-only page
  │                              ↓                                              ↓
  │                    Extract text with PyMuPDF                  Render page as image (PyMuPDF)
  │                              ↓                                              ↓
  │                   Send text to Gemini (text mode)            Send image to Gemini Vision
  │
  ├── DOC / DOCX ───────────────────────────────────────────→ python-docx
  │                                                               ↓
  │                                    Extract paragraphs, headings, tables, text
  │                                                               ↓
  │                                              Send text content to Gemini
  │
  └── IMAGE (JPG / JPEG / PNG / WEBP / HEIC) ───────────────→ OpenCV
                                                               ↓
                                                  Orientation correction
                                                  Image quality processing
                                                               ↓
                                                  Send preprocessed image to Gemini Vision
                                                  (OCR + document understanding)
  ↓
GEMINI API
  ↓
Structured JSON response
  ↓
Pydantic validation
  (types, dates, amounts, required fields, confidence range, source refs)
  ↓
Business rule validation
  (confidence thresholds, duplicate detection, invalid output rejection)
  ↓
POSTGRESQL
OCR Technology Decision
Format	Preprocessing	AI Layer	Method
Text-based PDF	PyMuPDF (text extraction)	Gemini (text understanding)	Text → Gemini
Scanned PDF	PyMuPDF (render page → image)	Gemini Vision (OCR + understanding)	Image → Gemini Vision
DOC / DOCX	python-docx (text extraction)	Gemini (text understanding)	Text → Gemini
JPG / JPEG / PNG / WEBP / HEIC	OpenCV (preprocessing)	Gemini Vision (OCR + understanding)	Image → Gemini Vision

No Tesseract. No ML Kit. No separate OCR engine of any kind.

E. Final Gemini Responsibility

Gemini is the central AI intelligence layer. It is called by the backend only.

What Gemini Does
Task	Input Mode
OCR — scanned documents and images	Gemini Vision
Document understanding — layout, tables, headings, context	Text or Vision
Summary generation — short, information-dense	Text or Vision
Action extraction — what the user must do	Text or Vision
Deadline extraction — exact / range / relative / conditional	Text or Vision
Fee extraction — amounts, currencies, purposes	Text or Vision
Required document extraction	Text or Vision
People & organization extraction	Text or Vision
Risk and warning detection	Text or Vision
Source page reference identification	Text or Vision
Confidence score assignment per extraction	Text or Vision
What Gemini Must NOT Do
Return uncontrolled prose that gets stored directly in PostgreSQL
Invent exact dates when the document only provides relative or conditional deadlines
Fabricate information when content is missing or unreadable
Receive the Gemini API key from Flutter (it is backend-only)
Gemini Output Contract

Gemini must return structured JSON conforming to the Pydantic schemas defined in ai/schemas.py.

Example structure:

{
  "summary": "Students must submit the examination form by 23 August 2026.",
  "actions": [
    {
      "title": "Submit examination form",
      "description": "Submit the completed examination form to the Examination Department.",
      "deadline": "2026-08-23",
      "deadline_type": "exact",
      "priority": "HIGH",
      "source_page": 3,
      "confidence": 0.98
    }
  ],
  "fees": [
    {
      "amount": 1250,
      "currency": "INR",
      "purpose": "Examination fee",
      "source_page": 3,
      "confidence": 0.99
    }
  ],
  "risks": [
    {
      "description": "Late submission may result in a ₹500 penalty.",
      "severity": "WARNING",
      "source_page": 3,
      "confidence": 0.96
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
      "organization": "ABC University",
      "source_page": 1
    }
  ]
}
Gemini SDK Note

Before implementing M5 (Gemini Integration), verify the currently appropriate official Gemini Python SDK package name and version.

Do not assume any previously known package name (e.g. google-generativeai or other). Check the official Google AI / Google Cloud documentation at implementation time and use the current official package.

F. Final Database Schema

Database: PostgreSQL

ORM: SQLAlchemy

Core Tables (MVP — 8 tables)

people and required_documents are part of the structured Pydantic/analysis model and stored as JSON fields within the documents or actions context — not as separate relational tables in the MVP.

users
Column	Type	Constraints	Description
id	UUID / SERIAL	PK	Unique user ID
name	TEXT	NOT NULL	Display name
email	TEXT	NOT NULL, UNIQUE	Login email
password_hash	TEXT	NOT NULL	bcrypt hash
created_at	TIMESTAMP	NOT NULL, DEFAULT NOW()	Account creation
documents
Column	Type	Constraints	Description
id	UUID / SERIAL	PK	Document ID
user_id	FK → users.id	NOT NULL	Owner
filename	TEXT	NOT NULL	Original filename
file_type	TEXT	NOT NULL	pdf / docx / jpg / png / webp / heic
file_size	INTEGER	NOT NULL	Size in bytes
file_path	TEXT	NOT NULL	Backend storage path
processing_status	TEXT	NOT NULL	uploading / processing / complete / failed / partial
uploaded_at	TIMESTAMP	NOT NULL, DEFAULT NOW()	Upload timestamp
document_pages
Column	Type	Constraints	Description
id	UUID / SERIAL	PK	Page record ID
document_id	FK → documents.id	NOT NULL	Related document
page_number	INTEGER	NOT NULL	Page number (1-indexed)
content	TEXT	NULLABLE	Extracted text content (null for image-only pages)
is_scanned	BOOLEAN	NOT NULL, DEFAULT FALSE	True if page rendered as image for Gemini Vision
actions
Column	Type	Constraints	Description
id	UUID / SERIAL	PK	Action ID
document_id	FK → documents.id	NOT NULL	Source document
title	TEXT	NOT NULL	Action title
description	TEXT	NOT NULL	Action description
deadline	TEXT	NULLABLE	Deadline value (may be relative/conditional — stored as text)
deadline_type	TEXT	NULLABLE	exact / range / relative / conditional
priority	TEXT	NOT NULL	HIGH / MEDIUM / LOW
confidence	FLOAT	NOT NULL	AI confidence (0.0–1.0)
source_page	INTEGER	NULLABLE	Source page number
fees
Column	Type	Constraints	Description
id	UUID / SERIAL	PK	Fee ID
document_id	FK → documents.id	NOT NULL	Source document
amount	NUMERIC	NOT NULL	Fee amount
currency	TEXT	NOT NULL	Currency code (INR, USD…)
purpose	TEXT	NOT NULL	Fee purpose
confidence	FLOAT	NOT NULL	AI confidence
source_page	INTEGER	NULLABLE	Source page number
risks
Column	Type	Constraints	Description
id	UUID / SERIAL	PK	Risk ID
document_id	FK → documents.id	NOT NULL	Source document
description	TEXT	NOT NULL	Risk description
severity	TEXT	NOT NULL	WARNING / CRITICAL
confidence	FLOAT	NOT NULL	AI confidence
source_page	INTEGER	NULLABLE	Source page number
tasks
Column	Type	Constraints	Description
id	UUID / SERIAL	PK	Task ID
user_id	FK → users.id	NOT NULL	Task owner
action_id	FK → actions.id	NULLABLE	Source action (null = manual task)
title	TEXT	NOT NULL	Task title
description	TEXT	NOT NULL	Task description
deadline	DATE	NULLABLE	Task deadline
priority	TEXT	NOT NULL	HIGH / MEDIUM / LOW
status	TEXT	NOT NULL	OPEN / COMPLETED / OVERDUE
created_at	TIMESTAMP	NOT NULL, DEFAULT NOW()	Creation timestamp

action_id is nullable — users can create manual tasks not derived from any extraction.

description is required — NOT NULL.

reminders
Column	Type	Constraints	Description
id	UUID / SERIAL	PK	Reminder ID
task_id	FK → tasks.id	NOT NULL	Related task
reminder_time	TIMESTAMP	NOT NULL	When to send notification
status	TEXT	NOT NULL	pending / sent / cancelled
Excluded from MVP Schema
Generic extractions table — not used; specific tables (actions, fees, risks) are used instead
people table — stored within structured analysis model / JSON, not a relational table in MVP
required_documents table — stored within structured analysis model / JSON, not a relational table in MVP
fcm_tokens — FCM token stored as a column in users (added in M9) or a simple lookup
G. Final Confidence / Safety Rules
Confidence Classification
Score Range	Classification	Label
>= 0.85	HIGH CONFIDENCE	✓ High Confidence
0.60 – 0.84	MEDIUM CONFIDENCE	~ Medium Confidence
< 0.60	NEEDS VERIFICATION	⚠ Needs Verification

Critical clarification:

"HIGH CONFIDENCE" does not mean the information has been verified by a human or confirmed as factual truth.

It means the AI extraction has a high confidence score.

The user remains responsible for verifying important information against the source document.

Safety Rules
Confidence Level	Can create task?	Can create reminder?	UI behavior
HIGH CONFIDENCE	Yes — directly	Yes — after task creation	✓ badge, task creation enabled
MEDIUM CONFIDENCE	Yes — directly	Yes — after task creation	~ badge shown, user can proceed
NEEDS VERIFICATION	No — blocked	No — blocked	⚠ badge, user must explicitly confirm first
Confirmation Flow for NEEDS VERIFICATION
NEEDS VERIFICATION extraction shown
  ↓
User taps [View Source] to inspect the original page
  ↓
User taps [Confirm This Information]
  ↓
Extraction status updated to confirmed
  ↓
Task creation and reminder creation now available

Low-confidence information must never silently become an active task or reminder without this explicit confirmation step.

H. Final Authentication Approach
Technology
JWT (JSON Web Tokens) — access tokens only
bcrypt — password hashing
flutter_secure_storage — secure client-side token storage
Flow
Register: POST /auth/register
  → validate email uniqueness
  → bcrypt hash password
  → store user in PostgreSQL
  → return JWT access token


Login: POST /auth/login
  → validate credentials
  → return JWT access token


Flutter stores token in flutter_secure_storage.


All subsequent API requests:
  → Dio interceptor attaches Authorization: Bearer <token>


Backend JWT middleware:
  → validates token on every protected route
  → extracts user_id from token claims
  → all queries filter by user_id
MVP Scope Exclusions
No refresh tokens in MVP
No OAuth / social login in MVP
No email verification in MVP
No password reset in MVP
Security Rules
Password stored as bcrypt hash only — never plaintext
JWT never stored in SharedPreferences — always flutter_secure_storage
All data queries include WHERE user_id = <jwt_user_id> — no cross-user access possible
Gemini API key stored as a backend environment variable — never in Flutter
I. Final 10-Milestone Implementation Plan

Philosophy: Each milestone must compile and run successfully before the next begins.

No future-milestone functionality is implemented early.

No unrelated parts are refactored during a milestone.

Milestone 1 — Project Scaffolding & Design System

Goal: Establish Flutter feature-based architecture, design system, placeholder navigation, and FastAPI skeleton. Nothing functional beyond structure and visual shell.

Flutter Scope
Restructure lib/ to the feature-based layout defined in section B
Add to pubspec.yaml: flutter_riverpod, riverpod_annotation, go_router, dio
Create ProviderScope in main.dart
Create AppTheme with all design tokens
Create router/app_router.dart with go_router routes for all 14 screens
Create placeholder screens: Home, Documents, Upload, Analysis, Tasks, Task Detail, Reminders, Profile, Login, Register
Bottom navigation bar with 4 tabs: Home / Documents / Tasks / Profile
Reusable UI components:
DocumentCard
ExtractionCard
TaskCard
ConfidenceBadge
DeadlineChip
FeeCard
RiskBanner
ActionCard
SourceRow
Backend Scope
backend/ directory created
requirements.txt with:
fastapi
uvicorn
main.py with FastAPI instance
GET /health → {"status": "ok"}
NOT in Scope
Authentication
Database
API calls
Gemini
Document upload
Tasks
Reminders
FCM
Testable Criteria
Flutter app launches with correct dark theme and bottom navigation
All 4 tabs navigate to placeholder screens without errors
Design tokens applied correctly
GET /health returns {"status": "ok"} from FastAPI
Flutter app compiles without errors
Milestone 2 — Database & Authentication

Goal: Working user registration and login with JWT, persisted to PostgreSQL.

Backend Scope
Add to requirements.txt:
sqlalchemy
psycopg2-binary
python-jose[cryptography]
passlib[bcrypt]
python-multipart
database/database.py — PostgreSQL connection, SQLAlchemy session
database/models.py — users table ORM model
POST /auth/register
POST /auth/login
GET /auth/me
JWT middleware / dependency
Passwords stored as bcrypt hashes only
Flutter Scope
Add flutter_secure_storage
Login screen
Register screen
Form validation
Dio authentication calls
JWT secure storage
Dio interceptor
go_router auth guard
Logout
Auth Riverpod providers
NOT in Scope
Document upload
Document-related tables
Gemini
Tasks
Reminders
Testable Criteria
Register new user → user stored in PostgreSQL
Login with correct credentials → JWT returned
Wrong password → error displayed
/auth/me with valid JWT → user returned
/auth/me without JWT → 401
Successful login → Home
Logout → Login
Flutter compiles
Milestone 3 — Document Upload & Storage

Goal: Upload a document from Flutter, validate it server-side, persist metadata, and display the document list.

Backend Scope
Add:
python-multipart
aiofiles (or equivalent)
Add documents ORM model
POST /documents/upload
GET /documents
GET /documents/{id}
DELETE /documents/{id}
Server-side file validation
File storage on server filesystem
Flutter Scope
file_picker
image_picker
Upload screen
File picker
Gallery picker
Camera capture
Upload progress
Document list
Pull-to-refresh
Document providers
NOT in Scope
Parsing
AI processing
Analysis screen
Testable Criteria
PDF upload works
Image upload works
Camera capture works
Delete works
Unsupported file rejected
User isolation works
Flutter compiles
Milestone 4 — Document Parsers

Goal: Backend can parse uploaded documents into structured text/image content ready for Gemini. No AI calls yet.

Backend Scope
Add:
pymupdf
python-docx
opencv-python
document_parser/validator.py
document_parser/pdf_parser.py
document_parser/docx_parser.py
document_parser/image_processor.py
Add document_pages ORM model
Store page-level parsing results
Update processing status
Flutter Scope
No new screens
Update document processing status
NOT in Scope
Gemini API calls
AI extraction
New Flutter screens
Testable Criteria
Text PDF → extracted text
Scanned PDF → is_scanned = true
DOCX → paragraphs, headings and tables extracted
JPG → OpenCV preprocessing
Correct processing status transitions
Flutter compiles
Milestone 5 — Gemini Integration & AI Extraction

Goal: Backend calls Gemini, validates structured output with Pydantic, applies business and confidence rules, stores results.

Backend Scope
Verify and add current official Gemini Python SDK
ai/gemini_client.py
ai/prompts.py
ai/schemas.py
ai/extraction.py
Pydantic validation
Business rule validation
Confidence classification
Add actions, fees, risks models
POST /documents/{id}/analyze
GET /documents/{id}/analysis
Partial processing support
Flutter Scope
None
NOT in Scope
Analysis UI
Task creation
Testable Criteria
Known PDF → Gemini analysis
Scanned image → Vision extraction
Relative deadline preserved correctly
Malformed JSON rejected
API key environment-only
Confidence stored correctly
Analysis endpoint returns results
Flutter compiles
Milestone 6 — Analysis UI

Goal: Flutter app displays complete AI analysis results to the user.

Flutter Scope

Create features/analysis/ with:

Document Detail screen
Overview tab
Actions tab
Deadlines tab
Fees tab
Required Documents tab
People tab
Risks tab
Source references
Confidence badges
Processing status
Failure states
Partial failure states
View Source button
Create Task button
Analysis Riverpod providers
NOT in Scope
Actual task creation
Source page viewer
Reminders
FCM
Testable Criteria
Analysis displayed correctly
Confidence badges correct
NEEDS VERIFICATION blocks task creation
Failure state works
Partial failure works
Processing state updates
Flutter compiles
Milestone 7 — Task Creation & Management

Goal: Users can create tasks from extracted actions and manage the full task lifecycle.

Backend Scope
Add tasks ORM model
task_service.py
POST /tasks
GET /tasks
PATCH /tasks/{id}
DELETE /tasks/{id}
User ownership verification
Flutter Scope
Task List
Today section
Upcoming section
Overdue section
Completed section
Task cards
Task creation from actions
Manual task creation
Task Detail
Task editing
Complete task
Delete task
Source document navigation
Source page viewer
NEEDS VERIFICATION gate
NOT in Scope
Reminders
FCM notifications
Testable Criteria
High-confidence action → task
Manual task works
Low-confidence task blocked
Complete task works
Edit works
Delete works
View Source works
Overdue tasks work
Flutter compiles
Milestone 8 — Reminders

Goal: Users can create reminders for tasks. Reminders are persisted. Low-confidence safety gate enforced.

Backend Scope
Add reminders ORM model
reminder_service.py
POST /reminders
GET /reminders
DELETE /reminders/{id}
Low-confidence reminder protection
Flutter Scope
Reminder picker
1 day before
2 days before
3 days before
1 week before
Custom date/time
Set Reminder from Task Detail
Display reminder on Task Card
Delete reminder
NOT in Scope
FCM dispatch
Testable Criteria
Reminder creation works
Custom reminder works
Delete works
Low-confidence reminder blocked
Reminder displayed correctly
Flutter compiles
Milestone 9 — Push Notifications (FCM)

Goal: FCM push notifications fire at configured reminder times.

Backend Scope
Add:
firebase-admin
apscheduler
Firebase Admin SDK
Add fcm_token to users
POST /auth/fcm-token
Background scheduler
Reminder notifications
Overdue notifications
Processing complete notifications
Flutter Scope
firebase_core
firebase_messaging
flutter_local_notifications
FCM initialization
Notification permissions
FCM token registration
Foreground notifications
Background notifications
Notification tap routing
Notification provider
NOT in Scope
Notification preferences
Testable Criteria
FCM token stored
Test reminder notification received
Processing complete notification received
Notification tap opens correct screen
Reminder status becomes sent
Flutter compiles
Milestone 10 — Profile, Preferences & Polish

Goal: Profile screen, notification preferences, UX polish, and remaining edge cases.

Backend Scope
Add notification_preferences JSON column
PATCH /auth/preferences
Respect notification preferences during dispatch
Flutter Scope
Profile screen
User name
User email
Notification preferences
Logout
Empty states
Loading skeletons
Error retry buttons
Camera preview / retake
Share-sheet integration
HEIC handling
NOT in Scope
New core features
Advanced source viewer improvements
Admin features
Multi-user features
Testable Criteria
Preferences work
Empty states work
Full document → analysis → task flow works
Share PDF works
Error handling works
Flutter compiles
Milestone Summary Table
Milestone	Focus	Key Deliverable
M1	Scaffolding + Design System	Themed app skeleton, placeholder screens, FastAPI /health
M2	Database + Authentication	PostgreSQL users, bcrypt, JWT, login/register, route guard
M3	Document Upload	File upload, metadata persistence, document list
M4	Document Parsers	PyMuPDF, python-docx, OpenCV, document_pages storage
M5	Gemini Integration	Gemini pipeline, Pydantic validation, extraction storage
M6	Analysis UI	Full analysis display, confidence badges, error states
M7	Task Management	Task CRUD, task creation from actions, source viewer
M8	Reminders	Reminder CRUD, timing picker, low-confidence gate
M9	Push Notifications	FCM setup, reminder dispatch, notification routing
M10	Profile + Polish	Preferences, empty states, share sheet, HEIC, edge cases
Dependency Chain
M1 (structure)
  ↓
M2 (database + auth)  ← M1 required
  ↓
M3 (upload)           ← M2 required
  ↓
M4 (parsers)          ← M3 required
  ↓
M5 (Gemini)           ← M4 required
  ↓
M6 (analysis UI)      ← M5 required
  ↓
M7 (tasks)            ← M6 required
  ↓
M8 (reminders)        ← M7 required
  ↓
M9 (FCM)              ← M8 required
  ↓
M10 (polish)          ← M9 required
Engineering Rules
Rule	Requirement
Fixed Stack	Do not replace any specified technology without an explicit architectural decision
Backend AI Key	Gemini API key never in Flutter — backend environment variable only
Validate AI	Never store raw Gemini output directly in PostgreSQL
Source Traceability	Every extraction retains its source page reference
No Fabrication	Report uncertainty; never invent missing information
Confidence Matters	NEEDS VERIFICATION items require user confirmation
User Control	User reviews and edits extracted actions before task creation
Document-to-Task Traceability	Tasks created from extractions remain linked to source document and action
MVP First	Complete document → action → task → reminder flow before any extras
Mobile First	Avoid dense desktop-style interfaces
Incremental Build	Each milestone compiles and runs before the next begins