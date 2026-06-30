from __future__ import annotations

import json

from pydantic import ValidationError

from llm_platform_starter.guardrails.pii import detect_pii
from llm_platform_starter.models import TicketClassification, ValidationResult


def parse_ticket_classification(text: str) -> TicketClassification:
    return TicketClassification.model_validate(json.loads(text))


def validate_ticket_output(text: str, source_text: str = "") -> tuple[TicketClassification | None, ValidationResult]:
    errors: list[str] = []
    parsed: TicketClassification | None = None
    try:
        parsed = parse_ticket_classification(text)
    except (json.JSONDecodeError, ValidationError) as exc:
        errors.append(str(exc))

    pii_findings = detect_pii(source_text)
    if pii_findings and parsed:
        parsed.needs_review = True

    return parsed, ValidationResult(
        passed=not errors and not pii_findings,
        errors=errors,
        pii_findings=pii_findings,
    )
