from core.task import Task

def test_task_generation():
    query = "Add 'Buy groceries' to the user's to-do list and also fetch the current weather for New York City"
    task_list = generate(query, agent_list)
    assert isinstance(task_list, TaskList)
    assert len(task_list.steps) == 2
    assert task_list.steps[0].task == "Add 'Buy groceries' to the user's to-do list"
    assert task_list.steps[1].task == "Fetch the current weather for New York City"
