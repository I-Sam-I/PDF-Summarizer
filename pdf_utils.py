from PyPDF2 import PdfReader
from subprocess import run


def ocr_pdf(file: str) -> str:
    """
    Converts standard PDF to OCR PDF which can be read by PyPDF2.

    Args:
        file (str): The filename of the PDF.

    Returns:
        str: The filename of the OCR PDF.
    """
    
    # Convert PDF to OCR PDF using ocrmypdf in the terminal
    run(["ocrmypdf", file, file, "--deskew", "--skip-text", "--quiet"], check=True)
        
    return file


def get_pdf_text(file: str) -> list[str]:
    """
    Reads the text from a PDF file.

    Args:
        file (str): The filename of the PDF.

    Returns:
        list[str]: The text from the PDF per page.
    """
    
    reader = PdfReader(file)

    text = []
    for page in reader.pages:
        text.append(page.extract_text())
    
    return text

