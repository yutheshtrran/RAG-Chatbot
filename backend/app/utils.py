import re

def clean_text(text: str) -> str:
    """
    Clean input text by stripping whitespace, lowercasing,
    normalizing spaces, and removing non-printable characters.
    """
    if not isinstance(text, str):
        return ""
    text = text.strip().lower()
    text = re.sub(r'\s+', ' ', text)
    text = ''.join(c for c in text if c.isprintable())
    return text
