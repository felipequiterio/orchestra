from core.task import Task, TaskList, route
from tests.mocks import agent_list
from tests.mocks import task_list as ok_tasks


def test_route_unknown_agent():
    extra = Task(
        step_number=3,
        task="Do something impossible",
        agent="non_existent_agent",
        expected_output="n/a",
        is_async=False,
    )
    bad_task_list = TaskList(steps=ok_tasks.steps + [extra])

    results = route(bad_task_list, agent_list)

    # Last result corresponds to the failing task
    last = results[-1]
    assert last["status"] == "error"
    assert "not found" in last["message"].lower()
