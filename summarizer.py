from helper import *
from argparse import Namespace
from sys import exit


def main() -> None:    
    args: Namespace = get_args()
    
    if not is_pdf(args.input_pdf):
        exit(1)
    
    text: list[str] = get_pdf_text(args.input_pdf)
    # text: list[str] = summarize_text(text)
    
    if not is_text(args.output_file):
        exit(1)
    
    write_text(text, args.output_file)
    
    if args.text_to_speech:
        if not is_audio(args.text_to_speech):
            exit(1)
        
        text_to_speech("\n".join(text), args.text_to_speech)
    

if __name__ == "__main__":
    main()