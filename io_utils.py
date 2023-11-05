from gtts import gTTS


def write_text(text: list[str], file: str) -> None:
    """
    Writes the text to a file.

    Args:
        text (list[str]): The text to write.
        file (str): The filename to write to.
    """
        
    with open(file, "w") as f:
        f.write("\n".join(text))


def text_to_speech(text: str, file: str) -> None:
    """
    Converts text to speech and saves it to a file.

    Args:
        text (str): The text to convert.
        file (str): The filename to save to.
    """
        
    tts = gTTS(text=text, lang='en')
    tts.save(file)
 