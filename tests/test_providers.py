import json

from llm_platform_starter.models import ProviderRequest
from llm_platform_starter.providers.mock import MockProvider


def test_mock_provider_returns_normalized_ticket_json():
    response = MockProvider().complete(
        ProviderRequest(
            prompt="Refund requested after duplicate billing.",
            model="mock-ticket-classifier",
        )
    )

    payload = json.loads(response.text)

    assert response.provider == "mock"
    assert payload["category"] == "billing"
    assert response.input_tokens > 0
