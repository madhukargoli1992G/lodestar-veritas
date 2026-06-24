from pathlib import Path

from PIL import Image


class ImageParser:
    """
    Image parser with metadata extraction.

    OCR/captioning can be added later.
    """

    def parse(self, file_path: str) -> dict:
        path = Path(file_path)

        with Image.open(file_path) as image:
            width, height = image.size
            image_format = image.format
            image_mode = image.mode

        content = (
            f"Image file: {path.name}. "
            f"Format: {image_format}. "
            f"Dimensions: {width}x{height}. "
            f"Mode: {image_mode}."
        )

        return {
            "content": content,
            "metadata": {
                "source": file_path,
                "file_name": path.name,
                "parser": "ImageParser",
                "width": width,
                "height": height,
                "format": image_format,
                "mode": image_mode,
                "ocr_available": False,
                "caption_available": False,
            },
        }