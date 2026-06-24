import re


class MetadataBuilder:
    """
    Enrichs chunk metadata before storage.
    """

    def enrich(
        self,
        text: str,
        metadata: dict,
    ) -> dict:

        enriched = metadata.copy()

        enriched["character_count"] = len(text)

        enriched["word_count"] = len(text.split())

        enriched["contains_numbers"] = bool(
            re.search(r"\d", text)
        )

        enriched["contains_dates"] = bool(
            re.search(r"\b\d{4}\b", text)
        )

        enriched["contains_currency"] = (
            "$" in text
            or "USD" in text
        )

        enriched["contains_percentage"] = "%" in text

        enriched["language"] = "english"

        return enriched