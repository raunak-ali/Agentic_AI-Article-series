# 🔹 4. Custom Tools & Multi-Step Workflows in LangGraph

## 4.1 Why LangGraph Shines Here

In LangChain, an “agent with tools” is usually just a loop: LLM → tool → back to LLM. It works, but quickly gets messy once you add multiple tools, intermediate reasoning, and longer queries.

LangGraph formalizes this with:

* **Nodes** → execution units (LLMs, tools, or even sub-graphs).
* **Edges** → explicit control flow between nodes.
* **State** → holds everything persistent: messages, tool results, scratchpad, metadata.

This graph-based structure makes multi-step tool workflows:
✅ Easier to **visualize** (via LangGraph Studio).
✅ Easier to **debug** (trace each edge).
✅ Easier to **scale** (swap tools, add more nodes, persist memory).

⚠️ **Caution:** More steps ≠ better. Each extra hop means latency, cost, and higher chance of the agent drifting off. Keep graphs as lean as the task allows.

---

## 4.2 Making Custom Tools in LangChain

LangChain provides a very clear way to define your own tools.
Requirements for a valid tool:

* A **Python function**.
* **Type annotations** on the arguments and return values (so LangChain can build a schema).
* A clear **docstring** describing what the tool does, when to use it, and how.

Example: a custom tool that reverses a string.

```python
from langchain.tools import tool

@tool
def reverse_text(text: str) -> str:
    """
    Reverses the input string.
    Use this when you want to flip text backwards.
    Example: 'hello' -> 'olleh'
    """
    return text[::-1]
```

Why these rules?

* **Annotations** (`text: str -> str`) let LangChain auto-generate JSON schemas for tool calls.
* **Docstring** becomes the natural-language description given to the LLM, guiding when and how to call it.
* Without these, the agent either can’t see the tool or won’t know when to use it.

---

## 4.3 Adding Custom Tools into LangGraph

Once you’ve got a valid tool, you can drop it into a LangGraph ReAct agent just like the built-ins:

```python
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import os

os.environ["GOOGLE_API_KEY"] = "YOUR_KEY"

llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)

# Custom + built-in tools
tools = [reverse_text]

agent = create_react_agent(
    llm=llm,
    tools=tools,
    state_modifier="Use the reverse_text tool when user asks for reversed words."
)

events = agent.stream({"messages": [("user", "Reverse the word 'LangGraph'")]})
for event in events:
    print(event)
```

That’s it. Your tool behaves like any other built-in one.

---

## 4.4 Multi-Step Workflows in LangGraph

Now imagine combining multiple tools:

* **Search tool** (fetch facts).
* **Calculator tool** (do math).
* **Custom reverse\_text tool** (format output).

LangGraph wires these as nodes with state. Example workflow:

1. **User query → LLM node.**
2. **Edge:** LLM decides to call `search`.
3. **Node:** Search tool returns result.
4. **Edge:** Result flows back into LLM.
5. **Node:** LLM decides to call `calculator`.
6. **Node:** Calculator returns result.
7. **Edge:** LLM formats final answer (maybe reversed if asked).
8. **State:** keeps the original query, intermediate observations, and the final answer.

---

### 🔎 Visual Representation (ASCII Graph)

```
 [User Query]
      |
      v
   [LLM Node]
      |
      | (decides action)
      v
 [Search Tool Node] -----> (observation returned) -----
      |                                              |
      v                                              |
   [LLM Node] (updates reasoning)                    |
      |                                              |
      v                                              |
 [Calculator Tool Node]                              |
      |                                              |
      v                                              |
   [LLM Node] <---------------------------------------
      |
      v
 [Custom Reverse Tool Node] (if needed)
      |
      v
 [Final Answer + State Stored]
```

---

## 4.5 References

* [LangChain Tools Guide](https://python.langchain.com/docs/modules/tools/)
* [LangGraph Prebuilt Agents](https://langchain-ai.github.io/langgraph/how-tos/create-react-agent/)
* [LangGraph Studio](https://langchain-ai.github.io/langgraph/concepts/langgraph_studio/)

---
