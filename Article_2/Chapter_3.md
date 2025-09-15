# Chapter 3: Making Autonomous Agents Using LangGraph

*In the previous chapter, we explored LangGraph's core building blocks—Nodes, Edges, and State. Now let's put them to work by building actual autonomous agents that can think, act, and remember.*

If you're jumping into this chapter directly, here's the quick context: LangGraph lets you create **stateful AI workflows** that go beyond simple chatbots. Instead of linear question-answer chains, you get **agents**, AI systems that can reason through problems, use tools, and maintain memory across interactions.

But what exactly is an **"agent"**, and why does it matter? Let's start there.

---

## What Are AI Agents? (A Quick Primer)

Traditional AI applications follow a **"prompt → response"** pattern. You ask, it answers, conversation ends. Agents are different, they follow a **"think → act → observe → repeat"** cycle until they solve your problem.

Think of the difference between:
- **Traditional**: "Translate this text to French." → Gets one response.
- **Agent**: "Plan my weekend trip to Paris." → Searches flights, checks weather, finds restaurants, compares hotel prices, creates an itinerary.

The agent **autonomously** breaks down complex tasks into steps, uses tools when needed, and builds context over multiple rounds.

*Want to dive deeper into this transition from traditional Gen AI to autonomous systems? Check out my [**Comprehensive guide on Gen AI to Agentic AI**](https://dev.to/raunaklallala/article-1-chapter-d-transition-from-gen-ai-to-agentic-ai-1k68) ,it covers everything from foundational concepts to real-world business applications.*

---

## Types of Agents (The Landscape)

Before we build one, it's worth understanding the different flavors of agents:

### **1. ReAct Agents** (Reason + Act)
- **Pattern**: Think → Tool Use → Observe → Think → Respond
- **Best for**: Research, Q&A, multi-step problem solving
- **Example**: "Find the CEO of the company that makes the iPhone" → Search "iPhone manufacturer" → Get "Apple" → Search "Apple CEO" → Return result

### **2. Planning Agents**
- **Pattern**: Create full plan upfront → Execute steps → Adapt if needed
- **Best for**: Complex workflows, project management
- **Example**: Event planning agent that outlines all tasks before executing them

### **3. Conversational Agents**
- **Pattern**: Maintain ongoing dialogue with memory
- **Best for**: Customer support, tutoring, personal assistants
- **Example**: Support agent that remembers your previous issues and preferences

### **4. Collaborative Agents** (Multi-agent systems)
- **Pattern**: Multiple specialized agents working together
- **Best for**: Complex business processes, specialized domains
- **Example**: HR system with separate agents for screening, interviewing, and onboarding

LangGraph excels at all of these, but today we'll focus on **ReAct agents**—they're the perfect starting point and most versatile.

***

## The ReAct Framework: Science Behind the Magic

LangGraph's `create_react_agent` isn't just a convenient function, it's built on solid research. The ReAct (Reasoning + Acting) framework was introduced in a [**Landmark 2022 paper by researchers at Princeton and Google**](https://arxiv.org/abs/2210.03629).

### **The core insight**:
 Instead of just "thinking" (chain-of-thought) or just "acting" (tool use), the most effective agents alternate between both:

1. **Reasoning traces** help the model plan, track progress, and handle exceptions
2. **Actions** let it gather real-world information and interact with external systems
3. **Interleaving both** creates a synergy where reasoning informs actions, and actions inform reasoning

This isn't just theoretical,The research showed ReAct agents significantly outperformed both pure reasoning and pure action approaches across question-answering, fact verification, and decision-making tasks.

***

## Enter LangGraph's create_react_agent

What if you just want to spin up a fully working agent without building every node and edge from scratch? That's where LangGraph's prebuilt helpers shine.

### **1. The One-Liner Setup**
```python
from langgraph.prebuilt import create_react_agent
```

This creates an agent powered by the ReAct framework we just discussed. Under the hood, it handles:
- **Reason** → the LLM decides what to do next
- **Act** → it either calls a tool or responds to the user
- **Loop** → continues until the problem is solved

### **2. Key Parameters**
- **llm** → The language model to use (ChatGoogleGenerativeAI, ChatOpenAI, etc.)
- **tools** → List of tools the agent can call. Can be empty for reasoning-only mode
- **prompt** → Custom instructions for the agent's behavior
- **state_schema** (optional) → Define custom state structure beyond the defaults

*📌 Full reference: [LangGraph Agent Documentation](https://langchain-ai.github.io/langgraph/reference/agents/)*

***

## Super Short Example (No Tools)

Here's the smallest possible ReAct agent—pure reasoning without external tools:

```python
# Install dependencies first:
# pip install -qU langchain langgraph langchain-google-genai

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

# ✅ Setup LLM (using your Google API key)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key="YOUR_API_KEY")

# ✅ Create an agent with no tools (pure reasoning)
agent = create_react_agent(llm, tools=[])

# ✅ Run the agent
response = agent.invoke({"messages": [("user", "Explain LangGraph in one sentence.")]})
print(response["messages"][-1].content)
```

**Output Example:**
*"LangGraph is a framework for building stateful, multi-step AI workflows where agents can reason through problems, use tools, and maintain context across conversations."*

---

## Why This Matters (The Bigger Picture)

This simple example demonstrates something profound:

- **Fastest path** to a thinking agent—no complex setup required
- **Production-ready** foundation that you can extend with tools, custom nodes, or complex workflows
- **Seamless integration**—this agent can become a node in larger LangGraph systems
- **Research-backed** architecture that's proven to work across diverse tasks

When I first built my own ReAct agent, what struck me was how *natural* the reasoning felt. Instead of getting a raw response, I could see the agent's "thought process"—it felt less like talking to a search engine and more like collaborating with a thoughtful colleague who thinks through problems step by step.

---

## What's Next?

We've just scratched the surface. A reasoning-only agent is useful, but the real power comes when you add **tools**—search engines, calculators, databases, APIs. That's when your agent transforms from a smart conversationalist into an autonomous problem-solver.

*In the next chapter, we'll extend this agent with real tools and see how it handles multi-step, real-world tasks.*

***

**Bridge to Previous Learning:**
- Want to understand the architectural concepts behind this magic? Check out [Core Concepts of LangGraph(A Deep Dive)](http://dev.to/raunaklallala/understanding-core-concepts-of-langgraph-deep-dive-1d7h) for a deep dive into Nodes, Edges, and State.
- New to the whole agent concept? My [Gen AI to Agentic AI guide](https://dev.to/raunaklallala/article-1-chapter-d-transition-from-gen-ai-to-agentic-ai-1k68) covers the foundational shift from traditional AI to autonomous systems.

***