# Based on code from the book "Agentic Design Patterns: A Hands-On Guide
# to Building Intelligent Systems" by Antonio Gullí
# Original code by Marco Fago: https://github.com/marfago/AgenticDesignPatterns
# Original code Copyright (c) 2025 Marco Fago
# Modifications Copyright (c) 2025 Hannah Falk
#
# This code is licensed under the MIT License.
# See the LICENSE file in the repository for the full license text.

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableBranch

# Define Simulated Sub-Agent Handlers


def booking_handler(request: str) -> str:
    """Simulates the Booking Agent handling a request."""
    print("\n--- DELEGATING TO BOOKING HANDLER ---")
    return f"Booking Handler processed request: '{request}'. Results: Simulated booking action."


def info_handler(request: str) -> str:
    """Simulates the Info Agent handling a request."""
    print("\n--- DELEGATING TO INFO HANDLER ---")
    return f"Info Handler processed request: '{request}'. Results: Simulated information retrieval."


def unclear_handler(request: str) -> str:
    """Handles requests that coudn't be delegated."""
    print("\n--- HANDLING UNCLEAR REQUEST ---")
    return f"Coordinator could not delegate request: '{request}'. Please clarify."


def execute(llm):

    # Define Coordinator Router Chain
    # This chain decides which handler to delegate to.
    coordinator_router_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """Analyze the user's request and determine which specialist handler should process it.
                - If the request is related to booking flights or hotels, output 'booker'.
                - For all other general information questions, output 'info'.
                - If the request is unclear or doesn't fit either category, output 'unclear'.
                ONLY output one word: 'booker', 'info', or 'unclear'.""",
            ),
            ("user", "{request}"),
        ]
    )

    if not llm:
        return

    coordinator_router_chain = coordinator_router_prompt | llm | StrOutputParser()

    # Define the Delegation Logic
    # Use RunnableBranch to route based on the router chain's output.

    # Define the branches for the RunnableBranch
    branches = {
        "booker": RunnablePassthrough.assign(
            output=lambda x: booking_handler(x["request"]["request"])
        ),
        "info": RunnablePassthrough.assign(
            output=lambda x: info_handler(x["request"]["request"])
        ),
        "unclear": RunnablePassthrough.assign(
            output=lambda x: unclear_handler(x["request"]["request"])
        ),
    }

    # Create the RunnableBranch. It takes the output of the router chain and routes the original input ('request') to the corresponding handler.
    delegation_branch = RunnableBranch(
        (lambda x: x["decision"].strip() == "booker", branches["booker"]),
        (lambda x: x["decision"].strip() == "info", branches["info"]),
        branches["unclear"],  # Default branch for 'unclear' or any other output,
    )

    # Combine the router chain and the delegation branch into a single runnable
    # The router chain's output ('decision') is passed along with the original input ('request') to the delegation branch.
    coordinator_agent = (
        {"decision": coordinator_router_chain, "request": RunnablePassthrough()}
        | delegation_branch
        | (lambda x: x["output"])
    )  # Extract the final output

    print("--- Running with a booking request ---")
    request_a = "Book me a flight to London."
    result_a = coordinator_agent.invoke({"request": request_a})
    print(f"Final Result A: {result_a}")
