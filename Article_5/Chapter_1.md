---

## 🔹 1. Why Memory Matters + Types of Memory in LangChain

In the last article, we built **multi-agent workflows** — systems where different agents specialize in research, writing, or critique. These were powerful, but there was still one glaring limitation: they were **stateless**.

That means once the graph execution ended, everything was forgotten. Every time you started fresh, the system had no idea what you had asked before.

That’s fine if you’re running **single-shot queries** like:

> “Translate this sentence into Shakespearean English.”

But in real-world use cases, it quickly becomes a deal-breaker:

* A **travel planner agent** that forgets you’re vegetarian each time you ask for new destinations.
* A **customer support bot** that resets after every question, forcing you to re-explain your issue.
* A **personal tutor agent** that doesn’t remember what topics you already studied.

Think of it like a friend who forgets every conversation right after you hang up — frustrating and unnatural.

This is why **memory** matters. Memory makes agents feel like consistent, reliable assistants rather than one-off calculators. And here’s the key: **LangGraph + LangChain give us two separate but complementary mechanisms — state and memory.**

---

### ⚡ State vs. Memory

Up until now, in our LangGraph workflows, we’ve worked with **State**.

* **State in LangGraph** is like a **whiteboard** during execution. It stores the current input, intermediate outputs, and final results while the graph is running. But once the execution finishes, that whiteboard is wiped clean — unless you explicitly persist it somewhere.

Now comes **Memory**, which is different:

* **Memory in LangChain** is like a **diary or notebook** that the agent carries across interactions. It doesn’t vanish after execution. It remembers history, summaries, or even embeddings from past conversations.

👉 Put simply:

* **State = short-lived, runtime container (temporary working memory).**
* **Memory = persistent, cross-session context (long-term memory).**

When you combine the two, you get **stateful execution (LangGraph)** that is also **context-aware across time (LangChain Memory)**.

---
### 🔹 Types of Memory in LangChain (with LangGraph context)

LangChain gives us several memory modules. Let’s see how each one works **and** how it would fit into a **LangGraph agent workflow**.

---

#### 1. **BufferMemory**

* **What it does:** Keeps the raw chat history exactly as it happened.
* **Pros:** Simple, transparent.
* **Cons:** Grows too large in long conversations.

👉 **In LangGraph:**
Imagine a **single-agent node** answering user questions. Without memory, each new run starts fresh. With BufferMemory, every past exchange is automatically appended to the state when the node executes.

```python
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI

# LLM
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

# Memory
memory = ConversationBufferMemory(return_messages=True)

# Storing messages
memory.save_context({"input": "Hi, I like Italian food."}, {"output": "Got it!"})
memory.save_context({"input": "Suggest me a dinner option."}, {"output": "Pasta works well."})

print(memory.load_memory_variables({}))
# {'history': 'User: Hi, I like Italian food.\nAI: Got it!\nUser: Suggest me a dinner option.\nAI: Pasta works well.'}
```

Here, if we plugged this into a **LangGraph node**, every time the node runs, it would automatically feed the *entire history* into the LLM.

---

#### 2. **ConversationSummaryMemory**

* **What it does:** Stores *summaries* of the dialogue instead of raw history.
* **Pros:** Keeps context compact.
* **Cons:** Summaries may lose subtle details.

👉 **In LangGraph:**
Useful when you expect **long-running workflows** (like a travel planner that spans weeks of conversation). The node receives a **short summary string** instead of bloated raw history.

```python
from langchain.memory import ConversationSummaryMemory

summary_memory = ConversationSummaryMemory(llm=llm)

# Simulate conversation
summary_memory.save_context({"input": "I love beaches and vegetarian food."}, {"output": "Great, noted your preferences."})
summary_memory.save_context({"input": "Plan a 5-day Bali trip."}, {"output": "Sure, including beach stays & veg food."})

print(summary_memory.load_memory_variables({}))
# {'history': 'User likes beaches and vegetarian food. Then asked for a Bali trip, AI suggested accordingly.'}
```

If tied to a **LangGraph travel planner node**, instead of re-feeding 100 lines of context, it injects just the **essence** of the conversation into state.

---

#### 3. **VectorStoreMemory**

* **What it does:** Encodes messages into embeddings and saves in a vector DB (like FAISS, Pinecone, or Chroma).
* **Pros:** Scalable, retrieves only *relevant past info*.
* **Cons:** Requires DB setup, retrieval logic.

👉 **In LangGraph:**
Perfect for **knowledge-heavy agents** (research assistants, customer service bots). The graph node queries the vector DB each time it executes, and only relevant chunks are pulled back into state.

```python
from langchain.memory import VectorStoreRetrieverMemory
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

# Setup FAISS vector store
embeddings = OpenAIEmbeddings()
faiss_store = FAISS.from_texts(["User likes vegetarian food", "User wants budget trips"], embeddings)

# Memory wrapper
retriever = faiss_store.as_retriever()
vector_memory = VectorStoreRetrieverMemory(retriever=retriever)

# Retrieve relevant info for a new query
print(vector_memory.load_memory_variables({"input": "Suggest travel options"}))
# {'history': 'User likes vegetarian food\nUser wants budget trips'}
```

Here, a **LangGraph TravelPlanner node** could automatically pull just the relevant user preferences instead of bloating the prompt with everything.

### 📝 Quick Comparison Table

| Memory Type           | How It Works                   | Pros                         | Cons                         | Best Use Case                         |
| --------------------- | ------------------------------ | ---------------------------- | ---------------------------- | ------------------------------------- |
| **BufferMemory**      | Stores raw history text        | Simple, transparent          | Bloats quickly in long chats | Debugging, small assistants           |
| **SummaryMemory**     | Stores LLM-generated summaries | Compact, scalable            | May lose details             | Customer support, tutoring            |
| **VectorStoreMemory** | Stores embeddings in DB        | Scalable, semantic retrieval | Setup overhead               | Long-term assistants, knowledge-heavy |

---

---

### ⚡ Quick Recap

* **BufferMemory:** Feeds full chat history into LangGraph nodes (like a “chat log”).
* **SummaryMemory:** Feeds summarized context, efficient for long workflows.
* **VectorStoreMemory:** Feeds *relevant retrieved snippets* into the node from a long-term memory store.

Combined with **State**, you now have both **runtime execution memory (state)** and **persistent, cross-session memory (LangChain memory modules)**.

---

