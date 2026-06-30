# Architecture

The project models a compact internal LLM platform layer. Application workflows call a stable platform interface instead of calling model providers directly.

## Components

- Provider gateway normalizes requests and responses across model providers.
- Prompt registry loads versioned templates and renders validated inputs.
- Guardrails validate structured outputs and flag basic PII risk.
- Observability stores request metadata, latency, token counts, estimated cost, validation status, and error category.
- Eval runner executes synthetic fixtures against the same platform path used by the API.

## Request Flow

1. A workflow submits a synthetic support ticket.
2. The prompt registry renders the active prompt version.
3. The provider gateway calls the configured model provider.
4. Guardrails parse and validate the JSON response.
5. The trace store writes operational metadata to SQLite.
6. The API returns a typed response object.

## Why SQLite

SQLite keeps the MVP runnable without managed infrastructure while still making traces queryable. In a production platform, this could be replaced by a warehouse table, OpenTelemetry collector, or observability backend.
