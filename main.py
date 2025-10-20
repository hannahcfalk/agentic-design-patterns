import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
import asyncio

from examples.langchain import parallelization

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
    llm = retrieve_langchain_llm()
    test_topic = "The history of space exploration"
    await parallelization.execute(test_topic)


if __name__ == "__main__":
    asyncio.run(main())
