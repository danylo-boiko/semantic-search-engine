import re
import unicodedata


def remove_diacritics(text: str) -> str:
    normalized_text = unicodedata.normalize("NFKC", text)

    return "".join(char for char in normalized_text if not unicodedata.combining(char))


def remove_cites(text: str) -> str:
    return re.sub(r"\[[^]]*]", "", text)


def normalize_punctuation(text: str) -> str:
    if text.endswith((".", "?", "!")):
        return text

    return text.rstrip(":;-—") + "."
