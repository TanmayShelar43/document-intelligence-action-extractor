DOCUMENT 1 — PRD
Document Intelligence & Action Extractor
1. Product Overview
Product Name: Document Intelligence & Action Extractor
Platform: Mobile Application
Purpose:
An AI-powered mobile application that analyzes uploaded documents and automatically identifies important information, required actions, deadlines, fees, people, required documents, and risks.
The application then converts actionable information into tasks and reminders, helping users avoid missing important deadlines.
Core Idea
Upload Document
       ↓
Understand Document
       ↓
Extract Important Information
       ↓
Identify Actions & Deadlines
       ↓
User Reviews Results
       ↓
Create Tasks
       ↓
Set Reminders
________________________________________
2. Problem Statement
Important information is often hidden inside long documents such as:
•	College notices 
•	Government notices 
•	Circulars 
•	Bills 
•	Application forms 
•	Contracts 
•	Policies 
•	Official letters 
•	Scanned documents 
Users may read the document but still miss:
•	Deadlines 
•	Required actions 
•	Fees 
•	Required documents 
•	Penalties 
•	Important conditions 
•	People they need to contact 
•	Risks 
Example
A college notice says:
Students must submit the examination form before 23 August 2026. The examination fee is ₹1,250. Late submissions will attract a penalty of ₹500.
The application automatically identifies:
Action:
Submit examination form

Deadline:
23 August 2026

Fee:
₹1,250

Risk:
₹500 late penalty
The user can then create a task:
Submit Examination Form — Due 23 August
________________________________________
3. Product Vision
The application should answer:
"I uploaded this document. What is important, and what do I need to do?"
The product is not a normal PDF summarizer.
Its primary purpose is to transform unstructured documents into actionable information.
Product Flow
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
________________________________________
4. Target Users
Students
•	College notices 
•	Exam forms 
•	Scholarship notices 
•	Assignment notices 
•	Admission documents 
Employees
•	HR circulars 
•	Company policies 
•	Internal notices 
•	Compliance documents 
Professionals
•	Contracts 
•	Business documents 
•	Financial documents 
•	Government documents 
General Users
•	Bills 
•	Application forms 
•	Insurance documents 
•	Official letters 
•	Scanned documents 
________________________________________
5. Supported Documents
The application must support:
PDF
•	Text-based PDFs 
•	Scanned PDFs 
•	Multi-page PDFs 
•	PDFs containing images 
•	PDFs containing tables 
DOC / DOCX
•	Text documents 
•	Tables 
•	Headings 
•	Structured documents 
Images
•	JPG 
•	JPEG 
•	PNG 
•	WEBP 
•	HEIC 
Camera Documents
Users can capture documents using the phone camera.
________________________________________
6. Document Upload
Users can upload documents from:
•	Device storage 
•	Gallery 
•	Camera 
•	Mobile share functionality 
The application should display:
Document Name
File Type
File Size
Processing Status
Example:
Exam_Notice.pdf

Analyzing...

✓ Document uploaded
✓ Document processed
✓ Information extracted
✓ Actions identified
________________________________________
7. Document Processing
The application must automatically process the uploaded document.
                DOCUMENT
                    │
                    ▼
             File Validation
                    │
                    ▼
             File Type Detection
                    │
                    ▼
        ┌───────────┼───────────┐
        │           │           │
       PDF        DOC/DOCX     IMAGE
        │           │           │
        ▼           ▼           ▼
     Gemini      Gemini      Gemini
        │           │           │
        └───────────┼───────────┘
                    ▼
          Document Understanding
                    │
                    ▼
           Structured Information
The system must not require a separate OCR installation.
________________________________________
8. OCR & Document Understanding
OCR Technology
Google Gemini API
Gemini will be responsible for:
•	Reading scanned documents 
•	Reading images 
•	Understanding document content 
•	Extracting text 
•	Understanding layout 
•	Understanding tables 
•	Identifying relevant information 
This removes the requirement for a locally installed OCR engine.
Processing principle
PDF / Image
     ↓
Gemini API
     ↓
Text + Visual Understanding
     ↓
Structured Information
The system should preserve the original document and its page/source information so extracted information can be verified.
________________________________________
9. AI Analysis
After the document is processed, Gemini analyzes its content.
The system must extract:
1.	Summary 
2.	Key information 
3.	Required actions 
4.	Deadlines 
5.	Fees 
6.	Required documents 
7.	People 
8.	Organizations 
9.	Risks 
10.	Warnings 
11.	Important conditions 
12.	Source references 
________________________________________
10. Summary Extraction
The application should generate a short, useful summary.
Example
Students must submit the examination form by 23 August 2026 and pay a ₹1,250 examination fee. Late submission may result in a ₹500 penalty.
The summary should focus on important information instead of generating unnecessary paragraphs.
________________________________________
11. Action Extraction
The system must identify actions that the user is required to perform.
Examples
•	Submit 
•	Apply 
•	Register 
•	Pay 
•	Upload 
•	Attend 
•	Sign 
•	Verify 
•	Contact 
•	Complete 
•	Renew 
•	Respond 
Example
Document:
Students must upload their Aadhaar Card and Income Certificate.
AI output:
Required Actions

1. Upload Aadhaar Card
2. Upload Income Certificate
________________________________________
12. Deadline Extraction
The system must identify:
Exact deadlines
23 August 2026
Date ranges
20 August – 25 August 2026
Relative deadlines
Within 7 days
Conditional deadlines
Within 15 days of receiving the notice
The system must not invent an exact date if the document does not provide enough information to calculate one.
________________________________________
13. Fee Extraction
The system must identify financial information such as:
•	Application fee 
•	Registration fee 
•	Examination fee 
•	Late fee 
•	Penalty 
•	Deposit 
•	Other charges 
Example:
Examination Fee
₹1,250

Late Fee
₹500
Each fee must contain its purpose and source.
________________________________________
14. Required Document Extraction
The system must identify documents that the user needs to submit.
Example:
Required Documents

• Aadhaar Card
• Income Certificate
• Previous Marksheet
• Passport Photograph
The user should be able to convert these into tasks.
________________________________________
15. People & Organization Extraction
The system should identify:
•	People 
•	Departments 
•	Organizations 
•	Contact persons 
•	Authorities 
•	Responsible parties 
Example:
Contact Person:
Dr. Rahul Sharma

Department:
Examination Department

Organization:
ABC University
________________________________________
16. Risk Detection
The system must identify consequences and warnings.
Example
Document:
Applications submitted after the deadline will not be accepted.
Application:
⚠ Risk

Late submission may result
in application rejection.
Other risks include:
•	Late fees 
•	Penalties 
•	Rejection 
•	Cancellation 
•	Missing documents 
•	Compliance issues 
•	Important conditions 
________________________________________
17. Source Traceability
Every extracted important item must contain a source reference.
Example:
Submit Examination Form

Deadline:
23 August 2026

Source:
Exam_Notice.pdf
Page 3

[View Source]
When the user selects View Source, the application should open the corresponding document page.
This allows users to verify AI-generated information.
________________________________________
18. AI Confidence & Verification
The application must not blindly trust AI output.
Each important extraction should contain a confidence level.
✓ High Confidence

Deadline:
23 August 2026
If information is uncertain:
⚠ Needs Verification

Possible Deadline:
23 August 2026

[View Source]
Low-confidence information must not automatically create an active reminder.
The user must confirm it first.
________________________________________
19. Task Creation
Users can convert extracted actions into tasks.
Example:
Submit Examination Form

Due:
23 August 2026

Priority:
High

Source:
Exam_Notice.pdf — Page 3

[Create Task]
Task fields:
•	Title 
•	Description 
•	Deadline 
•	Priority 
•	Status 
•	Source document 
•	Source page 
________________________________________
20. Reminder System
Users can create reminders for tasks.
Supported reminder timings:
•	1 day before 
•	2 days before 
•	3 days before 
•	1 week before 
•	Custom date/time 
Example:
Task:
Submit Examination Form

Deadline:
23 August

Reminder:
21 August — 9:00 AM
________________________________________
21. Home Screen
The home screen should show the user's most important information.
Good Evening 👋

What do you need to do?

[ + Analyze Document ]


Upcoming

🔴 Submit Exam Form
   Due Tomorrow

🟡 Scholarship Application
   Due 30 Aug


Recent Documents

Exam Notice.pdf
Scholarship Notice.pdf
College Circular.pdf
________________________________________
22. Documents Screen
Users can view all uploaded documents.
Each document displays:
•	Name 
•	Date 
•	Type 
•	Processing status 
•	Number of extracted actions 
Example:
Exam_Notice.pdf
Analyzed Today
3 Actions
2 Deadlines
2 Fees
________________________________________
23. Tasks Screen
Tasks should be organized into:
Today
Tasks due today.
Upcoming
Future tasks.
Overdue
Tasks whose deadline has passed.
Completed
Finished tasks.
Users can:
•	Complete task 
•	Edit task 
•	Delete task 
•	Change deadline 
•	Change priority 
•	View source document 
________________________________________
24. Document Detail Screen
The document detail screen contains:
Overview
────────────

Summary

Actions
────────────

Deadlines
────────────

Fees
────────────

Required Documents
────────────

People
────────────

Risks
────────────

Source
────────────
________________________________________
25. Notifications
The application must notify users about:
•	Upcoming deadlines 
•	Overdue tasks 
•	Important tasks 
•	Completed document processing 
Example:
🔔 Your examination form deadline is tomorrow.
________________________________________
26. Error Handling
The application must never silently generate incorrect information.
If processing fails:
Unable to fully analyze this document.

The document could not be reliably processed.

[Try Again]
[Upload Another Document]
If only some pages are successfully processed:
Document Partially Analyzed

Pages 1–8 were processed successfully.

Pages 9–12 require verification.

[Review Pages]
The system must never fabricate information to compensate for missing or unreadable content.
________________________________________
27. Privacy & Security
Documents may contain sensitive personal information.
Requirements:
•	Secure document transmission 
•	User authentication 
•	User-specific document access 
•	Secure Gemini API communication 
•	Document deletion 
•	Secure backend API 
Critical Requirement
The Gemini API key must never be stored inside the Flutter mobile application.
It must remain on the backend.
________________________________________
28. MVP Scope
Input
•	PDF 
•	DOC 
•	DOCX 
•	JPG 
•	JPEG 
•	PNG 
•	WEBP 
•	HEIC 
AI Processing
•	Document understanding 
•	OCR 
•	Summary 
•	Actions 
•	Deadlines 
•	Fees 
•	Required documents 
•	People 
•	Risks 
•	Source references 
•	Confidence 
App Features
•	Authentication 
•	Upload document 
•	Document history 
•	Document analysis 
•	Task creation 
•	Task management 
•	Reminders 
•	Notifications 
•	Source verification 
________________________________________
29. Core User Journey
Open App
   ↓
Upload / Scan Document
   ↓
Document Processing
   ↓
AI Analysis
   ↓
View Summary
   ↓
Review Actions
   ↓
Review Deadlines
   ↓
Review Fees & Risks
   ↓
Create Tasks
   ↓
Set Reminders
   ↓
Receive Notification
   ↓
Complete Task

