from pathlib import Path

import pandas as pd

from lodestar_veritas.parsers.csv_parser import CSVParser


def test_csv_parser_extracts_rows_and_columns(tmp_path: Path):
    csv_path = tmp_path / "sample.csv"

    dataframe = pd.DataFrame(
        {
            "Metric": ["Revenue", "Risk"],
            "Value": ["25%", "Inflation"],
        }
    )

    dataframe.to_csv(csv_path, index=False)

    parser = CSVParser()
    result = parser.parse(str(csv_path))

    assert result["metadata"]["parser"] == "CSVParser"
    assert result["metadata"]["row_count"] == 2
    assert result["metadata"]["column_count"] == 2
    assert "Revenue" in result["content"]


def test_xlsx_parser_extracts_rows_and_columns(tmp_path: Path):
    xlsx_path = tmp_path / "sample.xlsx"

    dataframe = pd.DataFrame(
        {
            "Metric": ["Revenue", "Risk"],
            "Value": ["25%", "Inflation"],
        }
    )

    dataframe.to_excel(xlsx_path, index=False)

    parser = CSVParser()
    result = parser.parse(str(xlsx_path))

    assert result["metadata"]["parser"] == "CSVParser"
    assert result["metadata"]["row_count"] == 2
    assert result["metadata"]["column_count"] == 2
    assert "Inflation" in result["content"]