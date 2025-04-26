from langchain.llms import OpenAI

class AnswerDrafterAgent:
    def __init__(self, api_key):
        self.llm = OpenAI(api_key=api_key, model="gpt-4o")

    def draft_response(self, structured_data):
        # Combine structured data into a single prompt
        combined_data = "\n".join([f"{item['title']}: {item['summary']}" for item in structured_data])
        prompt = f"Synthesize the following information into a coherent response:\n{combined_data}"

        # Generate final answer
        final_answer = self.llm(prompt)
        return final_answer