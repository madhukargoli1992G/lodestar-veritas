class TextParser:
    """
    Parses plain text and markdown files.
    """

    def parse(self, file_path: str) -> dict:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        return {
            "content": text,
            "metadata": {
                "source": file_path,
                "parser": "TextParser",
            },
        }