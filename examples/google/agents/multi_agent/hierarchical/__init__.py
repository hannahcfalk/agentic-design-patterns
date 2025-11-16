# Based on code from the book "Agentic Design Patterns: A Hands-On Guide
# to Building Intelligent Systems" by Antonio Gullí
# Modifications Copyright (c) 2025 Hannah Falk
#
# This code is licensed under the MIT License.
# See the LICENSE file in the repository for the full license text.

from google.adk.agents import LlmAgent, BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.genai.types import Content, Part
from typing import AsyncGenerator

GEMINI_MODEL = "gemini-2.0-flash-exp"


# Correctly implement a custom agent by extending BaseAgent
class TaskExecutor(BaseAgent):
    """A specialized agent with custom, non-LLM behavior."""

    name: str = "TaskExecutor"
    description: str = "Executes a predefined task."

    async def _run_async_impl(
        self, context: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        """Custom implementation logic for the task."""
        # This is where your custom logic would go.
        # For this example, we'll just yield a simple event.
        content = Content(
            parts=[Part(text="Task finished successfully.")],
            role="model"
        )
        yield Event(author=self.name, content=content)


# Define individual agents with proper intialization
# LlmAgent requires a model to be specified.
greeter = LlmAgent(
    name="Greeter",
    model=GEMINI_MODEL,
    instruction="You are a friendly greeter.",
)
task_doer = TaskExecutor()  # Instantiate our concrete custom agent

# Create a parent agent and assign its sub-agents
# The parent agent's description and instructions should guide its delegation logic.
coordinator = LlmAgent(
    name="Coordinator",
    model=GEMINI_MODEL,
    description="A coordinator that can greet users and execute tasks.",
    instruction="When asked to greet, delegate to the Greeter. When asked to perform a task, delegate to the TaskExecutor.",
    sub_agents=[greeter, task_doer],
)

# The ADK framework automatically established the parent-child relationships.
# These assertions will pass if checked after initialization.
assert greeter.parent_agent == coordinator
assert task_doer.parent_agent == coordinator

print("Agent hierarchy created successfully.")

root_agent = coordinator  # The top-level agent in this hierarchy
