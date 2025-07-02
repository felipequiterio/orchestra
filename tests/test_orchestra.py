import pytest
from ..orchestra import run
from ..tests.mocks import agent_list, task_list

def test_final_answer_generation():
    """Test answer synthesis from multiple results"""
    result = run(
        query="What's the weather and what's on my todo list?",
        agent_list=agent_list,
        task_list=task_list
    )
    print(f'result: \n{result}')
    assert "New York" in result["answer"]
    assert "groceries" in result["answer"]
    assert "weather" in result["answer"].lower()
    assert "todo" in result["answer"].lower()
