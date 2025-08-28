---

# 🔹 3. Design Patterns for Multi-Agent Collaboration

When building multi-agent systems, it’s not enough to just connect agents randomly. The *design pattern* you choose determines how effective the collaboration will be. LangGraph provides the primitives (nodes, edges, state), but **patterns give structure** to multi-agent workflows.

---

### 🔹 1. Role Specialization

* **Concept:** Each agent has a **defined role**. Instead of one generalist, you build a *team of specialists*.
* **Example:**

  * *Researcher* → fetches factual data.
  * *Writer* → turns facts into prose.
  * *Critic* → reviews tone, style, or correctness.
* **Advantage:** Mimics human workflows → better results, less confusion.

```python
researcher = create_react_agent(llm, tools=[wiki_tool])
writer = create_react_agent(llm, tools=[])
critic = create_react_agent(llm, tools=[])
```

---

### 🔹 2. Pipelining

* **Concept:** One agent’s output flows directly into the next agent’s input (linear workflow).
* **Example:**
  *Researcher* → notes → *Writer* → draft → *Critic* → feedback.
* **When to Use:** Tasks that naturally follow a sequence, like **data gathering → synthesis → editing**.
* **Limitation:** Rigid; if one step fails, the entire pipeline breaks.

---

### 🔹 3. Peer Review (Debate Pattern)

* **Concept:** Two or more agents critique or “debate” each other before finalizing.
* **Example:**

  * Agent A: Writes an essay.
  * Agent B: Points out flaws.
  * State stores both versions, and a **final node** reconciles them.
* **Advantage:** Reduces hallucination, improves accuracy.
* **Warning:** More expensive and slower (multiple agents running in loops).

---

### 🔹 4. Supervisor Pattern

* **Concept:** Instead of hardcoding order, a **Supervisor Agent** decides which agent should run next.
* **How it Works in LangGraph:**

  * The Supervisor is itself a node.
  * **Conditional edges** route control flow depending on Supervisor’s decision.
* **Example:**

  * Supervisor checks state.
  * If “data missing” → route back to *Researcher*.
  * If “draft ready” → send to *Critic*.

```python
workflow.add_conditional_edges(
    "supervisor",
    lambda state: "researcher" if "needs_data" in state else "writer"
)
```

---

## Why These Patterns Matter

* They **mirror human organizations** (specialization, pipelines, review cycles, managers).
* They **add reliability** (by splitting tasks) and **flexibility** (via supervisors + conditional edges).
* LangGraph makes them practical because you can **visualize the flow** and debug where breakdowns happen.

---

📖 **Reference:** [LangGraph Multi-Agent Documentation](https://python.langchain.com/docs/langgraph/multi_agent)

---

✅ **Key Takeaway:**
Design patterns prevent chaos in multi-agent setups. With clear roles, structured workflows, and supervisor logic, you move from “agents talking randomly” → **orchestrated collaboration**.

---
