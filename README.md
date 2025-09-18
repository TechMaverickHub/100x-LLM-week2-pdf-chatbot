# 📄 PDF Chatbot – 100x-week2-LLM

A FastAPI-based chatbot that answers client questions **only from an uploaded PDF document**.  
It uses **PyPDF2** for text extraction and **Groq’s LLaMA-3.1** model for generating grounded responses.  
If the PDF does not contain the answer, the bot responds with:  
> "The document does not contain that information."

---

## 🚀 Features
- Upload a single PDF file
- Extracts and stores text in memory
- Ask natural language questions grounded strictly in the uploaded PDF
- Returns polite fallback when information is missing
- Token-size check to prevent oversized PDFs

---

## 🛠️ Tech Stack
- **FastAPI** (backend API)
- **PyPDF2** (PDF text extraction)
- **Groq LLaMA-3.1** (LLM responses)
- **Uvicorn** (ASGI server)
- **Python-dotenv** for environment configuration

---

## 📂 Project Structure
```
/ (root)
  ├── app.py          # FastAPI app with endpoints
  ├── plan.md         # Detailed implementation plan
  ├── req.txt         # Dependencies
  └── README.md       # This file
```

---

## ⚡ API Endpoints

### Root
```http
GET /
```
**Response**
```json
{"status": "ok", "message": "PDF-Grounded Chatbot API"}
```

### Upload PDF
```http
POST /upload-pdf
```
- Input: PDF file (`multipart/form-data`)
- Output: `{ "status": "processed" }`

### Ask a Question
```http
POST /ask
```
- Input: `{ "question": "string" }`
- Output: `{ "answer": "string" }`

---

## ⚙️ Setup & Run

### 1. Clone the Repo
```bash
git clone https://github.com/your-username/pdf-chatbot-100x.git
cd pdf-chatbot-100x
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

pip install -r req.txt
```

### 3. Set Environment Variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
MAX_CONTEXT_TOKENS=8000
```

### 4. Run the Server
```bash
uvicorn app:app --reload
```

Server will be live at:  
👉 [http://localhost:8000](http://localhost:8000)

---

## 📖 Example Usage

1. Upload a PDF using `/upload-pdf`  
2. Ask questions using `/ask`

```json
POST /ask
{
  "question": "What features does this product support?"
}
```

**Response**
```json
{
  "answer": "According to the document, the product supports..."
}
```

## 🖼️ Screenshots

### Swagger 
![Upload PDF](screenshots\screenshot1.png)

### Upload Response
![Upload PDF](screenshots\screenshot2.png)

### Chat Response
![Chat with PDF](screenshots\screenshot3.png)

---

## 📊 Future Enhancements
- Multi-document support (RAG-style retrieval)
- Persistent storage for PDFs
- Chunking + embeddings for large documents
- Quote + page references in answers
- Gradio or Streamlit UI for end-users

---

## 🏗️ Credits
- Part of the **#0to100xEngineer** journey
- Built with ❤️ using FastAPI + Groq LLaMA-3.1
