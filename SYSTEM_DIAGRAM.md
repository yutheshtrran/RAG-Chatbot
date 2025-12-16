# RAG Chatbot System Diagram & Flow

## System Architecture

```
╔════════════════════════════════════════════════════════════════╗
║                        USER INTERFACE                           ║
║                  (Web Browser - React/Vite)                     ║
║                   http://127.0.0.1:5173                         ║
║                                                                  ║
║  ┌──────────────────────────────────────────────────────────┐  ║
║  │  Dashboard                                                │  ║
║  │  ├─ Chat Window (chatWindow.jsx)                         │  ║
║  │  │  ├─ Message display with markdown rendering          │  ║
║  │  │  ├─ Auto-scroll to latest messages                   │  ║
║  │  │  └─ Loading indicators                                │  ║
║  │  │                                                        │  ║
║  │  ├─ Patient Uploader (PatientUploader.jsx)              │  ║
║  │  │  ├─ Patient ID input                                  │  ║
║  │  │  ├─ File selection (TXT, PDF, CSV)                   │  ║
║  │  │  └─ Metadata input (name, age, gender)               │  ║
║  │  │                                                        │  ║
║  │  └─ Sidebar & Navigation                                 │  ║
║  │     ├─ Dashboard link                                    │  ║
║  │     ├─ Evaluation link                                   │  ║
║  │     └─ About link                                        │  ║
║  └──────────────────────────────────────────────────────────┘  ║
║                                                                  ║
║  API Client (api.js)                                            ║
║  ├─ sendMessage(userInput, patientId)                          ║
║  └─ uploadPatientFiles(patientId, name, age, gender, files)    ║
╚════════════════════════════════════════════════════════════════╝
                             ↑↓
                        HTTP Requests
                        (JSON/FormData)
                             ↓↑
╔════════════════════════════════════════════════════════════════╗
║                      BACKEND API SERVER                         ║
║                  (Flask - Python 3.8+)                          ║
║                   http://127.0.0.1:5000                         ║
║                                                                  ║
║  ┌──────────────────────────────────────────────────────────┐  ║
║  │  REST API Endpoints (routes.py)                          │  ║
║  │                                                            │  ║
║  │  GET  /api/health                                        │  ║
║  │  │    └─ Returns: {"status": "ok"}                       │  ║
║  │                                                            │  ║
║  │  POST /api/chat                                          │  ║
║  │  │    ├─ Input: {patient_id, message}                    │  ║
║  │  │    └─ Output: {reply: "AI generated answer"}          │  ║
║  │                                                            │  ║
║  │  POST /api/upload                                        │  ║
║  │       ├─ Input: FormData with files                      │  ║
║  │       └─ Output: {status, message}                       │  ║
║  └──────────────────────────────────────────────────────────┘  ║
║                             ↓                                   ║
║  ┌──────────────────────────────────────────────────────────┐  ║
║  │         RAG Chatbot Engine (chatbot_engine.py)           │  ║
║  │                                                            │  ║
║  │  ┌─────────────────────────────────────────────────────┐ │  ║
║  │  │ 1. Verify Patient Exists (db_handler.py)           │ │  ║
║  │  │    └─ Query SQLite database for patient            │ │  ║
║  │  └─────────────────────────────────────────────────────┘ │  ║
║  │                          ↓                                 │  ║
║  │  ┌─────────────────────────────────────────────────────┐ │  ║
║  │  │ 2. Retrieve Patient Context (retriever.py)         │ │  ║
║  │  │    ├─ Get all patient records from DB              │ │  ║
║  │  │    ├─ Convert question to embeddings               │ │  ║
║  │  │    │  └─ Using: sentence-transformers             │ │  ║
║  │  │    ├─ Compute cosine similarity                    │ │  ║
║  │  │    └─ Return top-3 most relevant documents         │ │  ║
║  │  └─────────────────────────────────────────────────────┘ │  ║
║  │                          ↓                                 │  ║
║  │  ┌─────────────────────────────────────────────────────┐ │  ║
║  │  │ 3. Generate Local Answer (if no Gemini)            │ │  ║
║  │  │    └─ Format retrieved documents as answer         │ │  ║
║  │  └─────────────────────────────────────────────────────┘ │  ║
║  │                          ↓                                 │  ║
║  │  ┌─────────────────────────────────────────────────────┐ │  ║
║  │  │ 4. Generate AI Response (Gemini API)               │ │  ║
║  │  │    ├─ Create prompt with retrieved context         │ │  ║
║  │  │    ├─ Call Google Gemini 2.5 Pro                   │ │  ║
║  │  │    └─ Return formatted markdown response           │ │  ║
║  │  └─────────────────────────────────────────────────────┘ │  ║
║  │                          ↓                                 │  ║
║  │  ┌─────────────────────────────────────────────────────┐ │  ║
║  │  │ 5. Return Response to Frontend                     │ │  ║
║  │  │    └─ {reply: "formatted AI answer"}               │ │  ║
║  │  └─────────────────────────────────────────────────────┘ │  ║
║  └──────────────────────────────────────────────────────────┘  ║
║                             ↓                                   ║
║  ┌──────────────────────────────────────────────────────────┐  ║
║  │         DATA LAYER - Database & Files                    │  ║
║  │                                                            │  ║
║  │  SQLite Database (patient_records.db)                     │  ║
║  │  ├─ patients table                                        │  ║
║  │  │  └─ patient_id, name, age, gender                     │  ║
║  │  │                                                        │  ║
║  │  └─ records table                                         │  ║
║  │     ├─ record_id, patient_id, filename, content          │  ║
║  │     └─ timestamp, foreign key to patients                │  ║
║  │                                                            │  ║
║  │  File Storage                                             │  ║
║  │  └─ /backend/data/uploads/                               │  ║
║  │     └─ {patient_id}_{filename}                           │  ║
║  └──────────────────────────────────────────────────────────┘  ║
╚════════════════════════════════════════════════════════════════╝
             ↓↑                      ↓↑
         EMBEDDINGS               GEMINI API
             ↓↑                      ↓↑
╔═══════════════════════╗  ╔═══════════════════════╗
║ sentence-transformers ║  ║  Google Gemini 2.5    ║
║ all-MiniLM-L6-v2      ║  ║  Pro API              ║
║                       ║  ║                       ║
║ - 384-dim vectors     ║  ║ - Medical knowledge   ║
║ - Fast inference      ║  ║ - Context awareness   ║
║ - Good semantics      ║  ║ - Markdown support    ║
╚═══════════════════════╝  ╚═══════════════════════╝
```

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INPUT                                    │
│  Example: "Patient 001 what is their diagnosis?"                 │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│               FRONTEND PROCESSING (React)                        │
│  - Extract patient ID: "001"                                     │
│  - Extract message: "what is their diagnosis?"                   │
│  - Send API request to backend                                   │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│              BACKEND RECEIVES REQUEST                            │
│  POST /api/chat                                                  │
│  {                                                               │
│    "patient_id": "001",                                          │
│    "message": "what is their diagnosis?"                         │
│  }                                                               │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│           STEP 1: VERIFY PATIENT EXISTS                          │
│                                                                  │
│  Query: SELECT * FROM patients WHERE patient_id = '001'         │
│  Result: ✓ Patient found                                        │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│        STEP 2: RETRIEVE PATIENT RECORDS                          │
│                                                                  │
│  Query: SELECT content FROM records WHERE patient_id = '001'    │
│  Result: [                                                       │
│    "Patient medical history...",                                │
│    "Lab results...",                                            │
│    "Medications..."                                             │
│  ]                                                               │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│      STEP 3: CONVERT TO EMBEDDINGS (sentence-transformers)      │
│                                                                  │
│  Question:                                                       │
│  "what is their diagnosis?" → [0.123, -0.456, ..., 0.789]      │
│  (384-dimensional vector)                                       │
│                                                                  │
│  Patient Records:                                                │
│  "Patient medical history..." → [0.112, -0.478, ..., 0.801]    │
│  "Lab results..." → [0.089, -0.512, ..., 0.742]                │
│  "Medications..." → [0.145, -0.401, ..., 0.823]                │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│     STEP 4: SEMANTIC SIMILARITY SEARCH (Cosine Similarity)      │
│                                                                  │
│  Compare question embedding with each patient record:           │
│  - "Patient medical history...": similarity = 0.87 ⭐⭐⭐ TOP-1 │
│  - "Medications...": similarity = 0.72 ⭐⭐ TOP-2             │
│  - "Lab results...": similarity = 0.68 ⭐⭐ TOP-3             │
│                                                                  │
│  Return top-3 documents with highest similarity                │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│     STEP 5: AUGMENT PROMPT WITH RETRIEVED CONTEXT               │
│                                                                  │
│  Create prompt:                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ You are a clinical assistant AI.                        │   │
│  │                                                          │   │
│  │ Internal patient records:                               │   │
│  │ - Patient medical history: [retrieved text]             │   │
│  │ - Medications: [retrieved text]                         │   │
│  │ - Lab results: [retrieved text]                         │   │
│  │                                                          │   │
│  │ Question: what is their diagnosis?                      │   │
│  │                                                          │   │
│  │ Provide a clear, structured answer in Markdown.        │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│          STEP 6: CALL GEMINI API FOR GENERATION                 │
│                                                                  │
│  API Call:                                                       │
│  genai.GenerativeModel("models/gemini-2.5-pro")                │
│  model.generate_content(prompt)                                 │
│                                                                  │
│  Gemini processes:                                              │
│  - Analyzes retrieved patient records                           │
│  - Applies medical knowledge                                    │
│  - Generates contextual answer                                  │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│              STEP 7: FORMAT RESPONSE                             │
│                                                                  │
│  Gemini Output (Markdown):                                       │
│  "Based on patient 001's records:                               │
│                                                                  │
│   **Primary Diagnosis**: Type 2 Diabetes                        │
│   - Diagnosed: 2015                                             │
│   - Recent HbA1c: 7.2%                                          │
│                                                                  │
│   **Secondary Conditions**:                                    │
│   - Hypertension                                                │
│   - High Cholesterol                                            │
│   - Previous cardiac event (2020)                               │
│                                                                  │
│   **Current Treatment**:                                        │
│   - Metformin 1000mg twice daily                                │
│   - Lisinopril 10mg daily                                       │
│   - Atorvastatin 40mg daily                                     │
│   - Aspirin 100mg daily"                                        │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│              RETURN RESPONSE TO FRONTEND                         │
│                                                                  │
│  HTTP 200 OK                                                     │
│  {                                                               │
│    "reply": "Based on patient 001's records: ..."              │
│  }                                                               │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│         FRONTEND PROCESSES & DISPLAYS RESPONSE                   │
│                                                                  │
│  1. Receives JSON response                                      │
│  2. Parses markdown content                                     │
│  3. Renders in ChatWindow component                             │
│  4. Displays with formatting:                                   │
│     - Bold text                                                 │
│     - Lists                                                     │
│     - Proper spacing                                            │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                  USER SEES ANSWER                                │
│                                                                  │
│  Chat Window displays:                                           │
│                                                                  │
│  User: "Patient 001 what is their diagnosis?"                   │
│                                                                  │
│  Bot: Based on patient 001's records:                           │
│       **Primary Diagnosis**: Type 2 Diabetes                    │
│       - Diagnosed: 2015                                         │
│       - Recent HbA1c: 7.2%                                      │
│       ... [full formatted response]                             │
│                                                                  │
│  Total Response Time: 3-6 seconds                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## File Upload Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER UPLOADS FILES                            │
│  Dashboard → "Upload Patient Records"                            │
│  - Patient ID: "001"                                             │
│  - Name: "John Doe"                                              │
│  - Age: 55                                                       │
│  - Gender: "Male"                                                │
│  - Files: [medical_history.txt, lab_results.pdf]                │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│        FRONTEND PREPARES UPLOAD (React + api.js)                │
│                                                                  │
│  1. Create FormData object                                      │
│  2. Add patient info fields                                     │
│  3. Add files to FormData                                       │
│  4. Send to POST /api/upload                                    │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│          BACKEND PROCESSES UPLOAD (routes.py)                   │
│                                                                  │
│  1. Extract patient_id from form data                           │
│  2. Extract optional: name, age, gender                         │
│  3. Get uploaded files from request                             │
│  4. Validate inputs                                             │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│     CREATE PATIENT IN DATABASE (if not exists)                  │
│                                                                  │
│  Query:                                                          │
│  INSERT OR IGNORE INTO patients                                │
│  VALUES ('001', 'John Doe', 55, 'Male')                        │
│                                                                  │
│  Result: ✓ Patient created/verified                            │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│          PROCESS EACH UPLOADED FILE                              │
│                                                                  │
│  For each file:                                                 │
│  1. Validate filename (secure_filename)                        │
│  2. Check file extension (.txt, .pdf, .csv)                    │
│  3. Save to /backend/data/uploads/{patient_id}_{filename}      │
│  4. Read file content                                           │
│  5. Store in database                                           │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│         STORE IN DATABASE (db_handler.py)                       │
│                                                                  │
│  For each file:                                                 │
│  INSERT INTO records                                            │
│  (patient_id, filename, content, timestamp)                    │
│  VALUES ('001', 'medical_history.txt', [content], NOW)         │
│                                                                  │
│  Result: ✓ Records created                                     │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│              RETURN SUCCESS RESPONSE                             │
│                                                                  │
│  HTTP 200 OK                                                     │
│  {                                                               │
│    "status": "success",                                          │
│    "message": "Files uploaded for patient 001:                 │
│               medical_history.txt, lab_results.pdf"            │
│  }                                                               │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│         FRONTEND SHOWS SUCCESS MESSAGE                           │
│                                                                  │
│  Display: "✓ Successfully uploaded 2 files for patient 001"    │
│                                                                  │
│  User can now ask questions about this patient                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## RAG Pipeline Components

```
┌────────────────────────────────────────────────────────────────────────┐
│                          RAG PIPELINE                                   │
│                   (Retrieval-Augmented Generation)                      │
└────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ RETRIEVAL                                                        │
│ ─────────────────────────────────────────────────────────────── │
│                                                                  │
│ Input: Question (string)                                        │
│ ├─ "What is their diagnosis?"                                   │
│ │                                                                │
│ ├─ Convert to embeddings (sentence-transformers)               │
│ │  └─ Output: [0.123, -0.456, ..., 0.789] (384-dim vector)    │
│ │                                                                │
│ ├─ Load patient records from database                          │
│ │  └─ "Type 2 Diabetes diagnosed 2015..."                     │
│ │  └─ "Lab results show elevated glucose..."                  │
│ │  └─ "Current medications: Metformin..."                     │
│ │                                                                │
│ ├─ Convert each record to embeddings                           │
│ │  └─ Multiple 384-dim vectors                                │
│ │                                                                │
│ ├─ Calculate cosine similarity (numpy)                         │
│ │  ├─ Question embedding vs Record 1: 0.87                    │
│ │  ├─ Question embedding vs Record 2: 0.72                    │
│ │  └─ Question embedding vs Record 3: 0.68                    │
│ │                                                                │
│ └─ Output: Top-3 most relevant documents                       │
│    [retrieved_doc_1, retrieved_doc_2, retrieved_doc_3]         │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│ AUGMENTATION                                                     │
│ ─────────────────────────────────────────────────────────────── │
│                                                                  │
│ Input: Original question + Retrieved documents                 │
│                                                                  │
│ Create enhanced prompt:                                         │
│ ┌─────────────────────────────────────────────────────────┐   │
│ │ You are a clinical assistant AI.                        │   │
│ │ Base your answer PRIMARILY on the provided records,    │   │
│ │ then supplement with general knowledge.                │   │
│ │                                                          │   │
│ │ Internal patient records:                               │   │
│ │ [retrieved_doc_1 content]                              │   │
│ │ [retrieved_doc_2 content]                              │   │
│ │ [retrieved_doc_3 content]                              │   │
│ │                                                          │   │
│ │ Question: What is their diagnosis?                     │   │
│ │                                                          │   │
│ │ Provide a clear, structured answer in Markdown.        │   │
│ └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│ Output: Augmented prompt ready for LLM                         │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│ GENERATION                                                       │
│ ─────────────────────────────────────────────────────────────── │
│                                                                  │
│ Input: Augmented prompt                                        │
│                                                                  │
│ Process:                                                         │
│ 1. Send to Google Gemini 2.5 Pro API                           │
│ 2. Gemini reads augmented prompt with context                  │
│ 3. Generates response:                                          │
│    - Analyzes retrieved patient records                         │
│    - Applies medical knowledge                                  │
│    - Creates structured answer                                  │
│    - Formats with Markdown                                      │
│                                                                  │
│ Output: AI-generated answer with sources                       │
│ ────────────────────────────────────────────────────────────── │
│ "Based on patient 001's records:                               │
│                                                                  │
│  **Primary Diagnosis**: Type 2 Diabetes                         │
│  - Diagnosed: 2015                                              │
│  - Control: Moderate (HbA1c 7.2%)                              │
│                                                                  │
│  **Secondary Conditions**:                                     │
│  - Hypertension (BP 145/92)                                    │
│  - Hyperlipidemia (Cholesterol 215)                            │
│  - History of MI (2020)                                        │
│                                                                  │
│  **Current Medications**:                                      │
│  - Metformin 1000mg BID                                        │
│  - Lisinopril 10mg daily                                       │
│  - Atorvastatin 40mg daily                                     │
│  - Aspirin 100mg daily                                         │
│                                                                  │
│  **Recommendations**: Continue current medications...          │
│ ────────────────────────────────────────────────────────────── │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│ FINAL OUTPUT                                                     │
│ ─────────────────────────────────────────────────────────────── │
│                                                                  │
│ Formatted response sent to frontend                            │
│ Rendered in chat window with markdown formatting               │
│ User sees professional, structured answer                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

```
FRONTEND LAYER
├─ React 19.1.1 (UI Framework)
├─ Vite 7.1.7 (Build tool)
├─ React Router 7.9.4 (Navigation)
├─ Axios 1.13.1 (HTTP client)
├─ Tailwind CSS 4.1.15 (Styling)
├─ React Markdown 10.1.0 (Markdown rendering)
└─ Lucide React 0.546.0 (Icons)

BACKEND LAYER
├─ Flask 3.0.0 (Web framework)
├─ Flask-CORS 4.0.0 (Cross-origin support)
└─ Python-dotenv 1.0.0 (Environment variables)

AI/ML LAYER
├─ sentence-transformers 2.2.2 (Embeddings)
│  └─ Model: all-MiniLM-L6-v2 (384-dim)
├─ google-generativeai 0.3.0 (Gemini API)
│  └─ Model: gemini-2.5-pro
├─ numpy 1.24.3 (Numerical computation)
└─ faiss-cpu 1.7.4 (Vector search - optional)

DATA LAYER
├─ SQLite 3 (Database)
└─ File system (Document storage)

UTILITIES
├─ pdfplumber 0.10.3 (PDF parsing)
└─ python-magic-bin 0.4.14 (File detection)
```

---

**This diagram shows how all components work together to provide intelligent, context-aware answers about patient medical records!**
