# Based on code from the book "Agentic Design Patterns: A Hands-On Guide
# to Building Intelligent Systems" by Antonio Gullí
# Modifications Copyright (c) 2025 Hannah Falk
#
# This code is licensed under the MIT License.
# See the LICENSE file in the repository for the full license text.

from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Crew, Task, Agent, Process

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Define Agents with specific roles and goals
researcher = Agent(
    role="Senior Research Analyst",
    goal="Find and summarize the latest trends in AI.",
    backstory="You are an experienced research analyst with a knack for identifying key trends and synthesizing information.",
    verbose=True,
    allow_delegation=False,
)

writer = Agent(
    role="Technical Content Writer",
    goal="Write a clear and engaging blog post based in research findings.",
    backstory="You are a skilled writer who can translate complex technical topics into accessible content.",
    verbose=True,
    allow_delegation=False,
)

# Define Tasks for the agents
research_task = Task(
    description="Research the top 3 emerging trends in Artificial Intelligence in 2025. Focus on practical applications and potential impact.",
    expected_output="A detailed summary of the top 3 AI trends, including key points and sources.",
    agent=researcher,
)

writing_task = Task(
    description="Write a 500-word blog post based on the research findings. The post should be engaging and easy for a general audience to understand.",
    expected_output="A complete 500-word blog post about the latest AI trends.",
    agent=writer,
    context=[research_task],
)

# Create the Crew
blog_creation_crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    llm=llm,
    verbose=True,  # Set verbosity for detailed crew execution logs
)


# Execute the Crew
def execute():
    print("## Running the blog creation crew with Gemini 2.0 Flash... ##")
    try:
        result = blog_creation_crew.kickoff()
        print("\n-----------------\n")
        print("## Crew Final Output ##")
        print(result)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
