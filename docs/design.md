# Document Intelligence & Action Extractor
## Master Product, Design & Technical Specification

> **Purpose:** This is the single source of truth for implementing the Document Intelligence & Action Extractor mobile application.
>
> The product transforms long documents into verified, actionable tasks, deadlines, reminders and decisions.

---

# 1. Product Overview

## Product Name

**Document Intelligence & Action Extractor**

## Platform

Mobile-first application.

## Core Product Idea

The application answers one question:

> **"I uploaded this document. What is important, and what do I need to do?"**

This is **not a normal PDF summarizer**.

The primary purpose is to transform unstructured documents into actionable information.

### Core Experience

```text
DOCUMENT
   ↓
INTELLIGENCE
   ↓
ACTION
   ↓
TASK
   ↓
REMINDER
   ↓
COMPLETION
```

### Product Pipeline

```text
Upload / Scan
      ↓
Understand
      ↓
Extract
      ↓
Review
      ↓
Verify
      ↓
Create Task
      ↓
Set Reminder
      ↓
Complete
```

---

# 2. Product Goals

The system should:

- Read and understand long documents.
- Support PDFs, DOC/DOCX files and images.
- Extract useful structured information.
- Identify actions the user needs to perform.
- Identify deadlines and date conditions.
- Identify fees and penalties.
- Identify required documents.
- Identify people and organizations.
- Identify risks and warnings.
- Preserve source-page references.
- Attach confidence levels to AI-generated information.
- Convert extracted actions into editable tasks.
- Allow users to create reminders.
- Prevent low-confidence information from silently becoming active reminders.
- Keep users in control through source verification.

---

# 3. Target Users

## Students

Typical documents:

- College notices
- Examination forms
- Scholarship notices
- Admission documents
- Circulars

Primary need:

> Never miss submission dates, fees or required documents.

## Employees

Typical documents:

- HR circulars
- Company policies
- Compliance notices

Primary need:

> Understand responsibilities and deadlines.

## Professionals

Typical documents:

- Contracts
- Financial documents
- Government documents

Primary need:

> Identify obligations, risks and important conditions.

## General Users

Typical documents:

- Bills
- Application forms
- Insurance documents
- Official letters

Primary need:

> Know what matters and what action is required.

---

# 4. Primary Use Case

### Example Document

> Submit exam form before 23 Aug. Fee ₹1,250. Late submission attracts ₹500 penalty.

### System Output

```text
Action:
Submit Exam Form

Deadline:
23 Aug

Fee:
₹1,250

Priority:
HIGH

Risk:
₹500 late penalty
```

The user should be able to turn the action into a task and configure a reminder.

---

# 5. Supported Documents

The application should support:

- PDF
- DOC
- DOCX
- JPG
- JPEG
- PNG
- WEBP
- HEIC
- Scanned PDFs
- Camera-captured documents

The system should support multi-page documents.

---

# 6. Information Architecture

The mobile application has four primary destinations.

## 6.1 Home

Contains:

- Upcoming tasks
- Urgent deadlines
- Recent documents
- Primary Analyze Document action

Primary CTA:

```text
+ Analyze Document
```

## 6.2 Documents

Contains:

- Uploaded documents
- Processing status
- Extraction counts
- Document history

Primary action:

```text
Open Document
```

## 6.3 Tasks

Organized into:

- Today
- Upcoming
- Overdue
- Completed

Primary actions:

- Complete
- Edit
- Delete
- Open source

## 6.4 Profile

Contains:

- Authentication/account controls
- Notification preferences
- Account settings

---

# 7. Core User Journey

```text
OPEN APP
   ↓
UPLOAD / SCAN
   ↓
PROCESS
   ↓
AI ANALYSIS
   ↓
REVIEW
   ↓
CREATE TASK
   ↓
REMINDER
   ↓
COMPLETE
```

## Journey Details

| Stage | User sees | System behavior |
|---|---|---|
| Upload | File name, type, size, status | Validate and detect file type |
| Processing | Progress/status | Parse document and send structured content to Gemini |
| Analysis | Summary and extraction cards | Extract actions, deadlines, fees, documents, people and risks |
| Review | Confidence and source references | Flag uncertain information and prevent unsafe automation |
| Task | Editable task fields | Persist task with source linkage |
| Reminder | Preset/custom timing | Create reminder for selected task |
| Completion | Completed state | Update task while retaining traceability |

---

# 8. Home Screen

The home screen should answer:

> **What do I need to do?**

Example:

```text
Good Evening 👋

What do you need to do?

UPCOMING

🔴 Submit Exam Form
   Due Tomorrow

🟡 Scholarship Application
   Due 30 Aug


RECENT DOCUMENTS

Exam Notice.pdf
Scholarship Notice.pdf
College Circular.pdf


+ Analyze Document
```

The primary CTA should remain highly visible.

---

# 9. Document Detail Screen

The document detail screen should contain:

```text
OVERVIEW
────────────
Short useful summary


ACTIONS
────────────
Required user actions


DEADLINES
────────────
Exact / range / relative / conditional


FEES
────────────
Amount + purpose + source


REQUIRED DOCUMENTS
────────────
Documents the user must submit


PEOPLE
────────────
People / departments / organizations


RISKS
────────────
Penalties / rejection / cancellation / warnings


SOURCE
────────────
Page-level traceability
```

Primary CTA:

```text
Create Task
```

---

# 10. Task Design

Example:

```text
SUBMIT EXAMINATION FORM

Due:
23 Aug 2026

Priority:
HIGH

Source:
Exam_Notice.pdf — Page 3
```

Task fields:

- ID
- Title
- Description
- Deadline
- Priority
- Status
- Related action
- Source document
- Source page
- Created timestamp

Task states:

```text
OPEN
COMPLETED
OVERDUE
```

---

# 11. Reminder Design

Users can choose:

- 1 day before
- 2 days before
- 3 days before
- 1 week before
- Custom date/time

Example:

```text
Task:
Submit Examination Form

Deadline:
23 August 2026

Reminder:
21 August 2026
9:00 AM
```

Low-confidence information must not automatically create an active reminder.

---

# 12. AI Extraction

Gemini is the central intelligence layer.

The UI should expose **structured, verifiable output rather than uncontrolled prose**.

The system extracts:

1. Summary
2. Actions
3. Deadlines
4. Fees
5. Required documents
6. People
7. Organizations
8. Risks
9. Warnings
10. Conditions
11. Source references
12. Confidence levels

---

# 13. Extraction Schema

## Summary

Required:

- Short useful summary

## Action

Required:

- Title
- Description
- Deadline
- Priority
- Confidence
- Source page

## Deadline

Required:

- Value
- Deadline type
- Source page
- Confidence

Supported types:

- Exact
- Range
- Relative
- Conditional

## Fee

Required:

- Amount
- Currency
- Purpose
- Source page
- Confidence

## Required Document

Required:

- Document name
- Source

## Person / Organization

Required:

- Name
- Role / department / organization
- Source

## Risk

Required:

- Description
- Severity
- Confidence
- Source page

## Condition / Warning

Required:

- Condition text
- Source

---

# 14. Deadline Rules

The system should identify:

### Exact

```text
23 August 2026
```

### Date Range

```text
20 August – 25 August 2026
```

### Relative

```text
Within 7 days
```

### Conditional

```text
Within 15 days of receiving the notice
```

## Critical Rule

The system must **not invent an exact date** if the document does not provide enough information to calculate one.

---

# 15. Action Extraction

The system should identify actions such as:

- Submit
- Apply
- Pay
- Upload
- Attend
- Sign
- Verify
- Contact
- Register
- Complete
- Renew
- Respond

Example:

```text
Document:
Students must upload their Aadhaar Card and Income Certificate.

Extracted actions:
1. Upload Aadhaar Card
2. Upload Income Certificate
```

Each actionable extraction should have a clear path to task creation.

---

# 16. Fee Extraction

Identify:

- Application fees
- Registration fees
- Examination fees
- Late fees
- Penalties
- Deposits
- Other charges

Each fee should include:

- Amount
- Currency
- Purpose
- Source page
- Confidence

Example:

```text
Examination Fee:
₹1,250

Late Fee:
₹500
```

---

# 17. Required Document Extraction

Identify documents the user needs to submit.

Examples:

- Aadhaar Card
- Income Certificate
- Previous Marksheet
- Passport Photograph

Each required document can become a task.

---

# 18. People & Organization Extraction

Identify:

- People
- Departments
- Organizations
- Contact persons
- Authorities
- Responsible parties

Example:

```text
Contact Person:
Dr. Rahul Sharma

Department:
Examination Department

Organization:
ABC University
```

---

# 19. Risk Detection

Identify consequences such as:

- Late fees
- Penalties
- Rejection
- Cancellation
- Missing-document consequences
- Compliance issues
- Important conditions

Example:

```text
Document:
Applications submitted after the deadline will not be accepted.

Risk:
Late submission may result in application rejection.
```

Risk severity should be represented in the UI.

---

# 20. Source Traceability

Every important extracted item should contain a source reference.

Example:

```text
Submit Examination Form

Deadline:
23 August 2026

Source:
Exam_Notice.pdf — Page 3

[View Source]
```

The View Source action should open the corresponding document page.

Source traceability is required for auditability and user trust.

---

# 21. Confidence & Verification

Every important AI extraction should have a confidence level.

### High Confidence

```text
✓ High Confidence

Deadline:
23 August 2026
```

### Needs Verification

```text
⚠ Needs Verification

Possible Deadline:
23 August 2026

[View Source]
```

## Safety Rule

```text
High confidence
      ↓
Can become active task

Needs verification
      ↓
User confirmation required
      ↓
Then task/reminder can become active
```

Low-confidence information must never silently become an active reminder.

---

# 22. AI Trust Pipeline

Gemini output must **never directly enter the database**.

```text
GEMINI
   ↓
STRUCTURED JSON
   ↓
PYDANTIC
   ↓
BUSINESS RULES
   ↓
CONFIDENCE VALIDATION
   ↓
DATABASE
```

Validation must check:

- Data types
- Required fields
- Valid dates
- Valid monetary values
- Confidence values
- Source references
- Duplicate information
- Invalid AI output

---

# 23. Technical Architecture

## Final Technology Stack

| Layer | Technology |
|---|---|
| Mobile Application | Flutter + Dart |
| Backend | Python + FastAPI |
| AI + OCR + Document Understanding | Google Gemini API |
| PDF Processing | PyMuPDF |
| DOC/DOCX Processing | python-docx |
| Image Processing | OpenCV |
| AI Response Validation | Pydantic |
| Database | PostgreSQL |
| Authentication | JWT |
| Notifications | Firebase Cloud Messaging |
| API Communication | REST API |

## Architecture

```text
┌─────────────────────────────┐
│       FLUTTER + DART        │
│                             │
│ Home / Documents / Tasks    │
│ Profile / Upload / Analysis │
└──────────────┬──────────────┘
               │
             REST API
               │
               ▼
┌─────────────────────────────┐
│       PYTHON + FASTAPI      │
│                             │
│ Auth / Documents / Analysis │
│ Tasks / Reminders           │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│     DOCUMENT PROCESSING     │
│                             │
│ PyMuPDF / python-docx       │
│ OpenCV                      │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│        GEMINI API           │
│                             │
│ OCR / Understanding         │
│ Extraction / Reasoning      │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       VALIDATION            │
│                             │
│ Pydantic / Business Rules   │
│ Confidence / Source Checks  │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│         POSTGRESQL          │
└─────────────────────────────┘
```

---

# 24. Flutter Architecture

Suggested structure:

```text
lib/
│
├── core/
│   ├── constants/
│   ├── network/
│   ├── storage/
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
│
├── services/
│
└── main.dart
```

---

# 25. FastAPI Architecture

Suggested structure:

```text
backend/
│
├── app/
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
└── main.py
```

---

# 26. Document Processing Pipeline

Use the lightest deterministic parser available before invoking AI understanding.

```text
FILE
 ↓
VALIDATE
 ↓
DETECT TYPE
 ↓
PARSE
 ↓
GEMINI
 ↓
STRUCTURE
 ↓
VALIDATE
 ↓
STORE
```

## PDF

Processor:

```text
PyMuPDF
```

Output:

- Page count
- Page content
- Page numbers
- Metadata
- Embedded content

## DOC / DOCX

Processor:

```text
python-docx
```

Output:

- Paragraphs
- Headings
- Tables
- Text
- Document structure

## Image

```text
Image
 ↓
OpenCV
 ↓
Orientation / Quality Processing
 ↓
Gemini
 ↓
OCR + Understanding
```

## Scanned PDF

```text
Scanned PDF
 ↓
Gemini Visual Understanding
 ↓
OCR + Layout/Table Understanding
```

---

# 27. Complete Backend Processing Flow

```text
USER
  │
  │ Upload document
  ▼
FLUTTER APP
  │
  │ REST API
  ▼
FASTAPI
  │
  ▼
FILE VALIDATION
  │
  ▼
FILE TYPE DETECTION
  │
  ├── PDF ────────→ PyMuPDF
  │
  ├── DOC/DOCX ───→ python-docx
  │
  └── IMAGE ──────→ OpenCV
  │
  ▼
GEMINI API
  │
  ├── OCR
  ├── Understanding
  ├── Action Extraction
  ├── Deadline Extraction
  ├── Fee Extraction
  ├── Risk Detection
  └── Source Identification
  │
  ▼
STRUCTURED JSON
  │
  ▼
PYDANTIC
  │
  ▼
BUSINESS VALIDATION
  │
  ▼
CONFIDENCE VALIDATION
  │
  ▼
POSTGRESQL
  │
  ▼
FASTAPI
  │
  ▼
FLUTTER
  │
  ▼
USER
```

---

# 28. Database Design

PostgreSQL will be used as the persistent database.

## users

| Field | Description |
|---|---|
| id | Unique user ID |
| name | User name |
| email | User email |
| password_hash | Hashed password |
| created_at | Account creation timestamp |

## documents

| Field | Description |
|---|---|
| id | Unique document ID |
| user_id | Owner |
| filename | Original filename |
| file_type | Document type |
| file_size | File size |
| processing_status | Processing state |
| uploaded_at | Upload timestamp |

## document_pages

| Field | Description |
|---|---|
| id | Page ID |
| document_id | Related document |
| page_number | Page number |
| content | Page content |

## extractions

| Field | Description |
|---|---|
| id | Extraction ID |
| document_id | Related document |
| type | Extraction type |
| content | Extracted content |
| confidence | AI confidence |
| source_page | Source page |

## actions

| Field | Description |
|---|---|
| id | Action ID |
| document_id | Related document |
| title | Action title |
| description | Action description |
| deadline | Deadline |
| priority | Priority |
| confidence | AI confidence |
| source_page | Source page |

## fees

| Field | Description |
|---|---|
| id | Fee ID |
| document_id | Related document |
| amount | Amount |
| currency | Currency |
| purpose | Purpose |
| source_page | Source page |

## risks

| Field | Description |
|---|---|
| id | Risk ID |
| document_id | Related document |
| description | Risk |
| severity | Severity |
| confidence | AI confidence |
| source_page | Source page |

## tasks

| Field | Description |
|---|---|
| id | Task ID |
| user_id | Owner |
| action_id | Related action |
| title | Task title |
| deadline | Deadline |
| priority | Priority |
| status | Status |
| created_at | Creation timestamp |

## reminders

| Field | Description |
|---|---|
| id | Reminder ID |
| task_id | Related task |
| reminder_time | Reminder date/time |
| status | Reminder status |

---

# 29. API Design

## Authentication

```text
POST /auth/register
POST /auth/login
GET  /auth/me
```

## Documents

```text
POST   /documents/upload
GET    /documents
GET    /documents/{id}
DELETE /documents/{id}
```

## Analysis

```text
POST /documents/{id}/analyze
GET  /documents/{id}/analysis
```

## Tasks

```text
POST   /tasks
GET    /tasks
PATCH  /tasks/{id}
DELETE /tasks/{id}
```

## Reminders

```text
POST   /reminders
GET    /reminders
DELETE /reminders/{id}
```

---

# 30. Security & Privacy

Documents can contain sensitive personal information.

## Authentication

Use JWT-based authentication.

Every document and task must be associated with the authenticated user.

## Gemini API Key

The Gemini API key must:

- Stay on the backend.
- Never be embedded in Flutter.
- Never be exposed to the mobile client.

## Secure Transmission

Documents and AI requests should travel through the secured backend path.

## Document Ownership

Server-side authorization must ensure that users can only access their own documents and related tasks.

## Deletion

Users should be able to delete documents.

## Trust

Source references must remain attached to extracted information.

Processing errors must be visible instead of being silently converted into potentially incorrect results.

---

# 31. Error Handling

## Processing Failure

```text
Unable to fully analyze this document.

The document could not be reliably processed.

[Try Again]
[Upload Another Document]
```

## Partial Analysis

```text
Document Partially Analyzed

Pages 1–8 were processed successfully.

Pages 9–12 require verification.

[Review Pages]
```

## No Fabrication

The system must never invent information to compensate for missing or unreadable content.

---

# 32. Visual Design System

The visual direction is:

- Dark interface
- Deep-purple gradients
- Bold typography
- Soft lighting
- High-contrast cards
- Futuristic but discreet
- Productivity-focused rather than decorative

The UI should feel premium without sacrificing readability.

---

# 33. Design Tokens

| Token | Value | Use |
|---|---|---|
| Background | `#0B0718` | App background / immersive surfaces |
| Primary Surface | `#17122B` | Navigation, hero sections, major containers |
| Card Surface | `#211A3B` | Extraction/task/document cards |
| Primary Accent | `#6C3BFF` | Primary actions and active states |
| Soft Accent | `#9B7BFF` | Highlights and secondary emphasis |
| Text | `#FFFFFF` | Primary headings and key values |
| Muted Text | `#B7B0C9` | Metadata and helper text |
| Success | `#57D39A` | Completed / verified / safe states |
| Warning | `#F4C95D` | Needs verification / medium priority |
| Risk | `#FF6B81` | High priority / penalties / critical warnings |

---

# 34. Typography

## Display

Use bold, high-impact headings for:

- Screen titles
- Key actions
- Important values

## Body

Use clean, highly readable sans-serif typography.

## Metadata

Use smaller muted typography for:

- Source pages
- File types
- Confidence
- Timestamps

---

# 35. Visual Behavior

- Use dark surfaces with restrained deep-purple gradients.
- Avoid flat black.
- Use soft glow/light effects sparingly.
- Keep cards rounded and spacious.
- Avoid dense tables on mobile.
- Use bold typography to establish hierarchy.
- Use color semantically:
  - Green = verified/completed
  - Amber = needs verification
  - Red = risk/critical

---

# 36. Component Library

## Document Card

Shows:

- Name
- Type
- Date
- Processing state
- Extraction counts

States:

```text
Uploading
Processing
Complete
Failed
```

## Extraction Card

Shows one important AI extraction.

States:

```text
Verified
Needs Verification
```

## Action Card

Represents a required action.

States:

```text
Not Created
Task Created
Completed
```

## Deadline Chip

States:

```text
Today
Tomorrow
Upcoming
Overdue
```

## Fee Card

Shows:

- Amount
- Purpose
- Source

## Risk Banner

States:

```text
Warning
Critical
```

## Source Row

Action:

```text
View Source
```

## Confidence Badge

States:

```text
High
Medium
Needs Verification
```

## Task Card

States:

```text
Open
Completed
Overdue
```

---

# 37. Notifications

Notifications should cover:

- Upcoming deadlines
- Overdue tasks
- Important tasks
- Document processing completion

Example:

```text
🔔 Your examination form deadline is tomorrow.
```

Firebase Cloud Messaging is used for push notifications.

---

# 38. MVP Scope

The MVP should prove the complete document-to-action loop.

## P0

### Authentication

- Register
- Login
- User-specific access

### Upload

- PDF
- DOC/DOCX
- Supported images

### Processing

- File validation
- Parser
- Gemini pipeline

### AI Extraction

- Summary
- Actions
- Deadlines
- Fees
- Required documents
- People
- Risks
- Source
- Confidence

### Verification

Low-confidence output requires user confirmation.

### Task Creation

Actions can become editable tasks.

### Reminders

Preset/custom reminders.

### Notifications

Upcoming/overdue task notifications.

## P1

- Document history
- Source viewer
- OCR/camera improvements

---

# 39. MVP Success Criterion

The success criterion is **not the number of AI features**.

The MVP is successful when a user can:

```text
Upload a real document
        ↓
Understand what matters
        ↓
Create a task
        ↓
Receive a reminder
        ↓
Verify the source
```

without leaving the application.

---

# 40. Implementation Structure

## Flutter

```text
core/
features/auth
features/home
features/documents
features/upload
features/analysis
features/tasks
features/reminders
features/notifications
models/
services/
```

## FastAPI

```text
api/auth.py
api/documents.py
api/analysis.py
api/tasks.py
api/reminders.py
```

## Document Parser

```text
pdf_parser.py
docx_parser.py
image_processor.py
validator.py
```

## AI

```text
gemini_client.py
prompts.py
extraction.py
schemas.py
```

## Database

```text
models.py
database.py
```

## Services

```text
document_service.py
task_service.py
reminder_service.py
```

## Entry Point

```text
main.py
```

---

# 41. Recommended Implementation Order

Build the project in this order:

```text
1. DATABASE + AUTH
          ↓
2. DOCUMENT UPLOAD
          ↓
3. DOCUMENT PARSERS
          ↓
4. GEMINI INTEGRATION
          ↓
5. PYDANTIC VALIDATION
          ↓
6. ANALYSIS UI
          ↓
7. TASKS
          ↓
8. REMINDERS
          ↓
9. NOTIFICATIONS
```

Do not build advanced features before the complete core loop works.

---

# 42. Engineering Rules

## Rule 1 — Fixed Stack

Do not replace the specified stack without an explicit architectural decision.

## Rule 2 — Backend AI Key

Never expose the Gemini API key in Flutter.

## Rule 3 — Validate AI

Never store raw Gemini output directly in the database.

## Rule 4 — Source Traceability

Every important extraction must retain its source page/reference.

## Rule 5 — No Fabrication

If information is missing or unreadable, report uncertainty instead of inventing information.

## Rule 6 — Confidence Matters

Low-confidence information requires user confirmation.

## Rule 7 — User Control

The user must be able to review and edit extracted actions before task creation.

## Rule 8 — Document-to-Task Traceability

Every task created from an extraction must remain linked to its source document and action.

## Rule 9 — MVP First

Prioritize the complete document → action → task → reminder flow.

## Rule 10 — Mobile First

Avoid unnecessarily dense desktop-style interfaces.

---

# 43. Final Product Direction

The product should feel less like a document reader and more like an **intelligent action layer sitting on top of every important document**.

```text
UNDERSTAND
AI reads and interprets the document.
        ↓
EXTRACT
Important facts become structured information.
        ↓
VERIFY
Sources and confidence keep the user in control.
        ↓
ACT
Actions become tasks and reminders.
```

## Final Product Statement

> **From documents to decisions.**

The application should make important information actionable while keeping the user in control of AI-generated decisions.
