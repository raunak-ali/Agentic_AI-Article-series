---

# 🔹 Chapter 5: Retriever Design (Search Parameters & Tuning)

### 1. Why Retriever Tuning Matters

Retrievers are the bridge between your knowledge base and the LLM. A poorly tuned retriever either:

* Returns **irrelevant results** → hallucinations.
* Misses key info → incomplete answers.

Goal: ensure the LLM receives the **most relevant context** without overloading it with noise.

---

### 2. Key Parameters

| Parameter                       | Explanation                                                    | Best Practices                                                     |
| ------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------ |
| **k**                           | Number of top documents to retrieve                            | Start small (3–5), inspect results, increase if context is missing |
| **Thresholding / Score Cutoff** | Only keep documents above a similarity score                   | Ensures noisy docs aren’t passed                                   |
| **Hybrid Search**               | Combine **vector similarity** + **keyword/metadata filtering** | Use when exact keywords matter (e.g., legal docs)                  |
| **Reranking**                   | Re-score top N docs with a second model                        | Improves relevance, especially for ambiguous queries               |
| **Metadata Filters**            | Use doc attributes like `source`, `date`, `category`           | Crucial for compliance or domain-specific queries                  |

---

### 3. Retriever Types & Tradeoffs

| Type                          | Use Case                     | Pros                                           | Cons                                                |
| ----------------------------- | ---------------------------- | ---------------------------------------------- | --------------------------------------------------- |
| **Vector-only**               | Semantic search              | Finds relevant content even if wording differs | May return unrelated content if embeddings are weak |
| **Keyword-only**              | Exact-match requirements     | Very precise                                   | Misses paraphrased or semantically similar info     |
| **Hybrid (Vector + Keyword)** | Most common in RAG pipelines | Balance precision + recall                     | Slightly more computation                           |

**Passage vs Document Retrieval**

* **Passage:** chunk-level, fine-grained, better for LLMs with limited context.
* **Document:** entire doc, easier for context but may include irrelevant parts.

---

### 4. Metadata Filtering & Reranking

Metadata can dramatically improve results:

```python
# LangChain hybrid retriever with metadata filter
retriever = vectorstore.as_retriever(
    search_type="hybrid",
    k=10,
    search_kwargs={
        "filter": {"source": "policy", "year": 2023}
    }
)

# Fetch relevant docs
docs = retriever.get_relevant_documents("What is the latest carbon policy?")
for d in docs:
    print("-", d.page_content[:150], "| Metadata:", d.metadata)
```

**Tips:**

* Start with a low `k` to avoid overwhelming the LLM.
* Inspect retrieved chunks to ensure relevance.
* Add reranking for ambiguous queries (e.g., semantic + entailment scoring).

---

### 5. Tuning Checklist

1. **Start small**: k = 3–5.
2. **Inspect snippets**: check if retrieved chunks answer the query.
3. **Increase k** only if necessary.
4. **Add metadata filters**: narrow down results by date, source, or type.
5. **Consider reranker** for top N results.
6. **Iterate** until the LLM consistently produces accurate answers.

---

### 6. Visual Pipeline for Retrieval

```
      ┌───────────────┐
      │   User Query   │
      └──────┬────────┘
             │
             ▼
      ┌───────────────┐
      │  Retriever    │
      │ (Vector +    │
      │  Metadata)   │
      └──────┬────────┘
             │
             ▼
      ┌───────────────┐
      │  Top-k Docs    │
      │ (Chunks/Passages) │
      └──────┬────────┘
             │
             ▼
      ┌───────────────┐
      │   LLM / Agent  │
      └───────────────┘
```

* Query passes through retriever → filtered & ranked docs → sent to LLM.
* Hybrid search + metadata ensures **precision + recall balance**.
* Visualization helps troubleshoot missing or irrelevant chunks.

---

This chapter **bridges the gap** between document ingestion, embedding, and how the agent actually retrieves context before answering, setting up the RAG workflow for the next chapter.

---