# Based on code from the book "Agentic Design Patterns: A Hands-On Guide
# to Building Intelligent Systems" by Antonio Gullí
# Modifications Copyright (c) 2025 Hannah Falk
#
# This code is licensed under the MIT License.
# See the LICENSE file in the repository for the full license text.

from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from google.genai import types

GEMINI_MODEL = "gemini-2.0-flash-exp"


# 1. A simple function tool for the core capability.
# This follows the best practice of separating actions from reasoning.
def generate_image(prompt: str) -> dict:
    """
    Generates an image based on a textual prompt.

    Args:
        prompt: A detailed description of the image to generate.

    Returns:
        A dictionary with the status and the generated image bytes.
    """
    print(f"TOOL: Generating image for prompt: '{prompt}'")
    # In a real implementation, this would call an image generation API.
    # For this example, we return mock image data.
    mock_image_bytes = b"mock_image_data_for_a_cat_wearing_a_hat"
    return {
        "status": "success",
        # The tool returns the raw bytes, the agent will handle the Part creation.
        "image_bytes": mock_image_bytes,
        "mime_type": "image/png",
    }


# 2. Refactor the ImageGeneratorAgent into an LlmAgent
# It noew correctly uses the input passed to it.
image_generator_agent = LlmAgent(
    name="ImageGen",
    model=GEMINI_MODEL,
    description="Generates an image based on a detailed text prompt.",
    instruction=(
        "You are an image generation specialist. Your task is to take the user's request "
        "and use the `generate_image` tool to create the image. "
        "The user's entire request should be used aas the 'prompt' argument for the tool. "
        "After the tool returns the image bytes, you MUST output the image."
    ),
    tools=[generate_image],
)

# 3. Wrap the corrected agent in an AgentTool.
# The AgentTool will use the agent's description automatically.
image_tool = agent_tool.AgentTool(
    agent=image_generator_agent,
)

# 4. The parent agent that uses the image generation tool.
artist_agent = LlmAgent(
    name="Artist",
    model=GEMINI_MODEL,
    instruction=(
        "You are a creative artist. First, invent a creative and descriptive prompt for an image. "
        "Then, use the `ImageGen` tool to generate the image using your prompt."
    ),
    tools=[image_tool],
)


root_agent = artist_agent
