from llm_platform_starter.prompts.registry import PromptRegistry


def test_prompt_registry_loads_and_renders_active_prompt():
    prompt = PromptRegistry().get("ticket_classifier")

    rendered = prompt.render(subject="API error", body="Export fails.")

    assert prompt.version == 1
    assert "API error" in rendered
    assert "Export fails." in rendered
