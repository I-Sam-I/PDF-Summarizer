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
from gtts import gTTS
import logging
from mimetypes import guess_type
import openai
from os import getenv
from PyPDF2 import PdfReader
from subprocess import run
from time import sleep

# Configurations
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)

load_dotenv()
openai.api_key = getenv("OPENAI_API_KEY")


def get_args() -> Namespace:
    """
    Creates an argument parser and returns the args

    Returns:
        Namespace: The "dictionary" of command line arguments
    """
    parser = ArgumentParser(prog="summarizer", description="Summarizes a PDF file into a txt and audio file")

    # Input and output files
    parser.add_argument('input_pdf', type=str, help="Input PDF file")
    parser.add_argument('-o', '--output-file', type=str, default="output.txt", help="Output file of summarized text")

    # Text to speech option and file
    parser.add_argument('-t', '--text-to-speech', type=str,  help="Audio file of summarized text")
    
    return parser.parse_args()


def OCR_pdf(file: str) -> str:
    """
    Converts standard PDF to OCR PDF which can be read by PyPDF2

    Args:
        file (str): The filename of the PDF

    Returns:
        str: The filename of the OCR PDF
    """
    
    logging.info(f"Converting {file} to OCR PDF")
    
    run(["ocrmypdf", file, file, "--deskew", "--skip-text", "--quiet"], check=True)
    
    logging.info(f"Converted {file} to OCR PDF")
    
    return file


def get_pdf_text(file: str) -> list[str]:
    """
    Reads the text from a PDF file

    Args:
        file (str): The filename of the PDF

    Returns:
        list[str]: The text from the PDF per page
    """
    
    logging.info(f"Reading {file}")
    
    reader = PdfReader(OCR_pdf(file))

    text = []
    for page in reader.pages:
        text.append(page.extract_text())

    logging.info(f"Read {file}")
    
    return text


def summarize_text(text: list[str]) -> list[str]:
    """
    Summarize the entire text

    Args:
        text (list[str]): The entire text to summarize

    Returns:
        list[str]: The summarized text
    """
    
    logging.info("Summarizing text")
        
    responses: list[str] = []
    for page in text:
        try: 
            responses.append(get_gpt_response(page))
        
        except Exception:
            logging.warning("OpenAI API error, waiting 60 seconds")
            sleep(60)
            responses.append(get_gpt_response(page))
    
    logging.info("Summarized text")
    return responses


def write_text(text: list[str], file: str) -> None:
    """
    Writes the text to a file

    Args:
        text (list[str]): The text to write
        file (str): The filename to write to
    """
    
    logging.info(f"Writing text to {file}")
    
    with open(file, "w") as f:
        for page in text:
            f.write(page)

    logging.info(f"Wrote text to {file}")


def get_gpt_response(text: str) -> str:
    """
    Connects with the OpenAI API and returns the response

    Args:
        text (str): The text to summarize

    Returns:
        str: Summarized text
    """
     
    return openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"Summarize the content you are given for a high school student. The text is {text}",
        temperature=0,
        max_tokens=8192 - len(text) // 3,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    ).choices[0].text
    

def text_to_speech(text: str, file: str) -> None:
    """
    Converts text to speech and saves it to a file

    Args:
        text (str): The text to convert
        file (str): The filename to save to
    """
    
    logging.info(f"Converting text to speech and saving to {file}")
    
    tts = gTTS(text=text, lang='en')
    tts.save(file)

    logging.info(f"Converted text to speech and saved to {file}")
    

def is_pdf(filename: str) -> bool:
    """
    Check if the given filename is a PDF file.

    Args:
        filename (str): The name of the file to check.

    Returns:
        bool: True if the file is a PDF file, False otherwise.
    """
    
    flag = guess_type(filename)[0] == 'application/pdf'
    
    if not flag:
        logging.error(f"{filename} is not a PDF file")
    
    return flag


def is_text(filename: str) -> bool:
    """
    Check if the file is a text file.

    Args:
        filename (str): The name of the file to check.

    Returns:
        bool: True if the file is a text file, False otherwise.
    """
    
    flag = guess_type(filename)[0] == 'text/plain'
    
    if not flag:
        logging.error(f"{filename} is not a text file")
    
    return flag


def is_audio(filename: str) -> bool:
    """
    Check if the given file is an audio file.
    
    Args:
        filename (str): The name of the file to check.
    
    Returns:
        bool: True if the file is an audio file, False otherwise.
    """
    
    flag = guess_type(filename)[0] == 'audio/mpeg'
    
    if not flag:
        logging.error(f"{filename} is not an audio file")
    
    return flag