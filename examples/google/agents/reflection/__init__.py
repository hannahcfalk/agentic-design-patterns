# Based on code from the book "Agentic Design Patterns: A Hands-On Guide
# to Building Intelligent Systems" by Antonio Gullí
# Modifications Copyright (c) 2025 Hannah Falk
#
# This code is licensed under the MIT License.
# See the LICENSE file in the repository for the full license text.

from google.adk.agents import SequentialAgent, LlmAgent
from google.adk.tools import google_search

GEMINI_MODEL = "gemini-2.0-flash"

# The first agent generates the intial draft.
generator = LlmAgent(
    name="DraftWriter",
    model=GEMINI_MODEL,
    description="Generates initial draft content on a given subject.",
    instruction="Write a short, informative paragraph about the user's subject.",
    tools=[google_search],
    output_key="draft_text",  # The output is saved to this state key.
)

reviewer = LlmAgent(
    name="FactChecker",
    model=GEMINI_MODEL,
    description="Reviews a given text for factual accuracy and provides a structured critique.",
    instruction="""
    You are a meticulous fact-checker.
    1. Read the text provided in the state key 'draft_text'.
    2. Carefully verify the factual accuracy of all claims.
    3. Your final output must be a dictionary containing two keys:
    - "status": A string, either "ACCURATE" or "INACCURATE".
    - "reasoning": A string providing a clear explanation for your status, citing specific issues if any are found.
    """,
    output_key="review_output",  # The structured dictionary is saved here.
)

# The SequentialAgent ensures the generator runs before the reviewer.
review_pipeline = SequentialAgent(
    name="WriteAndReview_Pipeline", sub_agents=[generator, reviewer]
)

# Execution Flow:
# 1. generator runs -> saves its paragraph to state['draft_text'].
# 2. reviewer runs -> reads state['draft_text'] and saves its dictionary ouptut to state['review_output']

root_agent = review_pipeline
