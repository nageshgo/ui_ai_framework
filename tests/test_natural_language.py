import pytest

from agents.test_agent import TestAgent

@pytest.mark.skip(reason="Need to be implemented")
def test_natural_language_generation():

    agent = TestAgent()

    result = agent.create_test_steps(
        "Add employee and validate in employee list"
    )

    print(result)

    assert result is not None
