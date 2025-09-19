import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from utils import _estimate_tokens, _extract_text_from_pdf

load_dotenv()

# Optional: lightweight token estimate to gate oversized PDFs
# Rough heuristic: ~4 characters per token
MAX_CONTEXT_TOKENS = int(os.getenv("MAX_CONTEXT_TOKENS", "8000"))

app = FastAPI(title="PDF-Grounded Chatbot API", version="0.1.0")

# In-memory store for the extracted PDF text (single active document)
_pdf_text: Optional[str] = None


class AskRequest(BaseModel):
	question: str


@app.get("/")
async def root():
	return {"status": "ok", "message": "PDF-Grounded Chatbot API"}


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
	global _pdf_text

	if not file or (not file.filename.lower().endswith(".pdf") and file.content_type != "application/pdf"):
		raise HTTPException(status_code=400, detail="Only PDF files are supported.")

	text = _extract_text_from_pdf(file)
	if not text:
		raise HTTPException(status_code=422, detail="Could not process this PDF. Please try another file.")

	if _estimate_tokens(text) > MAX_CONTEXT_TOKENS:
		raise HTTPException(status_code=413, detail="PDF too large, please shorten or split.")

	_pdf_text = text
	return JSONResponse(content={"status": "processed"})


@app.post("/ask")
async def ask(req: AskRequest):
	if not req.question or not req.question.strip():
		raise HTTPException(status_code=400, detail="Question must be provided.")

	if not _pdf_text:
		# Specified error handling message
		raise HTTPException(status_code=409, detail="Please upload a PDF first.")

	# Grounded prompting
	system_instructions = (
		"You are a helpful assistant that answers ONLY using the provided DOCUMENT. "
		"If the DOCUMENT does not contain the answer, reply exactly: "
		"'The document does not contain that information.' Keep answers concise."
	)

	prompt = (
		"[DOCUMENT]\n" + _pdf_text + "\n\n" +
		"[QUESTION]\n" + req.question.strip() + "\n\n" +
		"[INSTRUCTIONS]\n- Only answer using DOCUMENT.\n"
		"- If unsure or not present, say it is not in the document."
	)

	# Call OpenAI
	api_key = os.getenv("GROQ_API_KEY")
	if not api_key:
		# Return a descriptive error for missing key in development
		raise HTTPException(status_code=500, detail="Server configuration error: missing OPENAI_API_KEY.")

	try:
		# Lazy import to avoid hard dependency at import time
		from groq import Groq

		client = Groq(api_key=api_key)
		response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
				{"role": "system", "content": system_instructions},
				{"role": "user", "content": prompt},
			],
        temperature=0,
        max_completion_tokens=MAX_CONTEXT_TOKENS,
        top_p=1
    	)

		answer = (response.choices[0].message.content or "").strip()
		if not answer:
			answer = "The document does not contain that information."

		return JSONResponse(content={"answer": answer})
	except Exception as exc:
		# Generic failure path per plan
		raise HTTPException(status_code=500, detail="We’re having trouble generating an answer. Please try again.") from exc
