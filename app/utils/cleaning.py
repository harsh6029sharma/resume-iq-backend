import re

def remove_emojis_and_icons(text: str) -> str:
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F700-\U0001F77F"
        "\U0001F780-\U0001F7FF"
        "\U0001F800-\U0001F8FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FAFF"
        "\U00002700-\U000027BF"  # Dingbats
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(" ", text)

def clean_text(text:str)->str:
    # remove emojis and icons
    text = remove_emojis_and_icons(text)

    # remove newlines with space 
    text = re.sub(r"[\n\r\t]+", " ", text)

    # remove special chars
    text = re.sub(r"[^a-zA-Z0-9\s.,:;()\-\/@+#.]", " ", text)

    # Remove extra spaces 
    text = re.sub(r"\s+"," ",text)

    return text
