import collections 
try:
    from collections.abc import MutableSet, MutableMapping
    collections.MutableSet = MutableSet
    collections.MutableMapping = MutableMapping
except Exception:
    from collections import MutableSet, MutableMapping

from argparse import ArgumentParser, Namespace
from PyPDF2 import PdfReader
from os import system, getenv
import openai
from dotenv import load_dotenv


def get_args() -> Namespace:
    """Creates an argument parser and returns the args

    Returns:
        Namespace: The "list" of arguments
    """
    parser = ArgumentParser(prog="summarizer", description="Read a PDF contents to a TXT")

    parser.add_argument('input_pdf', type=str, nargs=1, help="Input PDF file")
    parser.add_argument('output_txt', type=str, nargs='*', default="output.txt", help="Output TXT file")

    return parser.parse_args()


def OCR_pdf(file: str) -> str:
    """Converts standard PDF to OCR PDF/A which can be read by PyPDF2

    Args:
        file (str): The filename of the PDF/A

    Returns:
        str: The filename of the OCR PDF/A
    """
    print(f"OCR'ing {file}")
    system(f"ocrmypdf '{file}' '{file}' --deskew --skip-text --quiet")
    print(f"OCR'd {file}")
    return file


def get_pdf_text(file: str) -> str:
    """Reads the text from a PDF/A file

    Args:
        file (str): The filename of the PDF/A

    Returns:
        str: The text from the PDF/A
    """
    reader = PdfReader(OCR_pdf(file))

    print(f"Reading {file}")

    text = ""
    for page in reader.pages:
        text += page.extract_text()

    print(f"Read {file}")
    return text


def summarize_text(text: str) -> str:
    load_dotenv()
    openai.api_key = getenv("OPENAI_API_KEY")
    
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"Summarize the content you are given for a high school student. The text is {text[0:1000]}",
        temperature=0,
        max_tokens=4096 - 231,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    return response.choices[0].text


def write_text(text: str, file: str) -> None:
    """Writes the text to a file

    Args:
        text (str): The text to write
        file (str): The filename to write to
    """
    print(f"Writing {file}")

    with open(file, "w") as f:
        f.write(text)

    print(f"Wrote {file}")


