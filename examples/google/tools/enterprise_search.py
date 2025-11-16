# Based on code from the book "Agentic Design Patterns: A Hands-On Guide
# to Building Intelligent Systems" by Antonio Gullí
# Modifications Copyright (c) 2025 Hannah Falk
#
# This code is licensed under the MIT License.
# See the LICENSE file in the repository for the full license text.

import os
from google.adk.agents import Agent
from google.adk.tools import VertexAiSearchTool
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from dotenv import load_dotenv

load_dotenv()

# Define variables required for Session setup and Agent execution
APP_NAME = "vsearch_agent"
USER_ID = "user1234"
SESSION_ID = "session_code_exec_async"

# Configuration
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
VERTEX_SEARCH_DATASTORE_ID = os.getenv("VERTEX_SEARCH_DATASTORE_ID")
DATASTORE_ID = f"projects/{GOOGLE_CLOUD_PROJECT}/locations/global/collections/default_collection/dataStores/{VERTEX_SEARCH_DATASTORE_ID}"
GEMINI_MODEL = "gemini-2.0-flash"

code_agent = Agent(
    name="vertex_search_agent",
    model=GEMINI_MODEL,
    instruction="Answer questions using Vertex AI Search to find information from internal documents. Always cite sources when available.",
    description="Enterprise document search assistant with Vertex AI Search capabilities",
    tools=[VertexAiSearchTool(data_store_id=DATASTORE_ID)],
)


# --- Agent Invocation Logic ---
async def call_agent(query: str):
    # Session and Runner
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    runner = Runner(
        agent=code_agent, app_name=APP_NAME, session_service=session_service
    )

    try:
        # Create message content
        content = types.Content(role="user", parts=[types.Part(text=query)])
        # Process events as they arrive
        async for event in runner.run_async(
            user_id=USER_ID, session_id=SESSION_ID, new_message=content
        ):
            if event.is_final_response():
                print(event.content.parts[0].text)

                # Optional: Show source count
                if event.grounding_metadata:
                    print(
                        f"\nBased on {len(event.grounding_metadata.grounding_chunks)} documents"
                    )
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print(
            "Please ensure your datastore ID is correct and that the service account has the necessary permissions."
        )


# Example usage in main
# async def main():
#     await call_agent("gcp revenue q1 2022")


# if __name__ == "__main__":
#     asyncio.run(main())
