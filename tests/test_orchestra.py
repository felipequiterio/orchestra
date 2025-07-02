from orchestra import run
from tests.mocks import agent_list, task_list


def test_final_answer_generation(monkeypatch):
    """End-to-end test of run() with a deterministic LLM reply."""
    canned_reply = (
        "The weather in New York is sunny and 72 °F. "
        "Your todo list says you still need to buy groceries."
    )

    def fake_model_invoke(*_args, **_kwargs):
        return canned_reply

    monkeypatch.setattr("core.task.model_invoke", fake_model_invoke)

    answer = run(
        query="What's the weather and what's on my todo list?",
        agent_list=agent_list,
        task_list=task_list,
    )

    assert answer == canned_reply  # exact content returned
    answer_lc = answer.lower()
    assert "new york" in answer_lc  # key facts present
    assert "groceries" in answer_lc
    assert "weather" in answer_lc
    assert "todo" in answer_lc
