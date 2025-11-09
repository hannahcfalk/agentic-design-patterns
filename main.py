import asyncio
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from examples.google.tools.enterprise_search import call_agent

load_dotenv()


def retrieve_langchain_llm():
    # Initialize the LLM
    try:
        llm = ChatAnthropic(
            model="claude-sonnet-4-5-20250929",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            temperature=0,
        )
        print(f"Language model intialized: {llm.model}")
    except Exception as e:
        print(f"Error initializing the language model: {e}")
        llm = None
    return llm


async def main():
    await call_agent("gcp revenue q1 2022")


if __name__ == "__main__":
    asyncio.run(main())
