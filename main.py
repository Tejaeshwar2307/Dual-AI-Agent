import os
from dotenv import load_dotenv
from agents.research_agent import ResearchAgent
from agents.drafter_agent import AnswerDrafterAgent
from workflows.langgraph_workflow import LangGraphWorkflow

# Load environment variables
load_dotenv()

def main():
    # Initialize agents
    research_agent = ResearchAgent(api_key=os.getenv("TAVILY_API_KEY"))
    drafter_agent = AnswerDrafterAgent(api_key=os.getenv("OPENAI_API_KEY"))
    # Initialize workflow
    workflow = LangGraphWorkflow(research_agent, drafter_agent)

    # User query
    user_query = input("Enter your research query: ")

    # Execute workflow
    final_answer = workflow.execute(user_query)
    print("\nFinal Answer:")
    print(final_answer)

if __name__ == "__main__":
    main()