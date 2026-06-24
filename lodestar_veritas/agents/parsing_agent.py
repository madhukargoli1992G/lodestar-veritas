from lodestar_veritas.agents.content_analyzer_agent import ContentAnalyzerAgent
from lodestar_veritas.agents.chunk_strategy_planner import ChunkStrategyPlanner
from lodestar_veritas.parsers.csv_parser import CSVParser
from lodestar_veritas.parsers.docx_parser import DOCXParser
from lodestar_veritas.parsers.image_parser import ImageParser
from lodestar_veritas.parsers.pdf_parser import PDFParser
from lodestar_veritas.parsers.ppt_parser import PPTParser
from lodestar_veritas.parsers.text_parser import TextParser


class ParsingAgent:
    """
    Orchestrates document analysis, chunk strategy planning, and parser selection.
    """

    def __init__(self):
        self.content_analyzer = ContentAnalyzerAgent()
        self.chunk_planner = ChunkStrategyPlanner()

        self.csv_parser = CSVParser()
        self.docx_parser = DOCXParser()
        self.image_parser = ImageParser()
        self.pdf_parser = PDFParser()
        self.ppt_parser = PPTParser()
        self.text_parser = TextParser()

    def parse(self, file_path: str) -> dict:
        analysis = self.content_analyzer.analyze(file_path)
        strategy = self.chunk_planner.plan(analysis)

        if analysis.document_type == "tabular_data":
            parsed_content = self.csv_parser.parse(file_path)
        elif analysis.document_type == "word_document":
            parsed_content = self.docx_parser.parse(file_path)
        elif analysis.document_type == "image":
            parsed_content = self.image_parser.parse(file_path)
        elif analysis.document_type == "pdf_document":
            parsed_content = self.pdf_parser.parse(file_path)
        elif analysis.document_type == "presentation":
            parsed_content = self.ppt_parser.parse(file_path)
        elif analysis.document_type == "plain_text":
            parsed_content = self.text_parser.parse(file_path)
        else:
            parsed_content = {
                "content": "",
                "metadata": {
                    "source": file_path,
                    "message": "Parser not yet implemented for this document type.",
                },
            }

        return {
            "analysis": analysis,
            "chunk_strategy": strategy,
            "parsed_content": parsed_content,
        }