from lodestar_veritas.guardrails.basic_guardrails import BasicGuardrails


class GuardrailAgent:
    def __init__(self):
        self.guardrails = BasicGuardrails()

    def validate_query(self, query: str) -> dict:
        return self.guardrails.validate_query(query)