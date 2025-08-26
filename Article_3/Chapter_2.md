Awesome—this is the chapter that turns “LLM = autocomplete” into “LLM = problem-solver.”

---

# 🔹 3. The Reasoning Loop (ReAct Pattern)

## 3.1 The idea 
Most questions need more than a single reply.
Example: “What’s the population of Japan squared?”

A good agent will:

1. **Think**: I should look up Japan’s population.
2. **Act**: Call a search/Wikipedia tool.
3. **Observe**: Tool returns “\~125,000,000”.
4. **Answer**: Compute `125,000,000²` and return the result.

That’s the **ReAct** pattern: **Reason** (Thought) ↔ **Act** (use a tool), loop until you can confidently answer. The original paper introduced interleaving “reasoning traces” with “actions” so the model plans, fetches facts, handles errors, and then concludes. ([arXiv][1], [Google Research][2], [ReAct][3])

---

## 3.2 What ReAct looks like under the hood

**Core roles:**

* **Thought**: free-form reasoning the model writes to plan (“I need a web lookup”).
* **Action**: a *structured* tool call (name + arguments).
* **Observation**: tool output fed back to the model as new context.
* **Answer**: final, user-facing result; loop stops here.

**Why interleave?**
Reasoning helps the model decide *which* tool, *when*, and *how* to use it; acting gets fresh facts or runs computations the model can’t “guess.” This synergy reliably beats “just think” or “just act.” ([arXiv][1], [Google Research][2])

**In LangChain/LangGraph terms:**

* A **tool** is a function/API (with a name, schema, and description) the model can call.
* A **ReAct agent** is an LLM loop that keeps selecting tools and ingesting observations until a stop condition (final answer, guardrail, or max steps).
* **LangGraph** wraps this as a compiled **graph** with state, nodes (LLM, Tool), and edges controlling the loop. The prebuilt helper is `create_react_agent`. ([LangChain AI][4])

---

## 3.3 Anatomy of a ReAct agent prompt (practical)

A solid ReAct system prompt tells the model:

* What it is solving.
* Which tools exist (names + when to use them).
* How to emit **Action** calls (structured).
* When to stop and give **Final Answer**.

*Sketch:*

```
You are a reasoning agent. When needed, use tools.
If you can answer directly, do so.
Otherwise follow: 
Thought: ...
Action: {"tool": "<name>", "tool_input": "<args>"}
Observation: <tool output here>
... repeat ...
Final Answer: <concise answer>
```

LangChain’s modern stack handles the JSON/tool-call formatting for you; you mainly provide tool descriptions and keep the prompt crisp. (LangChain’s legacy ReAct chain is marked deprecated; new work should use LangGraph.) ([LangChain][5])

---

## 3.4 How LangGraph runs the loop

At a high level:

```
state = { messages: [...], scratchpad: [] }

while not done:
  llm_output = LLM(state)
  if llm_output contains tool_call:
      tool = tools[tool_call.name]
      obs  = tool(tool_call.args)
      state.messages += [("tool", obs)]
  else:
      done = True
      state.answer = llm_output
```

* **State** carries messages (user, assistant, tool) and any scratchpad/variables.
* The prebuilt **`create_react_agent`** wires an LLM node + Tool node + a controller loop, with sensible stop conditions and max iterations. ([LangChain AI][4])

---

## 3.5 Tiny working example (Gemini + Search + Python “calculator”)

This mirrors the “Japan population squared” example. We use:

* **DuckDuckGo search tool** to fetch population (no key needed).
* **Python REPL tool** to square the number.
* **LangGraph `create_react_agent`** to run the ReAct loop.

```python
# Install
!pip install -qU langchain langgraph langchain-google-genai langchain-community

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun, PythonREPLTool
from langgraph.prebuilt import create_react_agent

# 1) LLM (Gemini)
os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)

# 2) Tools
search = DuckDuckGoSearchRun()   # web search (fetch facts)
python = PythonREPLTool()        # safe eval; prints result for return

tools = [search, python]

# 3) ReAct Agent (LangGraph)
agent = create_react_agent(
    llm=llm,
    tools=tools,
    # Optional: nudge the model to use tools sparingly and show work
    state_modifier=(
        "Use tools only when needed. "
        "When math is required, write a short plan, then call Python. "
        "Cite what you looked up. Return a Final Answer when done."
    ),
)

# 4) Run
question = "What is the population of Japan squared? Provide the final number only."
events = agent.stream({"messages": [("user", question)]})
for e in events:
    print(e)  # You'll see Thought/Action/Observation/Answer-like steps
```

Notes:

* **DuckDuckGo tool**: simple, fast, often enough for headline facts. For a Wikipedia-only version, use `WikipediaAPIWrapper` + `WikipediaQueryRun` from LangChain community tools. ([LangChain][6])
* **Python REPL** returns only what’s printed. Make sure the agent prints its result in tool code. (LangChain’s Python REPL docs explain this caveat.) ([LangChain][7])

---

## 3.6 Design tips (so it doesn’t fall apart)

* **Tool descriptions matter**: be explicit about *when* to use each tool. The model’s choice quality tracks the clarity of these descriptions. (This is why ReAct prompts include precise, minimal instructions.) ([LangChain][8])
* **Guardrails**: set max tool calls/steps and timeouts; log traces (LangSmith) when you go production. ([LangChain][9])
* **Latency & cost**: each tool hop adds delay. Prefer one high-signal lookup over many tiny calls. Cache frequent lookups.
* **Numerical reliability**: route math to Python/Calculator; don’t trust raw LLM arithmetic. ([LangChain][7])
* **Traceability**: ReAct is popular because you can *see* the chain of Thought/Action/Observation, which helps audits and debugging. ([arXiv][1])

---

## 3.7 The “Japan population squared” explained (end-to-end)

* **Thought**: “I need current population.”
* **Action**: call `DuckDuckGoSearchRun` with a query like *“Japan population”*.
* **Observation**: search snippet returns a value (e.g., \~125,000,000).
* **Action**: call `PythonREPLTool` with `print(125_000_000**2)`.
* **Observation**: `15625000000000000`.
* **Answer**: return the number (with optional citation note).

This is the exact loop you’ll see in the stream output from the example above. ([LangChain][6])

---

## References (for readers who want the deeper cut)

* **ReAct paper** (Yao et al., 2022) — reasoning + acting interleaved. ([arXiv][1])
* **LangGraph prebuilt ReAct agent** (`create_react_agent`) — reference + params. ([LangChain AI][4])
* **LangGraph agents guide** — how agent graphs loop with tools and state. ([LangChain AI][10])
* **LangChain tools** — DuckDuckGoSearchRun, Python REPL, and more. ([LangChain][6])
* **LangChain agent docs** (and deprecation note for legacy chains). ([LangChain][5])

[1]: https://arxiv.org/abs/2210.03629?utm_source=chatgpt.com "ReAct: Synergizing Reasoning and Acting in Language Models - arXiv"
[2]: https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/?utm_source=chatgpt.com "ReAct: Synergizing Reasoning and Acting in Language Models"
[3]: https://react-lm.github.io/?utm_source=chatgpt.com "ReAct: Synergizing Reasoning and Acting in Language Models"
[4]: https://langchain-ai.github.io/langgraph/reference/agents/?utm_source=chatgpt.com "Agents - GitHub Pages"
[5]: https://python.langchain.com/api_reference/langchain/agents/langchain.agents.react.base.ReActChain.html?utm_source=chatgpt.com "ReActChain — LangChain documentation"
[6]: https://python.langchain.com/api_reference/community/tools/langchain_community.tools.ddg_search.tool.DuckDuckGoSearchRun.html?utm_source=chatgpt.com "DuckDuckGoSearchRun — 🦜🔗 LangChain documentation"
[7]: https://python.langchain.com/docs/integrations/tools/python/?utm_source=chatgpt.com "Python REPL | 🦜️🔗 LangChain"
[8]: https://python.langchain.com/docs/tutorials/agents/?utm_source=chatgpt.com "Build an Agent - Python LangChain"
[9]: https://www.langchain.com/langgraph?utm_source=chatgpt.com "LangGraph - LangChain"
[10]: https://langchain-ai.github.io/langgraph/agents/agents/?utm_source=chatgpt.com "Start with a prebuilt agent - GitHub Pages"
