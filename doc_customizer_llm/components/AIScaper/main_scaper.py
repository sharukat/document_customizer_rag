# ==========================================================================================================================
# IMPORT DEPENDENCIES
# ==========================================================================================================================

import os
from dotenv import load_dotenv

# LANGCHAIN MODULES
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import initialize_agent, AgentType
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import (create_sync_playwright_browser,)


# ==========================================================================================================================
# LOAD API KEYS FROM THE .env FILE
# ==========================================================================================================================

load_dotenv(dotenv_path="/Users/sharukat/Documents/ResearchYU/Code/doc-customizer-llm/doc_customizer_llm/.env")
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")   # Claude LLM API Key
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")   # LangChain LLM API Key (To use LangSmith)

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "langchain-webscrape"


# ==========================================================================================================================
# MAIN CODE
# ==========================================================================================================================

llm = ChatAnthropic(temperature=0, model_name="claude-3-sonnet-20240229")

def main(web_page: str):
    print(f"AI-based Web Scraping Initiated!: {web_page}")
    sync_browser = create_sync_playwright_browser()
    toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=sync_browser)
    tools = toolkit.get_tools()

    agent_chain = initialize_agent(
        tools,
        llm,
        agent = AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    system = f"You are a helpful assistant that scrape given url to extract all the code as it is and return the result in markdown format"
    human = f"url : {web_page}"
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
    result = agent_chain.run(prompt)
    print(result)


# ==========================================================================================================================
# TEST EXECUTIONS
# ==========================================================================================================================

main(web_page="https://www.geeksforgeeks.org/save-and-load-models-in-tensorflow/")