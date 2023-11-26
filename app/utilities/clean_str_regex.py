import re


def regex_replace_str(data: str):
    return re.sub(r"[ ]+", " ", re.sub(r"[\n\t\r\\\"]", "", data))
