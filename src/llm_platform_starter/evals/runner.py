from __future__ import annotations

import json
from importlib import resources

from llm_platform_starter.evals.metrics import accuracy
from llm_platform_starter.examples.ticket_classifier import TicketClassifier
from llm_platform_starter.models import TicketRequest
from llm_platform_starter.providers.mock import MockProvider


def load_fixture(name: str = "ticket_classification.jsonl") -> list[dict]:
    raw = resources.files("llm_platform_starter.evals.fixtures").joinpath(name).read_text(
        encoding="utf-8"
    )
    return [json.loads(line) for line in raw.splitlines() if line.strip()]


def run_ticket_classification_eval() -> dict:
    classifier = TicketClassifier(provider=MockProvider(), model="mock-ticket-classifier")
    rows = load_fixture()
    checks = []
    cases = []
    for row in rows:
        result = classifier.classify(TicketRequest(subject=row["subject"], body=row["body"]))
        passed = result.category.value == row["expected_category"]
        checks.append(passed)
        cases.append(
            {
                "id": row["id"],
                "expected": row["expected_category"],
                "actual": result.category.value,
                "passed": passed,
            }
        )
    return {"accuracy": accuracy(checks), "cases": cases}


def main() -> None:
    print(json.dumps(run_ticket_classification_eval(), indent=2))


if __name__ == "__main__":
    main()
