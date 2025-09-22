from enum import Enum


class SuccessMessage(str, Enum):
    """Success messages used across the application."""

    # Generic
    ANSWER_GENERATED = "Answer generated successfully."
    PDF_PROCESSED = "PDF processed successfully."
    API_HEALTHY = "PDF-Grounded Chatbot API is healthy."


class ErrorMessage(str, Enum):
    """Error messages used across the application."""

    # Generic
    BAD_REQUEST = "Bad request."
    CONFLICT = "Conflict."
    INTERNAL_SERVER_ERROR = "Internal server error."
    NOT_FOUND = "Resource not found."
    SOMETHING_WENT_WRONG = "Something went wrong, please try again."
    UNPROCESSABLE_ENTITY = "Unprocessable entity."

    # App specific
    ANSWER_GENERATION_FAILED = "We’re having trouble generating an answer. Please try again."
    ONLY_PDF_SUPPORTED = "Only PDF files are supported."
    PDF_NOT_UPLOADED = "Please upload a PDF first."
    PDF_PROCESSING_FAILED = "Could not process this PDF. Please try another file."
    PDF_TOO_LARGE = "PDF too large, please shorten or split."
    QUESTION_REQUIRED = "Question must be provided."
    SERVER_MISCONFIGURED = "Server configuration error: missing GROQ_API_KEY."
