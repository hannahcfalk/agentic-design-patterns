import asyncio
import os
from enum import Enum
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from examples.crewai.multi_agent import execute

load_dotenv()


class Provider(Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"


def retrieve_langchain_llm(provider: Provider = Provider.ANTHROPIC):
    # Initialize the LLM
    llm = None
    try:
        match provider:
            case Provider.ANTHROPIC:
                llm = ChatAnthropic(
                    model="claude-sonnet-4-5-20250929",
                    api_key=os.getenv("ANTHROPIC_API_KEY"),
                    temperature=0,
                )
                print(f"Language model intialized: {llm.model}")
            case Provider.OPENAI:
                llm = ChatOpenAI(model="gpt-4-turbo")
                print(f"Language model initialized: {llm.model_name}")
            case _:
                raise ValueError(f"Unknown provider: {provider}")
    except Exception as e:
        print(f"Error initializing the language model: {e}")
    return llm


def main():
    execute()


if __name__ == "__main__":
    main()
