import json

from llm_platform_starter.guardrails.validation import validate_ticket_output


def test_validate_ticket_output_accepts_schema():
    text = json.dumps(
        {
            "category": "billing",
            "severity": "medium",
            "confidence": 0.9,
            "rationale": "Billing terms were present.",
            "needs_review": False,
        }
    )

    parsed, validation = validate_ticket_output(text)

    assert parsed is not None
    assert validation.passed


def test_validate_ticket_output_flags_pii():
    text = json.dumps(
        {
            "category": "account",
            "severity": "medium",
            "confidence": 0.8,
            "rationale": "Account access issue.",
            "needs_review": False,
        }
    )

    parsed, validation = validate_ticket_output(text, source_text="User email is test@example.com")

    assert parsed is not None
    assert not validation.passed
    assert parsed.needs_review
    assert validation.pii_findings == ["email"]
