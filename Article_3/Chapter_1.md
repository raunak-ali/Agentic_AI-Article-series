
# Chapter 1: Introduction & Tools (Article 3, Example Included)
---

## 🔹 1. Introduction

In the last article, we built a simple one-node agent that could translate text into Shakespearean English. It worked, but it was also very limited. Why? Because in the real world, queries rarely stop at “just generate text.”  
Think about it:  
- “What’s the population of Japan squared?” → requires external knowledge (population data) + calculation.  
- “Summarize today’s top news on AI and write it in haiku form.” → needs web search + reasoning + creative generation.  

A plain LLM agent can’t handle this on its own. That’s where tools come in. **Tools are what transform an LLM from a “chatbot” into a true agent that can do things.**

---

## 🔹 2. What Are Tools in LangChain?

In LangChain, tools are essentially functions or APIs that the LLM can call during its reasoning process.  
Instead of hallucinating a number or making up facts, the model can decide:  
“Wait, I need to use a tool to get this right.”

---

### Types of Tools

**Built-in tools:**  
- Python REPL (lets the agent execute Python code).  
- Calculator (quick math without needing to write code).

**API-based tools:**  
- Wikipedia search (fetch factual data).  
- SerpAPI (Google search results).  
- Any external REST API you wire up.

**Custom tools:**  
You can wrap your own function into a tool, e.g., a financial data fetcher, a database query, or even a business-specific calculator.

---

### Why Tools Matter

- **Accuracy** → Tools reduce hallucinations by letting the agent fetch data instead of guessing.
- **Flexibility** → You can extend your agent with any API relevant to your business or workflow.
- **Actionable AI** → Instead of just producing text, the agent can actually perform tasks.

---

### Limitations & Trade-offs

Like everything, tools aren’t free magic.

- **Latency** → Each tool call adds extra round-trips. Imagine chaining multiple API calls inside one query.
- **Cost** → More calls = higher usage costs if you’re on paid APIs.
- **LLM Guidance** → If the model isn’t prompted well, it might overuse tools unnecessarily, slowing things down.

A good agent is one that knows **when to use a tool, and when not to**.

📖 Reference: [LangChain Tools Documentation](https://python.langchain.com/docs/integrations/tools/)

---

## 🛠️ Tiny Example: Using a Calculator Tool in LangChain

Here’s a barebones example to make this real. Let’s connect an LLM with a simple calculator tool:

```
# ✅ Install required libraries
!pip install -qU langchain langgraph langchain-google-genai

# ✅ Imports
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import PythonREPLTool
from langgraph.prebuilt import create_react_agent

# ✅ Set Google API Key
os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"

# ✅ Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-pro")

# ✅ Define a tool (Python REPL acts like a calculator)
calculator = PythonREPLTool()

# ✅ Create a simple agent with the tool
agent = create_react_agent(llm, tools=[calculator])

# ✅ Run a test query
user_query = "What is 25 * 32?"
for s in agent.stream({"messages": [("user", user_query)]}):
    print(s)

```
➡️ Output:  
69104

This is the simplest taste of agents + tools in LangChain. The LLM doesn’t “guess” the multiplication; it decides to call the calculator tool, gets the result, and gives you the answer.

---

✅ With this, we’ve introduced the next big step: agents + tools.  
In the next chapter, we’ll unpack the Reasoning Loop — how LangChain agents decide when to think, when to act, and when to stop.

---

