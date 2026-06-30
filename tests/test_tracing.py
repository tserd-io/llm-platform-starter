from llm_platform_starter.examples.ticket_classifier import TicketClassifier
from llm_platform_starter.models import TicketRequest
from llm_platform_starter.observability.storage import TraceStore
from llm_platform_starter.providers.mock import MockProvider


def test_ticket_classifier_writes_trace(tmp_path):
    store = TraceStore(tmp_path / "traces.sqlite3")
    classifier = TicketClassifier(
        provider=MockProvider(),
        model="mock-ticket-classifier",
        trace_store=store,
    )

    classifier.classify(TicketRequest(subject="Refund", body="Duplicate billing charge."))
    metrics = store.metrics()

    assert metrics["request_count"] == 1
    assert metrics["total_estimated_cost_usd"] == 0
