# Document Intelligence & Action Extractor
# Frontend Implementation Plan

> This document defines the complete frontend responsibility for the frontend developer.
>
> The locked architecture in `docs/architecture.md` is the source of truth.
> This document does NOT replace the architecture.
> It converts the architecture into an executable frontend task plan.

---

# 1. Frontend Ownership

The frontend developer is responsible for the complete Flutter mobile application.

## Frontend Technologies

- Flutter
- Dart
- Riverpod
- go_router
- Dio
- flutter_secure_storage
- file_picker
- image_picker
- Firebase Core
- Firebase Messaging
- flutter_local_notifications

## Frontend Responsibilities

The frontend developer owns:

1. Flutter project structure
2. Design system
3. Theme
4. Navigation
5. Authentication UI
6. Riverpod state management
7. API integration using Dio
8. Secure JWT storage
9. Document upload UI
10. Document list UI
11. Analysis UI
12. Task UI
13. Reminder UI
14. FCM client integration
15. Notification routing
16. Profile screen
17. Notification preferences
18. Empty/loading/error states
19. Camera flow
20. Share-sheet integration
21. Frontend validation and polish

---

# 2. Frontend Folder Structure

The Flutter application must follow the architecture defined in `docs/architecture.md`.

lib/
│
├── core/
│   ├── constants/
│   ├── network/
│   ├── storage/
│   ├── theme/
│   └── utils/
│
├── features/
│   ├── auth/
│   ├── home/
│   ├── documents/
│   ├── upload/
│   ├── analysis/
│   ├── tasks/
│   ├── reminders/
│   └── notifications/
│
├── models/
├── services/
├── router/
└── main.dart

Do not unnecessarily redesign this structure.

---

# 3. Git Branch

Frontend development happens only on:

frontend

Create it using:

git checkout -b frontend

Push:

git push -u origin frontend

Do not directly develop frontend features on `main`.

---

# 4. Core Rule

Frontend development follows:

M1 → M2 → M3 → M4 → M5 → M6 → M7 → M8 → M9 → M10

Each milestone must:

1. Implement only its defined scope.
2. Compile successfully.
3. Be tested.
4. Be committed.
5. Be pushed to the frontend branch.

---

# 5. MILESTONE 1 — Flutter Scaffolding & Design System

## Goal

Create the complete visual and navigation shell of the application.

Nothing should depend on the backend yet.

---

## 5.1 Project Structure

Create:

lib/
├── core/
├── features/
├── models/
├── services/
├── router/
└── main.dart

Create feature folders:

features/
├── auth/
├── home/
├── documents/
├── upload/
├── analysis/
├── tasks/
├── reminders/
└── notifications/

---

## 5.2 Dependencies

Add to pubspec.yaml:

- flutter_riverpod
- riverpod_annotation
- go_router
- dio

Do NOT install future-milestone dependencies unnecessarily.

---

## 5.3 Riverpod

main.dart must use:

ProviderScope

Example architecture:

ProviderScope
    ↓
MaterialApp.router
    ↓
go_router

No global mutable state.

---

## 5.4 Design System

Create:

core/theme/

Implement:

AppTheme

Use the locked colors:

#0B0718
#17122B
#211A3B
#6C3BFF
#9B7BFF
#FFFFFF
#B7B0C9
#57D39A
#F4C95D
#FF6B81

The application should use the dark visual system defined by the architecture.

---

## 5.5 Navigation

Create:

router/app_router.dart

Use:

go_router

Create routes for the application's screens.

The architecture specifies 14 screens.

All screens can initially contain placeholders.

Authentication guard logic is implemented in M2.

---

## 5.6 Bottom Navigation

Create four primary tabs:

Home
Documents
Tasks
Profile

The bottom navigation should use go_router navigation.

---

## 5.7 Placeholder Screens

Create initial versions of:

- Home
- Documents
- Upload
- Analysis
- Tasks
- Task Detail
- Reminders
- Profile
- Login
- Register

Additional screens required by the final navigation design can be added without implementing their actual functionality yet.

---

## 5.8 Reusable Components

Create reusable visual components:

- DocumentCard
- ExtractionCard
- TaskCard
- ConfidenceBadge
- DeadlineChip
- FeeCard
- RiskBanner
- ActionCard
- SourceRow

At M1 these components are visual shells only.

No real API data.

---

## DO NOT IMPLEMENT

- Login API
- Registration API
- PostgreSQL
- JWT
- Gemini
- Document upload API
- AI analysis
- Tasks API
- Reminder API
- FCM

---

## M1 Completion Criteria

- Flutter application launches.
- Dark theme works.
- Bottom navigation works.
- Home/Documents/Tasks/Profile navigation works.
- Placeholder screens exist.
- Reusable components exist.
- App compiles without errors.
- Code is committed and pushed.

Commit example:

git add .
git commit -m "feat: add Flutter scaffolding and design system"
git push

---

# 6. MILESTONE 2 — Authentication

## Goal

Implement complete login/register frontend.

Backend provides:

POST /auth/register
POST /auth/login
GET /auth/me

---

# 6.1 Secure Storage

Add:

flutter_secure_storage

Create:

core/storage/

Implement a secure storage wrapper.

JWT must be stored here.

NEVER use:

SharedPreferences

for JWT storage.

---

# 6.2 Network Layer

Create:

core/network/

Configure a single Dio instance.

Dio should:

- contain the backend base URL
- attach JWT automatically
- handle HTTP errors
- provide typed responses where practical

---

# 6.3 Authentication Screens

Implement:

Login screen

Fields:

- email
- password

Actions:

- Login
- Navigate to Register

Register screen:

- name
- email
- password

Actions:

- Register
- Navigate to Login

---

# 6.4 Validation

Implement client-side validation:

- required fields
- valid email
- minimum password length

Backend remains the final authority for validation.

---

# 6.5 JWT Flow

Login:

Flutter
↓
POST /auth/login
↓
receive JWT
↓
store in flutter_secure_storage
↓
navigate to Home

Register:

Flutter
↓
POST /auth/register
↓
receive JWT
↓
store token
↓
navigate to Home

---

# 6.6 Auth State

Create Riverpod providers for:

authStateProvider
loginProvider
registerProvider

Authentication state must not be stored as random global mutable variables.

---

# 6.7 go_router Guard

Implement:

No JWT
→ /login

Valid JWT
→ /home

Logout:

delete JWT
↓
navigate to /login

---

## M2 Completion Criteria

- Registration UI works.
- Login UI works.
- Validation works.
- JWT is securely stored.
- Dio sends Authorization header.
- Auth guard works.
- Logout works.
- App compiles.

---

# 7. MILESTONE 3 — Document Upload & Document List

## Goal

Allow users to upload documents and view their documents.

Backend APIs:

POST /documents/upload
GET /documents
GET /documents/{id}
DELETE /documents/{id}

---

# 7.1 Dependencies

Add:

- file_picker
- image_picker

---

# 7.2 Upload Screen

Implement:

features/upload/

Allow:

1. Select document from storage.
2. Select image from gallery.
3. Capture image using camera.

Supported:

- PDF
- DOC
- DOCX
- JPG
- JPEG
- PNG
- WEBP
- HEIC

---

# 7.3 Upload Flow

User selects file.

Flutter:

select file
↓
validate basic file information
↓
show preview/name
↓
upload through Dio
↓
show progress
↓
show success/failure

Status:

Uploading…

then:

✓ Document uploaded

---

# 7.4 Document List

Implement:

features/documents/

Show:

- filename
- file type
- upload date
- processing status

Use:

DocumentCard

Add:

- pull-to-refresh
- delete action
- loading state
- empty state

---

# 7.5 Providers

Create:

documentListProvider
uploadDocumentProvider

---

## M3 Completion Criteria

- PDF upload works.
- Image upload works.
- Gallery works.
- Camera works.
- Upload progress works.
- Document appears in list.
- Delete works.
- Unsupported file displays error.
- App compiles.

---

# 8. MILESTONE 4 — Processing Status

## Goal

Display backend parsing/processing status.

No parser implementation is required in Flutter.

Backend handles:

- PyMuPDF
- python-docx
- OpenCV

Frontend only displays status.

---

# 8.1 Status

Display states such as:

Uploading…

Processing…

Parsed…

Complete

Failed

Partial

---

# 8.2 Document Card

Update DocumentCard so status changes are visible.

Possible implementation:

poll:

GET /documents/{id}

or refresh after upload.

Do not create unnecessary realtime infrastructure.

---

## M4 Completion Criteria

- Processing status visible.
- UI updates correctly.
- Failed state visible.
- Partial state visible.
- No backend parsing code added to Flutter.

---

# 9. MILESTONE 5 — Gemini Integration

## IMPORTANT

There is NO major frontend implementation in M5.

Gemini runs only in the backend.

Architecture:

Flutter
↓
FastAPI
↓
Gemini

NOT:

Flutter
↓
Gemini

---

## Frontend Responsibility

Only ensure that the existing frontend architecture can later consume:

GET /documents/{id}/analysis

Do NOT:

- add Gemini API key
- call Gemini directly
- add Gemini SDK to Flutter
- implement AI logic in Flutter

---

# 10. MILESTONE 6 — Analysis UI

## Goal

Display complete AI analysis.

Backend provides:

GET /documents/{id}/analysis

---

# 10.1 Analysis Screen

Create:

features/analysis/

Document Detail screen.

Use sections/tabs:

- Overview
- Actions
- Deadlines
- Fees
- Required Documents
- People
- Risks
- Source

---

# 10.2 Overview

Display:

summary

---

# 10.3 Actions

Use:

ActionCard

Display:

- title
- description
- deadline
- priority
- confidence
- source page

---

# 10.4 Fees

Use:

FeeCard

Display:

- amount
- currency
- purpose
- source page
- confidence

---

# 10.5 Risks

Use:

RiskBanner

Display:

- description
- severity
- confidence
- source page

Severity:

WARNING

CRITICAL

---

# 10.6 Required Documents

Display extracted document names.

Example:

- Aadhaar Card
- Income Certificate

---

# 10.7 People

Display:

- name
- role
- department
- organization
- source page

---

# 10.8 Confidence Badges

HIGH:

✓ High Confidence

MEDIUM:

~ Medium Confidence

NEEDS VERIFICATION:

⚠ Needs Verification

Important:

HIGH CONFIDENCE does not mean human verification.

---

# 10.9 Needs Verification

For confidence < 0.60:

Show:

⚠ Needs Verification

Show:

"Confirm before creating task"

Provide:

View Source

Confirm This Information

Task creation must remain blocked until confirmation.

---

# 10.10 Processing Screen

While analysis is running:

✓ Document uploaded

Analyzing…

✓ Information extracted

Poll backend until analysis is available.

---

# 10.11 Failure States

Full failure:

"Unable to fully analyze this document."

Buttons:

Try Again

Upload Another Document

Partial failure:

"Document Partially Analyzed."

Show affected pages.

---

# 10.12 Providers

Create:

documentAnalysisProvider

processingStatusProvider

---

## M6 Completion Criteria

- Analysis loads from backend.
- All extraction sections display.
- Confidence badges work.
- Source pages display.
- Low-confidence extraction is blocked from task creation.
- Processing state works.
- Full failure works.
- Partial failure works.

---

# 11. MILESTONE 7 — Task Management

## Goal

Implement complete task UI.

Backend APIs:

POST /tasks
GET /tasks
PATCH /tasks/{id}
DELETE /tasks/{id}

---

# 11.1 Task List

Create:

features/tasks/

Organize tasks into:

- Today
- Upcoming
- Overdue
- Completed

---

# 11.2 Task Card

Use:

TaskCard

Display:

- title
- deadline
- priority
- status
- reminder information if available

---

# 11.3 Create Task From Action

From ActionCard:

Create Task

Pre-fill:

- title
- description
- deadline
- priority

User can review/edit before creating.

---

# 11.4 Manual Task

Allow user to create a task without an extracted action.

Required:

- title
- description

Optional:

- deadline

Priority:

- HIGH
- MEDIUM
- LOW

---

# 11.5 Needs Verification Gate

If extraction is not confirmed:

Disable:

Create Task

Show explanation:

"This information needs verification before a task can be created."

Allow:

View Source

Confirm This Information

After confirmation:

Create Task becomes available.

---

# 11.6 Task Detail

Show:

- title
- description
- deadline
- priority
- status
- source document
- source page

Actions:

- edit
- complete
- delete
- set reminder
- view source

---

# 11.7 Source Viewer

Display the original document/page referenced by an extraction.

At minimum:

- correct document
- correct page reference

---

# 11.8 Providers

Create:

taskListProvider

createTaskProvider

updateTaskProvider

---

## M7 Completion Criteria

- Task list works.
- Extracted task creation works.
- Manual task creation works.
- Edit works.
- Complete works.
- Delete works.
- Overdue section works.
- Needs Verification gate works.
- Source navigation works.

---

# 12. MILESTONE 8 — Reminders

## Goal

Allow users to configure reminders for tasks.

Backend APIs:

POST /reminders
GET /reminders
DELETE /reminders/{id}

---

# 12.1 Reminder Screen

Create:

features/reminders/

Options:

- 1 day before
- 2 days before
- 3 days before
- 1 week before
- Custom date/time

---

# 12.2 Custom Reminder

Use:

Date Picker

Time Picker

Calculate:

reminder_time

from task deadline + selected offset.

---

# 12.3 Task Detail

Add:

Set Reminder

Show existing reminder:

Reminder: 21 Aug — 9:00 AM

Allow delete.

---

# 12.4 Safety

If task is from an unconfirmed NEEDS VERIFICATION extraction:

Do not allow reminder creation.

Display explanation.

---

# 12.5 Providers

Create:

reminderProvider

createReminderProvider

---

## M8 Completion Criteria

- Reminder picker works.
- Preset options work.
- Custom date/time works.
- Reminder appears on task.
- Reminder deletion works.
- Low-confidence gate works.

---

# 13. MILESTONE 9 — Firebase Cloud Messaging

## Goal

Receive and route push notifications.

Backend handles actual FCM dispatch.

Frontend handles:

- Firebase initialization
- permissions
- token
- notification reception
- notification tap routing

---

# 13.1 Dependencies

Add:

- firebase_core
- firebase_messaging
- flutter_local_notifications

---

# 13.2 Firebase

Initialize Firebase in:

main.dart

Do not commit private Firebase service account credentials.

---

# 13.3 Notification Permission

Request notification permissions.

Support appropriate Android/iOS behavior.

---

# 13.4 FCM Token

Get device FCM token.

Send to backend:

POST /auth/fcm-token

Backend stores the token.

---

# 13.5 Foreground Notifications

When app is open:

Show local notification banner.

---

# 13.6 Background Notifications

Allow Firebase Messaging to handle background delivery.

---

# 13.7 Notification Routing

Reminder notification:

Notification tap
↓
Task Detail

Processing complete:

Notification tap
↓
Document Detail

---

# 13.8 Provider

Create:

fcmTokenProvider

---

## M9 Completion Criteria

- Firebase initializes.
- Notification permissions work.
- FCM token obtained.
- Token registered with backend.
- Foreground notification works.
- Background notification works.
- Reminder tap opens Task Detail.
- Processing-complete tap opens Document Detail.

---

# 14. MILESTONE 10 — Profile, Preferences & Polish

## Goal

Complete profile, notification preferences and UX polish.

---

# 14.1 Profile

Display:

- name
- email

---

# 14.2 Notification Preferences

Preferences:

- upcoming deadlines
- overdue tasks
- processing complete

Use toggles.

Backend API:

PATCH /auth/preferences

---

# 14.3 Empty States

Documents:

"No documents yet — tap + to analyze your first document"

Tasks:

"No tasks yet"

Other appropriate empty states should be added.

---

# 14.4 Loading States

Add loading skeletons or appropriate loading indicators to:

- document list
- analysis
- tasks
- reminders
- profile

---

# 14.5 Error States

Every network-based screen should have:

- meaningful error message
- retry button where appropriate
- navigation option where appropriate

Do not show raw exception messages to users.

---

# 14.6 Camera Flow

Improve:

Camera capture
↓
Preview
↓
Retake / Use Photo
↓
Upload

---

# 14.7 Share Sheet

Support documents shared from other applications.

Android:

handle incoming intents.

iOS:

support share extension where required.

Shared document:

↓
Upload
↓
Analyze

---

# 14.8 HEIC

If HEIC is supported:

Upload normally.

If unsupported:

Show:

"HEIC image could not be processed. Please convert it to JPG or PNG."

Do not silently fail.

---

## M10 Completion Criteria

- Profile works.
- Preferences work.
- Logout works.
- Empty states exist.
- Loading states exist.
- Error states exist.
- Camera flow polished.
- Share flow works.
- HEIC handling is clear.
- Full app flow works.

---

# 15. Frontend API Dependency

The frontend developer depends on the backend developer for REST APIs.

Frontend must NOT implement backend logic.

The communication architecture is:

Flutter
↓
Dio
↓
FastAPI
↓
PostgreSQL / Gemini / FCM

---

# 16. API Contract Requirement

Whenever frontend integrates an API, the backend developer should provide:

1. Endpoint
2. HTTP method
3. Authentication requirement
4. Request body
5. Request parameters
6. Successful response
7. Error response
8. Required headers

Example:

POST /auth/login

Request:

{
  "email": "user@example.com",
  "password": "password"
}

Response:

{
  "access_token": "...",
  "token_type": "bearer"
}

The frontend should not guess API contracts.

---

# 17. Frontend Models

Create Dart models in:

lib/models/

Models should mirror backend API responses.

Examples:

- User
- Document
- DocumentPage
- Action
- Fee
- Risk
- Person
- Task
- Reminder
- Analysis

Use typed models instead of passing large dynamic maps throughout the UI.

---

# 18. Frontend State Management

Use Riverpod.

Do not create random global state.

Recommended pattern:

UI
↓
Riverpod Provider
↓
Service
↓
Dio
↓
FastAPI

Example:

TaskScreen
↓
taskListProvider
↓
TaskService
↓
Dio
↓
GET /tasks

---

# 19. Services

Shared API/business communication should live in:

lib/services/

Examples:

- auth_service.dart
- document_service.dart
- analysis_service.dart
- task_service.dart
- reminder_service.dart
- notification_service.dart

Do not put API calls directly inside UI widgets unless there is a strong reason.

---

# 20. Network Rules

All HTTP calls must go through the centralized Dio instance.

Do NOT:

- create random Dio instances throughout the app
- hardcode JWT
- hardcode Gemini API key
- call Gemini directly
- store secrets in Flutter

---

# 21. Authentication Rules

JWT must be stored only using:

flutter_secure_storage

Never:

SharedPreferences

Never log JWT tokens.

Never display JWT tokens in the UI.

---

# 22. Frontend Security Rules

The frontend must:

- securely store JWT
- never contain Gemini API key
- never contain backend Firebase service account credentials
- never trust client-side confidence values as security decisions
- display backend errors safely
- handle expired JWT
- redirect to login on unauthorized response

Backend remains responsible for actual authorization.

---

# 23. Error Handling

Handle at least:

400 Bad Request

401 Unauthorized

403 Forbidden

404 Not Found

409 Conflict

422 Validation Error

500 Server Error

Network timeout

No internet

Gemini processing failure

File upload failure

UI should show user-friendly messages.

Do not expose:

- stack traces
- internal server errors
- database errors
- API keys
- tokens

---

# 24. Git Workflow

Frontend developer works on:

frontend

Do not commit directly to main.

After completing a milestone:

git status

git add .

git commit -m "feat: complete Mx"

git push

Example:

git commit -m "feat: implement document upload UI"

---

# 25. Coordination With Backend Developer

Frontend and backend are separate responsibilities.

Frontend developer should NOT modify backend files.

Backend developer should NOT modify frontend UI unless explicitly coordinated.

Communication happens through API contracts.

---

# 26. Backend Integration Order

Frontend integration should happen in this order:

M2
→ Authentication APIs

M3
→ Document APIs

M4
→ Processing status

M5/M6
→ Analysis APIs

M7
→ Task APIs

M8
→ Reminder APIs

M9
→ FCM APIs

M10
→ Preferences API

---

# 27. Mock Data Rule

If a backend API is not ready:

Frontend may temporarily use mock data for UI development.

However:

- clearly mark mock data
- do not commit fake production logic
- replace mock data when API becomes available
- do not change API contract just to fit mock data

Example:

const useMockData = true;

This must be removed/disabled before final integration.

---

# 28. Frontend Definition of Done

Frontend is complete only when:

- All M1–M10 frontend tasks are implemented.
- Navigation works.
- Authentication works.
- Document upload works.
- Document list works.
- Analysis works.
- Confidence states work.
- Tasks work.
- Reminders work.
- FCM works.
- Profile works.
- Preferences work.
- Empty states work.
- Loading states work.
- Error states work.
- Camera flow works.
- Share flow works.
- App compiles successfully.
- Frontend is pushed to the frontend branch.

---

# 29. What Frontend Developer Must NOT Do

Do not:

- implement FastAPI
- implement PostgreSQL
- implement SQLAlchemy
- implement Gemini backend
- put Gemini API key in Flutter
- implement Tesseract
- implement backend OCR
- bypass backend authentication
- store JWT in SharedPreferences
- modify database schema directly
- add unnecessary backend infrastructure
- replace Riverpod
- replace go_router
- replace Dio
- call Gemini directly
- bypass backend confidence rules

---

# 30. Final Frontend Flow

The final application flow should be:

Login/Register
↓
Home
↓
Upload Document
↓
Document List
↓
Processing
↓
AI Analysis
↓
Review Extracted Actions
↓
Confirm if Required
↓
Create Task
↓
Set Reminder
↓
Receive Notification
↓
Complete Task

---

# 31. Working Principle

The frontend developer should treat:

docs/architecture.md

as the technical source of truth.

This file:

docs/frontend-plan.md

defines the frontend execution order.

If there is a conflict:

architecture.md wins.

If implementation requires a new architectural decision:

STOP and discuss with the team before changing the architecture.

---

# 32. Final Responsibility Split

## Backend Developer

Owns:

FastAPI
PostgreSQL
SQLAlchemy
JWT
bcrypt
File Storage
PyMuPDF
python-docx
OpenCV
Gemini
Pydantic
AI Extraction
Tasks API
Reminders API
FCM Backend
Scheduler
Notification Preferences API

## Frontend Developer

Owns:

Flutter
Dart
Riverpod
go_router
Dio
Secure Storage
UI
Navigation
Upload UI
Document UI
Analysis UI
Task UI
Reminder UI
FCM Client
Notification Routing
Profile
Preferences
UX Polish

---

# 33. Final Team Architecture

                    ┌─────────────────────┐
                    │      Flutter        │
                    │  Frontend Developer │
                    └──────────┬──────────┘
                               │
                              Dio
                               │
                               ▼
                    ┌─────────────────────┐
                    │       FastAPI       │
                    │   Backend Developer │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
        PostgreSQL          Gemini             FCM
             │                 │                 │
             └─────────────────┼─────────────────┘
                               │
                               ▼
                         Application Data