---

# 🔹 Chapter 4: Embeddings & Vector Stores

### 1. Why Embeddings?

When you ask *“How does climate change affect wheat yield?”*, the words need to be transformed into a mathematical representation so the system can compare it against stored documents.

* **Embeddings** = dense vector representations of text (e.g., 768 dimensions).
* Similar text → vectors close in space.
* Dissimilar text → vectors far apart.

**Analogy:** Like mapping books in a library into a 3D coordinate system. Queries and relevant passages land near each other.

---

### 2. Embedding Model Choices

| Type            | Examples                                            | Pros                                | Cons                                            |
| --------------- | --------------------------------------------------- | ----------------------------------- | ----------------------------------------------- |
| **Cloud APIs**  | OpenAI, Cohere, Google                              | High-quality, scalable, easy to use | Ongoing cost, data leaves org, privacy concerns |
| **Local / OSS** | `SentenceTransformers`, Hugging Face models         | Free, private, customizable         | Need compute (GPU/CPU), may lag behind SOTA     |
| **Hybrid**      | Use cloud for prototyping → swap in OSS model later | Flexibility                         | Migration complexity                            |

📌 **Tip:** Start with OSS like `all-MiniLM-L6-v2` for dev, upgrade later.

---

### 3. Vector Databases

Once you have embeddings, you need to store and search them efficiently.

* **Local**: FAISS, Chroma.
* **Managed**: Pinecone, Weaviate, Milvus.

**Indexing options**:

* **Flat** = exact search, slow at scale.
* **IVF / PQ** = approximate, balances speed and memory.
* **HNSW** = graph-based, extremely fast nearest-neighbor lookups.

---

### 4. Metadata & Namespaces

* Each chunk gets metadata (`source`, `page`, `timestamp`).
* Namespaces separate corpora (*HR docs*, *Product docs*).
* Incremental updates = add new docs without re-building index.

---

### 5. Risks & Challenges

* **Stale index** → need to re-embed when docs change.
* **Cloud cost** → embeddings + hosting add up.
* **Privacy** → embeddings may encode sensitive data permanently.

---

### 6. Mini Code: FAISS + SentenceTransformers

```python
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document

# Sample texts
texts = [
    "Climate change reduces crop yield due to drought.",
    "Artificial irrigation can help mitigate water scarcity.",
    "Wheat is sensitive to temperature variations."
]

# Load embedding model (local Hugging Face)
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(texts)

# Wrap in LangChain-friendly docs
docs = [Document(page_content=t, metadata={"id": i}) for i, t in enumerate(texts)]

# Build FAISS index
vectorstore = FAISS.from_embeddings(embeddings, docs)

# Query
query = "How does heat impact wheat farming?"
q_emb = model.encode([query])[0]

results = vectorstore.similarity_search_by_vector(q_emb, k=2)

print("🔎 Retrieved Chunks:")
for r in results:
    print("-", r.page_content, "| Metadata:", r.metadata)
```

👉 Try this in Jupyter; you’ll see semantic retrieval in action.

---

### 7. Decision Matrix

| Need                         | Best Option                   |
| ---------------------------- | ----------------------------- |
| **Local dev, prototypes**    | FAISS or Chroma               |
| **Small team, Python-first** | Chroma                        |
| **Enterprise scale, SLA**    | Pinecone, Weaviate, Milvus    |
| **Privacy / on-prem**        | FAISS or self-hosted Weaviate |

---

### 8. Visual Pipeline Diagram

```
        ┌───────────────────┐
        │   Raw Documents   │
        └─────────┬─────────┘
                  │
        ┌─────────▼─────────┐
        │ Preprocessing &   │
        │   Chunking        │
        └─────────┬─────────┘
                  │
        ┌─────────▼─────────┐
        │ Embedding Model   │
        │ (e.g., MiniLM)    │
        └─────────┬─────────┘
                  │ vectors
        ┌─────────▼─────────┐
        │ Vector Database   │
        │ (FAISS/Chroma)    │
        └─────────┬─────────┘
                  │
        ┌─────────▼─────────┐
        │ Retriever         │
        └─────────┬─────────┘
                  │
        ┌─────────▼─────────┐
        │ LLM / Agent       │
        └───────────────────┘
```

This diagram shows the **RAG flow**:

1. Docs get cleaned + chunked.
2. Converted into embeddings.
3. Stored in a vector DB.
4. Query → embedding → nearest neighbors retrieved.
5. Passed to the agent/LLM.

---