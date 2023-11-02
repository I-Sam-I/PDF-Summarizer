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
from time import sleep


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


def get_pdf_text(file: str) -> list[str]:
    """Reads the text from a PDF/A file

    Args:
        file (str): The filename of the PDF/A

    Returns:
        list[str]: The text from the PDF/A per page
    """
    reader = PdfReader(OCR_pdf(file))

    print(f"Reading {file}")

    text = []
    for page in reader.pages:
        text.append(page.extract_text())

    print(f"Read {file}")
    return text


def summarize_text(text: list[str]) -> str:
    load_dotenv()
    openai.api_key = getenv("OPENAI_API_KEY")
    
    print("Summarizing text")
    
    responses: list[str] = []
    for page in text:
        
        try: 
            responses.append(
                openai.completions.create(
                    model="gpt-3.5-turbo-instruct",
                    prompt=f"Summarize the content you are given for a high school student. The text is {page}",
                    temperature=0,
                    max_tokens=4096 - len(page) // 3,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                    ).choices[0].text
                )
        except Exception as e:
            print("OpenAI API limit reached. Waiting 1 minute...")
            sleep(60)
            responses.append(
                openai.completions.create(
                    model="gpt-3.5-turbo-instruct",
                    prompt=f"Summarize the content you are given for a high school student. The text is {page}",
                    temperature=0,
                    max_tokens=4096 - len(page) // 3,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                    ).choices[0].text
                )
    
    print("Summarized text")
    return responses


def write_text(text: list[str], file: str) -> None:
    """Writes the text to a file

    Args:
        text (list[str]): The text to write
        file (str): The filename to write to
    """
    print(f"Writing {file}")

    with open(file, "w") as f:
        for page in text:
            f.write(page)

    print(f"Wrote {file}")


