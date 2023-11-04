# Weird OpenAI bug
import collections 
try:
    from collections.abc import MutableSet, MutableMapping
    collections.MutableSet = MutableSet
    collections.MutableMapping = MutableMapping
except Exception:
    from collections import MutableSet, MutableMapping

from argparse import ArgumentParser, Namespace
from dotenv import load_dotenv
import openai
from os import system, getenv
from PyPDF2 import PdfReader
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
    """Converts standard PDF to OCR PDF which can be read by PyPDF2

    Args:
        file (str): The filename of the PDF

    Returns:
        str: The filename of the OCR PDF
    """
    print(f"OCR'ing {file}")
    system(f"ocrmypdf '{file}' '{file}' --deskew --skip-text --quiet")
    print(f"OCR'd {file}")
    return file


def get_pdf_text(file: str) -> list[str]:
    """Reads the text from a PDF file

    Args:
        file (str): The filename of the PDF

    Returns:
        list[str]: The text from the PDF per page
    """
    reader = PdfReader(OCR_pdf(file))

    print(f"Reading {file}")

    text = []
    for page in reader.pages:
        text.append(page.extract_text())

    print(f"Read {file}")
    return text


def summarize_text(text: list[str]) -> str:
    """Summarize the entire text

    Args:
        text (list[str]): The entire text to summarize

    Returns:
        str: The summarized text
    """    
    print("Summarizing text")
    
    responses: list[str] = []
    for page in text:
        try: 
            responses.append(get_gpt_response(page))
        except Exception as e:
            print("OpenAI API limit reached. Waiting 1 minute...")
            sleep(60)
            responses.append(get_gpt_response(page))
    
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


def get_gpt_response(text: str) -> str:
    """Connects with the OpenAI API and returns the response

    Args:
        text (str): The text to summarize

    Returns:
        str: Summarized text
    """
    
    load_dotenv()
    openai.api_key = getenv("OPENAI_API_KEY")
    
    return openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"Summarize the content you are given for a high school student. The text is {text}",
        temperature=0,
        max_tokens=8192 - len(text) // 3,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    ).choices[0].text