## LangGraphとは？
LangGraph は、LLMを利用したアプリケーションを
グラフ構造として設計できるフレームワークです。

### 構成要素

- State・・・状態。基本的に共有される。
- Node・・・処理を行う
- Edge・・・どのノードへ遷移するか
- Graph・・・NodeとEdgeで構成

ワークフローをグラフ構造にして、マルチエージェントのような複数のエージェントが協調したシステムなどを構成することができる。

## LangGraph × Gemini API Calculator Agent

本レポジトリのコードは、LangGraph と Gemini API を組み合わせて、
関数ツールを呼び出しながら計算する AI エージェントを実装したサンプルとなっています。

### Gemini APIを利用

無料で使えるので、今回はGemini APIを選定。

```bash
pip install -U "langchain[google-genai]" langgraph
```

### ディレクトリの構成
```
├─ main.py              # 実行スクリプト
├─ calc_state.py        # Stateの定義
├─ tools.py             # add / multiply などの計算ツール
├─ show_graph.py        # Ascii ArtでGraphの可視化
└─ graph.py             # LangGraph構築
```
