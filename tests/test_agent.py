# import pytest
# from orchestra.core.agent import AgentTask
# from orchestra.examples.todo_agent import TodoAgent


# @pytest.fixture
# def todo_agent():
#     return TodoAgent(
#         name="todo",
#         description="Test Todo Agent",
#         system_prompt="You are a todo manager",
#         input_schema={},  # Add your schema
#         output_schema={},  # Add your schema
#     )


# def test_todo_agent_capabilities(todo_agent):
#     capabilities = todo_agent.capabilities()
#     assert "actions" in capabilities
#     assert "add" in capabilities["actions"]
#     assert "priorities" in capabilities


# def test_todo_agent_execute_add(todo_agent):
#     task = AgentTask(
#         task="Add a new todo item",
#         expected_output="Task added successfully",
#         metadata={"action": "add", "title": "Test Task"},
#     )
#     result = todo_agent.execute(task)
#     assert result["status"] == "success"
