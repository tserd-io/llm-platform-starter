from llm_platform_starter.evals.runner import run_ticket_classification_eval


def test_ticket_classification_eval_passes_with_mock_provider():
    report = run_ticket_classification_eval()

    assert report["accuracy"] == 1.0
    assert all(case["passed"] for case in report["cases"])
