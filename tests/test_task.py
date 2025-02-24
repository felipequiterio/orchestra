from core.task import generate, TaskList, route
from tests.mocks import agent_list, task_list
import pytest

def test_task_generation():
    query = "Add 'Buy groceries' to the user's to-do list and also fetch the current weather for New York City"
    task_list = generate(query, agent_list)
    assert isinstance(task_list, TaskList)
    assert len(task_list.steps) == 2
    # assert task_list.steps[0].task == "Add 'Buy groceries' to the user's to-do list"
    # assert task_list.steps[1].task == "Fetch the current weather for New York City"

@pytest.mark.focus
def test_route():
    results = route(task_list, agent_list)
    print(f'results: \n{results}')
    assert results is None
    assert len(results) == 2
    
    for result in results:
        assert result['status'] == 'success'
        assert isinstance(result['result'], dict)
        assert 'is_async' in result