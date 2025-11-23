from langgraph.graph import StateGraph, START ,END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import SystemMessage,ToolMessage
from calc_state import CalcState
from tools import Tool
from calc_state import CalcState

tool = Tool()

# model nodeの作成
def llm_node(state: CalcState,model: ChatGoogleGenerativeAI):
    # LLMがどのツールを使うか使わないかを選択

    response =  model.invoke(
                [
                    SystemMessage(content="You are a math assistant. Use tools if needed."),
                    *state["messages"]
                ]
            )

    return {
        "messages":[
            response
        ],
        "logs":[f"[LLM] {response.content}"],
    }



# tool nodeの作成
def tool_node(state: CalcState):
    
    last_message = state["messages"][-1] # 最後のメッセージ
    logs = []

    for call in last_message.tool_calls:
        t = tool.get_tool_func_name(call["name"])

        result = t.invoke(call["args"])
        logs.append(f"[TOOL] {tool.name} → {result}")
        state["ans"] = result

        yield {"messages": [ToolMessage(content=str(result), tool_call_id=call["id"])]}
        yield {"logs": logs, "ans": result}

def continue_check(state: CalcState):
    last_message = state["messages"][-1] # 最後のメッセージ
    return "tool" if last_message.tool_calls else END


# エージェントの作成

def create_agent():
    graph = StateGraph(CalcState)

    # ノードの追加
    graph.add_node("llm",llm_node)
    graph.add_node("tool",tool_node)

    # エッジの追加
    graph.add_edge(START,"llm")
    # 条件付
    graph.add_conditional_edges("llm", continue_check, ["tool", END])
    
    graph.add_edge("tool", "llm")

    return graph.compile()