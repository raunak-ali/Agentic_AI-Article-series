---

# 🔹 5. Use Case: Researcher + Writer Agents

### **Goal**

Generate a LinkedIn-style blog post on:
👉 “Climate change impact on agriculture.”

The idea is to **split responsibilities**:

* One agent (*Researcher*) fetches and compiles facts.
* Another agent (*Writer*) transforms those facts into a professional LinkedIn-style post.

---

## 🏗️ Implementation Details

### 1. **Nodes (Execution Units)**

In LangGraph, **nodes are the agents**. Each will be created via `create_react_agent` with its own role:

* **Researcher Node:**

  * Equipped with a tool → Wikipedia search API.
  * Task: Find relevant facts (climate change impact, crop yields, risks).
  * Output: Structured factual notes.

* **Writer Node:**

  * Equipped only with the LLM.
  * Task: Take Researcher’s notes, rewrite into a LinkedIn-style blog (clear, short, professional tone).
  * Output: Final blog post text.

---

### 2. **Edges (Control Flow)**

Edges define the sequence of execution:

```
User Input → Researcher → Writer → Final Output
```

* **Step 1:** User provides a topic (e.g., “Climate change impact on agriculture”).
* **Step 2:** Input flows via **edge** into the Researcher node.
* **Step 3:** Researcher’s output (facts) flows to Writer node.
* **Step 4:** Writer’s output flows to the Final Output node.

LangGraph makes this traceable → you can visualize every step in **LangGraph Studio**.

---

### 3. **State (Memory)**

The **state stores both raw research and final blog output**.

Example state object:

```python
{
  "topic": "Climate change impact on agriculture",
  "research_notes": "Climate change reduces crop yields, increases droughts...",
  "final_post": "Climate change is reshaping global agriculture. Farmers face..."
}
```

* When **Researcher Node** runs → it updates `research_notes`.
* When **Writer Node** runs → it updates `final_post`.
* Final state contains everything → useful for debugging, auditing, or extending later.

---

### 4. **Graph Construction**

The LangGraph graph would look like this:

```
[Input Node] → [Researcher Node] → [Writer Node] → [Output Node]
```

* **Input Node:** Accepts the user query/topic.
* **Researcher Node:** Uses Wikipedia tool, populates `research_notes`.
* **Writer Node:** Consumes `research_notes`, generates final blog text.
* **Output Node:** Displays or returns the result (`final_post`).

---

### 5. **Why This Workflow Matters**

* **Specialization** → Each agent focuses on one task.
* **Transparency** → State keeps raw + final versions for review.
* **Scalability** → Could easily add a Critic Agent in future.
* **Business Relevance** → Output is a LinkedIn-style blog (direct real-world use).

---

✅ With this design clear, the **next step** is to turn it into a **LangGraph implementation** inside a Jupyter/Colab notebook.
That will involve:

* Initializing agents with `create_react_agent`.
* Defining the state structure.
* Creating the graph with nodes + edges.
* Running the graph with user input.
* Printing the final blog post output.

---

Do you want me to now **draft the Jupyter notebook code** for this step-by-step (with comments like a tutorial)?
