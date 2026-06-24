from pathlib import Path

import pandas as pd


class CSVParser:
    """
    Parses CSV and Excel tabular data.
    """

    def parse(self, file_path: str) -> dict:
        path = Path(file_path)
        extension = path.suffix.lower()

        if extension == ".csv":
            dataframe = pd.read_csv(file_path)
            sheet_name = None
        elif extension in [".xlsx", ".xls"]:
            dataframe = pd.read_excel(file_path)
            sheet_name = "default"
        else:
            raise ValueError(f"Unsupported tabular file type: {extension}")

        rows = dataframe.fillna("").to_dict(orient="records")
        columns = list(dataframe.columns)

        text_rows = []
        for index, row in enumerate(rows, start=1):
            row_text = " | ".join(f"{column}: {row[column]}" for column in columns)
            text_rows.append(f"[Row {index}] {row_text}")

        content = "\n".join(text_rows)

        return {
            "content": content,
            "rows": rows,
            "columns": columns,
            "metadata": {
                "source": file_path,
                "file_name": path.name,
                "parser": "CSVParser",
                "row_count": len(rows),
                "column_count": len(columns),
                "columns": columns,
                "sheet_name": sheet_name,
            },
        }