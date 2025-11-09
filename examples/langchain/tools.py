# Based on code from the book "Agentic Design Patterns: A Hands-On Guide
# to Building Intelligent Systems" by Antonio Gullí
# Modifications Copyright (c) 2025 Hannah Falk
#
# This code is licensed under the MIT License.
# See the LICENSE file in the repository for the full license text.

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool as langchain_tool
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor


# --- Define a Tool ---
@langchain_tool
def search_information(query: str) -> str:
    """
    Provides factual information on a given topic. Use this tool to find answers to phrases
    like 'capital of France' or 'weather in London?'.
    """
    print(f"\n--- Tool Called: search_information with query: '{query}' ---")

    # Simulate a search tool with a dictionary of predefined results.
    simulated_results = {
        "weather in london": "The weather in London is currently cloudy with a temperature of 15°C.",
        "capital of france": "The capital of France is Paris.",
        "population of earth": "The estimated population of Earth is around 8 billion people.",
        "tallest mountain": "Mount Everest is the tallest mountain above sea level.",
        "default": f"Simulated search result for '{query}': No specific information found, but the topic seems interesting.",
    }
    result = simulated_results.get(query.lower(), simulated_results["default"])
    print(f"--- TOOL RESULT: {result} ---")
    return result


tools = [search_information]


# --- Create a Tool-Calling Agent ---
def setup(llm):
    # This prompt template requires an `agent_scratchpad` placeholder for the agent's internal steps.
    agent_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    # Create the agent, binding the LLM, tools, and prompt together.
    agent = create_tool_calling_agent(llm, tools, agent_prompt)

    # AgentExecutor is the runtime that invokes the agent and executes the chosen tools.
    # The 'tools' argument is not needed here as they are already bound to the agent.
    return AgentExecutor(agent=agent, verbose=True, tools=tools)


async def run_agent_with_tool(agent_executor: AgentExecutor, query: str):
    """Invokes the agent executor with a query and prints the final response."""
    print(f"\n--- Running Agent with Query: '{query}' ---")
    try:
        response = await agent_executor.ainvoke({"input": query})
        print("\n--- Final Agent Response ---")
        print(response["output"])
    except Exception as e:
        print(f"\n An error occurred during agent execution: {e}")


# Example usage in main.py:
# async def main():
#     """Sets up the agent and runs all agent queries concurrently."""
#     llm = retrieve_langchain_llm()
#     if llm:
#         agent_executor = tools.setup(llm)
#         tasks = [
#             tools.run_agent_with_tool(agent_executor, "What is the capital of France?"),
#             tools.run_agent_with_tool(
#                 agent_executor, "What is the weather like in London?"
#             ),
#             tools.run_agent_with_tool(
#                 agent_executor, "Tell me something about dogs."
#             ),  # Should trigger the default tool response
#         ]
#         await asyncio.gather(*tasks)
