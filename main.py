from argparse import ArgumentParser, Namespace
import logging

from file_type_utils import is_file_type
from pdf_utils import ocr_pdf, get_pdf_text
from io_utils import write_text, text_to_speech
from summarize_utils import summarize_text


def main() -> None:
    # Create a custom logger
    logger = create_logger()
    
    # Get the command line arguments
    args: Namespace = get_args()
    
    # Check if the input file is a PDF
    if not is_file_type(args.input_pdf, "application/pdf"):
        exit(f"{args.input_pdf} is not a valid PDF file.")
    
    # Convert PDF to OCR PDF
    logger.info(f"Converting {args.input_pdf} to OCR PDF.")
    ocr_pdf_file_name = ocr_pdf(args.input_pdf)
    logger.info(f"Converted {args.input_pdf} to OCR PDF.")
    
    # Read the text from the OCR PDF
    logger.info(f"Reading {ocr_pdf_file_name}.")
    text: list[str] = get_pdf_text(ocr_pdf_file_name)
    logger.info(f"Read {ocr_pdf_file_name}.")
    
    # Summarize the text
    logger.info("Summarizing text.")
    text: list[str] = summarize_text(text)
    logger.info("Summarized text.")
    
    # Check if the output file is a text file
    if not is_file_type(args.output_file, "text/plain"):
        exit(f"{args.output_file} is not a valid text file.")
    
    # Write the text to the output file
    logger.info(f"Writing text to {args.output_file}.")
    write_text(text, args.output_file)
    logger.info(f"Wrote text to {args.output_file}.")
    
    # Check if the text to speech file is an audio file
    if args.text_to_speech:
        if not is_file_type(args.text_to_speech, "audio/mpeg"):
            exit(f"{args.text_to_speech} is not a valid audio file.")
        
        logger.info(f"Converting text to speech and saving to {args.text_to_speech}.")
        text_to_speech("\n".join(text), args.text_to_speech)
        logger.info(f"Converted text to speech and saved to {args.text_to_speech}.")
 
 
def get_args() -> Namespace:
    """
    Creates an argument parser and returns the arguments.

    Returns:
        Namespace: The "dictionary" of command line arguments.
    """
    parser = ArgumentParser(prog="python main.py", description="Summarizes a PDF file into a txt and audio file.")

    # Input and output files
    parser.add_argument('input_pdf', type=str, help="Input PDF file")
    parser.add_argument('-o', '--output-file', type=str, default="output.txt", help="Output file of summarized text.")

    # Text to speech option and file
    parser.add_argument('-t', '--text-to-speech', type=str, help="Audio file of summarized text.")
    
    return parser.parse_args()


def create_logger() -> logging.Logger:
    """
    Creates a custom logger with a console handler and a specific formatter.

    Returns:
        logging.Logger: A custom logger object.
    """
    # Create a custom logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create a console handler
    handler = logging.StreamHandler()

    # Create a formatter: HH:MM:SS - [Info]: MESSAGE
    formatter = logging.Formatter('%(asctime)s - [%(levelname)s]: %(message)s', datefmt='%H:%M:%S')

    # Add the formatter to the handler
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)
    
    return logger


if __name__ == "__main__":
    main()
