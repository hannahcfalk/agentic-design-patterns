# Based on code from the book "Agentic Design Patterns: A Hands-On Guide
# to Building Intelligent Systems" by Antonio Gullí
# Modifications Copyright (c) 2025 Hannah Falk
#
# This code is licensed under the MIT License.
# See the LICENSE file in the repository for the full license text.

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def execute(llm):

    # Prompt 1: Extract Information
    prompt_extract = ChatPromptTemplate.from_template(
        "Extract the technical specifications from the following text:\n\n{text_input}"
    )

    # Prompt 2: Transform to JSON
    prompt_transform = ChatPromptTemplate.from_template(
        "Transform the following specifications into a JSON object with 'cpu', 'memory', and 'storage' as keys:\n\n{specifications}"
    )

    # Build the Chain using  (LangChain Expression Language)

    # StrOutputParser converts the LLM's message output to a simple string
    extraction_chain = prompt_extract | llm | StrOutputParser()

    # The full chain passes the output of the extraction chain into the 'specifications' variable for the transformation prompt.
    full_chain = (
        {"specifications": extraction_chain}
        | prompt_transform
        | llm
        | StrOutputParser()
    )

    # Run the chain
    input_text = "The new laptop model features a 3.5 GHz octa-core processor, 16GB of RAM, and a 1TB NVMe SSD."

    # Execute the full chain
    final_result = full_chain.invoke({"text_input": input_text})

    print("\n--- Final JSON Output ---")
    print(final_result)
