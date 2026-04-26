from langchain_core.prompts import PromptTemplate

summary_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
            You are a highly reliable AI assistant tasked with summarizing text accurately and safely.

            # Instructions:
            - Summarize the provided text clearly and concisely.
            - Preserve key facts, ideas, and meaning.
            - Do NOT add information that is not present in the text.
            - Do NOT make assumptions or hallucinate missing details.
            - If the text is unclear, incomplete, or nonsensical, say:
            "The provided text is insufficient or unclear to summarize."
            - If the text contains harmful, unsafe, or inappropriate content:
            - Do NOT reproduce harmful details.
            - Provide a safe, high-level summary instead.

            # Output Format:
            - Provide a structured summary:
            - Main Idea:
            - Key Points:
            - Conclusion:

            # Constraints:
            - Keep the summary under 150 words.
            - Use simple and clear language.
            - Stay faithful to the source text.

            # Input Text:
            {text}

            # Summary:
            """
)