# Document Intelligence & Action Extractor

# Technical Stack & Architecture

---

# 1. Final Technology Stack

| Layer                             | Technology               |
| --------------------------------- | ------------------------ |
| Mobile Application                | Flutter + Dart           |
| Backend                           | Python + FastAPI         |
| AI + OCR + Document Understanding | Google Gemini API        |
| PDF Processing                    | PyMuPDF                  |
| DOC/DOCX Processing               | python-docx              |
| Image Processing                  | OpenCV                   |
| AI Response Validation            | Pydantic                 |
| Database                          | PostgreSQL               |
| Authentication                    | JWT                      |
| Notifications                     | Firebase Cloud Messaging |
| API Communication                 | REST API                 |

> **Note:** No Docker, deployment infrastructure, or cloud deployment stack is included at this stage.

---

# 2. Overall Architecture

```text
┌─────────────────────────────────────────┐
│              MOBILE APP                 │
│                                         │
│             Flutter + Dart              │
│                                         │
│   Home | Documents | Tasks | Profile    │
└────────────────────┬────────────────────┘
                     │
                     │ REST API
                     ▼
┌─────────────────────────────────────────┐
│                BACKEND                  │
│                                         │
│            Python + FastAPI             │
│                                         │
│  Authentication                         │
│  Document Management                    │
│  Analysis                               │
│  Task Management                         │
│  Reminder Management                     │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│          DOCUMENT PROCESSING            │
│                                         │
│  PDF      → PyMuPDF                     │
│  DOC/DOCX → python-docx                │
│  Image    → OpenCV                      │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│              GEMINI API                 │
│                                         │
│  OCR                                    │
│  Document Understanding                 │
│  Information Extraction                 │
│  Action Detection                       │
│  Deadline Detection                     │
│  Fee Detection                          │
│  Risk Detection                         │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│          VALIDATION LAYER               │
│                                         │
│  Pydantic                               │
│  Business Rules                         │
│  Confidence Checking                    │
│  Source Verification                    │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│               DATABASE                  │
│                                         │
│              PostgreSQL                 │
│                                         │
│  Users                                  │
│  Documents                              │
│  Pages                                  │
│  Extractions                            │
│  Actions                                │
│  Deadlines                              │
│  Fees                                   │
│  Risks                                  │
│  Tasks                                  │
│  Reminders                              │
└─────────────────────────────────────────┘
```

---

# 3. Mobile Application Architecture

The Flutter application will follow a feature-based project structure.

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

### Main Feature Modules

| Module          | Responsibility                               |
| --------------- | -------------------------------------------- |
| `auth`          | User registration, login and authentication  |
| `home`          | Dashboard and upcoming tasks                 |
| `documents`     | Document history and document management     |
| `upload`        | Upload and scan documents                    |
| `analysis`      | Display AI analysis results                  |
| `tasks`         | Create and manage tasks                      |
| `reminders`     | Manage task reminders                        |
| `notifications` | Handle application notifications             |
| `models`        | Application data models                      |
| `services`      | Shared application services                  |
| `core`          | Constants, networking, storage and utilities |

---

# 4. Backend Architecture

The backend will be implemented using **Python + FastAPI**.

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

# 5. Document Processing Architecture

```text
FILE
 │
 ▼
File Validation
 │
 ▼
Detect File Type
 │
 ├───────────────┬────────────────┐
 ▼               ▼                ▼
PDF            DOC/DOCX         IMAGE
 │               │                │
 ▼               ▼                ▼
PyMuPDF       python-docx      OpenCV
 │               │                │
 └───────────────┼────────────────┘
                 │
                 ▼
             Gemini API
                 │
                 ▼
       Document Understanding
                 │
                 ▼
        Structured AI Output
                 │
                 ▼
        Pydantic Validation
                 │
                 ▼
             Database
```

---

# 6. PDF Processing

For PDF files, **PyMuPDF** will inspect and process the document.

The system will obtain:

* Page count
* Page content
* Page numbers
* Document metadata
* Embedded content information

The extracted document/page information will then be passed to Gemini for document understanding and structured extraction.

---

# 7. DOC/DOCX Processing

For DOC/DOCX files, **python-docx** will extract:

* Paragraphs
* Headings
* Tables
* Text
* Document structure

The extracted content will then be passed to Gemini.

---

# 8. Image Processing

For image documents:

```text
Image
  ↓
OpenCV
  ↓
Orientation
  ↓
Image Quality Processing
  ↓
Gemini API
  ↓
OCR + Understanding
  ↓
Structured Data
```

OpenCV is used for preprocessing before Gemini receives the image.

---

# 9. Gemini Processing

Gemini is the central AI layer.

It performs:

* OCR
* Document Understanding
* Information Extraction
* Reasoning
* Classification

Gemini identifies:

* Summary
* Actions
* Deadlines
* Fees
* People
* Organizations
* Required Documents
* Risks
* Warnings
* Conditions
* Source References
* Confidence

---

# 10. Structured Gemini Response

Gemini must return **structured data rather than uncontrolled text**.

### Example

```json
{
  "summary": "Students must submit the examination form by 23 August 2026.",
  "actions": [
    {
      "title": "Submit examination form",
      "deadline": "2026-08-23",
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
      "source_page": 3,
      "confidence": 0.96
    }
  ]
}
```

---

# 11. Validation Layer

Gemini output should **never directly enter the database**.

```text
Gemini
  ↓
JSON
  ↓
Pydantic
  ↓
Business Validation
  ↓
Confidence Validation
  ↓
Database
```

The validation layer checks:

* Correct data types
* Valid dates
* Valid monetary values
* Required fields
* Source references
* Confidence values
* Duplicate information
* Invalid AI output

This layer prevents malformed or unreliable AI responses from directly affecting application data.

---

# 12. Database Structure

The application will use **PostgreSQL**.

## users

| Field         | Description                |
| ------------- | -------------------------- |
| id            | Unique user ID             |
| name          | User name                  |
| email         | User email                 |
| password_hash | Hashed password            |
| created_at    | Account creation timestamp |

## documents

| Field             | Description              |
| ----------------- | ------------------------ |
| id                | Unique document ID       |
| user_id           | Owner of document        |
| filename          | Original filename        |
| file_type         | Document type            |
| file_size         | File size                |
| processing_status | Current processing state |
| uploaded_at       | Upload timestamp         |

## document_pages

| Field       | Description      |
| ----------- | ---------------- |
| id          | Page ID          |
| document_id | Related document |
| page_number | Page number      |
| content     | Page content     |

## extractions

| Field       | Description       |
| ----------- | ----------------- |
| id          | Extraction ID     |
| document_id | Related document  |
| type        | Extraction type   |
| content     | Extracted content |
| confidence  | AI confidence     |
| source_page | Source page       |

## actions

| Field       | Description        |
| ----------- | ------------------ |
| id          | Action ID          |
| document_id | Related document   |
| title       | Action title       |
| description | Action description |
| deadline    | Action deadline    |
| priority    | Action priority    |
| confidence  | AI confidence      |
| source_page | Source page        |

## fees

| Field       | Description      |
| ----------- | ---------------- |
| id          | Fee ID           |
| document_id | Related document |
| amount      | Fee amount       |
| currency    | Currency         |
| purpose     | Fee purpose      |
| source_page | Source page      |

## risks

| Field       | Description      |
| ----------- | ---------------- |
| id          | Risk ID          |
| document_id | Related document |
| description | Risk description |
| severity    | Risk severity    |
| confidence  | AI confidence    |
| source_page | Source page      |

## tasks

| Field      | Description        |
| ---------- | ------------------ |
| id         | Task ID            |
| user_id    | Task owner         |
| action_id  | Related action     |
| title      | Task title         |
| deadline   | Task deadline      |
| priority   | Task priority      |
| status     | Task status        |
| created_at | Creation timestamp |

## reminders

| Field         | Description        |
| ------------- | ------------------ |
| id            | Reminder ID        |
| task_id       | Related task       |
| reminder_time | Reminder date/time |
| status        | Reminder status    |

---

# 13. API Structure

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

# 14. Complete Processing Flow

```text
USER
 │
 │ Upload PDF / DOC / DOCX / Image
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
DOCUMENT PROCESSOR
 │
 ├── PDF → PyMuPDF
 ├── DOC/DOCX → python-docx
 └── IMAGE → OpenCV
 │
 ▼
GEMINI API
 │
 ├── OCR
 ├── Document Understanding
 ├── Action Extraction
 ├── Deadline Extraction
 ├── Fee Extraction
 ├── Risk Detection
 └── Source Identification
 │
 ▼
PYDANTIC VALIDATION
 │
 ▼
POSTGRESQL
 │
 ├── Documents
 ├── Actions
 ├── Deadlines
 ├── Fees
 ├── Risks
 ├── Tasks
 └── Reminders
 │
 ▼
FASTAPI
 │
 ▼
FLUTTER APP
 │
 ▼
USER
```

---

# 15. Final Architecture Decision

The project will use **one fixed technology stack**.

| Component                         | Final Technology         |
| --------------------------------- | ------------------------ |
| Mobile Application                | Flutter + Dart           |
| Backend                           | Python + FastAPI         |
| AI / OCR / Document Understanding | Google Gemini API        |
| PDF Processing                    | PyMuPDF                  |
| DOC/DOCX Processing               | python-docx              |
| Image Preprocessing               | OpenCV                   |
| AI Response Validation            | Pydantic                 |
| Database                          | PostgreSQL               |
| Authentication                    | JWT                      |
| Notifications                     | Firebase Cloud Messaging |
| API Communication                 | REST API                 |

## Final Architecture

```text
┌───────────────────────┐
│     Flutter App       │
│       Dart            │
└───────────┬───────────┘
            │
         REST API
            │
            ▼
┌───────────────────────┐
│   Python + FastAPI    │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Document Processing   │
│                       │
│ PyMuPDF               │
│ python-docx           │
│ OpenCV                │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│     Gemini API        │
│                       │
│ OCR                   │
│ Understanding         │
│ Extraction            │
│ Reasoning             │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Pydantic Validation   │
│ + Business Rules      │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│      PostgreSQL       │
└───────────────────────┘
```

> **Architecture Principle:** The Flutter application is responsible for the mobile user interface, the FastAPI backend handles application logic and secure API communication, document-specific libraries handle preprocessing, Gemini performs AI-based document understanding and extraction, Pydantic validates AI output, and PostgreSQL stores the application's persistent data.
