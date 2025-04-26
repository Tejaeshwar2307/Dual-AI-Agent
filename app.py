import streamlit as st
from dotenv import load_dotenv
from agents.research_agent import ResearchAgent
from agents.drafter_agent import AnswerDrafterAgent
from workflows.langgraph_workflow import LangGraphWorkflow
import json
import os
from tavily import TavilyClient
from langchain.llms import OpenAI

# Load environment variables
load_dotenv()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "query_history" not in st.session_state:
    st.session_state.query_history = []

# Sidebar for settings
st.sidebar.title("Settings")
verbose_mode = st.sidebar.checkbox("Verbose Mode", value=False)
clear_history = st.sidebar.button("Clear History")

if clear_history:
    st.session_state.messages = []
    st.session_state.query_history = []
    st.experimental_rerun()

# Main title
st.title("AI Agent-Based Deep Research System")

# Chat-like interface
st.subheader("Conversation")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_query = st.chat_input("Enter your research query:")

if user_query:
    # Add user query to history
    st.session_state.query_history.append(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Progress indicators
    progress_bar = st.progress(0)
    status_text = st.empty()
    status_text.text("Step 1: Searching the web...")

    # Initialize agents and workflow
    research_agent = ResearchAgent()
    drafter_agent = AnswerDrafterAgent(api_key=os.getenv("OPENAI_API_KEY"))
    workflow = LangGraphWorkflow(research_agent, drafter_agent)

    # Step 1: Research Agent performs search and summarization
    class ResearchAgent:
        def __init__(self, api_key):
         self.api_key = api_key
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
    # Display structured data if verbose mode is enabled
    if verbose_mode:
        st.subheader("Search Results")
        st.table(structured_data)

    # Step 2: Answer Drafter Agent synthesizes the final response
    progress_bar.progress(66)
    status_text.text("Step 3: Drafting the final response...")
    final_answer = workflow.execute(user_query)

    # Update progress bar and status
    progress_bar.progress(100)
    status_text.text("Complete!")

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": final_answer})
    with st.chat_message("assistant"):
        st.markdown(final_answer)

    # Feedback mechanism
    st.subheader("Was this response helpful?")
    feedback = st.radio("Rate the response:", ["👍 Yes", "👎 No"], horizontal=True)
    if feedback == "👎 No":
        user_feedback = st.text_area("Please provide feedback:")
        if st.button("Submit Feedback"):
            st.success("Thank you for your feedback!")
            # Save feedback to a file or database
            feedback_data = {
                "query": user_query,
                "response": final_answer,
                "feedback": user_feedback
            }
            with open("data/feedback.json", "a") as f:
                json.dump(feedback_data, f)
                f.write("\n")

# Query history sidebar
st.sidebar.subheader("Query History")
for idx, query in enumerate(st.session_state.query_history):
    if st.sidebar.button(f"{idx + 1}. {query}"):
        st.session_state.messages = [{"role": "user", "content": query}]
        st.experimental_rerun()

       