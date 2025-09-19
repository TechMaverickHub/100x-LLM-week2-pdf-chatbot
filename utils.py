import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from fastapi import HTTPException, UploadFile

load_dotenv()

CHARS_PER_TOKEN = int(os.getenv("CHARS_PER_TOKEN", "4"))

def _estimate_tokens(text: str) -> int:
	return max(1, len(text) // CHARS_PER_TOKEN)

def _extract_text_from_pdf(upload: UploadFile) -> str:
	try:
		reader = PdfReader(upload.file)
		texts = []
		for page in reader.pages:
			content = page.extract_text() or ""
			texts.append(content)
		return "\n\n".join(texts).strip()
	except Exception as exc:
		raise HTTPException(status_code=422, detail="Could not process this PDF. Please try another file.") from exc