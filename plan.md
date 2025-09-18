## Chatbot From PDF – Implementation Plan

### 1) Overview
Build a chatbot that answers client questions strictly from an uploaded PDF feature document. The system extracts text from the PDF and uses an LLM to answer questions with that text as its sole context. If the answer is not present, the bot replies politely that the document does not contain the answer.

### 2) Scope
- In: single-PDF upload, text extraction, LLM responses grounded in PDF, simple Gradio UI, stateless API between sessions (single active PDF in memory).
- Out: non-PDF formats, multi-document memory, feature feasibility checks.

### 3) User Stories
- Client: upload a PDF and ask questions about the feature.
- Developer: responses must use the PDF as the single source of truth.
- Manager: fast answers without needing the team for routine questions.

### 4) Architecture Overview
- UI: Gradio app with two sections: upload panel, chat panel.
- Backend services (single app process):
  - PDF ingestion: PyPDF2 extracts text from uploaded PDF.
  - Context store: in-memory string (and optionally pre-chunked segments if needed later).
  - LLM service: Groq chat/completions API (model: llama-3.1-8b-instant) with a grounding prompt including PDF context.
  - API layer: two endpoints (`POST /upload-pdf`, `POST /ask`) exposed via Gradio function handlers and optionally FastAPI if needed; for this plan, Gradio endpoints suffice.

### 5) Tech Stack
- Python 3.10+
- PyPDF2 for extraction
- Groq Python SDK
- Gradio for UI
- Optional (later): FastAPI for a decoupled API, Redis for caching

### 6) API Design (logical)
- POST `/upload-pdf`
  - Input: PDF file (multipart/form-data)
  - Output: `{ "status": "processed" }`
  - Errors: 400 non-PDF, 413 too large, 422 extraction failure
- POST `/ask`
  - Input: `{ "question": "string" }`
  - Output: `{ "answer": "string" }`
  - Errors: 409 no PDF uploaded, 429 rate limit, 500 LLM failure

For the pilot, Gradio functions will implement the same semantics via UI callbacks. If later exposed as HTTP, mirror the signatures in FastAPI.

### 7) Data Flow
- Upload: PDF → PyPDF2 → extracted text (in memory) → status: processed
- Ask: question + PDF text → prompt assembly → Groq (llama-3.1-8b-instant) → grounded answer or fallback

### 8) Prompting Strategy
- System prompt: instruct the model to rely only on provided document context, refuse to fabricate, and cite “According to the document…” style phrasing.
- Context window: include the full extracted text when within size limits; otherwise, return “PDF too large, please shorten or split.” (v1)
- Fallback rule: if model likelihood is low or content not found, answer with the fallback message.

Suggested system prompt (concise):
```text
You are a helpful assistant that answers only using the provided DOCUMENT. If the DOCUMENT does not contain the answer, say: "The document does not contain that information."
Keep answers concise and quote/refer to relevant sections when helpful.
```

Message template for requests:
```text
[DOCUMENT]
{pdf_text}

[QUESTION]
{user_question}

[INSTRUCTIONS]
- Only answer using DOCUMENT.
- If unsure or not present, say it is not in the document.
```

### 9) UI/UX (Gradio)
- Screen 1: Upload
  - File upload component (PDF only)
  - Status indicator: “✅ PDF processed” or error text
- Screen 2: Chat
  - Chatbot component (history visible)
  - Textbox for new question
  - “Clear chat” button

Behavior:
- Disable chat input until a PDF is uploaded.
- Show brief spinner during LLM calls.

### 10) Error Handling
- No PDF uploaded → “Please upload a PDF first.”
- Non-PDF → “Only PDF files are supported.”
- PDF too large (heuristic: extracted text token estimate exceeds threshold) → “PDF too large, please shorten or split.”
- Extraction failure → “Could not process this PDF. Please try another file.”
- LLM error/timeouts → “We’re having trouble generating an answer. Please try again.”

### 11) Performance & Limits (v1)
- Token limit check: if `len(pdf_text)` or approximate tokens exceed threshold (e.g., ~8k tokens for llama-3.1-8b-instant), return too large error.
- Targets: ≤2s average latency (small docs). Caching not required in v1, can add later.

### 12) Security & Privacy
- Only non-sensitive PDFs should be used.
- No PII collection; no persistent storage in v1.
- Keep Groq API key in the `GROQ_API_KEY` environment variable.

### 13) Metrics & Acceptance Criteria
- KPIs:
  - ≥80% of questions answered directly from the PDF (manual eval set)
  - ≤2s average response time for small docs
  - 0 extraction errors for valid PDFs
- Acceptance:
  - Upload works and shows processed status
  - Multiple sequential questions work within one session
  - Fallback message appears when info isn’t in PDF

### 14) Implementation Steps
1) Project setup
- Create virtual env (already present) and install `PyPDF2`, `groq`, `gradio` (optional for token count).

2) PDF upload & extraction
- Validate file type is PDF.
- Extract text with PyPDF2, concatenate page texts.
- Store extracted text in a module-level variable or simple in-memory store.

3) LLM connection
- Read `GROQ_API_KEY` from env.
- Build prompt using system + context + question.
- Call Groq chat/completions API (model: llama-3.1-8b-instant), parse response.

4) Gradio UI
- Upload component → triggers extraction and sets a status state.
- Chatbot component → sends question to handler which uses in-memory text.
- Clear chat button → resets Gradio chat state.

5) Fallbacks & errors
- Guard clauses for missing PDF, over-size documents, and extraction/LLM errors.

6) Testing
- Use a few feature PDFs; craft a small eval set of Q&A.
- Verify latency, correctness, and fallbacks.

7) Pilot deployment
- Run as a Gradio app, optionally share link or run behind a simple reverse proxy.

### 15) Local Setup & Run
- Environment variables:
  - `GROQ_API_KEY`: required
- Install dependencies:
```bash
pip install PyPDF2 groq gradio 
```
- Run the app:
```bash
python app.py
```

### 16) Repository Structure (proposed)
```
/ (root)
  app.py                # Gradio app + handlers
  plan.md               # This plan
  requirements.txt      # Pinned deps (optional)
  README.md             # Quickstart
```

### 17) Dependencies (minimum)
- PyPDF2
- groq
- gradio
- tiktoken (optional; token counting)

### 18) Core Handlers (pseudocode)
```python
# state: pdf_text: str | None

def handle_upload(pdf_file) -> str:
    if not pdf_file or not pdf_file.name.lower().endswith(".pdf"):
        return "Only PDF files are supported."
    try:
        text = extract_text_with_pypdf2(pdf_file)
    except Exception:
        return "Could not process this PDF. Please try another file."
    if is_too_large(text):
        return "PDF too large, please shorten or split."
    set_pdf_text_in_memory(text)
    return "✅ PDF processed"


def handle_ask(question: str) -> str:
    text = get_pdf_text_in_memory()
    if not text:
        return "Please upload a PDF first."
    prompt = build_prompt(system_instructions, text, question)
    try:
        answer = call_groq(prompt, model="llama-3.1-8b-instant")
    except Exception:
        return "We’re having trouble generating an answer. Please try again."
    if not likely_grounded(answer):  # optional heuristic
        return "The document does not contain that information."
    return answer
```

### 19) Testing Plan
- Unit: test extraction on sample PDFs.
- Integration: upload then ask → validate correct answers.
- Negative: ask before upload, non-PDF upload, overly large document.
- Manual QA: example conversations from the spec.

### 20) Deployment Plan (pilot)
- Run Gradio app on an internal VM or dev machine.
- Optionally add FastAPI wrapper later if external API is needed.

### 21) Future Enhancements (not in v1)
- Chunking + retrieval (RAG) for longer PDFs instead of hard rejection.
- Source snippets/quotes and page references in answers.
- Persistent storage for documents per session/user.
- Auth and per-tenant isolation.
- Observability: logging, tracing, prompt/latency dashboards.
