from argparse import ArgumentParser, Namespace
from PyPDF2 import PdfReader
from os import system


def get_args() -> Namespace:
    """Creates an argument parser and returns the args

    Returns:
        Namespace: The "list" of arguments
    """
    parser = ArgumentParser(prog="main", description="Read a PDF contents to a TXT")

    parser.add_argument('input_pdf', type=str, nargs=1, help="Input PDF file")
    parser.add_argument('output_txt', type=str, nargs='*', default="output.txt", help="Output TXT file")

    return parser.parse_args()


def get_pdf_text(file: str) -> str:
    """Reads the text from a PDF/A file

    Args:
        file (str): The filename of the PDF/A

    Returns:
        str: The text from the PDF/A
    """
    reader = PdfReader(OCR_pdf(file))
    
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    return text


def OCR_pdf(file: str) -> str:
    """Converts standard PDF to OCR PDF/A which can be read by PyPDF2

    Args:
        file (str): The filename of the PDF/A

    Returns:
        str: The filename of the OCR PDF/A
    """
    system(f"ocrmypdf '{file}' '{file}' --deskew")
    return file
