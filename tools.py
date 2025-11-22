from langchain.tools import tool
from dataclasses import dataclass,field
from langchain_core.tools.base import BaseTool

# 今回用意した計算ツール

@tool
def add(a: int, b:int) -> int:
    return a + b

@tool
def multiply(a :int, b:int) -> int:
    return a * b

@tool 
def subtract(a:int ,b:int) -> int:
    return a - b

@tool
def mess_calc(a: int, b: int) -> int:
    return (a - b) * (a + b) * 4 * a * b

@dataclass
class Tool:
    tool_func_list :list[BaseTool] =  [add, multiply, subtract , mess_calc]
    tool_func_name :dict[str,BaseTool] = field(init=False)

    def __post_init__(self):
         self.tool_func_name = {tool.name: tool for tool in self.tool_func_list}

    # ツールを返す
    def get_tool_func_list(self) -> list[BaseTool]:
        return self.tool_func_list
    
    # ツール名を含んだ辞書を返す
    def get_tool_func_name(self) -> dict[str,BaseTool]:
        return self.tool_func_name