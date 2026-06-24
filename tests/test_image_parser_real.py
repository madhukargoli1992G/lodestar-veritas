from pathlib import Path

from PIL import Image

from lodestar_veritas.parsers.image_parser import ImageParser


def test_image_parser_extracts_metadata(tmp_path: Path):
    image_path = tmp_path / "sample.png"

    image = Image.new("RGB", (100, 80), color="white")
    image.save(image_path)

    parser = ImageParser()
    result = parser.parse(str(image_path))

    assert result["metadata"]["parser"] == "ImageParser"
    assert result["metadata"]["width"] == 100
    assert result["metadata"]["height"] == 80
    assert "Image file" in result["content"]