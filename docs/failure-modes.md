# Failure Modes

Important failure modes this project is designed to surface:

- Provider timeout or unavailable model
- Invalid JSON from a model
- Schema mismatch after a prompt or model change
- Low-confidence output that should route to review
- PII in source input or generated output
- Cost or latency regression
- Prompt version drift between development and production

The MVP handles a subset directly and documents the rest as production extensions.
