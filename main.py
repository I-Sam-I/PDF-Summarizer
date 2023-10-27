from helper import *
from argparse import Namespace


def main() -> None:
    args: Namespace = get_args()
    text: str = get_pdf_text(args.input_pdf[0])
    print(text)
    

if __name__ == "__main__":
    main()