from tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from langchain.messages import HumanMessage
from graph import create_agent

load_dotenv()

# 環境変数
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
MODEL_NAME = os.environ["MODEL_NAME"]


model = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=0,
    google_api_key=GEMINI_API_KEY
)

# ツールの適用

tool = Tool()

model_with_tools = model.bind_tools(tool.get_tool_func_list())


state = {
    "a": 5,
    "b": 8,
    "ans": 0,
    "messages": [HumanMessage(content="Perform a custom calculation.a = 5,b = 8")],
    "logs": []
}

agent = create_agent(model_with_tools)

result = agent.invoke(state)

print("\n=== RESULT ===")
print(result["ans"])

print("\n=== LOGS ===")
for log in result["logs"]:
    print("・", log)