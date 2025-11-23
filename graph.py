from langgraph.graph import StateGraph, START ,END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import SystemMessage,ToolMessage
from calc_state import CalcState
from tools import Tool
from calc_state import CalcState

tool = Tool()
tools_by_name = tool.get_tool_func_name()


def create_agent(model_with_tools: ChatGoogleGenerativeAI):

    # model nodeの作成
    def llm_node(state: CalcState):
        # LLMがどのツールを使うか使わないかを選択

        response = model_with_tools.invoke(
            [
                SystemMessage(
                    content=(
                        "You are a helpful math assistant. "
                        "Use the provided tools to perform arithmetic on the given inputs."
                    )
                )
            ]
            + state["messages"]
        )
        return {
            "messages": [response],
            "logs": [f"[LLM] {response.content}"],
        }



    # tool nodeの作成
    def tool_node(state: CalcState):
        
        last_message = state["messages"][-1]
        result_messages: list[ToolMessage] = []
        logs: list[str] = []

        for tool_call in last_message.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            t = tools_by_name[tool_name]
            observation = t.invoke(tool_args)

            # ans にも保存（最後の計算結果として）
            state["ans"] = observation

            # ToolMessage を作って返す
            result_messages.append(
                ToolMessage(
                    content=str(observation),
                    tool_call_id=tool_call["id"],
                )
            )
            logs.append(f"[TOOL] {t.name} → {observation}")

        return {
            "messages": result_messages,
            "ans": state["ans"],
            "logs": logs,
        }


    def should_continue(state: CalcState):
        last_message = state["messages"][-1]
        if last_message.tool_calls:
            return "tool"
        return END



    # エージェントの作成
    graph = StateGraph(CalcState)

    # ノードの追加
    graph.add_node("llm",llm_node)
    graph.add_node("tool",tool_node)

    # エッジの追加
    graph.add_edge(START,"llm")
    # 条件付
    graph.add_conditional_edges(
        "llm",
        should_continue,
        ["tool", END],
    )    
    graph.add_edge("tool", "llm")

    return graph.compile()