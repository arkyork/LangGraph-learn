from typing_extensions import TypedDict,Annotated
import operator

# 今回共有する状態
# TypedDict -> キーの状態が固定されている
class CalcState(TypedDict):
    # 入力値
    a : int
    b : int

    # 計算結果
    ans : int

    # ログ(Annotated -> 型に追加メタ情報を付ける)
    logs : Annotated[list[str],operator.add]