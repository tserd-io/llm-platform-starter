# Eval Methodology

The MVP uses small, synthetic JSONL fixtures to test task-specific behavior. Each fixture defines an input ticket and an expected category.

The current eval measures exact category accuracy. This is enough for a compact regression harness because the mock provider is deterministic and the example task has a narrow schema.

Future versions can add:

- prompt-version comparisons
- provider/model comparisons
- structured-output validity rate
- cost and latency by eval run
- rubric scoring for summarization or extraction tasks
- human review sampling
