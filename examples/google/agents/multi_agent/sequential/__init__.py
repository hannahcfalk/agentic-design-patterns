# Based on code from the book "Agentic Design Patterns: A Hands-On Guide
# to Building Intelligent Systems" by Antonio Gullí
# Modifications Copyright (c) 2025 Hannah Falk
#
# This code is licensed under the MIT License.
# See the LICENSE file in the repository for the full license text.

from google.adk.agents import SequentialAgent, Agent

GEMINI_MODEL = "gemini-2.0-flash-exp"

# This agent's output will be saved to session.state["data"]
step1 = Agent(name="Step1_Fetch", model=GEMINI_MODEL, output_key="data")

# This agent will use the data from the previous step.
# We instruct it on how to find and use this data.
step2 = Agent(
    name="Step2_Process",
    model=GEMINI_MODEL,
    instruction="Analyze the information found in state['data'] and provide a summary.",
)

pipeline = SequentialAgent(
    name="MyPipeline",
    sub_agents=[step1, step2],
)

# When the pipeline is run with an initial input, Step1 will execute,
# its response will be stored in session.state["data"], and then
# Step2 will execute, using the information from the state as instructed.

root_agent = pipeline
