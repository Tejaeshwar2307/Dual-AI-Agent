import os
from tavily import TavilyClient
from langchain.llms import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("TAVILY_API_KEY")

class ResearchAgent:
    def __init__(self):
        self.tavily_client = TavilyClient(api_key)
        self.llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4")

    def search_and_summarize(self, query):
        # Perform web search
        search_results = self.tavily_client.search(query)

        # Debugging: Print the structure of search_results
        print("Search Results:", search_results)

        # Summarize results using LLM
        summarized_results = []
        for result in search_results:
            # Ensure result is a dictionary and contains the expected keys
            if isinstance(result, dict) and 'content' in result:
                summary = self.llm(f"Summarize the following content: {result['content']}")
                summarized_results.append({
                    "title": result.get("title", "No Title"),
                    "summary": summary
                })
            else:
                print(f"Unexpected result format: {result}")

        return summarized_results