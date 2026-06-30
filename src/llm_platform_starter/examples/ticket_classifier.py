from __future__ import annotations

import time
import uuid

from llm_platform_starter.guardrails.validation import validate_ticket_output
from llm_platform_starter.models import ProviderRequest, TicketClassification, TicketRequest, TraceRecord
from llm_platform_starter.observability.cost import estimate_cost
from llm_platform_starter.observability.storage import TraceStore
from llm_platform_starter.prompts.registry import PromptRegistry
from llm_platform_starter.providers.base import LLMProvider


class TicketClassifier:
    prompt_id = "ticket_classifier"

    def __init__(
        self,
        provider: LLMProvider,
        model: str,
        prompt_registry: PromptRegistry | None = None,
        trace_store: TraceStore | None = None,
    ) -> None:
        self.provider = provider
        self.model = model
        self.prompt_registry = prompt_registry or PromptRegistry()
        self.trace_store = trace_store

    def classify(self, ticket: TicketRequest) -> TicketClassification:
        request_id = str(uuid.uuid4())
        prompt_template = self.prompt_registry.get(self.prompt_id)
        prompt = prompt_template.render(subject=ticket.subject, body=ticket.body)
        started = time.perf_counter()
        error_category: str | None = None
        try:
            response = self.provider.complete(
                ProviderRequest(
                    prompt=prompt,
                    model=self.model,
                    metadata={"request_id": request_id, "prompt_id": self.prompt_id},
                )
            )
            parsed, validation = validate_ticket_output(
                response.text,
                source_text=f"{ticket.subject}\n{ticket.body}",
            )
            if parsed is None:
                error_category = "validation_error"
                raise ValueError("; ".join(validation.errors))
            return parsed
        finally:
            if self.trace_store and "response" in locals():
                latency_ms = round((time.perf_counter() - started) * 1000, 2)
                self.trace_store.insert(
                    TraceRecord(
                        request_id=request_id,
                        prompt_id=self.prompt_id,
                        prompt_version=prompt_template.version,
                        provider=response.provider,
                        model=response.model,
                        latency_ms=latency_ms,
                        input_tokens=response.input_tokens,
                        output_tokens=response.output_tokens,
                        estimated_cost_usd=estimate_cost(
                            response.model,
                            response.input_tokens,
                            response.output_tokens,
                        ),
                        validation_passed=validation.passed if "validation" in locals() else False,
                        error_category=error_category,
                    )
                )
