
from io import BytesIO
from pathlib import PurePath

import pymupdf

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}


def extract_text(filename: str, content: bytes) -> str:
    extension = PurePath(filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError("Unsupported file type. Upload PDF, TXT, or MD.")

    if not content:
        raise ValueError("The uploaded file is empty.")

    if extension == ".pdf":
        try:
            with pymupdf.open(stream=BytesIO(content), filetype="pdf") as pdf:
                if pdf.needs_pass:
                    raise ValueError("Password-protected PDFs are not supported.")

                text = "\n".join(page.get_text() for page in pdf)
        except ValueError:
            raise
        except Exception as exc:
            raise ValueError("Unable to read this PDF file.") from exc
    else:
        try:
            text = content.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise ValueError("Text files must use UTF-8 encoding.") from exc

    text = text.replace("\x00", "").strip()

    if not text:
        raise ValueError(
            "No extractable text found. Scanned PDFs require OCR, "
            "which is not included in this phase."
        )

    return text
