from graph import create_agent
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# 環境変数
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
MODEL_NAME = os.environ["MODEL_NAME"]


model = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=0,
    google_api_key=GEMINI_API_KEY
)

if __name__ == "__main__":

    graph = create_agent(model)

    graph.get_graph().print_ascii()

