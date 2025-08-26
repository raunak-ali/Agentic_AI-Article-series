# Chapter 2: Agents Using LangGraph


What if you just want a quick way to spin up a fully working agent? That’s where LangGraph’s prebuilt helpers come in.

---

### ⚡ create_react_agent

LangGraph ships with a ready-to-use factory method:
```
from langgraph.prebuilt import create_react_agent
```
This creates an agent powered by the ReAct framework (Reason + Act). In simple terms:  
- **Reason** → the LLM decides what to do.  
- **Act** → it either calls a tool, or responds to the user.

---

### 🛠 Parameters

- **llm** → The language model to use (e.g., ChatGoogleGenerativeAI, ChatOpenAI).
- **tools** → List of tools the agent can call. Can be empty if you just want reasoning.
- **state_schema (optional)** → Define custom state structure. Defaults to a simple dict.

📌 Reference: [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

---

### 🧩 Super Short Example

Here’s the smallest possible agent using create_react_agent.  
We won’t add tools yet — just show reasoning + response.

```
# Install dependencies first:
# pip install -qU langchain langgraph langchain-google-genai

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

# ✅ Setup LLM (using your Google API key)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key="YOUR_API_KEY")

# ✅ Create an agent with no tools
agent = create_react_agent(llm, tools=[])

# ✅ Run the agent manually
response = agent.invoke({"messages": [("user", "Explain LangGraph in one sentence.") ]})
print(response["messages"][-1].content)
```

---

#### 🔍 Output:

The agent will generate a concise explanation of LangGraph — reasoning internally, then responding.

---

### 🎯 Why This Matters

- Fastest way to spin up a thinking agent.
- Great starting point before adding tools, custom nodes, or complex workflows.
- Integrates seamlessly with LangGraph graphs — you can drop this agent in as a node.

---
