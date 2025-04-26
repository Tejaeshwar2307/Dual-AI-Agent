class LangGraphWorkflow:
    def __init__(self, research_agent, drafter_agent):
        self.research_agent = research_agent
        self.drafter_agent = drafter_agent

    def execute(self, query):
        # Step 1: Research Agent performs search and summarization
        structured_data = self.research_agent.search_and_summarize(query)

        # Step 2: Answer Drafter Agent synthesizes the final response
        final_answer = self.drafter_agent.draft_response(structured_data)

        return final_answer