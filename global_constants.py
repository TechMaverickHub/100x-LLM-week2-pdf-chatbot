from enum import Enum


class SuccessMessage(str, Enum):
    # Generic CRUD
    RECORD_CREATED = "Record created successfully."
    RECORD_RETRIEVED = "Record retrieved successfully."
    RECORD_UPDATED = "Record updated successfully."
    RECORD_DELETED = "Record deleted successfully."

    # Auth
    CREDENTIALS_MATCHED = "Login successful."
    CREDENTIALS_REMOVED = "Logout successful."

    # App specific
    API_HEALTHY = "PDF-Grounded Chatbot API is healthy."
    PDF_PROCESSED = "PDF processed successfully."
    ANSWER_GENERATED = "Answer generated successfully."


class ErrorMessage(str, Enum):
    # Generic
    SOMETHING_WENT_WRONG = "Something went wrong, please try again."
    BAD_REQUEST = "Bad request."
    FORBIDDEN = "Not Authorized."
    NOT_FOUND = "Resource not found."
    UNAUTHORIZED = "Not Authenticated."
    CONFLICT = "Conflict."
    UNPROCESSABLE_ENTITY = "Unprocessable entity."
    PAYLOAD_TOO_LARGE = "Payload too large."
    INTERNAL_SERVER_ERROR = "Internal server error."

    # Validation/auth specifics
    PASSWORD_MISMATCH = "Password Mismatch."
    MISSING_FIELDS = "Fields Missing"
    THROTTLE_LIMIT_EXCEEDED = "Throttle Limit Exceeded"

    # Domain examples
    CATEGORY_NOT_FOUND = "Category not found"
    POST_ALREADY_LIKE = "Post already liked"

    # App specific
    ONLY_PDF_SUPPORTED = "Only PDF files are supported."
    PDF_PROCESSING_FAILED = "Could not process this PDF. Please try another file."
    PDF_TOO_LARGE = "PDF too large, please shorten or split."
    PDF_NOT_UPLOADED = "Please upload a PDF first."
    QUESTION_REQUIRED = "Question must be provided."
    SERVER_MISCONFIGURED = "Server configuration error: missing GROQ_API_KEY."
    ANSWER_GENERATION_FAILED = "We’re having trouble generating an answer. Please try again."


